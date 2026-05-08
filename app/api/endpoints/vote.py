from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import getDb

from app.schemas.vote import VoteRequest, VoteResponse, VoteDetails
from app.crud.vote import createVote

router = APIRouter()

@router.post("/{pollId}/vote", response_model=VoteResponse, status_code=status.HTTP_201_CREATED)
async def submitVote(
    pollId: int,
    voteData: VoteRequest,
    db: Session = Depends(getDb)
    # currentUser: User = Depends(getCurrentUser)
):
    # 테스트용 현재 유저 아이디(db에 동일 아이디 값이 있는 유저가 있어야함)
    tempUserId = 2
    
    vote, result = createVote(
        db=db, 
        pollId=pollId, 
        userId=tempUserId, 
        selection=voteData.selection
    )
    
    if result == "ALREADY_VOTED":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="이미 참여한 투표입니다. 배팅 현황 페이지로 이동합니다."
        )
    if result == "INVALID_POLL":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="투표 정보를 찾을 수 없거나 선택지가 부족합니다."
        )

    return VoteResponse(
        message="투표 성공! 100 크레딧이 지급되었습니다.",
        earnedCredit=100,
        voteDetails=VoteDetails(
            pollId=pollId, 
            selectedOption=voteData.selection
        )
    )