from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import getDb
from app.schemas.user import UserCreate, UserResponse, EmailCheckRequest, NicknameCheckRequest
from app.crud import user as userCrud

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