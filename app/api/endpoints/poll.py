from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta

from app.schemas.poll import PollCreateRequest, PollCreateResponse
from app.api.deps import getDb
from app.crud import poll as crudPoll

router = APIRouter()

@router.post("", response_model=PollCreateResponse, status_code=status.HTTP_201_CREATED)
async def createPoll(
    pollData: PollCreateRequest,
    db: Session = Depends(getDb)
):
    try:
        currentTime = datetime.now()
        endTime = currentTime + timedelta(hours=pollData.durationHours)
        
        # 향후 인증 로직이 추가되면 해당 유저의 ID로 대체
        # currentUserId
        
        createdPoll = crudPoll.createPoll(
            db=db, 
            pollData=pollData, 
            endTime=endTime, 
            # creatorId=currentUserId
        )
        
        return PollCreateResponse(
            message="투표 게시물이 성공적으로 생성되었습니다.",
            pollId=createdPoll.id,
            # creatorId=createdPoll.creator_id,
            endTime=createdPoll.end_time
        )
        
    # DB 트랜잭션 등 데이터베이스 관련 예외
    except SQLAlchemyError as databaseError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"데이터베이스 처리 중 오류가 발생했습니다: {str(databaseError)}"
        )
    # 시간 계산 등 그 외 예상치 못한 서버 예외
    except Exception as unexpectedError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"서버 내부 오류가 발생했습니다: {str(unexpectedError)}"
        )