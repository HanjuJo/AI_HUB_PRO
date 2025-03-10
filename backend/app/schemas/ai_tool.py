from typing import Optional, List
from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime


# Shared properties
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None


# Properties to receive on category creation
class CategoryCreate(CategoryBase):
    pass


# Properties to receive on category update
class CategoryUpdate(CategoryBase):
    pass


# Properties shared by models stored in DB
class CategoryInDBBase(CategoryBase):
    id: int

    class Config:
        from_attributes = True


# Properties to return via API
class Category(CategoryInDBBase):
    pass


# Shared properties
class AIToolBase(BaseModel):
    name: str
    description: Optional[str] = None
    url: HttpUrl
    logo_url: Optional[HttpUrl] = None
    pricing_type: Optional[str] = None  # free, freemium, paid, etc.
    pricing_details: Optional[str] = None
    features: Optional[List[str]] = None


# Properties to receive on item creation
class AIToolCreate(AIToolBase):
    category_ids: List[int]


# Properties to receive on item update
class AIToolUpdate(AIToolBase):
    name: Optional[str] = None
    category_ids: Optional[List[int]] = None


# Properties shared by models stored in DB
class AIToolInDBBase(AIToolBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Properties to return via API
class AITool(AIToolInDBBase):
    categories: List[Category]


# Properties properties stored in DB
class AIToolInDB(AIToolInDBBase):
    pass
