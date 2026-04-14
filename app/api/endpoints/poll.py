from fastapi import APIRouter, status, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta

from app.schemas.poll import PollCreateRequest, PollCreateResponse, PollListResponse
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

@router.get("", response_model=PollListResponse, status_code=status.HTTP_200_OK)
async def getPollList(
    # FastAPI의 내부 status 모듈과 이름이 겹치지 않게 변수명은 pollStatus로 하되, 클라이언트에게는 alias="status"를 통해 ?status= 로 받도록 설정
    pollStatus: str = Query("ongoing", alias="status", description="투표 진행 상태 (ongoing, ended)"),
    sort: str = Query("latest", description="정렬 기준 (latest, popular)"),
    page: int = Query(1, ge=1, description="조회할 페이지 번호"),
    limit: int = Query(10, ge=1, le=50, description="한 페이지당 가져올 투표 개수"),
    db: Session = Depends(getDb)
):
    try:
        # 1. CRUD 호출하여 데이터 가져오기
        totalCount, pollList = crudPoll.getPolls(
            db=db,
            status=pollStatus,
            sort=sort,
            page=page,
            limit=limit
        )
        
        # 2. Pydantic 응답 스키마에 맞춰 반환
        return PollListResponse(
            totalCount=totalCount,
            currentPage=page,
            polls=pollList
        )
        
    except SQLAlchemyError as databaseError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"데이터베이스 조회 중 오류가 발생했습니다: {str(databaseError)}"
        )
    except Exception as unexpectedError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"서버 내부 오류가 발생했습니다: {str(unexpectedError)}"
        )