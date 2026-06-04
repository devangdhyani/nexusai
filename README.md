# ⚡ NexusAI

**Autonomous AI research agent** powered by LangGraph, Groq, and Tavily Search.

[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.36-red)](https://streamlit.io)
[![LangGraph](https://img.shields.io/badge/LangGraph-1.0-green)](https://langchain-ai.github.io/langgraph)
[![Groq](https://img.shields.io/badge/Groq-llama--3.3--70b-orange)](https://groq.com)

---

## Features

- **ReAct Loop** — Reason → Act → Observe, powered by LangGraph
- **Web Search** — Real-time results via Tavily Search API
- **Math Tools** — Built-in arithmetic operations
- **Streaming UI** — Modern dark-theme chat interface built with Streamlit
- **Persistent History** — Full conversation context across turns
- **One-click Deploy** — Render.com ready out of the box

---

## Architecture

```
START
  │
  ▼
tool_calling_llm (Groq llama-3.3-70b-versatile)
  │
  ├─ tool call? ──► tools (TavilySearch | multiply)
  │                   │
  │◄──────────────────┘  (ReAct loop)
  │
  └─ no tool call? ──► END
```

### Project Structure

```
NexusAI/
├── app.py                  # Streamlit web application
├── src/
│   └── agent/
│       ├── __init__.py
│       └── graph.py        # LangGraph ReAct agent
├── notebooks/              # Development / experiment notebooks
├── .streamlit/
│   └── config.toml         # Streamlit theme & server config
├── .env.example            # Environment variable template
├── requirements.txt        # Python dependencies
├── render.yaml             # Render.com deployment config
└── .gitignore
```

---

## Quick Start

### 1. Clone

```bash
git clone https://github.com/YOUR_USERNAME/nexusai.git
cd nexusai
```

### 2. Create virtual environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Mac / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and fill in your API keys:

```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

Get your keys:
- **Groq** → https://console.groq.com/keys (free tier available)
- **Tavily** → https://app.tavily.com/home (1 000 free searches/month)

### 5. Run locally

```bash
streamlit run app.py
```

Opens at `http://localhost:8501`

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | ✅ | Groq API key for the LLM |
| `TAVILY_API_KEY` | ✅ | Tavily API key for web search |
| `LANGCHAIN_API_KEY` | ❌ | LangSmith tracing (optional) |
| `LANGSMITH_PROJECT` | ❌ | LangSmith project name |
| `LANGSMITH_TRACING` | ❌ | `true` to enable tracing |

---

## Deploy to Render

1. Push this repository to GitHub
2. Go to [render.com](https://render.com) → **New → Web Service**
3. Connect your GitHub repo — Render auto-detects `render.yaml`
4. Go to **Environment** and add:
   - `GROQ_API_KEY` = your key
   - `TAVILY_API_KEY` = your key
5. Click **Deploy**

The `render.yaml` sets:
- Build: `pip install -r requirements.txt`
- Start: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true`

---

## Development

### Running the agent standalone

```python
from src.agent.graph import build_agent, run_agent

agent = build_agent()
response = run_agent(agent, "What is the latest news in AI?")
print(response)
```

### Notebooks

Experiment notebooks are in `notebooks/`. Run with:

```bash
jupyter notebook notebooks/
```

---

## Stack

| Layer | Technology |
|---|---|
| LLM | Groq — `llama-3.3-70b-versatile` |
| Agent framework | LangGraph 1.0 |
| Web search | Tavily Search |
| UI | Streamlit 1.36 |
| Language | Python 3.12 |
| Deployment | Render.com |

---

## License

MIT — see [LICENSE](LICENSE) for details.
