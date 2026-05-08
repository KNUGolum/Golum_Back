from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import getDb
from app.schemas.poll_result import EvaluatePollResponse
from app.crud.poll_result import evaluatePollResult

router = APIRouter()

@router.post("/{pollId}/evaluate", response_model=EvaluatePollResponse, status_code=status.HTTP_200_OK)
async def evaluatePoll(
    pollId: int,
    db: Session = Depends(getDb)
):
    resultData, statusMsg = evaluatePollResult(db=db, pollId=pollId)
    
    if statusMsg == "POLL_NOT_FOUND":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="존재하지 않는 투표입니다."
        )
    # PR 피드백 반영 - 종료 후 판정
    if statusMsg == "POLL_STILL_ONGOING":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="아직 투표가 종료되지 않았습니다."
        )
    if statusMsg == "ALREADY_EVALUATED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="이미 마감 및 판정이 완료된 투표입니다."
        )
    if statusMsg == "NOT_ENOUGH_OPTIONS":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="투표 선택지가 부족하여 판정할 수 없습니다."
        )
        
    return EvaluatePollResponse(
        message="투표 승패 판정이 완료되었습니다.",
        pollId=pollId,
        pollResultStatus=resultData["pollResultStatus"],
        winningOptionId=resultData["winningOptionId"],
        totalVoteCount=resultData["totalVoteCount"]
    )