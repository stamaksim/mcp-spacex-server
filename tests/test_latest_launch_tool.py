import pytest

from src.tools.latest_launch_tool import LatestLaunchTool


class FakeClient:
    async def list_launches(self):
        return [
            {
                "id": "1",
                "name": "Old Mission",
                "date_utc": "2020-01-01T00:00:00.000Z",
            },
            {
                "id": "2",
                "name": "New Mission",
                "date_utc": "2022-12-05T00:00:00.000Z",
            },
        ]


@pytest.mark.asyncio
async def test_latest_launch_returns_most_recent():
    tool = LatestLaunchTool(FakeClient())

    result = await tool.execute({})

    assert result.id == "2"
    assert result.name == "New Mission"
    assert result.date_utc == "2022-12-05T00:00:00.000Z"


class EmptyClient:
    async def list_launches(self):
        return []


@pytest.mark.asyncio
async def test_latest_launch_raises_when_no_launches():
    tool = LatestLaunchTool(EmptyClient())

    with pytest.raises(ValueError):
        await tool.execute({})
