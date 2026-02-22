"""
Tool registry for SpaceX API operations.

This module provides a centralized mechanism for managing and executing
various tools that interact with the SpaceX API.
"""

from src.schemas import ExecuteToolResponse, ToolManifest, ToolParameters, ToolParameterSchema
from src.tools.latest_launch_tool import LatestLaunchTool
from src.tools.launch_by_id_tool import LaunchByIdTool
from src.tools.launch_tool import SpaceXLaunchTool
from src.tools.rocket_tool import SpaceXRocketTool


class ToolRegistry:
    """
    Registry for centralized tool management and execution.

    Responsibilities:
      - Store and manage available tools.
      - Execute tools by name with provided arguments.
      - Handle errors and format responses.
      - Provide a list of available tools.

    Non-responsibilities:
      - Direct interaction with SpaceX API (delegated to client).
      - Tool-specific logic (encapsulated in separate classes).
      - HTTP routing or FastAPI-specific logic.

    Attributes:
        tools: Dictionary of registered tools (name -> tool instance).
    """

    def __init__(self, client):
        """
        Initialize the registry with available tools.

        Args:
            client: SpaceXClient instance for API interaction.
                    Injected as a dependency into all tools.
        """
        # Register available tools by their unique names
        self.tools = {
            "list_launches": SpaceXLaunchTool(client),
            "get_launch_by_id": LaunchByIdTool(client),
            # "list_rockets": RocketListTool(client),      # TODO: Not yet implemented
            "get_rocket_by_id": SpaceXRocketTool(client),
            "get_latest_launch": LatestLaunchTool(client),
        }

        # Define manifests for all tools
        # ⚠️ IMPORTANT: Keep this in sync with self.tools!
        # Each tool in self.tools must have a corresponding manifest.
        self.manifests = [
            ToolManifest(
                name="list_launches",
                description="Retrieve a comprehensive list of all SpaceX launches with ID"
                            "mission name, and launch date.",
                parameters=ToolParameters(
                    type="object",
                    properties={},
                    required=[],
                ),
            ),
            ToolManifest(
                name="get_latest_launch",
                description="Retrieve the most recent SpaceX launch based on launch date."
                            "Returns launch ID, mission name, and UTC launch date.",
                parameters=ToolParameters(
                    type="object",
                    properties={},
                    required=[],
                ),
            ),
            ToolManifest(
                name="get_launch_by_id",
                description="Retrieve detailed information about a specific"
                            "SpaceX launch using its unique identifier.",
                parameters=ToolParameters(
                    type="object",
                    properties={
                        "launch_id": ToolParameterSchema(
                            type="string",
                            description="The unique identifier of the SpaceX launch"
                                        "(24-character hexadecimal string, e.g., "
                                        "'5eb87cd9ffd86e000604b32a')",
                        )
                    },
                    required=["launch_id"],
                ),
            ),
            ToolManifest(
                name="get_rocket_by_id",
                description="Retrieve detailed information about a specific SpaceX rocket "
                            "using its unique identifier.",
                parameters=ToolParameters(
                    type="object",
                    properties={
                        "rocket_id": ToolParameterSchema(
                            type="string",
                            description="The unique identifier of the SpaceX rocket "
                                        "(24-character hexadecimal string, e.g., "
                                        "'5e9d0d95eda69955f709d1eb')",
                        )
                    },
                    required=["rocket_id"],
                ),
            ),
            # Add new tool manifests here when implementing new tools:
            # ToolManifest(
            #     name="list_rockets",
            #     description="Retrieve a list of all SpaceX rockets.",
            #     parameters=ToolParameters(
            #         type="object",
            #         properties={},
            #         required=[],
            #     ),
            # ),
        ]

    async def execute(
            self,
            tool_name: str,
            arguments: dict
    ) -> ExecuteToolResponse:
        """
        Execute a tool by name with provided arguments.

        Args:
            tool_name: Name of the tool to execute (must be registered).
            arguments: Dictionary of arguments to pass to the tool.
                      Format depends on the specific tool.

        Returns:
            ExecuteToolResponse: Response object with execution result:
                - ok=True, result=<data>: successful execution
                - ok=False, error=<message>: execution error
        """
        # Check if tool exists in the registry
        if tool_name not in self.tools:
            return ExecuteToolResponse(
                ok=False,
                error=f"Unknown tool: {tool_name}. Available tools: {list(self.tools.keys())}"
            )

        try:
            # Execute the tool and get the result
            result = await self.tools[tool_name].execute(arguments)
            return ExecuteToolResponse(ok=True, result=result)
        except Exception as e:
            # Handle any errors during tool execution
            return ExecuteToolResponse(ok=False, error=str(e))

    def list_tools(self) -> list[dict[str, str]]:
        """
        Return a simple list of available tool names.

        Returns:
            list[dict[str, str]]: List of dictionaries with tool names.
        """
        return [{"name": name} for name in self.tools.keys()]

    def get_manifests(self) -> list[ToolManifest]:
        """
        Return manifests for all registered tools.

        Returns:
            list[ToolManifest]: List of tool manifests with descriptions and parameters.
        """
        return self.manifests

    def get_manifest(self, tool_name: str) -> ToolManifest | None:
        """
        Get the manifest for a specific tool by name.

        Args:
            tool_name: Name of the tool to get manifest for.

        Returns:
            ToolManifest: The tool's manifest if found, None otherwise.
        """
        for manifest in self.manifests:
            if manifest.name == tool_name:
                return manifest
        return None
