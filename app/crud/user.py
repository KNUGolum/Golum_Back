from sqlalchemy.orm import Session
from app.models.user import User, AuthToken
from app.schemas.user import UserCreate
from app.core.security import hashPassword

INITIAL_SIGNUP_CREDIT = 1000

def getUserByEmail(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def getUserByNickname(db: Session, nickname: str):
    return db.query(User).filter(User.nickname == nickname).first()

def createUser(db: Session, userIn: UserCreate):
    hashedPassword = hashPassword(userIn.password)
    
    newUser = User(
        email=userIn.email,
        nickname=userIn.nickname,
        password_hash=hashedPassword,
        credit=INITIAL_SIGNUP_CREDIT
    )
    
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    
    return newUser

def getUserById(db: Session, userId: int):
    return db.query(User).filter(User.id == userId).first()

def upsertRefreshToken(db: Session, userId: int, refreshToken: str, expiresAt):
    authToken = db.query(AuthToken).filter(AuthToken.user_id == userId).first()

    if authToken:
        authToken.refresh_token = refreshToken
        authToken.expires_at = expiresAt
    else:
        authToken = AuthToken(
            user_id=userId,
            refresh_token=refreshToken,
            expires_at=expiresAt
        )
        db.add(authToken)

    db.commit()
    db.refresh(authToken)

    return authToken

def getAuthTokenByUserId(db: Session, userId: int):
    return db.query(AuthToken).filter(AuthToken.user_id == userId).first()