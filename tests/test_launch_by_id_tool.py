import pytest

from src.tools.launch_by_id_tool import LaunchByIdTool


class FakeClient:
    async def get_launch_by_id(self, launch_id: str):
        return {
            "id": launch_id,
            "name": "Test Mission",
            "date_utc": "2022-01-01T00:00:00.000Z",
        }


@pytest.mark.asyncio
async def test_launch_by_id_success():
    tool = LaunchByIdTool(FakeClient())

    result = await tool.execute({"launch_id": "abc123"})

    assert result.id == "abc123"
    assert result.name == "Test Mission"
    assert result.date_utc == "2022-01-01T00:00:00.000Z"


@pytest.mark.asyncio
async def test_launch_by_id_missing_argument():
    tool = LaunchByIdTool(FakeClient())

    with pytest.raises(ValueError):
        await tool.execute({})
