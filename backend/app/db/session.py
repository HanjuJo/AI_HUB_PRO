import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# PostgreSQL 연결 시도, 실패 시 SQLite 사용
try:
    engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
    # 연결 테스트
    with engine.connect() as conn:
        pass
    print("PostgreSQL 데이터베이스에 연결되었습니다.")
except Exception as e:
    print(f"PostgreSQL 연결 실패: {e}")
    print("SQLite 데이터베이스를 대신 사용합니다.")
    sqlite_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "instance", "ai_hub.db")
    sqlite_url = f"sqlite:///{sqlite_file_path}"
    engine = create_engine(sqlite_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
