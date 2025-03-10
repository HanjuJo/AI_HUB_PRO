from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


# Shared properties for YouTube Data
class YoutubeDataBase(BaseModel):
    keyword: str
    popularity_score: Optional[float] = 0.0
    search_volume: Optional[int] = 0
    is_trending: Optional[bool] = False


# Properties to receive on item creation
class YoutubeDataCreate(YoutubeDataBase):
    pass


# Properties to receive on item update
class YoutubeDataUpdate(YoutubeDataBase):
    keyword: Optional[str] = None


# Properties shared by models stored in DB
class YoutubeDataInDBBase(YoutubeDataBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Properties to return via API
class YoutubeData(YoutubeDataInDBBase):
    pass


# Shared properties for YouTube Channel
class YoutubeChannelBase(BaseModel):
    channel_id: str
    channel_name: Optional[str] = None
    subscriber_count: Optional[int] = 0
    video_count: Optional[int] = 0
    is_monetized: Optional[bool] = False
    category: Optional[str] = None
    description: Optional[str] = None


# Properties to receive on item creation
class YoutubeChannelCreate(YoutubeChannelBase):
    pass


# Properties to receive on item update
class YoutubeChannelUpdate(YoutubeChannelBase):
    channel_id: Optional[str] = None
    channel_name: Optional[str] = None


# Properties shared by models stored in DB
class YoutubeChannelInDBBase(YoutubeChannelBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Properties to return via API
class YoutubeChannel(YoutubeChannelInDBBase):
    pass


# Shared properties for Recommended Channel
class RecommendedChannelBase(BaseModel):
    channel_id: str
    channel_name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    reason: Optional[str] = None


# Properties to receive on item creation
class RecommendedChannelCreate(RecommendedChannelBase):
    pass


# Properties to receive on item update
class RecommendedChannelUpdate(RecommendedChannelBase):
    channel_id: Optional[str] = None
    channel_name: Optional[str] = None


# Properties shared by models stored in DB
class RecommendedChannelInDBBase(RecommendedChannelBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Properties to return via API
class RecommendedChannel(RecommendedChannelInDBBase):
    pass
