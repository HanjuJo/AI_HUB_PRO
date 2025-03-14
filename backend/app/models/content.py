from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Content(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), index=True)
    description = Column(Text)
    content_type = Column(String(50))  # video, blog, social
    keywords = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # SEO 관련 필드
    seo_score = Column(Float, default=0.0)
    meta_description = Column(String(300))
    meta_keywords = Column(String(200))
    
    # 콘텐츠 품질 점수
    readability_score = Column(Float, default=0.0)
    engagement_score = Column(Float, default=0.0)
    technical_score = Column(Float, default=0.0)
    
    # 외래 키
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="contents")
    
    # 최적화 제안
    optimization_suggestions = relationship("OptimizationSuggestion", back_populates="content")
    
    def calculate_overall_score(self) -> float:
        """전체 콘텐츠 점수 계산"""
        weights = {
            "seo": 0.4,
            "readability": 0.2,
            "engagement": 0.2,
            "technical": 0.2
        }
        return (
            self.seo_score * weights["seo"] +
            self.readability_score * weights["readability"] +
            self.engagement_score * weights["engagement"] +
            self.technical_score * weights["technical"]
        )
    
    def to_dict(self) -> dict:
        """콘텐츠 객체를 딕셔너리로 변환"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "content_type": self.content_type,
            "keywords": self.keywords,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "seo_score": self.seo_score,
            "meta_description": self.meta_description,
            "meta_keywords": self.meta_keywords,
            "readability_score": self.readability_score,
            "engagement_score": self.engagement_score,
            "technical_score": self.technical_score,
            "overall_score": self.calculate_overall_score(),
            "user_id": self.user_id
        }

class OptimizationSuggestion(Base):
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(50))  # seo, readability, engagement, technical
    suggestion = Column(Text)
    priority = Column(Integer)  # 1 (높음) ~ 3 (낮음)
    implemented = Column(Integer, default=0)  # 0: 미구현, 1: 구현
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 외래 키
    content_id = Column(Integer, ForeignKey("content.id"))
    content = relationship("Content", back_populates="optimization_suggestions")
    
    def to_dict(self) -> dict:
        """최적화 제안을 딕셔너리로 변환"""
        return {
            "id": self.id,
            "category": self.category,
            "suggestion": self.suggestion,
            "priority": self.priority,
            "implemented": self.implemented,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "content_id": self.content_id
        }
