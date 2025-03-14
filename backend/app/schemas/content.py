from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class OptimizationSuggestionBase(BaseModel):
    category: str = Field(..., description="Suggestion category (seo, readability, engagement, technical)")
    suggestion: str = Field(..., description="Detailed optimization suggestion")
    priority: int = Field(..., ge=1, le=3, description="Priority level (1: high, 2: medium, 3: low)")
    implemented: int = Field(0, ge=0, le=1, description="Implementation status (0: not implemented, 1: implemented)")

class OptimizationSuggestionCreate(OptimizationSuggestionBase):
    content_id: int

class OptimizationSuggestion(OptimizationSuggestionBase):
    id: int
    created_at: datetime
    content_id: int

    class Config:
        from_attributes = True

class ContentBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    content_type: str = Field(..., description="Content type (video, blog, social)")
    keywords: str = Field(..., max_length=500)
    meta_description: Optional[str] = Field(None, max_length=300)
    meta_keywords: Optional[str] = Field(None, max_length=200)

class ContentCreate(ContentBase):
    pass

class ContentUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1)
    content_type: Optional[str] = None
    keywords: Optional[str] = Field(None, max_length=500)
    meta_description: Optional[str] = Field(None, max_length=300)
    meta_keywords: Optional[str] = Field(None, max_length=200)

class Content(ContentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    seo_score: float
    readability_score: float
    engagement_score: float
    technical_score: float
    user_id: int
    optimization_suggestions: List[OptimizationSuggestion] = []

    class Config:
        from_attributes = True

class ContentWithScore(Content):
    overall_score: float = Field(..., description="Overall content quality score")
