from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.api import deps
from app.models.tool_combination import ToolCombination
from app.models.ai_tool import AITool
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[schemas.tool_combination.ToolCombination])
def read_tool_combinations(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve tool combinations for the current user.
    """
    tool_combinations = (
        db.query(ToolCombination)
        .filter(ToolCombination.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return tool_combinations


@router.post("/", response_model=schemas.tool_combination.ToolCombination)
def create_tool_combination(
    *,
    db: Session = Depends(deps.get_db),
    tool_combination_in: schemas.tool_combination.ToolCombinationCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new tool combination for the current user.
    """
    tool_combination = ToolCombination(
        name=tool_combination_in.name,
        description=tool_combination_in.description,
        content_type=tool_combination_in.content_type,
        user_id=current_user.id,
    )
    
    # Add tools
    for tool_id in tool_combination_in.tool_ids:
        tool = db.query(AITool).filter(AITool.id == tool_id).first()
        if not tool:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"AI tool with id {tool_id} not found",
            )
        tool_combination.tools.append(tool)
    
    db.add(tool_combination)
    db.commit()
    db.refresh(tool_combination)
    return tool_combination


@router.get("/{tool_combination_id}", response_model=schemas.tool_combination.ToolCombination)
def read_tool_combination(
    *,
    db: Session = Depends(deps.get_db),
    tool_combination_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get tool combination by ID.
    """
    tool_combination = db.query(ToolCombination).filter(
        ToolCombination.id == tool_combination_id,
        ToolCombination.user_id == current_user.id,
    ).first()
    
    if not tool_combination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tool combination not found",
        )
    return tool_combination


@router.put("/{tool_combination_id}", response_model=schemas.tool_combination.ToolCombination)
def update_tool_combination(
    *,
    db: Session = Depends(deps.get_db),
    tool_combination_id: int,
    tool_combination_in: schemas.tool_combination.ToolCombinationUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a tool combination.
    """
    tool_combination = db.query(ToolCombination).filter(
        ToolCombination.id == tool_combination_id,
        ToolCombination.user_id == current_user.id,
    ).first()
    
    if not tool_combination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tool combination not found",
        )
    
    update_data = tool_combination_in.dict(exclude_unset=True)
    
    # Handle tool updates
    if "tool_ids" in update_data:
        tool_ids = update_data.pop("tool_ids")
        tool_combination.tools = []
        for tool_id in tool_ids:
            tool = db.query(AITool).filter(AITool.id == tool_id).first()
            if not tool:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"AI tool with id {tool_id} not found",
                )
            tool_combination.tools.append(tool)
    
    # Update remaining fields
    for field, value in update_data.items():
        setattr(tool_combination, field, value)
    
    db.add(tool_combination)
    db.commit()
    db.refresh(tool_combination)
    return tool_combination


@router.delete("/{tool_combination_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tool_combination(
    *,
    db: Session = Depends(deps.get_db),
    tool_combination_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a tool combination.
    """
    tool_combination = db.query(ToolCombination).filter(
        ToolCombination.id == tool_combination_id,
        ToolCombination.user_id == current_user.id,
    ).first()
    
    if not tool_combination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tool combination not found",
        )
    db.delete(tool_combination)
    db.commit()
    return None


@router.get("/recommend/{content_type}", response_model=List[schemas.tool_combination.ToolCombination])
def recommend_tool_combinations(
    *,
    db: Session = Depends(deps.get_db),
    content_type: str,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get recommended tool combinations based on content type.
    """
    # This is a placeholder for the recommendation algorithm
    # In a real implementation, this would use more sophisticated logic
    tool_combinations = (
        db.query(ToolCombination)
        .filter(ToolCombination.content_type == content_type)
        .limit(5)
        .all()
    )
    return tool_combinations
