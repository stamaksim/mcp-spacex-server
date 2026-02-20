from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.spacex_client import SpaceXClient

# Single shared client instance for the application.
# In production, this should be created during startup and closed during shutdown.
client = SpaceXClient()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI application lifecycle manager.

    Responsibilities:
      - Provide a clean startup/shutdown hook for shared resources.
      - Ensure the shared SpaceXClient is properly closed on shutdown.

    Notes:
      - Code before `yield` is startup logic.
      - Code after `yield` is shutdown logic.
      - Keeping a single shared client avoids multiple connection pools.
    """
    # Startup phase (optional initialization could go here).
    yield
    # Shutdown phase: release network resources.
    await client.close()


# FastAPI app instance with lifespan lifecycle enabled.
app = FastAPI(title="MCP SpaceX Server", lifespan=lifespan)


@app.get("/")
def root():
    """Basic root endpoint to confirm the server is running."""
    return {"message": "MCP SpaceX Server is running"}


@app.get("/health")
def health():
    """Lightweight health check endpoint (no external dependencies)."""
    return {"status": "ok"}


@app.get("/test-launches")
async def test_launches():
    """
    Development-only endpoint to verify SpaceXClient connectivity.

    Returns:
      - Raw JSON list of launches from the SpaceX API.

    Notes:
      - This endpoint should be removed or protected before final release,
        since it exposes external API output directly.
    """
    return await client.list_launches()
