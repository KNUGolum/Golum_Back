from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# PostgreSQL 연결 엔진 생성
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
# 세션 팩토리 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)