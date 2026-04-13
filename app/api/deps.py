from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.db.session import SessionLocal
from sqlalchemy.orm import Session
from app.core.config import settings
from app.crud import user as user_crud

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login/swagger")
# 중앙관리를 위해 getDb와 getCurrentUser 함수를 이곳에 모아둡니다.
def getDb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
