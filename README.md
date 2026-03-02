
MCP SpaceX Server — Design Document
Version: 1.0
Date: 2026-02-25

1. Project Overview
This project implements a lightweight RPC-style MCP server that exposes structured tools for
retrieving data from the public SpaceX API.
Instead of traditional REST resource endpoints (e.g. /launches), the server follows a Remote
Procedure Call (RPC) pattern. Clients invoke tools dynamically via a single execution endpoint.
The project demonstrates:
• RPC-based tool execution
• Clean layered architecture
• Dependency injection
• Pydantic-based validation
• Tool discovery via structured manifests
• Unit-tested business logic

2. Architecture Overview
The system follows a layered architecture with strict downward dependencies.
FastAPI (API Layer)
↓
ToolRegistry (Dispatch Layer)
↓
Tools (Business Logic Layer)
↓
SpaceXClient (Infrastructure Layer)
↓
External SpaceX API

Layer Responsibilities
API Layer (FastAPI)
• Handles HTTP transport
• Validates request bodies
• Exposes /execute, /tools, and manifest endpoints
• No business logic
Registry Layer (ToolRegistry)
• Stores registered tools
• Dispatches execution by tool name
• Wraps responses in ExecuteToolResponse
• Exposes tool manifests
Tool Layer
• Contains isolated business logic
• Calls SpaceXClient
• Returns validated Pydantic models
• No FastAPI imports
Infrastructure Layer (SpaceXClient)
• Handles HTTP communication using httpx.AsyncClient
• Provides reusable API methods
• Shared instance injected into tools

Dependencies flow strictly downward. No circular coupling.

3. Execution Flow
1. Client sends a POST request to /execute.
2. The request contains:
• tool (string)
• arguments (object)
3. FastAPI validates the request using ExecuteToolRequest.
4. ToolRegistry locates the tool by name.
5. The selected tool executes business logic.
6. SpaceXClient performs the external API request.
7. The tool returns validated Pydantic models.
8. Registry wraps the result in ExecuteToolResponse.
9. JSON response is returned to the client.
This follows an RPC-style execution model.

4. Tool System
The server currently exposes the following tools:
• list_launches
• get_launch_by_id
• get_latest_launch
• list_rockets
• get_rocket_by_id

Each tool:
• Accepts SpaceXClient via dependency injection
• Exposes a single async execute(arguments: dict) method
• Performs input validation if required
• Returns Pydantic models
• Is registered in ToolRegistry
• Has a corresponding structured manifest

5. Tool Manifest System
Each tool is described via a structured manifest containing:
• name
• description
• parameter schema (JSON-schema style)

Manifests allow:
• Tool discovery (GET /tools)
• Structured metadata access (GET /tools/manifests)
• Future AI/LLM integration

Example manifest structure:
{
"name": "get_launch_by_id",
"description": "...",
"parameters": {
"type": "object",
"properties": {
"launch_id": {
"type": "string",
"description": "SpaceX launch ID"
}
},
"required": ["launch_id"]
}
}

6. Module Structure
src/
├── main.py
├── registry.py
├── schemas.py
├── spacex_client.py
└── tools/
    ├── launch_tool.py
    ├── launch_by_id_tool.py
    ├── latest_launch_tool.py
    ├── rocket_tool.py
    └── rocket_list_tool.py
tests/
├── test_launch_by_id_tool.py
├── test_latest_launch_tool.py
└── test_registry.py

7. Data Handling
• No persistent storage
• All data retrieved live from SpaceX public API
• Data validated using Pydantic models
• Transient in-memory processing only

8. Testing Strategy
Unit tests cover:
• Tool logic (success and validation errors)
• Registry dispatch behavior
• Error handling

Tests are written using:
• pytest
• pytest-asyncio
• mocked SpaceXClient

No external API calls are performed during unit testing.

Run tests:
uv run pytest

9. Setup & Running
Requirements
• Python 3.12+
• uv package manager

Install dependencies
uv sync

Run server
uv run uvicorn src.main:app --reload

Access:
• Root: http://127.0.0.1:8000/
• Swagger UI: http://127.0.0.1:8000/docs
• Tool list: http://127.0.0.1:8000/tools
• Tool manifests: http://127.0.0.1:8000/tools/manifests

Execute example:
curl -X POST http://127.0.0.1:8000/execute -H "Content-Type: application/json" -d '{"tool":"list_rockets","arguments":{}}'

10. Future Improvements
• Add caching (TTL-based in-memory cache)
• Add retry with exponential backoff
• Add rate-limit handling
• Introduce structured logging
• Add CI pipeline
• Extend tool set (payloads, missions, crew)

11. Design Principles Applied
• Single Responsibility Principle
• Dependency Injection
• Clean Layered Architecture
• RPC-style tool execution
• Explicit schema validation
• Testable isolated components

This version is:
• Clear
• Minimal
• Professional
• Architecturally correct
• Interview-ready
• Easy to present

If you want, I can now:
• Make a shorter academic version (if required by university format)✂
• Prepare a spoken explanation version🎤
• Or create a diagram text block you can paste directly into Confluence🧠
