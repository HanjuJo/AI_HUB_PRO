"""
데이터베이스에 초기 데이터를 추가하는 스크립트
"""
import os
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

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
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<User {self.username}>'

class AITool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, index=True)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    url = db.Column(db.String(255))
    pricing_model = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<AITool {self.name}>'

class ToolCombination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True)
    description = db.Column(db.Text)
    use_case = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
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
    published_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<YoutubeData {self.title}>'

# 초기 데이터 추가 함수
def add_initial_data():
    # 관리자 사용자 추가
    admin_user = User(
        username="admin",
        email="admin@aihub.com",
        password_hash=generate_password_hash("admin123"),
        is_active=True,
        is_superuser=True
    )
    
    # 일반 사용자 추가
    test_user = User(
        username="testuser",
        email="test@example.com",
        password_hash=generate_password_hash("test123"),
        is_active=True,
        is_superuser=False
    )
    
    # AI 도구 추가
    ai_tools = [
        AITool(
            name="ChatGPT",
            description="OpenAI에서 개발한 대화형 AI 모델로, 자연어 처리 및 대화 생성에 특화되어 있습니다.",
            category="텍스트 생성",
            url="https://chat.openai.com",
            pricing_model="무료/유료"
        ),
        AITool(
            name="DALL-E",
            description="텍스트 설명을 기반으로 이미지를 생성하는 AI 도구입니다.",
            category="이미지 생성",
            url="https://openai.com/dall-e-2",
            pricing_model="유료"
        ),
        AITool(
            name="Midjourney",
            description="텍스트 프롬프트를 기반으로 고품질 이미지를 생성하는 AI 도구입니다.",
            category="이미지 생성",
            url="https://www.midjourney.com",
            pricing_model="유료"
        ),
        AITool(
            name="Descript",
            description="오디오 및 비디오 편집을 위한 AI 기반 도구로, 텍스트 편집을 통해 오디오를 편집할 수 있습니다.",
            category="오디오/비디오 편집",
            url="https://www.descript.com",
            pricing_model="무료/유료"
        ),
        AITool(
            name="Canva",
            description="디자인 및 그래픽 제작을 위한 도구로, AI 기능이 통합되어 있습니다.",
            category="디자인",
            url="https://www.canva.com",
            pricing_model="무료/유료"
        )
    ]
    
    # 도구 조합 추가
    tool_combinations = [
        ToolCombination(
            name="콘텐츠 제작 기본 세트",
            description="유튜브 콘텐츠 제작을 위한 기본 AI 도구 조합입니다.",
            use_case="유튜브 콘텐츠 제작"
        ),
        ToolCombination(
            name="이미지 중심 콘텐츠 세트",
            description="시각적 콘텐츠 제작에 특화된 AI 도구 조합입니다.",
            use_case="인스타그램/핀터레스트 콘텐츠"
        ),
        ToolCombination(
            name="오디오 콘텐츠 제작 세트",
            description="팟캐스트 및 오디오 콘텐츠 제작을 위한 AI 도구 조합입니다.",
            use_case="팟캐스트/오디오북"
        )
    ]
    
    # 데이터베이스에 추가
    try:
        db.session.add(admin_user)
        db.session.add(test_user)
        for tool in ai_tools:
            db.session.add(tool)
        for combo in tool_combinations:
            db.session.add(combo)
        
        db.session.commit()
        print("초기 데이터가 성공적으로 추가되었습니다.")
    except Exception as e:
        db.session.rollback()
        print(f"오류 발생: {e}")

# 애플리케이션 컨텍스트 내에서 초기 데이터 추가
with app.app_context():
    add_initial_data()
