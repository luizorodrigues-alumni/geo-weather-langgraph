# Geo Weather LangGraph

A small Python project that demonstrates a graph-based conversational assistant for geographic and weather queries. It combines a state-driven graph (via `langgraph`) with LLM calls and simple external tools for geocoding and weather lookup.

**Quick summary**
- **Purpose:** Provide a conversational CLI that can call external tools to fetch location and weather information.
- **Main entry:** `main.py` — starts an interactive CLI loop.
- **Core idea:** Use `langgraph` to build a state graph that alternates between LLM calls and tool execution.

**Files**
- `main.py`: CLI entrypoint; builds the graph and runs a loop to send user messages to the graph.
- `graph.py`: Constructs the `StateGraph` with nodes, routing logic, and the LLM/tool flow.
- `prompts.py`: Central place for the system prompt and conversational instructions.
- `state.py`: Typed state definition used by the graph.
- `tools.py`: Tool implementations (geocoding via Geoapify and weather via wttr.in) and tool registry.

**Requirements**
- Python 3.9+
- Recommended packages: `langchain`, `langgraph`, `requests`, `python-dotenv`

Install (example):
```
pip install langchain langgraph requests python-dotenv
```

**Environment variables**
- `GEO_APIFY_API_KEY` — required for the geocoding tool in `tools.py`.
- Any credentials required by your LLM provider should be set in the environment as needed by `langchain`.

**Run**
```
python3 main.py
```
The program starts an interactive prompt. Type a location or weather-related question and press Enter. Type `q`, `quit`, or `exit` to leave.

**Notes for developers**
- Edit `prompts.py` to change the assistant's system prompt and behavior.
- Add or update tools in `tools.py` to extend capabilities (remember to update `TOOLS` and `TOOLS_BY_NAME`).
- Modify the routing or nodes in `graph.py` to change the conversation flow.

If you want, I can also add a `requirements.txt` or a short CONTRIBUTING note.
