from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required
import os
import requests
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from app.models import db
from app.models.youtube_data import YoutubeData, YoutubeChannel, RecommendedChannel

youtube_bp = Blueprint('youtube', __name__, url_prefix='/api/youtube')

def get_youtube_service():
    """Create a YouTube API service object"""
    api_key = os.environ.get('YOUTUBE_API_KEY')
    return build('youtube', 'v3', developerKey=api_key)

@youtube_bp.route('/trending', methods=['GET'])
def get_trending_keywords():
    """Get trending YouTube keywords"""
    trending_keywords = YoutubeData.query.filter_by(is_trending=True).order_by(YoutubeData.popularity_score.desc()).limit(20).all()
    
    return jsonify({
        'trending_keywords': [keyword.to_dict() for keyword in trending_keywords]
    }), 200

@youtube_bp.route('/search', methods=['GET'])
def search_youtube():
    """Search YouTube for videos by keyword"""
    keyword = request.args.get('q')
    
    if not keyword:
        return jsonify({'error': 'Keyword is required'}), 400
    
    try:
        youtube = get_youtube_service()
        
        # Search for videos
        search_response = youtube.search().list(
            q=keyword,
            part='id,snippet',
            maxResults=10,
            type='video'
        ).execute()
        
        # Get video statistics
        video_ids = [item['id']['videoId'] for item in search_response['items']]
        videos_response = youtube.videos().list(
            id=','.join(video_ids),
            part='statistics,contentDetails'
        ).execute()
        
        # Combine search and video data
        videos = []
        for i, search_item in enumerate(search_response['items']):
            video_id = search_item['id']['videoId']
            video_stats = next((item for item in videos_response['items'] if item['id'] == video_id), None)
            
            video_data = {
                'id': video_id,
                'title': search_item['snippet']['title'],
                'description': search_item['snippet']['description'],
                'thumbnail': search_item['snippet']['thumbnails']['high']['url'],
                'channel_title': search_item['snippet']['channelTitle'],
                'channel_id': search_item['snippet']['channelId'],
                'published_at': search_item['snippet']['publishedAt']
            }
            
            if video_stats:
                video_data.update({
                    'view_count': video_stats['statistics'].get('viewCount', 0),
                    'like_count': video_stats['statistics'].get('likeCount', 0),
                    'comment_count': video_stats['statistics'].get('commentCount', 0),
                    'duration': video_stats['contentDetails']['duration']
                })
            
            videos.append(video_data)
        
        # Save keyword to database if it doesn't exist
        existing_keyword = YoutubeData.query.filter_by(keyword=keyword).first()
        if not existing_keyword:
            new_keyword = YoutubeData(keyword=keyword)
            db.session.add(new_keyword)
            db.session.commit()
        else:
            # Update search volume
            existing_keyword.search_volume += 1
            db.session.commit()
        
        return jsonify({
            'keyword': keyword,
            'videos': videos
        }), 200
        
    except HttpError as e:
        return jsonify({'error': f'YouTube API error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500

@youtube_bp.route('/channel/check', methods=['POST'])
def check_channel_monetization():
    """Check if a YouTube channel is monetized"""
    data = request.get_json()
    
    if not data or not data.get('channel_url'):
        return jsonify({'error': 'Channel URL is required'}), 400
    
    channel_url = data['channel_url']
    
    # Extract channel ID from URL
    channel_id = None
    if 'youtube.com/channel/' in channel_url:
        channel_id = channel_url.split('youtube.com/channel/')[1].split('/')[0]
    elif 'youtube.com/c/' in channel_url:
        # For custom URLs, we need to fetch the channel page and extract the ID
        # This is a simplified approach and might not work for all cases
        try:
            response = requests.get(channel_url)
            html = response.text
            start_index = html.find('"channelId":"') + 13
            end_index = html.find('"', start_index)
            channel_id = html[start_index:end_index]
        except:
            return jsonify({'error': 'Could not extract channel ID from URL'}), 400
    elif 'youtube.com/@' in channel_url:
        # For handle URLs, similar approach as custom URLs
        try:
            response = requests.get(channel_url)
            html = response.text
            start_index = html.find('"channelId":"') + 13
            end_index = html.find('"', start_index)
            channel_id = html[start_index:end_index]
        except:
            return jsonify({'error': 'Could not extract channel ID from URL'}), 400
    
    if not channel_id:
        return jsonify({'error': 'Invalid channel URL'}), 400
    
    try:
        youtube = get_youtube_service()
        
        # Get channel details
        channel_response = youtube.channels().list(
            id=channel_id,
            part='snippet,statistics,status'
        ).execute()
        
        if not channel_response['items']:
            return jsonify({'error': 'Channel not found'}), 404
        
        channel_data = channel_response['items'][0]
        
        # Check if channel is in Partner Program
        # Note: YouTube API doesn't directly expose monetization status
        # We'll use some heuristics based on available data
        
        subscriber_count = int(channel_data['statistics'].get('subscriberCount', 0))
        video_count = int(channel_data['statistics'].get('videoCount', 0))
        view_count = int(channel_data['statistics'].get('viewCount', 0))
        
        # Heuristic: Channels need 1000+ subscribers and 4000+ watch hours to be eligible
        is_likely_monetized = subscriber_count >= 1000 and video_count >= 10 and view_count >= 4000 * 60
        
        # Save or update channel in database
        existing_channel = YoutubeChannel.query.filter_by(channel_id=channel_id).first()
        if existing_channel:
            existing_channel.subscriber_count = subscriber_count
            existing_channel.video_count = video_count
            existing_channel.is_monetized = is_likely_monetized
            db.session.commit()
        else:
            new_channel = YoutubeChannel(
                channel_id=channel_id,
                channel_name=channel_data['snippet']['title'],
                subscriber_count=subscriber_count,
                video_count=video_count,
                is_monetized=is_likely_monetized,
                description=channel_data['snippet'].get('description', '')
            )
            db.session.add(new_channel)
            db.session.commit()
        
        return jsonify({
            'channel_id': channel_id,
            'channel_name': channel_data['snippet']['title'],
            'subscriber_count': subscriber_count,
            'video_count': video_count,
            'view_count': view_count,
            'is_likely_monetized': is_likely_monetized,
            'monetization_status': 'Likely monetized' if is_likely_monetized else 'Likely not monetized',
            'requirements': {
                'subscribers': {
                    'required': 1000,
                    'current': subscriber_count,
                    'met': subscriber_count >= 1000
                },
                'watch_time': {
                    'required': '4000 hours',
                    'estimated': 'Unknown (YouTube API limitation)',
                    'met': 'Unknown'
                }
            }
        }), 200
        
    except HttpError as e:
        return jsonify({'error': f'YouTube API error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500

@youtube_bp.route('/recommended-channels', methods=['GET'])
def get_recommended_channels():
    """Get recommended YouTube channels for AI content creation"""
    category = request.args.get('category')
    
    query = RecommendedChannel.query
    
    if category:
        query = query.filter_by(category=category)
    
    recommended_channels = query.all()
    
    return jsonify({
        'recommended_channels': [channel.to_dict() for channel in recommended_channels]
    }), 200
