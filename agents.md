# agents.md

**AI Coding Assistant Guide for RAG-OpenInference-OpenTelemetry-Pydantic-Streamlit**

---

## 📘 Project Overview

**Name:** RAG-OpenInference-OpenTelemetry-Pydantic-Streamlit  
**Purpose:** A research and observability-ready Retrieval-Augmented Generation (RAG) application built with Streamlit, OpenInference, and OpenTelemetry/Phoenix tracing.  
**Goal:** Demonstrate how to combine LLM reasoning (Pydantic AI) with real-time observability, structured logging, and trace correlation for reproducible, auditable AI behavior.

**Key Characteristics:**
- Type-safe AI agents with Pydantic validation
- Full observability with Phoenix/OpenTelemetry tracing
- Document retrieval from GitHub repositories
- Interactive Streamlit UI for RAG queries
- Comprehensive logging for debugging and audit trails

---

## 🧱 Tech Stack

| Layer | Technology | Notes |
|-------|-----------|-------|
| **Frontend / UI** | Streamlit | Lightweight UI for RAG queries and monitoring. **CRITICAL:** Always use `streamlit run app.py`, never `python app.py` |
| **LLM / Agent Framework** | Pydantic AI | Defines structured AI agents with validated inputs/outputs. Supports tool tracing via decorators |
| **Observability** | OpenTelemetry + Phoenix (OpenInference) | Traces model calls, tools, and events. Avoid logging API keys or PII |
| **RAG Backend** | MinSearch | Local vector index for document retrieval. Fast, lightweight, in-memory search |
| **Language Models** | OpenAI (GPT-4o-mini) | Configurable via environment variables. Default model for agent responses |
| **Runtime / Packaging** | Python 3.12+, UV/pip | UV is recommended for faster dependency management |

---

## ⚙️ Setup & Commands

```bash
# Clone and navigate
git clone https://github.com/denis911/RAG-openinference-opentelemetry-Pydantic-streamlit.git
cd RAG-openinference-opentelemetry-Pydantic-streamlit

# Create .env file from template
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=your_actual_openai_api_key_here

# Install dependencies (using UV - recommended)
uv sync

# Install dependencies (using pip - alternative)
pip install -e .

# Start Phoenix server (in separate terminal)
python -m phoenix.server.main serve
# Phoenix available at http://localhost:6006

# Run the Streamlit app (CORRECT way)
uv run streamlit run app.py
# or
streamlit run app.py

# ❌ NEVER run with:
# python app.py  # Will cause "Session state does not function" error
# uv run app.py  # Will cause "Session state does not function" error
```

---

## 🧩 Project Architecture

```
root/
├── app.py                  # Streamlit UI + query flow (main entry point)
├── search_agent.py         # Core LLM agent (Pydantic AI with tools)
├── search_tools.py         # SearchTool class for FAQ retrieval
├── ingest.py              # Document ingestion / vector index builder
├── tracing.py             # OpenTelemetry / Phoenix tracing setup
├── logs.py                # Structured JSON logging
├── pyproject.toml         # Project dependencies and metadata
├── .env                   # Environment config (create from .env.example)
├── .env.example           # Environment template
└── logs/                  # Conversation logs directory (auto-created)
```

### Key Design Notes

1. **Separation of Concerns:** Ingestion (`ingest.py`), search (`search_tools.py`), agent logic (`search_agent.py`), tracing (`tracing.py`), and UI (`app.py`) are modular.

2. **Lazy Initialization:** Heavy resources (indexes, LLMs) load via `st.cache_resource` to prevent Streamlit freezing and improve performance.

3. **Safe Observability:** All traces must mask API keys and user PII before export. Never log sensitive data.

4. **Reproducibility:** All agent configs (model, temperature, tools) are logged as structured metadata in traces and logs.

5. **Minimal-Changes Tracing:** 
   - Tool wrapping via `tracer.tool()` decorator
   - Top-level spans for agent queries
   - Automatic context propagation through Pydantic AI

---

## 🧠 Agent Design Principles

1. **Simplicity First** — Prefer clear, linear code; avoid clever abstractions or complex inheritance patterns.

2. **Explicit I/O Schemas** — Use Pydantic models for agent inputs/outputs. Every function should have clear type hints.

3. **Ask Before Acting** — The agent should plan, propose, and confirm before executing side effects (especially destructive operations).

4. **Trace Every Call** — Every LLM or tool invocation emits an OpenTelemetry span with timing, status, and error metadata.

5. **Validate Everything** — Use Pydantic validation before sending or persisting data. Never trust unvalidated input.

6. **Tool-First Design** — Break complex operations into discrete, traceable tools. Each tool should do one thing well.

---

## 📋 AI Coding Workflow (Based on Best Practices Checklist)

