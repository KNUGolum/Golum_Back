from sqlalchemy.orm import Session
from app.models.user import User
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