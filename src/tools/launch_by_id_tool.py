from typing import Any

from src.schemas import LaunchResponse
from src.spacex_client import SpaceXClient


class LaunchByIdTool:
    """
    Tool responsible for retrieving a specific SpaceX launch by ID.
    """

    def __init__(self, client: SpaceXClient) -> None:
        self.client = client

    async def execute(self, arguments: dict[str, Any]) -> LaunchResponse:
        """
        Execute the tool.

        Args:
            arguments: Must contain 'launch_id'.

        Returns:
            LaunchResponse

        Raises:
            ValueError: If launch_id is missing or invalid.
        """
        launch_id = arguments.get("launch_id")

        if not isinstance(launch_id, str) or not launch_id.strip():
            raise ValueError("launch_id is required")

        raw = await self.client.get_launch_by_id(launch_id)

        return LaunchResponse(
            id=raw["id"],
            name=raw["name"],
            date_utc=raw["date_utc"],
        )
