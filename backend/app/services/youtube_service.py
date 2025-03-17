import os
import googleapiclient.discovery
import googleapiclient.errors
from datetime import datetime, timedelta
import isodate

class YouTubeService:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("YOUTUBE_API_KEY", "YOUR_API_KEY_HERE")
        self.youtube = self._init_youtube_client()

    def _init_youtube_client(self):
        """YouTube API 클라이언트를 초기화합니다."""
        return googleapiclient.discovery.build(
            "youtube", "v3", developerKey=self.api_key, cache_discovery=False
        )

    def get_channel_id_from_url(self, channel_url):
        """채널 URL에서 채널 ID를 추출합니다."""
        if "youtube.com/channel/" in channel_url:
            return channel_url.split("youtube.com/channel/")[1].split("/")[0]
        elif "youtube.com/user/" in channel_url:
            handle = channel_url.split("youtube.com/user/")[1].split("/")[0]
            return self.get_channel_id_from_handle(handle)
        elif "youtube.com/@" in channel_url:
            handle = channel_url.split("youtube.com/@")[1].split("/")[0]
            return self.get_channel_id_from_handle(handle)
        return None

    def get_channel_id_from_handle(self, handle):
        """사용자 핸들에서 채널 ID를 가져옵니다."""
        try:
            request = self.youtube.search().list(
                part="snippet",
                q=handle,
                type="channel",
                maxResults=1
            )
            response = request.execute()
            if response["items"]:
                return response["items"][0]["id"]["channelId"]
        except Exception as e:
            print(f"Error fetching channel ID: {str(e)}")
        return None

    def get_channel_info(self, channel_id):
        """채널 정보를 가져옵니다."""
        try:
            request = self.youtube.channels().list(
                part="snippet,statistics,contentDetails",
                id=channel_id
            )
            response = request.execute()
            
            if not response["items"]:
                return None
                
            channel_data = response["items"][0]
            
            return {
                "id": channel_id,
                "title": channel_data["snippet"]["title"],
                "description": channel_data["snippet"]["description"],
                "thumbnail": channel_data["snippet"]["thumbnails"]["high"]["url"],
                "subscriberCount": int(channel_data["statistics"]["subscriberCount"]),
                "videoCount": int(channel_data["statistics"]["videoCount"]),
                "viewCount": int(channel_data["statistics"]["viewCount"]),
                "publishedAt": channel_data["snippet"]["publishedAt"],
                "country": channel_data["snippet"].get("country", "알 수 없음"),
                "uploadsPlaylistId": channel_data["contentDetails"]["relatedPlaylists"]["uploads"]
            }
        except Exception as e:
            print(f"Error fetching channel info: {str(e)}")
            return None

    def get_channel_videos(self, uploads_playlist_id, max_results=50):
        """채널의 비디오 목록을 가져옵니다."""
        try:
            request = self.youtube.playlistItems().list(
                part="snippet,contentDetails",
                playlistId=uploads_playlist_id,
                maxResults=max_results
            )
            response = request.execute()
            
            videos = []
            for item in response["items"]:
                video_id = item["contentDetails"]["videoId"]
                videos.append({
                    "id": video_id,
                    "title": item["snippet"]["title"],
                    "description": item["snippet"]["description"],
                    "thumbnail": item["snippet"]["thumbnails"]["high"]["url"],
                    "publishedAt": item["snippet"]["publishedAt"],
                    "videoId": video_id
                })
                
            return videos
        except Exception as e:
            print(f"Error fetching channel videos: {str(e)}")
            return []

    def get_video_details(self, video_ids):
        """비디오 세부 정보를 가져옵니다."""
        try:
            # 최대 50개의 비디오만 한 번에 요청 가능
            chunks = [video_ids[i:i + 50] for i in range(0, len(video_ids), 50)]
            
            all_videos = []
            for chunk in chunks:
                request = self.youtube.videos().list(
                    part="snippet,statistics,contentDetails",
                    id=",".join(chunk)
                )
                response = request.execute()
                
                for item in response["items"]:
                    duration = isodate.parse_duration(item["contentDetails"]["duration"]).total_seconds()
                    
                    video_data = {
                        "id": item["id"],
                        "title": item["snippet"]["title"],
                        "description": item["snippet"]["description"],
                        "thumbnail": item["snippet"]["thumbnails"]["high"]["url"],
                        "publishedAt": item["snippet"]["publishedAt"],
                        "viewCount": int(item["statistics"].get("viewCount", 0)),
                        "likeCount": int(item["statistics"].get("likeCount", 0)),
                        "commentCount": int(item["statistics"].get("commentCount", 0)),
                        "duration": int(duration),
                        "tags": item["snippet"].get("tags", [])
                    }
                    all_videos.append(video_data)
                    
            return all_videos
        except Exception as e:
            print(f"Error fetching video details: {str(e)}")
            return []
            
    def analyze_channel(self, channel_url):
        """채널 분석을 실행합니다."""
        channel_id = self.get_channel_id_from_url(channel_url)
        if not channel_id:
            return {"error": "채널 ID를 찾을 수 없습니다."}
            
        channel_info = self.get_channel_info(channel_id)
        if not channel_info:
            return {"error": "채널 정보를 가져올 수 없습니다."}
            
        # 최근 비디오 목록 가져오기
        videos = self.get_channel_videos(channel_info["uploadsPlaylistId"], 20)
        video_ids = [v["id"] for v in videos]
        
        # 비디오 세부 정보 가져오기
        video_details = self.get_video_details(video_ids)
        
        # 채널 통계 분석
        analysis = self.analyze_videos(video_details)
        
        return {
            "channel": channel_info,
            "videos": video_details,
            "analysis": analysis
        }
        
    def analyze_videos(self, videos):
        """비디오 데이터를 분석합니다."""
        if not videos:
            return {"error": "분석할 비디오가 없습니다."}
            
        total_views = sum(video["viewCount"] for video in videos)
        total_likes = sum(video["likeCount"] for video in videos)
        total_comments = sum(video["commentCount"] for video in videos)
        total_duration = sum(video["duration"] for video in videos)
        
        avg_views = total_views / len(videos) if videos else 0
        avg_likes = total_likes / len(videos) if videos else 0
        avg_comments = total_comments / len(videos) if videos else 0
        avg_duration = total_duration / len(videos) if videos else 0
        
        # 태그 분석
        all_tags = []
        for video in videos:
            all_tags.extend(video.get("tags", []))
            
        tag_count = {}
        for tag in all_tags:
            tag_count[tag] = tag_count.get(tag, 0) + 1
            
        # 가장 많이 사용된 태그 (최대 10개)
        popular_tags = sorted(tag_count.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # 게시일 분석
        current_date = datetime.now()
        recent_videos = [v for v in videos if (current_date - datetime.fromisoformat(v["publishedAt"].replace("Z", "+00:00"))).days <= 30]
        upload_frequency = len(recent_videos) / 30 * 30 if recent_videos else 0  # 한 달 평균 업로드 수
        
        # 인기 비디오
        most_viewed = sorted(videos, key=lambda x: x["viewCount"], reverse=True)[:5]
        most_liked = sorted(videos, key=lambda x: x["likeCount"], reverse=True)[:5]
        most_commented = sorted(videos, key=lambda x: x["commentCount"], reverse=True)[:5]
        
        return {
            "totalVideos": len(videos),
            "totalViews": total_views,
            "totalLikes": total_likes,
            "totalComments": total_comments,
            "avgViews": int(avg_views),
            "avgLikes": int(avg_likes),
            "avgComments": int(avg_comments),
            "avgDuration": int(avg_duration),
            "popularTags": [{"tag": tag, "count": count} for tag, count in popular_tags],
            "uploadFrequency": round(upload_frequency, 1),
            "mostViewed": [{"id": v["id"], "title": v["title"], "viewCount": v["viewCount"]} for v in most_viewed],
            "mostLiked": [{"id": v["id"], "title": v["title"], "likeCount": v["likeCount"]} for v in most_liked],
            "mostCommented": [{"id": v["id"], "title": v["title"], "commentCount": v["commentCount"]} for v in most_commented]
        }
        
    def get_channel_recommendations(self, channel_id, max_results=10):
        """유사한 채널을 추천합니다."""
        try:
            channel_info = self.get_channel_info(channel_id)
            if not channel_info:
                return []
                
            # 채널 제목으로 관련 채널 검색
            request = self.youtube.search().list(
                part="snippet",
                q=channel_info["title"],
                type="channel",
                maxResults=max_results + 1  # 자기 자신 제외
            )
            response = request.execute()
            
            recommendations = []
            for item in response["items"]:
                rec_channel_id = item["id"]["channelId"]
                if rec_channel_id != channel_id:  # 자기 자신 제외
                    recommendations.append({
                        "id": rec_channel_id,
                        "title": item["snippet"]["title"],
                        "description": item["snippet"]["description"],
                        "thumbnail": item["snippet"]["thumbnails"]["high"]["url"]
                    })
                    
                    if len(recommendations) >= max_results:
                        break
                        
            return recommendations
        except Exception as e:
            print(f"Error fetching channel recommendations: {str(e)}")
            return []

# 서비스 인스턴스 생성
youtube_service = YouTubeService() 