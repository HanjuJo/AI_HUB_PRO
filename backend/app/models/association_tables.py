from sqlalchemy import Column, Integer, ForeignKey, Table

from app.db.base_class import Base

# Association table for AI tools and categories
tool_categories = Table(
    "tool_categories",
    Base.metadata,
    Column("tool_id", Integer, ForeignKey("ai_tool.id"), primary_key=True),
    Column("category_id", Integer, ForeignKey("category.id"), primary_key=True),
)

# Association table for tool combinations and AI tools
combination_tools = Table(
    "combination_tools",
    Base.metadata,
    Column("combination_id", Integer, ForeignKey("tool_combination.id"), primary_key=True),
    Column("tool_id", Integer, ForeignKey("ai_tool.id"), primary_key=True),
)
