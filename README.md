# MCP SpaceX Server - Group Design Document

**Team Members:** Name 1, Name 2, Name 3, Name 4  
**Date:** YYYY-MM-DD  
**Version:** 1.0

---

## 1. Project Overview

This repository implements a lightweight MCP (Model Context Protocol) server
for fetching SpaceX data. The service exposes a small set of tools that call
the SpaceX public API and return validated responses. The code is
intentionally simple and structured to demonstrate clean‑architecture layering
and dependency injection in a university project.

The system is aimed at learners who want to understand how to separate
business logic from web frameworks while still providing a usable HTTP
interface.

---

## 2. Goals & Objectives

- **Core Goal:**
  Build a server that provides MCP tools for accessing SpaceX public API data
  in a clean, maintainable fashion.

- **Secondary Goals:**
  - Implement a shared asynchronous HTTP client (`SpaceXClient`).
  - Define clear Pydantic schemas for tool input and output validation.
  - Keep tool logic free of FastAPI and HTTP concerns.
  - Document architecture, design decisions and provide a reproducible
    environment for team collaboration.

---

## 3. The User Journey

- **The Experience:**
  Users send HTTP requests to tool endpoints or the generic `/execute` route.
  The server routes the call through `ToolRegistry`, the selected tool runs
  business logic, and a structured JSON response is returned.

- **Inputs:**
  JSON objects containing a `tool` name and an `arguments` dictionary.

- **Outputs:**
  Pydantic‑validated models such as `LaunchResponse` and `RocketResponse` wrapped
  by `ExecuteToolResponse` for generic execution endpoints.

---

## 4. Program Logic (Step‑by‑Step)

1. **Initialization:**
   FastAPI application starts and creates a shared `httpx.AsyncClient`
   instance used by `SpaceXClient`.
2. **Input Phase:**
   Client calls a tool via dedicated route or `/execute` with arguments.
3. **Processing Phase:**
   Tool invokes `SpaceXClient` to fetch data from the SpaceX API and applies any
   internal logic (filtering, selection, mapping).
4. **Output Phase:**
   Tool returns a Pydantic model or list of models, the registry wraps it in
   an `ExecuteToolResponse` if necessary.
5. **Loop / Cleanup:**
   The server continues handling requests; on shutdown the shared HTTP client
   is closed.

---

## 5. Team Responsibility Breakdown

- **Member 1:** SpaceXClient and infrastructure layer.
- **Member 2:** MCP tools (launches, rockets).
- **Member 3:** Pydantic schemas and `ToolRegistry`.
- **Member 4:** Testing, documentation (README, DESIGN.md, CHANGELOG).

---

## 6. Module & Function Breakdown

- **`src/main.py`** – FastAPI entry point and lifecycle management.
- **`src/infrastructure/spacex/client.py`** – HTTP client for SpaceX API.
- **`src/registry.py`** – Central registry of available tools.
- **`src/tools/`** – Individual tool implementations:
  - `launch_tool.py`, `latest_launch_tool.py`, `launch_by_id_tool.py`,
    `rocket_list_tool.py`, `rocket_tool.py`.
- **`src/schemas.py`** – Pydantic models used throughout the app.

---

## 7. Data Storage & Structures

- All data is transient and retrieved live from the SpaceX public API.
- Lists and dictionaries are used for interim processing; Pydantic models
  validate shapes before returning to callers.

---

## 8. Development Timeline (Milestones)

1. **Milestone 1:** Initial repository layout and uv environment set up.
2. **Milestone 2:** SpaceXClient, tool implementations and schemas completed.
3. **Milestone 3:** End‑to‑end testing, cleanup and documentation finalized.

---

## MCP Tools List

- **`list_launches`** – retrieve all SpaceX launches.
- **`get_launch_by_id`** – fetch a single launch using its ID.
- **`get_latest_launch`** – return the most recent launch.
- **`list_rockets`** – list all SpaceX rockets.
- **`get_rocket_by_id`** – fetch a rocket by its ID.

Each tool:
- uses `SpaceXClient` for API calls,
- is independent of FastAPI,
- has input/output schemas and is registered with `ToolRegistry`.

---

## Project Structure

```
src/
├── infrastructure/spacex/client.py
├── registry.py
├── schemas.py
└── tools/
    ├── launch_tool.py
    ├── latest_launch_tool.py
    ├── launch_by_id_tool.py
    ├── rocket_list_tool.py
    └── rocket_tool.py

README.md
DESIGN.md
CHANGELOG.md
pyproject.toml
uv.lock
.gitignore
docs/
└── images/architecture.png
```

---

## Architecture

![Architecture Diagram](docs/images/architecture.png)

Layers:

1. **API Layer** – FastAPI routes and request validation.
2. **Tool Layer** – business logic encapsulated in small classes.
3. **Infrastructure Layer** – `SpaceXClient` handles HTTP communication.

Dependencies flow downward (API → Tools → Infrastructure).

---

## Setup & Running

### Prerequisites

- Python 3.12+
- `uv` environment manager (see below)

### 1. Install `uv` (one‑time per machine)

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
irm https://astral.sh/uv/install.ps1 | iex
```

Verify installation:

```bash
uv --version
```

### 2. Sync dependencies

From the project root:

```bash
uv sync
```

If someone adds or bumps a package, run `uv add <pkg>` and commit the
updated `pyproject.toml` and `uv.lock`. After pulling changes everyone should
run `uv sync`.

### 3. Run the server

```bash
uv run uvicorn src.main:app --reload
```

Open your browser:

- http://127.0.0.1:8000/
- http://127.0.0.1:8000/docs  (Swagger UI)

### 4. Execute a tool (example)

```bash
curl -X POST http://127.0.0.1:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"tool":"list_launches","arguments":{}}'
```

---

## Testing

Run the unit tests with:

```bash
uv run pytest -q
```

Tests cover the `ToolRegistry` and individual tool classes using pytest and
pytest‑asyncio.

---

## Team Checklist

- ✅ Naming style: `snake_case` for Python
- ✅ Communication channel: Discord/Teams/WhatsApp (set by team)
- ✅ Integration: tools tested via registry and manual API calls
- ✅ Documentation: README, DESIGN.md and CHANGELOG.md updated

---

## Future Improvements

- Add tools for payloads, missions, crew, etc.
- Introduce caching or retry logic in `SpaceXClient`.
- Enhance error handling and logging.
- Add CI pipelines and automated tests.

---

## License

University group project for learning purposes; no external license.
