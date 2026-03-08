import pytest

from src.registry import ToolRegistry
from src.schemas import ExecuteToolResponse

# --- Mock Classes for Testing ---

class FakeSuccessTool:
    """Simulates a tool that executes successfully."""
    async def execute(self, arguments: dict):
        return {"message": "ok"}

class FakeFailTool:
    """Simulates a tool that raises an exception during execution."""
    async def execute(self, arguments: dict):
        raise ValueError("Something went wrong")

class FakeClient:
    """Stub client required by the ToolRegistry constructor."""
    pass

# --- Pytest Fixtures ---

@pytest.fixture
def registry():
    """Provides a fresh ToolRegistry instance for each test."""
    return ToolRegistry(FakeClient())

# --- Test Cases ---

@pytest.mark.asyncio
async def test_execute_success(registry):
    """Tests if the registry correctly executes a registered tool and returns success."""
    # Manually inject the fake tool into the registry
    registry.tools = {"test_tool": FakeSuccessTool()}

    response: ExecuteToolResponse = await registry.execute("test_tool", {})

    assert response.ok is True
    assert response.result == {"message": "ok"}
    assert response.error is None

@pytest.mark.asyncio
async def test_execute_unknown_tool(registry):
    """Tests the registry's behavior when trying to execute a non-existent tool."""
    response: ExecuteToolResponse = await registry.execute("unknown_tool", {})

    assert response.ok is False
    assert "Unknown tool" in response.error

@pytest.mark.asyncio
async def test_execute_tool_raises_exception(registry):
    """Tests if the registry gracefully handles exceptions raised by tools."""
    # Inject a tool that is guaranteed to fail
    registry.tools = {"fail_tool": FakeFailTool()}

    response: ExecuteToolResponse = await registry.execute("fail_tool", {})

    assert response.ok is False
    assert "Something went wrong" in response.error