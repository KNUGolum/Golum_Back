import os
from dotenv import load_dotenv

# .env 파일을 읽어서 환경변수로 설정
load_dotenv()

class Settings:
    PROJECT_NAME: str = "Golum"
    
    # DB 연결 주소 (.env에 없으면 기본값 사용)
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://golum_user:golum_password@db:5432/golum_db"
    )
    
    # JWT 암호화 키
    SECRET_KEY: str = os.getenv("SECRET_KEY", "fallback-secret-key")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

# 이 settings 객체를 다른 파일들에서 import 해서 사용하게 됩니다.
settings = Settings()