"""
AI 도구 추천 API 엔드포인트
"""
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import schemas
from app.api import deps
from app.models.user import User
from app.services.recommendation import RecommendationService

router = APIRouter()


@router.get("/by-category/{category_name}", response_model=List[schemas.ai_tool.AITool])
def recommend_by_category(
    *,
    db: Session = Depends(deps.get_db),
    category_name: str,
    limit: int = Query(5, ge=1, le=20),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    카테고리별 AI 도구 추천
    """
    tools = RecommendationService.recommend_by_category(db, category_name, limit)
    return tools


@router.get("/by-use-case", response_model=List[schemas.ai_tool.AITool])
def recommend_by_use_case(
    *,
    db: Session = Depends(deps.get_db),
    use_case: str = Query(..., min_length=2),
    limit: int = Query(5, ge=1, le=20),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    사용 사례별 AI 도구 추천
    """
    tools = RecommendationService.recommend_by_use_case(db, use_case, limit)
    return tools


@router.get("/personalized", response_model=List[schemas.ai_tool.AITool])
def recommend_personalized(
    *,
    db: Session = Depends(deps.get_db),
    limit: int = Query(5, ge=1, le=20),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    사용자 맞춤형 AI 도구 추천
    """
    tools = RecommendationService.recommend_personalized(db, current_user, limit)
    return tools


@router.get("/popular", response_model=List[schemas.ai_tool.AITool])
def recommend_popular(
    *,
    db: Session = Depends(deps.get_db),
    limit: int = Query(5, ge=1, le=20),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    인기 AI 도구 추천
    """
    tools = RecommendationService.recommend_popular(db, limit)
    return tools


@router.get("/similar/{tool_id}", response_model=List[schemas.ai_tool.AITool])
def recommend_similar(
    *,
    db: Session = Depends(deps.get_db),
    tool_id: int,
    limit: int = Query(3, ge=1, le=10),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    유사한 AI 도구 추천
    """
    tools = RecommendationService.recommend_similar(db, tool_id, limit)
    return tools


@router.get("/complementary/{tool_id}", response_model=List[schemas.ai_tool.AITool])
def recommend_complementary(
    *,
    db: Session = Depends(deps.get_db),
    tool_id: int,
    limit: int = Query(3, ge=1, le=10),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    보완적인 AI 도구 추천 (함께 사용하면 좋은 도구)
    """
    tools = RecommendationService.recommend_complementary(db, tool_id, limit)
    return tools
