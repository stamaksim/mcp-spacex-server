from pydantic import BaseModel
from typing import Optional, Any, Dict

class LaunchResponse(BaseModel):
    id: str
    name: str
    date_utc: str

class RocketResponse(BaseModel):
    id: str
    name: str
    description: str

class ExecuteToolRequest(BaseModel):
    arguments: Dict[str, Any]

class ExecuteToolResponse(BaseModel):
    ok: bool
    result: Optional[Any] = None
    error: Optional[str] = None
