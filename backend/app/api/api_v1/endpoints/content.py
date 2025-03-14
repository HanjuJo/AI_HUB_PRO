from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.api import deps
from app.services.content_analyzer import ContentAnalyzer

router = APIRouter()
content_analyzer = ContentAnalyzer()

@router.post("/", response_model=schemas.content.Content)
def create_content(
    *,
    db: Session = Depends(deps.get_db),
    content_in: schemas.content.ContentCreate,
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    """새로운 콘텐츠를 생성합니다."""
    content = models.Content(
        title=content_in.title,
        description=content_in.description,
        content_type=content_in.content_type,
        keywords=content_in.keywords,
        meta_description=content_in.meta_description,
        meta_keywords=content_in.meta_keywords,
        user_id=current_user.id
    )
    
    # 콘텐츠 분석 수행
    analysis = content_analyzer.analyze_content({
        "title": content.title,
        "description": content.description,
        "content_type": content.content_type,
        "keywords": content.keywords,
        "meta_description": content.meta_description,
        "meta_keywords": content.meta_keywords
    })
    
    # 분석 결과 저장
    content.seo_score = analysis["seo_score"]
    content.readability_score = analysis["readability_score"]
    content.engagement_score = analysis["engagement_score"]
    content.technical_score = analysis["technical_score"]
    
    db.add(content)
    db.commit()
    db.refresh(content)
    
    # 최적화 제안 저장
    for suggestion in analysis["suggestions"]:
        optimization = models.OptimizationSuggestion(
            category=suggestion["category"],
            suggestion=suggestion["suggestion"],
            priority=suggestion["priority"],
            content_id=content.id
        )
        db.add(optimization)
    
    db.commit()
    return content

@router.get("/me", response_model=List[schemas.content.Content])
def read_user_contents(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    """현재 사용자의 모든 콘텐츠를 조회합니다."""
    contents = (
        db.query(models.Content)
        .filter(models.Content.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return contents

@router.get("/{content_id}", response_model=schemas.content.ContentWithScore)
def read_content(
    *,
    db: Session = Depends(deps.get_db),
    content_id: int,
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    """특정 콘텐츠의 상세 정보를 조회합니다."""
    content = (
        db.query(models.Content)
        .filter(models.Content.id == content_id)
        .first()
    )
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )
    if content.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return content

@router.put("/{content_id}", response_model=schemas.content.Content)
def update_content(
    *,
    db: Session = Depends(deps.get_db),
    content_id: int,
    content_in: schemas.content.ContentUpdate,
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    """콘텐츠를 업데이트합니다."""
    content = (
        db.query(models.Content)
        .filter(models.Content.id == content_id)
        .first()
    )
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )
    if content.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    update_data = content_in.dict(exclude_unset=True)
    if update_data:
        # 업데이트할 데이터가 있는 경우에만 분석 수행
        analysis = content_analyzer.analyze_content({
            "title": update_data.get("title", content.title),
            "description": update_data.get("description", content.description),
            "content_type": update_data.get("content_type", content.content_type),
            "keywords": update_data.get("keywords", content.keywords),
            "meta_description": update_data.get("meta_description", content.meta_description),
            "meta_keywords": update_data.get("meta_keywords", content.meta_keywords)
        })
        
        # 분석 결과 업데이트
        update_data.update({
            "seo_score": analysis["seo_score"],
            "readability_score": analysis["readability_score"],
            "engagement_score": analysis["engagement_score"],
            "technical_score": analysis["technical_score"]
        })
        
        # 기존 최적화 제안 삭제
        db.query(models.OptimizationSuggestion).filter(
            models.OptimizationSuggestion.content_id == content.id
        ).delete()
        
        # 새로운 최적화 제안 추가
        for suggestion in analysis["suggestions"]:
            optimization = models.OptimizationSuggestion(
                category=suggestion["category"],
                suggestion=suggestion["suggestion"],
                priority=suggestion["priority"],
                content_id=content.id
            )
            db.add(optimization)
        
        for key, value in update_data.items():
            setattr(content, key, value)
        
        db.commit()
        db.refresh(content)
    
    return content

@router.delete("/{content_id}")
def delete_content(
    *,
    db: Session = Depends(deps.get_db),
    content_id: int,
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    """콘텐츠를 삭제합니다."""
    content = (
        db.query(models.Content)
        .filter(models.Content.id == content_id)
        .first()
    )
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )
    if content.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # 관련된 최적화 제안도 함께 삭제
    db.query(models.OptimizationSuggestion).filter(
        models.OptimizationSuggestion.content_id == content.id
    ).delete()
    
    db.delete(content)
    db.commit()
    return {"message": "Content deleted successfully"}