### Phase 1 — Preparation (Before Coding)

**✅ Context Setup:**
- Maintain this `agents.md` as static, foundational context
- Use `@git` or `@codebase` mentions for dynamic, task-specific context
- Reference specific files with `@filename` when working on isolated changes

**✅ Planning Requirements:**
- **Before coding, require a plan:** Ask the AI to outline risks, potential issues, and quick tests
- **Prefer "ask mode":** AI must seek confirmation before major changes
- **Use extended reasoning models** (e.g., Claude Opus 4) for planning tasks and architectural decisions
- **Explore options:** Ask for 2-3 different approaches with pros/cons
- **Draft first, refine second:** Write your own solution first, then use AI to improve it (keeps your skills sharp!)

**Example prompt for planning:**
```
Before implementing X, please:
1. Outline the required steps
2. Identify potential risks or gotchas
3. Propose quick tests to validate the approach
4. Wait for my approval before proceeding
```

### Phase 2 — Coding

**✅ Code Quality:**
- Write small, linear functions; one responsibility per function
- Keep function names clear and descriptive
- Avoid complex patterns (inheritance, metaclasses, "clever" hacks)
- Provide complete function signatures when requesting code

**✅ Context Management:**
- Use `clear` command or new sessions for each independent task
- Commit frequently to Git; branch for experiments (`git checkout -b experiment-xyz`)
- Summarize progress in `progress.md` when resuming long-running tasks ("compaction" technique)

**✅ Debugging:**
- Leverage logs (`logs.py`) for debugging
- Instruct the agent to check logs before refactoring
- Add sufficient logging statements, especially in new code paths

**✅ Model Selection:**
- Match model power to task complexity:
  - **Fast models** (Sonnet 4.5): Routine edits, simple refactors
  - **Extended reasoning models** (Opus 4): Complex debugging, architectural design
  - **Specialized models**: Vision tasks, long context needs

**✅ Library Usage:**
- Prefer established libraries (well-represented in training data)
- For newer libraries: provide documentation and examples
- Don't invent solutions that existing libraries already solve well

### Phase 3 — Testing

**✅ Follow AI-Assisted TDD:**
1. **Generate tests first** based on expected input/output pairs
2. **Confirm tests fail initially** (proves they target non-existent functionality)
3. **Implement code to make tests pass** (instruct AI not to modify tests during this step)

**✅ Test Review:**
- Ensure all AI-generated tests are manually reviewed
- Check for edge cases, error conditions, and boundary values
- Verify tests are not just mocking out the functionality they're supposed to test

**Example TDD prompt:**
```
We're following TDD. Please:
1. Write tests for function X that expects [input] and returns [output]
2. Do NOT implement the function yet
3. Do NOT use mocks for the core logic
```

### Phase 4 — Review

**✅ AI-Assisted Review:**
- Have the AI perform an initial self-review of its code
- Optionally use a second, more powerful AI agent for a second opinion

**✅ Mandatory Human Review:**
- **Always conduct a line-by-line review before merge** (non-negotiable!)
- Watch for:
  - Sweeping changes affecting multiple files
  - Inefficient algorithms or data structures
  - Subtle bugs that tests might miss
  - Unintended side effects or breaking changes
  - Hardcoded values that should be configurable

---

## 🔍 Logging & Tracing Conventions

### Structured Logging (`logs.py`)

- Use structured JSON logs for all conversation history
- Include timestamps, query, response, and metadata
- Store in `logs/` directory with timestamp-based filenames
- **Redact secrets, emails, and PII** before logging

### OpenTelemetry Tracing (`tracing.py`)

**Span Hierarchy:**
```
agent-query (root span)
├── Input: User question
├── search_faq (tool span)
│   ├── Arguments: Search query
│   └── Results: Retrieved documents
├── LLM call (implicit, via Pydantic AI)
└── Output: Agent response
```

**Critical Rules:**
- Each user query = 1 root span ("agent-query")
- Child spans for retrieval, LLM, and tool calls
- Use trace IDs to correlate UI errors with backend logs
- Set span status (OK/ERROR) and record exceptions
- Never include API keys or PII in span attributes

**Adding Custom Spans:**
```python
from tracing import tracer

with tracer.start_as_current_span("my-operation") as span:
    span.set_attribute("custom.attribute", "value")
    # Your code here
    span.set_attribute("output.value", result)
```

**Tool Tracing:**
```python
# Wrap tools with tracer.tool() decorator
from tracing import tracer

@tracer.tool()
def my_search_tool(query: str) -> list[dict]:
    # Automatically traced
    return results
```

---

## 🧰 Common Gotchas & Solutions

