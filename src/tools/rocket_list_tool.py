
from src.schemas import RocketResponse
from src.spacex_client import SpaceXClient


class SpaceXRocketListTool:
    """
    Tool responsible for retrieving and validating the list of SpaceX rockets.

    Responsibilities:
        - Calls SpaceXClient.list_rockets() to fetch raw rocket data.
        - Validates each rocket using the RocketResponse Pydantic schema.
        - Returns a list of validated rocket dictionaries.

    This tool does NOT:
        - Perform HTTP requests directly (delegates to SpaceXClient).
        - Contain any FastAPI logic.
        - Perform input validation (no arguments required).

    Returns:
        List[dict]: A list of validated rocket data.
    """

    def __init__(self, client: SpaceXClient) -> None:
        self.client = client

    async def execute(self, arguments: dict) -> list[RocketResponse]:
        """
        Executes the rocket list retrieval process.

        Args:
            arguments (dict): Not used. Required for tool interface consistency.

        Returns:
            List[dict]: A list of validated rocket data.
        """
        raw_rockets = await self.client.list_rockets()

        validated = [RocketResponse.model_validate(r) for r in raw_rockets]

        return validated