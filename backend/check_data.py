"""
데이터베이스에 저장된 데이터를 확인하는 스크립트
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# Flask 애플리케이션 초기화
app = Flask(__name__)

# 데이터베이스 설정
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///ai_hub.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 데이터베이스 초기화
db = SQLAlchemy(app)

# 데이터베이스 모델 정의
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_superuser = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<User {self.username}>'

class AITool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, index=True)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    url = db.Column(db.String(255))
    pricing_model = db.Column(db.String(50))
    
    def __repr__(self):
        return f'<AITool {self.name}>'

class ToolCombination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True)
    description = db.Column(db.Text)
    use_case = db.Column(db.String(100))
    
    def __repr__(self):
        return f'<ToolCombination {self.name}>'

class YoutubeData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.String(100), index=True)
    video_id = db.Column(db.String(100), unique=True, index=True)
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    view_count = db.Column(db.Integer)
    like_count = db.Column(db.Integer)
    comment_count = db.Column(db.Integer)
    
    def __repr__(self):
        return f'<YoutubeData {self.title}>'

# 데이터베이스 데이터 확인 함수
def check_data():
    # 사용자 데이터 확인
    users = User.query.all()
    print(f"\n=== 사용자 데이터 ({len(users)}명) ===")
    for user in users:
        print(f"ID: {user.id}, 사용자명: {user.username}, 이메일: {user.email}, 관리자: {user.is_superuser}")
    
    # AI 도구 데이터 확인
    ai_tools = AITool.query.all()
    print(f"\n=== AI 도구 데이터 ({len(ai_tools)}개) ===")
    for tool in ai_tools:
        print(f"ID: {tool.id}, 이름: {tool.name}, 카테고리: {tool.category}, 가격 모델: {tool.pricing_model}")
    
    # 도구 조합 데이터 확인
    tool_combinations = ToolCombination.query.all()
    print(f"\n=== 도구 조합 데이터 ({len(tool_combinations)}개) ===")
    for combo in tool_combinations:
        print(f"ID: {combo.id}, 이름: {combo.name}, 사용 사례: {combo.use_case}")
    
    # YouTube 데이터 확인
    youtube_data = YoutubeData.query.all()
    print(f"\n=== YouTube 데이터 ({len(youtube_data)}개) ===")
    for data in youtube_data:
        if data:
            print(f"ID: {data.id}, 제목: {data.title}, 조회수: {data.view_count}")

# 애플리케이션 컨텍스트 내에서 데이터 확인
with app.app_context():
    check_data()
