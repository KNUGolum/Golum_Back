from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import getCurrentUser, getDb

from app.schemas.vote import VoteRequest, VoteResponse, VoteDetails, VoteHistoryItem
from app.crud.vote import VOTE_REWARD_CREDIT, createVote, getVoteHistoryByUserId
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
    if result == "CREATOR_CANNOT_VOTE":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="자신이 만든 투표에는 참여할 수 없습니다."
        )

    return VoteResponse(
        message="투표 성공! 100 크레딧이 지급되었습니다.",
        earnedCredit=VOTE_REWARD_CREDIT,
        voteDetails=VoteDetails(
            pollId=pollId, 
            selectedOption=voteData.selection
        )
    )

@router.get("/history", response_model=List[VoteHistoryItem], status_code=status.HTTP_200_OK)
def getMyVoteHistory(db: Session = Depends(getDb), currentUser: User = Depends(getCurrentUser)):
    votes = getVoteHistoryByUserId(db=db, userId=currentUser.id)
    return [
        VoteHistoryItem(
            id=v.id,
            pollId=v.poll_id,
            optionId=v.option_id,
            createdAt=v.created_at
        ) for v in votes
    ]