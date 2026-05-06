from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.core.config import settings
from app.crud import user as userCrud

# 중앙관리를 위해 getDb와 getCurrentUser 함수를 이곳에 모아둡니다.
def getDb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Swagger 및 토큰 검증용 주소 설정
oauth2Scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login/swagger")

def getCurrentUser(token: str = Depends(oauth2Scheme), db: Session = Depends(getDb)):
    credentialsException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="인증 정보가 유효하지 않습니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        userId: str = payload.get("sub")
        if userId is None:
            raise credentialsException
    except JWTError:
        raise credentialsException
        
    user = userCrud.getUserById(db, userId=int(userId))
    if user is None:
        raise credentialsException
    return user