| Issue | Prevention/Solution |
|-------|-------------------|
| **Streamlit freezing** | Don't run ingestion or heavy model loads at import time. Use `st.cache_resource` for expensive operations |
| **Session state errors** | Always use `streamlit run app.py`, never `python app.py` or `uv run app.py` |
| **Prompt drift** | Keep prompt templates versioned in `search_agent.py`. Use constants for prompts, never inline strings |
| **Trace overload** | Adjust sampling in production; disable Phoenix tracing for local quick tests |
| **Inconsistent environments** | Always sync dependencies via `uv.lock` or `requirements.txt` after changes |
| **Over-verbose AI output** | Set `max_output_tokens` and temperature bounds in agent config |
| **Missing traces in Phoenix** | Ensure Phoenix server is running (`python -m phoenix.server.main serve`) and check `PHOENIX_HOST`/`PHOENIX_PORT` in `.env` |
| **API key errors** | Verify `.env` exists, contains valid `OPENAI_API_KEY`, and has sufficient quota/credits |

---

## 🛠️ Advanced Patterns

### Autonomous Workflows (Expert Level)

For maximum efficiency with AI assistants:
- Set up feedback loops where the agent can make changes, run tests, observe failures, and iterate
- Grant controlled autonomy with clear boundaries
- Use sub-agents for investigating specific questions while preserving main agent context
- Implement approval gates for destructive operations

### Context Compaction for Long Sessions

When resuming work after breaks:
1. Ask agent to summarize progress into `progress.md`
2. Include: end goal, chosen approach, completed steps, current blocker
3. Start new session with summarized context
4. Prevents context window pollution and improves focus

### Customizing for Your Repo

**Change Data Source:**
```python
# In app.py
repo_owner = "YourOrg"
repo_name = "your-repo"
```

**Add Document Chunking:**
```python
# In app.py
index = ingest.index_data(
    repo_owner,
    repo_name,
    filter=your_filter_function,
    chunk=True,
    chunking_params={'size': 2000, 'step': 1000}
)
```

**Modify Agent Prompts:**
```python
# In search_agent.py
SYSTEM_PROMPT_TEMPLATE = """
Your custom prompt here...
"""
```

**Add New Tools:**
1. Add tool method to `SearchTool` class in `search_tools.py`
2. Wrap with `tracer.tool()` decorator in `search_agent.py`
3. Add to agent's tools list in agent initialization

---

## 🧩 Quick Reference Checklist

### ✅ Pre-Coding
- [ ] Create/maintain this `agents.md` for static context
- [ ] Use `@git`, `@codebase`, `@docs` for dynamic context
- [ ] Require plan + approval before coding
- [ ] Use extended reasoning models for complex planning
- [ ] Draft your own solution first, then refine with AI

### ✅ During Coding
- [ ] Keep code simple and linear
- [ ] Use `clear` command between distinct tasks
- [ ] Commit often to Git; branch for experiments
- [ ] Match AI model to task complexity
- [ ] Add sufficient logging for debugging

### ✅ Testing
- [ ] Practice AI-assisted TDD (tests first, then implementation)
- [ ] Confirm tests fail before implementing functionality
- [ ] Manually review all AI-generated tests

### ✅ Review
- [ ] Have AI perform self-review first
- [ ] **Always perform human line-by-line review** (non-negotiable!)
- [ ] Check for sweeping changes across multiple files
- [ ] Verify no secrets or PII in code or logs

### ✅ Observability
- [ ] Verify traces appear in Phoenix after changes
- [ ] Check logs for structured JSON format
- [ ] Ensure no API keys or PII in traces/logs
- [ ] Validate span hierarchy and timing data

---

## 🧠 Keep Your Skills Sharp

**Critical Reminder:** AI assistants are powerful tools, but they are not replacements for:
- Deep technical expertise
- Strong problem-solving skills
- Sound engineering judgment
- System design capabilities
- Clear communication with stakeholders

**Best practices to maintain your edge:**
- Draft solutions yourself before asking for AI refinement
- Regularly solve coding challenges without AI assistance
- Study and understand the code AI generates (never blindly accept)
- Keep learning new technologies and patterns
- Teach others (explaining solidifies understanding)

**In short:** *Don't let AI give you donkey brains 🧠🐴*

---

## 📚 Additional Resources

- **Pydantic AI Docs:** https://ai.pydantic.dev/
- **OpenInference Spec:** https://github.com/Arize-ai/openinference
- **Phoenix Documentation:** https://docs.arize.com/phoenix
- **Streamlit Docs:** https://docs.streamlit.io/
- **OpenTelemetry Python:** https://opentelemetry.io/docs/languages/python/

---

**Last Updated:** October 23, 2025  
**Version:** 1.0  
**Maintainers:** Project contributors

---

*This file should be updated as the project evolves. Keep it current to ensure AI assistants have accurate context.*