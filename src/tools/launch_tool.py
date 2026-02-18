
# Importing tools
from spacex_client import SpaceXClient
from tools.schemas import LaunchResponse
from typing import Any, Dict, List


class SpaceXLaunchTool:
    def __init__(self, client: SpaceXClient) -> None:
        self.client = client
    """
       Tool responsible for retrieving and transforming SpaceX launch data.

       Responsibilities:
           - Call SpaceXClient to fetch raw launch data.
           - Transform raw JSON into validated LaunchResponse models.
           - Return structured and type-safe output.

       This tool does NOT:
           - Perform HTTP requests directly (uses SpaceXClient).
           - Contain any FastAPI route logic.
       """

    async def execute(self, arguments: Dict[str, Any]) -> List[LaunchResponse]:
        raw = await self.client.list_launches()
        """
            Execute the launch listing tool.

            Args:
                arguments: Dictionary of arguments passed to the tool.
                           (Currently unused for list_launches.)

            Returns:
                A list of LaunchResponse objects containing:
                    - id
                    - name
                    - date_utc

            Process:
                1. Fetch raw launch data from SpaceXClient.
                2. Map raw JSON into LaunchResponse models.
                3. Return validated list of launches.
            """
        launches: List[LaunchResponse] = []

# Transform raw SpaceX API data into validated LaunchResponse models

        for item in raw:
            launches.append(
                LaunchResponse(
                    id=item["id"],
                    name=item["name"],
                    date_utc=item["date_utc"],
                )
            )

        return launches