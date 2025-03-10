from datetime import datetime
from typing import List, Optional

from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class YoutubeData(Base):
    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String(100), nullable=False, index=True)
    popularity_score = Column(Float, default=0.0)
    search_volume = Column(Integer, default=0)
    is_trending = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "keyword": self.keyword,
            "popularity_score": self.popularity_score,
            "search_volume": self.search_volume,
            "is_trending": self.is_trending,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self) -> str:
        return f"<YoutubeData {self.keyword}>"

class YoutubeChannel(Base):
    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(String(100), unique=True, nullable=False, index=True)
    channel_name = Column(String(100))
    subscriber_count = Column(Integer, default=0)
    video_count = Column(Integer, default=0)
    is_monetized = Column(Boolean, default=False)
    category = Column(String(50))
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "channel_id": self.channel_id,
            "channel_name": self.channel_name,
            "subscriber_count": self.subscriber_count,
            "video_count": self.video_count,
            "is_monetized": self.is_monetized,
            "category": self.category,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self) -> str:
        return f"<YoutubeChannel {self.channel_name}>"

class RecommendedChannel(Base):
    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(String(100), unique=True, nullable=False, index=True)
    channel_name = Column(String(100))
    category = Column(String(50))
    description = Column(Text)
    reason = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "channel_id": self.channel_id,
            "channel_name": self.channel_name,
            "category": self.category,
            "description": self.description,
            "reason": self.reason,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self) -> str:
        return f"<RecommendedChannel {self.channel_name}>"
