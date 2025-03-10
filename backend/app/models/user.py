from datetime import datetime
from typing import List, Optional

from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.core.security import get_password_hash, verify_password


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, index=True)
    email = Column(String(120), unique=True, index=True)
    password_hash = Column(String(128), nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    tool_combinations = relationship("ToolCombination", back_populates="user")
    
    def set_password(self, password: str) -> None:
        self.password_hash = get_password_hash(password)
    
    def verify_password(self, password: str) -> bool:
        return verify_password(password, self.password_hash)
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_active": self.is_active,
            "is_superuser": self.is_superuser,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None
        }
    
    def __repr__(self) -> str:
        return f"<User {self.username}>"

