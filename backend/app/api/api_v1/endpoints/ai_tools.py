from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.api import deps
from app.models.ai_tool import AITool, Category
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[schemas.ai_tool.AITool])
def read_ai_tools(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve AI tools.
    """
    ai_tools = db.query(AITool).offset(skip).limit(limit).all()
    return ai_tools


@router.post("/", response_model=schemas.ai_tool.AITool)
def create_ai_tool(
    *,
    db: Session = Depends(deps.get_db),
    ai_tool_in: schemas.ai_tool.AIToolCreate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new AI tool.
    """
    ai_tool = AITool(
        name=ai_tool_in.name,
        description=ai_tool_in.description,
        url=str(ai_tool_in.url),
        logo_url=str(ai_tool_in.logo_url) if ai_tool_in.logo_url else None,
        pricing_type=ai_tool_in.pricing_type,
        pricing_details=ai_tool_in.pricing_details,
        features=ai_tool_in.features,
    )
    
    # Add categories
    for category_id in ai_tool_in.category_ids:
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {category_id} not found",
            )
        ai_tool.categories.append(category)
    
    db.add(ai_tool)
    db.commit()
    db.refresh(ai_tool)
    return ai_tool


@router.get("/{ai_tool_id}", response_model=schemas.ai_tool.AITool)
def read_ai_tool(
    *,
    db: Session = Depends(deps.get_db),
    ai_tool_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get AI tool by ID.
    """
    ai_tool = db.query(AITool).filter(AITool.id == ai_tool_id).first()
    if not ai_tool:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="AI tool not found",
        )
    return ai_tool


@router.put("/{ai_tool_id}", response_model=schemas.ai_tool.AITool)
def update_ai_tool(
    *,
    db: Session = Depends(deps.get_db),
    ai_tool_id: int,
    ai_tool_in: schemas.ai_tool.AIToolUpdate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update an AI tool.
    """
    ai_tool = db.query(AITool).filter(AITool.id == ai_tool_id).first()
    if not ai_tool:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="AI tool not found",
        )
    
    update_data = ai_tool_in.dict(exclude_unset=True)
    
    # Handle URL fields separately
    if "url" in update_data and update_data["url"]:
        ai_tool.url = str(update_data["url"])
        del update_data["url"]
    
    if "logo_url" in update_data:
        ai_tool.logo_url = str(update_data["logo_url"]) if update_data["logo_url"] else None
        del update_data["logo_url"]
    
    # Handle category updates
    if "category_ids" in update_data:
        category_ids = update_data.pop("category_ids")
        ai_tool.categories = []
        for category_id in category_ids:
            category = db.query(Category).filter(Category.id == category_id).first()
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Category with id {category_id} not found",
                )
            ai_tool.categories.append(category)
    
    # Update remaining fields
    for field, value in update_data.items():
        setattr(ai_tool, field, value)
    
    db.add(ai_tool)
    db.commit()
    db.refresh(ai_tool)
    return ai_tool


@router.delete("/{ai_tool_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ai_tool(
    *,
    db: Session = Depends(deps.get_db),
    ai_tool_id: int,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete an AI tool.
    """
    ai_tool = db.query(AITool).filter(AITool.id == ai_tool_id).first()
    if not ai_tool:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="AI tool not found",
        )
    db.delete(ai_tool)
    db.commit()
    return None


# Category endpoints
@router.get("/categories/", response_model=List[schemas.ai_tool.Category])
def read_categories(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve categories.
    """
    categories = db.query(Category).offset(skip).limit(limit).all()
    return categories


@router.post("/categories/", response_model=schemas.ai_tool.Category)
def create_category(
    *,
    db: Session = Depends(deps.get_db),
    category_in: schemas.ai_tool.CategoryCreate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new category.
    """
    category = Category(
        name=category_in.name,
        description=category_in.description,
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category
