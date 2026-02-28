import pytest

from src.registry import ToolRegistry
from src.schemas import ExecuteToolResponse


class FakeSuccessTool:
    async def execute(self, arguments: dict):
        return {"message": "ok"}


class FakeFailTool:
    async def execute(self, arguments: dict):
        raise ValueError("Something went wrong")


class FakeClient:
    """Not used directly, but required by registry constructor."""
    pass


@pytest.mark.asyncio
async def test_execute_success():
    registry = ToolRegistry(FakeClient())

    # Overwrite registry tools manually for isolation
    registry.tools = {"test_tool": FakeSuccessTool()}

    response: ExecuteToolResponse = await registry.execute("test_tool", {})

    assert response.ok is True
    assert response.result == {"message": "ok"}
    assert response.error is None


@pytest.mark.asyncio
async def test_execute_unknown_tool():import pytest

from src.registry import ToolRegistry
from src.schemas import ExecuteToolResponse


class FakeSuccessTool:
    async def execute(self, arguments: dict):
        return {"message": "ok"}


class FakeFailTool:
    async def execute(self, arguments: dict):
        raise ValueError("Something went wrong")


class FakeClient:
    """Not used directly, but required by registry constructor."""
    pass


@pytest.mark.asyncio
async def test_execute_success():
    registry = ToolRegistry(FakeClient())

    # Overwrite registry tools manually for isolation
    registry.tools = {"test_tool": FakeSuccessTool()}

    response: ExecuteToolResponse = await registry.execute("test_tool", {})

    assert response.ok is True
    assert response.result == {"message": "ok"}
    assert response.error is None


@pytest.mark.asyncio
async def test_execute_unknown_tool():
    registry = ToolRegistry(FakeClient())

    response: ExecuteToolResponse = await registry.execute("unknown_tool", {})

    assert response.ok is False
    assert "Unknown tool" in response.error


@pytest.mark.asyncio
async def test_execute_tool_raises_exception():
    registry = ToolRegistry(FakeClient())

    registry.tools = {"fail_tool": FakeFailTool()}

    response: ExecuteToolResponse = await registry.execute("fail_tool", {})

    assert response.ok is False
    assert "Something went wrong" in response.error

    registry = ToolRegistry(FakeClient())

    response: ExecuteToolResponse = await registry.execute("unknown_tool", {})

    assert response.ok is False
    assert "Unknown tool" in response.error


@pytest.mark.asyncio
async def test_execute_tool_raises_exception():
    registry = ToolRegistry(FakeClient())

    registry.tools = {"fail_tool": FakeFailTool()}

    response: ExecuteToolResponse = await registry.execute("fail_tool", {})

    assert response.ok is False
    assert "Something went wrong" in response.error
