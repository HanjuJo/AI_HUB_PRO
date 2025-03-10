from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.api import deps
from app.models.youtube_data import YoutubeData, YoutubeChannel, RecommendedChannel
from app.models.user import User
from app.core.config import settings

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
        .filter(YoutubeData.is_trending == True)
        .order_by(YoutubeData.popularity_score.desc())
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
    *,
    db: Session = Depends(deps.get_db),
    channel_id: str,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get YouTube channel by ID.
    """
    channel = db.query(YoutubeChannel).filter(YoutubeChannel.channel_id == channel_id).first()
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found",
        )
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
