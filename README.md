# AI HUB Project

AI HUB는 콘텐츠 제작자를 위한 AI 도구 허브 플랫폼입니다.

## 주요 기능

1. 콘텐츠 제작자를 위한 AI 툴 모음 및 링크 제공
2. 회원 가입 및 개인 대시보드 제공
3. 콘텐츠 분류별 최적 AI 툴 조합 생성 및 저장
4. 유튜브 콘텐츠 분석 및 가이드라인 제공
5. 최신 AI 툴 정보 및 콘텐츠 제작 가이드 제공
6. 숏츠 및 롱폼 제작 노하우 정보
7. 크리에이터 제작 도구 정보와 가이드
8. 유튜브 채널 수익화 여부 확인
9. 유튜브 인기 검색어 제공
10. 유튜브 AI 콘텐츠 제작 관련 채널 추천

## 설치 방법

1. 프로젝트 클론:
```bash
git clone <repository-url>
cd AI_HUB_ProJect
```

2. 가상 환경 설정 및 패키지 설치:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. 환경 변수 설정:
`.env` 파일을 생성하고 필요한 환경 변수를 설정합니다.

4. 데이터베이스 초기화:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

5. 서버 실행:
```bash
flask run
```

## 기술 스택

- Backend: Flask, SQLAlchemy
- Frontend: React, Bootstrap
- Database: SQLite (개발), PostgreSQL (배포)
- API: YouTube Data API, 기타 AI 서비스 API

## 프로젝트 구조

```
AI_HUB_ProJect/
├── backend/            # Flask 백엔드
│   ├── app/            # 애플리케이션 코드
│   ├── migrations/     # 데이터베이스 마이그레이션
│   └── config.py       # 설정 파일
├── frontend/           # React 프론트엔드
│   ├── public/         # 정적 파일
│   ├── src/            # 소스 코드
│   └── package.json    # 패키지 정보
└── README.md           # 프로젝트 문서
```
