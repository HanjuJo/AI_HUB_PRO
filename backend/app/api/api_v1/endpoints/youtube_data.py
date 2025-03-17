from typing import Any, List, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.api import deps
from app.models.youtube_data import YoutubeData, YoutubeChannel, RecommendedChannel
from app.models.user import User
from app.core.config import settings
from app.services.youtube_service import youtube_service

# For YouTube API integration
import googleapiclient.discovery
import googleapiclient.errors

router = APIRouter()


@router.get("/trending", response_model=List[schemas.youtube_data.YoutubeData])
def get_trending_keywords(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get trending YouTube keywords.
    """
    trending_keywords = (
        db.query(YoutubeData)
        .order_by(YoutubeData.popularity.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return trending_keywords


@router.get("/keywords", response_model=List[schemas.youtube_data.YoutubeData])
def get_keywords(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get YouTube keywords.
    """
    keywords = (
        db.query(YoutubeData)
        .order_by(YoutubeData.search_volume.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return keywords


@router.post("/keywords", response_model=schemas.youtube_data.YoutubeData)
def create_keyword(
    *,
    db: Session = Depends(deps.get_db),
    keyword_in: schemas.youtube_data.YoutubeDataCreate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new YouTube keyword.
    """
    keyword = YoutubeData(
        keyword=keyword_in.keyword,
        popularity_score=keyword_in.popularity_score,
        search_volume=keyword_in.search_volume,
        is_trending=keyword_in.is_trending,
    )
    db.add(keyword)
    db.commit()
    db.refresh(keyword)
    return keyword


@router.get("/channels", response_model=List[schemas.youtube_data.YoutubeChannel])
def get_channels(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get YouTube channels.
    """
    channels = (
        db.query(YoutubeChannel)
        .order_by(YoutubeChannel.subscriber_count.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return channels


@router.post("/channels", response_model=schemas.youtube_data.YoutubeChannel)
def create_channel(
    *,
    db: Session = Depends(deps.get_db),
    channel_in: schemas.youtube_data.YoutubeChannelCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create or update YouTube channel.
    """
    channel = db.query(YoutubeChannel).filter(YoutubeChannel.channel_id == channel_in.channel_id).first()
    
    if channel:
        # Update existing channel
        for field, value in channel_in.dict(exclude_unset=True).items():
            setattr(channel, field, value)
    else:
        # Create new channel
        channel = YoutubeChannel(**channel_in.dict())
        db.add(channel)
    
    db.commit()
    db.refresh(channel)
    return channel


@router.get("/channels/{channel_id}", response_model=schemas.youtube_data.YoutubeChannel)
def get_channel(
    channel_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get YouTube channel details.
    """
    channel = db.query(YoutubeChannel).filter(YoutubeChannel.channel_id == channel_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    return channel


@router.post("/check-monetization", response_model=schemas.youtube_data.YoutubeChannel)
async def check_channel_monetization(
    *,
    db: Session = Depends(deps.get_db),
    channel_id: str,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Check if a YouTube channel is monetized.
    """
    # First check if we already have this channel in our database
    channel = db.query(YoutubeChannel).filter(YoutubeChannel.channel_id == channel_id).first()
    
    # If not, fetch it from YouTube API
    if not channel:
        try:
            # Initialize YouTube API client
            api_service_name = "youtube"
            api_version = "v3"
            youtube = googleapiclient.discovery.build(
                api_service_name, api_version, developerKey=settings.YOUTUBE_API_KEY
            )
            
            # Get channel info
            request = youtube.channels().list(
                part="snippet,statistics,status",
                id=channel_id
            )
            response = request.execute()
            
            if not response["items"]:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Channel not found on YouTube",
                )
            
            channel_data = response["items"][0]
            
            # Create new channel in our database
            channel = YoutubeChannel(
                channel_id=channel_id,
                channel_name=channel_data["snippet"]["title"],
                subscriber_count=int(channel_data["statistics"].get("subscriberCount", 0)),
                video_count=int(channel_data["statistics"].get("videoCount", 0)),
                description=channel_data["snippet"].get("description", ""),
                # This is a simplification - actual monetization status requires more complex checks
                is_monetized=channel_data["status"].get("madeForKids", False) == False and 
                            int(channel_data["statistics"].get("subscriberCount", 0)) >= 1000 and
                            int(channel_data["statistics"].get("videoCount", 0)) >= 10,
            )
            db.add(channel)
            db.commit()
            db.refresh(channel)
            
        except googleapiclient.errors.HttpError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"YouTube API error: {str(e)}",
            )
    
    return channel


@router.get("/recommended-channels", response_model=List[schemas.youtube_data.RecommendedChannel])
def get_recommended_channels(
    db: Session = Depends(deps.get_db),
    category: str = None,
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get recommended YouTube channels, optionally filtered by category.
    """
    query = db.query(RecommendedChannel)
    
    if category:
        query = query.filter(RecommendedChannel.category == category)
    
    recommended_channels = query.offset(skip).limit(limit).all()
    return recommended_channels


@router.get("/recommendations/{channel_id}", response_model=List[schemas.youtube_data.RecommendedChannel])
def get_recommended_channels(
    channel_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get recommended channels based on a YouTube channel.
    """
    recommendations = (
        db.query(RecommendedChannel)
        .filter(RecommendedChannel.source_channel_id == channel_id)
        .all()
    )
    return recommendations


@router.post("/analyze", response_model=Dict[str, Any])
async def analyze_youtube_channel(
    data: Dict[str, str],
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    분석할 유튜브 채널 URL을 받아 채널 통계 및 비디오 분석 결과를 반환합니다.
    """
    channel_url = data.get("channel_url")
    if not channel_url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="채널 URL이 제공되지 않았습니다."
        )
    
    # 채널 분석 실행
    analysis_result = youtube_service.analyze_channel(channel_url)
    
    if "error" in analysis_result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=analysis_result["error"]
        )
    
    return analysis_result


@router.get("/recommendations", response_model=List[Dict[str, Any]])
async def get_channel_recommendations(
    channel_id: str,
    max_results: int = 10,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    유튜브 채널 ID를 기반으로 유사한 채널을 추천합니다.
    """
    if not channel_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="채널 ID가 제공되지 않았습니다."
        )
    
    recommendations = youtube_service.get_channel_recommendations(channel_id, max_results)
    
    if not recommendations:
        return []
    
    return recommendations
