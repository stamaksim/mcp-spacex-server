from typing import Any

from pydantic import BaseModel, Field

# Response model for SpaceX launch information


# Returned when user requests launch data
class LaunchResponse(BaseModel):
    id: str
    name: str
    date_utc: str


# Response model for Spacex rocket information
class RocketResponse(BaseModel):
    id: str
    name: str
    description: str


# Request model used when executing a tool
class ExecuteToolRequest(BaseModel):
    tool: str
    arguments: dict[str, Any] = Field(default_factory=dict)


# Standard response returned after tool execution
class ExecuteToolResponse(BaseModel):
    ok: bool  # Indicates success or failure
    result: Any | None = None  # Tool result if it successful
    error: str | None = None  # Error message if it failed

# Tool manifest schemas (simple approach)
class ToolParameterSchema(BaseModel):
    """Schema for a single tool parameter."""
    type: str
    description: str


class ToolParameters(BaseModel):
    """Schema for tool parameters structure."""
    type: str
    properties: dict[str, ToolParameterSchema]
    required: list[str] = []


class ToolManifest(BaseModel):
    """Simple tool manifest for describing available tools."""
    name: str
    description: str
    parameters: ToolParameters