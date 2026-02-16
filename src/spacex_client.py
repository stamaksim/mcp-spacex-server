import httpx

# Default base URL for the public SpaceX REST API (v4).
BASE_URL = "https://api.spacexdata.com/v4"


class SpaceXClient:
    """
    Async HTTP client for the public SpaceX API (v4).

    Responsibilities:
      - Perform HTTP requests to SpaceX endpoints.
      - Raise on non-2xx responses.
      - Return parsed JSON payloads (dict/list).

    Non-responsibilities:
      - No business logic, filtering, or formatting for tools.
      - No FastAPI-specific logic (routes, dependencies, etc.).

    Lifecycle:
      - The underlying httpx.AsyncClient must be closed via `close()`.
        In production, manage it from application startup/shutdown.
    """

    def __init__(self, base_url: str = BASE_URL, timeout_s: float = 10.0):
        """
        Initialize SpaceXClient.

        Args:
            base_url: Base URL for the SpaceX API.
            timeout_s: Request timeout in seconds.

        Notes:
            A single instance should be shared across the app to avoid creating
            multiple connection pools.
        """
        self.base_url = base_url
        # Underlying HTTP client with connection pooling.
        self._client = httpx.AsyncClient(base_url=self.base_url, timeout=timeout_s)

    async def close(self) -> None:
        """Close the underlying HTTP client and release network resources."""
        await self._client.aclose()

    async def _get(self, path: str):
        """
        Perform GET request and return parsed JSON.

        Args:
            path: API path starting with '/' (e.g., '/launches').

        Returns:
            Parsed JSON response (typically a list or dict).

        Raises:
            httpx.HTTPStatusError: If the response status is not 2xx.
            httpx.RequestError: On network/transport errors.
        """
        r = await self._client.get(path)
        r.raise_for_status()
        return r.json()

    async def list_launches(self):
        """Return the list of launches."""
        return await self._get("/launches")

    async def get_launch_by_id(self, launch_id: str):
        """
        Fetch a single launch by its ID.

        Args:
            launch_id: SpaceX launch ID.

        Raises:
            ValueError: If `launch_id` is empty.
        """
        if not launch_id:
            raise ValueError("launch_id is required")
        return await self._get(f"/launches/{launch_id}")

    async def list_rockets(self):
        """Return the list of rockets."""
        return await self._get("/rockets")

    async def get_rocket_by_id(self, rocket_id: str):
        """
        Fetch a single rocket by its ID.

        Args:
            rocket_id: SpaceX rocket ID.

        Raises:
            ValueError: If `rocket_id` is empty.
        """
        if not rocket_id:
            raise ValueError("rocket_id is required")
        return await self._get(f"/rockets/{rocket_id}")
