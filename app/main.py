from fastapi import FastAPI
from app.api.routers import apiRouter  # <--- 멀티탭 하나만 가져옴
from app.core.scheduler import scheduler

# DB 자동 생성을 위한 임포트
from app.db.session import engine
from app.db.base import Base
import app.models  # __init__.py에 임포트된 모델들을 인식시키기 위해 필수

# FastAPI 앱 객체 생성 전에 DB 테이블을 생성합니다.
# (이미 테이블이 존재하면 아무 작업도 하지 않고 넘어갑니다.)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Golum API", version="0.1.0")

# PR 피드백 반영 - 수동 호출 방식에서 end_time 기반 자동 승패 판정 로직으로 전환
@app.on_event("startup")
def start_scheduler():
    if not scheduler.running:
        scheduler.start()
        print("--- APScheduler Started: 자동 판정 모니터링 중 ---")

@app.on_event("shutdown")
def stop_scheduler():
    scheduler.shutdown()
    print("--- APScheduler Shutdown 완료 ---")

# 중앙 라우터를 /api 접두사와 함께 등록합니다.
# 최종 URL은 /api/auth/signin 형태가 됩니다.
app.include_router(apiRouter, prefix="/api")

@app.get("/")
def readRoot():
    return {"message": "Welcome to Golum - Interactive Voting Platform"}