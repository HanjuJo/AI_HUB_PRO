from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

from .ai_tool import AITool


# Shared properties
class ToolCombinationBase(BaseModel):
    name: str
    description: Optional[str] = None
    content_type: Optional[str] = None  # shorts, long-form, podcast, etc.


# Properties to receive on item creation
class ToolCombinationCreate(ToolCombinationBase):
    tool_ids: List[int]


# Properties to receive on item update
class ToolCombinationUpdate(ToolCombinationBase):
    name: Optional[str] = None
    tool_ids: Optional[List[int]] = None


# Properties shared by models stored in DB
class ToolCombinationInDBBase(ToolCombinationBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Properties to return via API
class ToolCombination(ToolCombinationInDBBase):
    tools: List[AITool]


# Properties properties stored in DB
class ToolCombinationInDB(ToolCombinationInDBBase):
    pass
