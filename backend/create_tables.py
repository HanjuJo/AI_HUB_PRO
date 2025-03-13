from app.db.base import Base
from app.db.session import engine
from app.models.user import User  # 다른 모델들도 필요하다면 여기에 import

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    print("Creating database tables...")
    init_db()
    print("Database tables created successfully!")
