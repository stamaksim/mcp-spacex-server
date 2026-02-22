from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from src.registry import ToolRegistry
from src.schemas import ExecuteToolRequest, ExecuteToolResponse
from src.spacex_client import SpaceXClient

# Single shared client instance for the application
client = SpaceXClient()
registry = ToolRegistry(client)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI application lifecycle manager."""
    yield
    await client.close()


app = FastAPI(title="MCP SpaceX Server", lifespan=lifespan)


@app.get("/")
def root():
    """Basic root endpoint to confirm the server is running."""
    return {"message": "MCP SpaceX Server is running"}


@app.get("/health")
def health():
    """Lightweight health check endpoint."""
    return {"status": "ok"}


@app.get("/tools")
async def list_tools():
    """
    Get a simple list of available tool names.

    Returns:
        [{"name": "list_launches"}, {"name": "get_latest_launch"}, ...]
    """
    return registry.list_tools()


@app.get("/tools/manifests")
async def get_all_manifests():
    """
    Get detailed manifests for all available tools.

    Returns all tools with their descriptions and parameter schemas.
    """
    return {"tools": registry.get_manifests()}


@app.get("/tools/{tool_name}/manifest")
async def get_tool_manifest(tool_name: str):
    """
    Get detailed manifest for a specific tool.

    Args:
        tool_name: Name of the tool (e.g., "get_latest_launch")

    Returns:
        Tool manifest with name, description, and parameters.

    Raises:
        HTTPException(404): If tool not found.
    """
    manifest = registry.get_manifest(tool_name)

    if manifest is None:
        raise HTTPException(
            status_code=404,
            detail=f"Tool '{tool_name}' not found. Available tools: {list(registry.tools.keys())}"
        )

    return manifest


@app.post("/execute", response_model=ExecuteToolResponse)
async def execute_tool(request: ExecuteToolRequest):
    """
    Execute a tool by name with provided arguments.

    Request body example:
        {
            "tool": "get_launch_by_id",
            "arguments": {"launch_id": "5eb87cd9ffd86e000604b32a"}
        }
    """
    return await registry.execute(request.tool, request.arguments)


@app.get("/test-launches")
async def test_launches():
    """Development endpoint to verify SpaceXClient connectivity."""
    return await client.list_launches()
