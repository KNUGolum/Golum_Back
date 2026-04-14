from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api.deps import getDb, getCurrentUser
from app.schemas.user import UserCreate, UserResponse, EmailCheckRequest, NicknameCheckRequest, SignInRequest, TokenResponse
from app.crud import user as userCrud
from app.core.security import verifyPassword, createAccessToken
from app.models.user import User

router = APIRouter()

@router.post("/check-email", status_code=status.HTTP_200_OK)
def checkEmailDuplication(request: EmailCheckRequest, db: Session = Depends(getDb)):
    existingUser = userCrud.getUserByEmail(db, email=request.email)
    
    if existingUser:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 가입된 메일입니다. 로그인 페이지로 이동하시겠습니까?"
        )
        
    return {"message": "사용 가능한 이메일입니다."}

@router.post("/check-nickname", status_code=status.HTTP_200_OK)
def checkNicknameDuplication(request: NicknameCheckRequest, db: Session = Depends(getDb)):
    existingUser = userCrud.getUserByNickname(db, nickname=request.nickname)
    
    if existingUser:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 존재하는 닉네임입니다."
        )
        
    return {"message": "사용 가능한 닉네임입니다."}

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signUp(userIn: UserCreate, db: Session = Depends(getDb)):
    existingEmail = userCrud.getUserByEmail(db, email=userIn.email)
    if existingEmail:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이메일 중복 확인이 완료되지 않았거나 이미 가입된 메일입니다."
        )
        
    existingNickname = userCrud.getUserByNickname(db, nickname=userIn.nickname)
    if existingNickname:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="닉네임 중복 확인이 완료되지 않았거나 이미 사용 중인 닉네임입니다."
        )
        
    newUser = userCrud.createUser(db=db, userIn=userIn)
    return newUser


@router.post("/signin", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def signIn(request: SignInRequest, db: Session = Depends(getDb)):
    user = userCrud.getUserByEmail(db, email=request.email)
    
    if not user or not verifyPassword(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다."
        )
    
    token = createAccessToken(subject=user.id)
    
    return {
        "accessToken": token,
        "tokenType": "bearer"
    }

@router.post("/login/swagger", include_in_schema=False)
def swaggerLogin(formData: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(getDb)):
    user = userCrud.getUserByEmail(db, email=formData.username)
    if not user or not verifyPassword(formData.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다."
        )
    
    token = createAccessToken(subject=user.id)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
def getMyInfo(currentUser: User = Depends(getCurrentUser)):
    return currentUser