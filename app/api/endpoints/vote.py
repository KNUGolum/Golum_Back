from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import getCurrentUser, getDb

from app.schemas.vote import VoteRequest, VoteResponse, VoteDetails
from app.crud.vote import createVote
from app.models.user import User

router = APIRouter()

@router.post("/{pollId}/vote", response_model=VoteResponse, status_code=status.HTTP_201_CREATED)
async def submitVote(
    pollId: int,
    voteData: VoteRequest,
    db: Session = Depends(getDb),
    currentUser: User = Depends(getCurrentUser)
):
    vote, result = createVote(
        db=db, 
        pollId=pollId, 
        userId=currentUser.id, 
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
    if result == "POLL_CLOSED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="종료된 투표에는 참여할 수 없습니다."
        )

    return VoteResponse(
        message="투표 성공! 100 크레딧이 지급되었습니다.",
        earnedCredit=100,
        voteDetails=VoteDetails(
            pollId=pollId, 
            selectedOption=voteData.selection
        )
    )
