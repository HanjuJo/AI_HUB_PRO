from datetime import datetime
from typing import List, Optional

from sqlalchemy import Column, Integer, String, Text, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

# Association table for categories
tool_categories = Table(
    "tool_categories",
    Base.metadata,
    Column("tool_id", Integer, ForeignKey("aitool.id"), primary_key=True),
    Column("category_id", Integer, ForeignKey("category.id"), primary_key=True),
)

# Association table for tool combinations
combination_tools = Table(
    "combination_tools",
    Base.metadata,
    Column("combination_id", Integer, ForeignKey("toolcombination.id"), primary_key=True),
    Column("tool_id", Integer, ForeignKey("aitool.id"), primary_key=True),
)

class Category(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), unique=True, index=True)
    description = Column(Text, nullable=True)
    
    # Relationships
    tools = relationship("AITool", secondary=tool_categories, back_populates="categories")
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }
    
    def __repr__(self) -> str:
        return f"<Category {self.name}>"

class AITool(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text)
    url = Column(String(255), nullable=False)
    image_url = Column(String(255), nullable=True)
    pricing_type = Column(String(50))  # free, freemium, paid
    pricing_details = Column(Text, nullable=True)
    features = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    categories = relationship("Category", secondary=tool_categories, back_populates="tools")
    combinations = relationship("ToolCombination", secondary=combination_tools, back_populates="tools")
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "url": self.url,
            "image_url": self.image_url,
            "pricing_type": self.pricing_type,
            "pricing_details": self.pricing_details,
            "features": self.features,
            "categories": [category.to_dict() for category in self.categories],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self) -> str:
        return f"<AITool {self.name}>"
