from fastapi import APIRouter

from app.api.api_v1.endpoints import auth, users, content, ai_tools, tool_combinations, youtube_data, recommendations

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(content.router, prefix="/content", tags=["content"])
api_router.include_router(ai_tools.router, prefix="/ai-tools", tags=["ai-tools"])
api_router.include_router(tool_combinations.router, prefix="/tool-combinations", tags=["tool-combinations"])
api_router.include_router(youtube_data.router, prefix="/youtube", tags=["youtube-data"])
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])
