# Importing tools
from typing import Any

from src.spacex_client import SpaceXClient
from src.tools.schemas import RocketResponse


class SpaceXRocketTool:
    """
    Tool responsible for retrieving and transforming SpaceX rocket data.

    Responsibilities:
        - Call SpaceXClient to fetch raw rocket data by ID.
        - Transform raw JSON into a validated RocketResponse model.
        - Return structured and type-safe output.

    This tool does NOT:
        - Perform HTTP requests directly (uses SpaceXClient).
        - Contain any FastAPI route logic.
    """

    def __init__(self, client: SpaceXClient) -> None:
        self.client = client

    async def execute(self, arguments: dict[str, Any]):
        """
        Execute the rocket retrieval tool.

        Args:
            arguments: Dictionary containing required input:
                - rocket_id (str): Unique SpaceX rocket ID.

        Returns:
            A RocketResponse object containing:
                - id
                - name
                - description

        Raises:
            ValueError: If 'rocket_id' is missing or invalid.

        Process:
            1. Validate that 'rocket_id' exists in arguments.
            2. Fetch raw rocket data from SpaceXClient.
            3. Map raw JSON into a RocketResponse model.
            4. Return validated rocket data.
        """
        rocket_id = arguments.get("rocket_id")
        if not isinstance(rocket_id, str) or not rocket_id.strip():
            raise ValueError("Rocket_id is required")

        raw = await self.client.get_rocket_by_id(rocket_id)

        return RocketResponse(
            id=raw["id"],
            name=raw["name"],
            description=raw["description"],
        )
