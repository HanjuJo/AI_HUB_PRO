import os
import sys
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api_v1.api import api_router
from app.core.config import settings
from dotenv import load_dotenv

# 로깅 설정
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("app")

# Load environment variables
load_dotenv()

# Set default environment variables if not present
if not os.environ.get('SECRET_KEY'):
    os.environ['SECRET_KEY'] = settings.SECRET_KEY
    print("Warning: Using default SECRET_KEY. This is not secure for production.")

# Database URL will be handled by SQLAlchemy configuration

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI 콘텐츠 제작 지원 플랫폼 API",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    debug=True
)

logger.info("FastAPI 애플리케이션 초기화 완료")

# Set up CORS - 개발 환경에서는 모든 오리진 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "http://localhost:5173", "http://127.0.0.1:5173", "http://127.0.0.1:58694"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*", "Authorization", "Content-Type", "Accept"],
    expose_headers=["*"],
    max_age=3600,
)

logger.info("CORS 설정 완료: 모든 오리진 허용")

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "AI HUB API 서비스에 오신 것을 환영합니다!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
