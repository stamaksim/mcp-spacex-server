#Importing library

from pydantic import BaseModel
from typing import Optional, Any, Dict

#Response model for SpaceX launch information

#Returned when user requests launch data
class LaunchResponse(BaseModel):
    id: str
    name: str
    date_utc: str

#Response model for Spacex rocket information
class RocketResponse(BaseModel):
    id: str
    name: str
    description: str

#Request model used when executing a tool
class ExecuteToolRequest(BaseModel):
    arguments: Dict[str, Any]     # Contains arguments passed by the client


#Standard response returned after tool execution
class ExecuteToolResponse(BaseModel):
    ok: bool                        # Indicates success or failure
    result: Optional[Any] = None    # Tool result if it successful
    error: Optional[str] = None     # Error message if it failed
