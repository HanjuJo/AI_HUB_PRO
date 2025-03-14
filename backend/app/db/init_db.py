import logging
from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.session import engine
from app.models.user import User
from app.core.config import settings


logger = logging.getLogger(__name__)


def init_db(db: Session) -> None:
    try:
        # 테이블 생성
        Base.metadata.create_all(bind=engine)
        logger.info("데이터베이스 테이블이 성공적으로 생성되었습니다.")
        
        # 초기 관리자 계정 생성
        user = db.query(User).filter(User.email == settings.FIRST_SUPERUSER_EMAIL).first()
        if not user:
            user = User(
                email=settings.FIRST_SUPERUSER_EMAIL,
                username=settings.FIRST_SUPERUSER_USERNAME,
                is_superuser=True,
                is_active=True
            )
            user.set_password(settings.FIRST_SUPERUSER_PASSWORD)
            db.add(user)
            db.commit()
            db.refresh(user)
            logger.info(f"초기 관리자 계정이 생성되었습니다: {user.email}")
        else:
            logger.info("관리자 계정이 이미 존재합니다.")
            
    except Exception as e:
        logger.error(f"데이터베이스 초기화 오류: {str(e)}")
        raise
