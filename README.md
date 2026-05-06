# Golum - Interactive Voting Community Platform
<br>

## 1. Vision statement

“골름(Golum)"은 사용자의 빠르고 직관적인 의사 표현을 돕고 여론과 트렌드를 쉽게 확인할 수 있게 해주는 상호작용 투표 커뮤니티 플랫폼입니다. 기존의 단순 투표 서비스들과 달리, 본 서비스는 실시간 토론과 참여형 베팅 시스템을 결합하여 사용자 간의 상호작용을 극대화합니다. 

이 플랫폼은 일상적인 선택의 기로에서 심리적 부담감을 느끼거나 가벼운 킬링타임이 필요한 일반 커뮤니티 사용자들에게, 단순한 흑백 논리를 넘어선 몰입도 높은 실시간 참여형 커뮤니티 경험을 제공할 것입니다.
<br>

## 2. Project goals & Scope

본 프로젝트는 로컬 환경에서의 핵심 로직 시연 및 API 완성을 최우선 목표로 합니다. 회원 관리, 2지 선다 투표 및 커뮤니티 기능, 베팅/정산 시스템, 최소한의 상점 기능 등 백엔드 핵심 기능 구현에 집중하며, Docker 기반의 환경 세팅을 통해 향후 유연한 배포에 대비합니다.
<br>

### 프로젝트 목표 (Success criteria)

- 로컬 환경에서의 핵심 로직 시연 및 기능 완성(API 완성)을 최우선 목표로 합니다.
- 개발 초기 단계부터 도커(Docker) 환경 세팅 등을 통해 배포를 염두에 두고 개발을 진행하며, 상용 배포 여부는 전체 일정과 비용을 고려하여 추후 결정합니다.

### 필수 구현 범위

- **회원가입 및 로그인:** 유효성 검사 및 중복 가입 방지 로직이 적용된 회원가입, 로그인 기능 구현
- **투표 게시판:** 게시글 생성, 조회, 수정, 삭제(CRUD) 및 핵심인 2지 선다 투표 로직 구현, 게시글 내 댓글 및 답글 작성을 통한 유저 간 소통 및 토론 기능 구현
- **배팅 시스템:** 투표 참여 및 결과에 따른 크레딧 지급/정산 로직 구현 (크레딧 정산 시 발생할 수 있는 오류를 막기 위한 최소한의 동시성 제어 포함)
- **상점 (크레딧 소비처):** 서비스 지속성과 흥미 유발을 위한 MVP 필수 기능으로 상점을 구현. 크레딧으로 칭호 등 간단한 아이템을 구매하고 프로필에 적용하는 기능을 우선하되, 복잡한 프론트엔드 UI 연동은 개발 일정에 따라 후순위로 조정

### 제외 범위

- WebSocket 등을 활용한 실시간 채팅 수준의 동기화된 토론 시스템
- 대규모 트래픽 대응을 목적으로 하는 복잡한 분산 서버 시스템 설계
- 사용자 데이터를 기반으로 하는 맞춤형 게시물 추천 알고리즘
<br>

## 3. Stakeholders & Users

- **핵심 유저:** 일반 사용자 (게시글 올리고 투표/베팅/토론 참여)
- **개발 팀:** 기한 내에 안정적으로 핵심 기능 구현
- **테스터:** 테스트 시나리오 검증 및 다수 사용자 이용 시 발생하는 버그 리포트와 통합 테스트를 최우선으로 진행
<br>

## 4. Milestone

| 일정 | 주요 개발 내용 및 목표 |
| :--- | :--- |
| **3월** | 기획 고도화, API/DB 설계, 깃허브 세팅 |
| **4월** | 기본 회원 및 게시판(투표) 로직 구현 |
| **5월** | 핵심 엔진(배팅 로직, 댓글 연동) 구현 |
| **6월** | 기능 통합 테스트, 다수 사용자 환경에서의 버그 수정, 최종 발표 준비 (여유 시 성능 지표 점검 및 배포 시도) |
<br>

## 5. Github address

- **Repository:** [https://github.com/KNUGolum/Golum_Back](https://github.com/KNUGolum/Golum_Back)
<br>

## 6. User Story Map
<br>

<img width="1066" height="457" alt="스크린샷 2026-05-06 오후 3 58 14" src="https://github.com/user-attachments/assets/08a74d8e-9aaf-4fe7-8d0e-d1ba8df2e48d" />

<br>

## 7. Directory Structure

본 프로젝트는 유지보수와 확장성을 고려하여 계층형(Layered) 아키텍처 구조를 따르고 있습니다.

```text
.
├── app/
│   ├── api/                  # API 라우팅 관련 폴더
│   │   ├── endpoints/        # 엔드포인트 파일 모음
│   │   ├── deps.py           # 공통 의존성 함수 관리
│   │   └── routers.py        # 라우터 등록 및 통합
│   ├── core/                 # 공통 설정 관리
│   │   └── config.py         # 환경변수 및 설정값 관리
│   ├── db/                   # 데이터베이스 연결 설정
│   │   ├── base.py           # SQLAlchemy Base 정의
│   │   └── session.py        # DB 세션 및 엔진 설정
│   ├── models/               # 데이터베이스 모델 정의
│   │   ├── __init__.py       # 모델 패키지 초기화
│   │   ├── bet.py            # 베팅 관련 모델
│   │   ├── poll.py           # 투표 관련 모델
│   │   └── user.py           # 사용자 관련 모델
│   └── main.py               # FastAPI 앱 실행 파일
├── migrations/               # DB 마이그레이션 파일
├── .env                      # 로컬 환경 변수 파일
├── .env.example              # 환경 변수 예시 파일
├── .gitignore                # Git 추적 제외 설정
├── docker-compose.yml        # 컨테이너 실행 설정
├── Dockerfile                # Docker 이미지 빌드 설정
├── README.md                 # 프로젝트 설명 문서
└── requirements.txt          # Python 패키지 목록
```
<br>

## 8. Getting Started

최초로 프로젝트를 Clone 받거나 Pull 받은 후, 로컬 환경에서 서버를 실행하기 위한 가이드입니다. 본 프로젝트는 Docker를 기반으로 구동되므로 로컬에 Docker가 설치되어 있어야 합니다.

### Step 1. Clone & Environment Setup
```bash
# 1. 저장소 클론
git clone [https://github.com/KNUGolum/Golum_Back.git](https://github.com/KNUGolum/Golum_Back.git)
cd Golum_Back

# 2. 환경변수 세팅
# 최상단 루트 디렉토리에 .env 파일을 생성하고 필요한 환경변수를 입력합니다.
# (DB 연결 주소, JWT Secret Key 등 - 팀 내 공유된 키 사용)
```

### Step 2. Build & Run Docker Containers
```bash
# 백그라운드에서 DB와 웹 서버 컨테이너 빌드 및 실행
docker-compose up --build -d
```

### Step 3. API Docs Check
서버가 정상적으로 구동되었다면 브라우저를 열고 아래 주소로 접속합니다.
- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs) (로컬 포트 매핑에 따라 다를 수 있습니다)
- 이곳에서 API 명세서를 확인하고 직접 테스트(Try it out)해 볼 수 있습니다.

### Step 4. Branch & PR Workflow
- 새로운 기능 개발 시 `main` 브랜치에서 새로운 `feature/기능명` 브랜치를 파서 작업합니다.
- 작업 완료 후 Github에 Push 하고, 코드 리뷰를 요청하여 승인(Approve) 후 머지하는 흐름으로 진행합니다.
