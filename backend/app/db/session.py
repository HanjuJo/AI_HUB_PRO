import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# 데이터베이스 엔진 생성
engine = create_engine(
    str(settings.SQLALCHEMY_DATABASE_URI),
    pool_pre_ping=True,  # 연결 상태 확인
    connect_args={"check_same_thread": False}  # SQLite를 위한 설정
)

# 데이터베이스 파일 경로 확인 및 생성 (SQLite 사용 시)
if settings.SQLALCHEMY_DATABASE_URI.startswith("sqlite"):
    db_path = settings.SQLALCHEMY_DATABASE_URI.replace("sqlite:///", "")
    db_dir = os.path.dirname(os.path.abspath(db_path))
    
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
        print(f"Created database directory: {db_dir}")
    
    print(f"Using SQLite database at: {db_path}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
