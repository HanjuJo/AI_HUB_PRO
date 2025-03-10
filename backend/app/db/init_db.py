import logging
from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.session import engine
from app.models.user import User
from app.core.config import settings


logger = logging.getLogger(__name__)


def init_db(db: Session) -> None:
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create initial superuser if it doesn't exist
    user = db.query(User).filter(User.email == settings.FIRST_SUPERUSER_EMAIL).first()
    if not user:
        user = User(
            email=settings.FIRST_SUPERUSER_EMAIL,
            username=settings.FIRST_SUPERUSER_USERNAME,
            is_superuser=True,
        )
        user.set_password(settings.FIRST_SUPERUSER_PASSWORD)
        db.add(user)
        db.commit()
        logger.info("Initial superuser created")
    else:
        logger.info("Superuser already exists")
