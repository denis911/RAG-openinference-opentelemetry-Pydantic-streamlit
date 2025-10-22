# RAG Agent with OpenInference & OpenTelemetry Tracing

A Retrieval-Augmented Generation (RAG) agent built with Pydantic AI, integrated with OpenInference and OpenTelemetry for comprehensive observability and tracing. The application uses Streamlit for the UI and Phoenix for trace visualization.

## Features

- 🤖 **Pydantic AI Agent** - Structured, type-safe AI agent with tool use
- 🔍 **RAG Pipeline** - Document search and retrieval from GitHub repositories
- 📊 **OpenInference Tracing** - Full observability with Phoenix/OpenTelemetry
- 💬 **Streamlit UI** - Interactive chat interface
- 🛠️ **Tool Tracing** - Automatic tracing of search tool calls

### Key Components

1. **search_agent.py** - Pydantic AI agent with traced search tools
2. **search_tools.py** - SearchTool class for FAQ retrieval
3. **ingest.py** - Document ingestion and indexing from GitHub repos
4. **tracing.py** - Phoenix/OpenTelemetry tracer initialization
5. **app.py** - Streamlit application with tracing spans
6. **logs.py** - Conversation logging to JSON files

## Prerequisites

- Python 3.12 or higher
- OpenAI API key
- UV package manager (recommended) or pip

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/denis911/RAG-openinference-opentelemetry-Pydantic-streamlit.git
cd RAG-openinference-opentelemetry-Pydantic-streamlit
```

### 2. Set up environment

Create a `.env` file from the template:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=your_actual_openai_api_key_here
```

### 3. Install dependencies

Using UV (recommended):
```bash
uv sync
```

Or using pip:
```bash
pip install -e .
```

## Usage

### Start Phoenix (Optional - for trace visualization)

In a separate terminal, start Phoenix server:

```bash
python -m phoenix.server.main serve
```

Phoenix will be available at `http://localhost:6006`

### Run the Streamlit App

**⚠️ IMPORTANT: You MUST use `streamlit run` command, not `python app.py`**

**Using UV (recommended):**
```bash
uv run streamlit run app.py
```

**Using system streamlit:**
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### ❌ Common Mistakes - DO NOT USE:
```bash
# ❌ WRONG - Will cause "Session state does not function" error
python app.py

# ❌ WRONG - Will cause "Session state does not function" error  
uv run app.py

# ✅ CORRECT - Use streamlit run
uv run streamlit run app.py
```

## How It Works

### 1. Document Indexing

On first run, the app:
- Downloads the DataTalksClub/faq repository
- Filters for data-engineering related documents
- Indexes documents using minsearch

### 2. Query Processing with Tracing

When you ask a question:
1. **Span "agent-query"** is created with input tracking
2. Agent processes the query using the search tool
3. **Search tool call** is automatically traced via `tracer.tool()`
4. Agent generates response using GPT-4o-mini
5. Output and status are recorded in the span
6. Conversation is logged to JSON file

### 3. Trace Visualization

All traces are sent to Phoenix where you can:
- View the complete execution flow
- See input/output for each step
- Monitor tool calls and LLM interactions
- Analyze performance metrics

## Configuration

### Environment Variables

```bash
# Required
OPENAI_API_KEY=your_key

# Optional Phoenix Configuration
PHOENIX_PORT=6006                              # Default: 6006
PHOENIX_HOST=127.0.0.1                         # Default: 127.0.0.1
PHOENIX_PROJECT_NAME=rag-project               # Default: rag-openinference-pydantic-streamlit
PHOENIX_API_KEY=phoenix_cloud_key              # For Phoenix Cloud only

# Optional Logs Configuration
LOGS_DIRECTORY=logs                            # Default: logs
```

## Project Structure

```
.
├── app.py                     # Main Streamlit application with tracing
├── search_agent.py            # Pydantic AI agent with traced tools
├── search_tools.py            # SearchTool implementation
├── ingest.py                  # Document ingestion and indexing
├── tracing.py                 # Phoenix/OpenTelemetry tracer setup
├── logs.py                    # Conversation logging utilities
├── pyproject.toml             # Project dependencies
├── .env                       # Environment configuration (create from .env.example)
├── .env.example               # Environment template
└── logs/                      # Conversation logs directory (auto-created)
```

## Tracing Implementation

### Minimal Changes Approach

The integration uses a minimal-changes strategy:

1. **Tool Wrapping**: Search tool is wrapped with `tracer.tool()` decorator
2. **Top-level Spans**: Agent queries are wrapped in "agent-query" spans
3. **Automatic Tracing**: Pydantic AI's built-in operations benefit from OpenTelemetry context propagation

### Tracing Points

- **Agent Query Span**: Tracks entire user query lifecycle
  - Input: User question
  - Output: Agent response
  - Status: OK/ERROR
  
- **Search Tool Span**: Automatically traced tool calls
  - Tool name: "search_faq"
  - Arguments: Search query
  - Results: Retrieved documents

## Customization

### Modify the Data Source

Edit `app.py` to change the repository:

```python
repo_owner = "YourOrg"
repo_name = "your-repo"
```

### Adjust Chunking Parameters

In `app.py`, modify the filter or add chunking:

```python
index = ingest.index_data(
    repo_owner, 
    repo_name, 
    filter=your_filter_function,
    chunk=True,
    chunking_params={'size': 2000, 'step': 1000}
)
```

### Customize Agent Prompt

Edit the `SYSTEM_PROMPT_TEMPLATE` in `search_agent.py`

## Troubleshooting

### "Session state does not function" Error

**Error Message:** `Session state does not function when running a script without 'streamlit run'`

**Cause:** You're running the app with `python app.py` or `uv run app.py` instead of using Streamlit's runner.

**Solution:** Always use the `streamlit run` command:
```bash
# Correct commands:
uv run streamlit run app.py
# or
streamlit run app.py
```

Streamlit requires its own runner to initialize session state, set up the web server, and provide the interactive UI. Running the script directly with Python will not work.

### Phoenix Connection Issues

If traces aren't showing in Phoenix:
1. Ensure Phoenix server is running: `python -m phoenix.server.main serve`
2. Check `PHOENIX_HOST` and `PHOENIX_PORT` in `.env`
3. Verify no firewall blocking localhost connections

### Import Errors

If you see import errors:
```bash
# Reinstall dependencies
uv sync --force
# or
pip install -e . --force-reinstall
```

### OpenAI API Errors

- Verify your API key is set correctly in `.env`
- Check you have credits/quota available
- Ensure your key has access to GPT-4o-mini

## Development

### Adding More Tracing

To add custom spans:

```python
from tracing import tracer

with tracer.start_as_current_span("my-operation") as span:
    span.set_attribute("custom.attribute", "value")
    # Your code here
    span.set_attribute("output.value", result)
```

### Adding New Tools

1. Add tool method to `SearchTool` class
2. Wrap with `tracer.tool()` in `search_agent.py`
3. Add to agent's tools list

## References

- [Pydantic AI Documentation](https://ai.pydantic.dev/)
- [Phoenix Documentation](https://docs.arize.com/phoenix)
- [OpenInference Specification](https://github.com/Arize-ai/openinference)
- [OpenTelemetry Python](https://opentelemetry.io/docs/languages/python/)
