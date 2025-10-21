import streamlit as st
import asyncio

import ingest
import search_agent
import logs
from tracing import tracer
from opentelemetry.trace import Status, StatusCode

# to run it use << uv run streamlit run app.py >> command in the terminal

from dotenv import load_dotenv
import os

load_dotenv()  # this loads .env automatically

api_key = os.getenv("OPENAI_API_KEY")
print(f"Using OpenAI key: {api_key[:8]}...")  # test (don't print full key!)


# --- Initialization ---
@st.cache_resource
def init_agent():
    repo_owner = "DataTalksClub"
    repo_name = "faq"

    def filter(doc):
        return 'data-engineering' in doc['filename']

    st.write("🔄 Indexing repo...")
    index = ingest.index_data(repo_owner, repo_name, filter=filter)
    agent = search_agent.init_agent(index, repo_owner, repo_name)
    return agent


agent = init_agent()

# --- Streamlit UI ---
st.set_page_config(page_title="AI FAQ Assistant", page_icon="🤖", layout="centered")
st.title("🤖 AI FAQ Assistant")
st.caption("Ask me anything about the DataTalksClub/faq repository")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask your question..."):
    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant response with OpenInference tracing
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            with tracer.start_as_current_span("agent-query", attributes={
                "openinference.span.kind": "chain",
                "input.value": prompt[:500],  # Truncate long inputs
            }) as span:
                try:
                    response = asyncio.run(agent.run(user_prompt=prompt))
                    answer = response.output
                    
                    # Set output attribute
                    span.set_attribute("output.value", answer[:500])  # Truncate long outputs
                    span.set_status(Status(StatusCode.OK))
                    
                    st.markdown(answer)
                except Exception as e:
                    span.record_exception(e)
                    span.set_status(Status(StatusCode.ERROR))
                    st.error(f"Error: {str(e)}")
                    answer = f"Error: {str(e)}"

    # Save response to history + logs
    st.session_state.messages.append({"role": "assistant", "content": answer})
    logs.log_interaction_to_file(agent, response.new_messages())
