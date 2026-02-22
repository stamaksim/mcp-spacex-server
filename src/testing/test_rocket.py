import asyncio

from src.spacex_client import SpaceXClient
from src.tools.rocket_tool import SpaceXRocketTool


async def main() -> None:
    client = SpaceXClient()

    tool = SpaceXRocketTool(client)

    # Falcon 9 rocket id (SpaceX v4): 5e9d0d95eda69973a809d1ec
    result = await tool.execute({"rocket_id": "5e9d0d95eda69973a809d1ec"})
    print(result)

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
