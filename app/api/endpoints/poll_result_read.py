from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import getDb
from app.schemas.poll_result_read import PollResultReadResponse
from app.crud.poll_result_read import getPollResult

router = APIRouter()


@router.get("/{pollId}/result", response_model=PollResultReadResponse)
async def getPollResultEndpoint(
    pollId: int,
    db: Session = Depends(getDb)
):
    resultData, statusMsg = getPollResult(db=db, pollId=pollId)

    if statusMsg == "POLL_NOT_FOUND":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="존재하지 않는 투표입니다."
        )

    if statusMsg == "NOT_FINISHED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="아직 종료되지 않은 투표입니다."
        )

    assert resultData is not None

    return PollResultReadResponse(
        message="투표 결과 조회 성공",
        pollId=pollId,
        resultStatus=resultData["resultStatus"],
        winningOptionId=resultData["winningOptionId"],
        winningOptionText=resultData["winningOptionText"],
        totalVotes=resultData["totalVotes"],
    )