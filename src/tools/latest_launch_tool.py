from typing import Any

from src.schemas import LaunchResponse
from src.spacex_client import SpaceXClient


class LatestLaunchTool:
    """
    Tool responsible for returning the most recent SpaceX launch.

    Responsibilities:
      - Fetch launch data via SpaceXClient.
      - Determine the latest launch (by `date_utc`).
      - Return a validated LaunchResponse.

    This tool does NOT:
      - Perform HTTP requests directly (uses SpaceXClient).
      - Contain FastAPI route logic.
      - Wrap responses into ExecuteToolResponse (handled by registry / API layer).
    """

    def __init__(self, client: SpaceXClient) -> None:
        """
        Initialize the tool with its dependencies.

        Args:
            client: Shared SpaceXClient instance (injected dependency).
        """
        self.client = client

    async def execute(self, arguments: dict[str, Any]) -> LaunchResponse:
        """
        Execute the tool and return the latest launch.

        Args:
            arguments: Tool arguments (unused for this tool). Kept for a consistent tool interface.

        Returns:
            LaunchResponse: The latest launch (id, name, date_utc).

        Raises:
            ValueError: If no launches are available from the API.
            httpx.HTTPError: Propagated from SpaceXClient on request failures.
        """
        # Retrieve all launches from the SpaceX API (raw JSON list).
        raw_launches = await self.client.list_launches()

        # Guard against empty API response.
        if not raw_launches:
            raise ValueError("No launches available")

        # `date_utc` is an ISO timestamp string; lexicographic max works for ISO8601.
        latest = max(raw_launches, key=lambda x: x["date_utc"])

        # Map raw API payload into a validated response schema.
        return LaunchResponse(
            id=latest["id"],
            name=latest["name"],
            date_utc=latest["date_utc"],
        )
