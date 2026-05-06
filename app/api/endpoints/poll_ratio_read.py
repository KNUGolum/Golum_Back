from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import getDb
from app.schemas.poll_ratio_read import PollRatioReadResponse
from app.crud.poll_ratio_read import getPollRatio

router = APIRouter()


@router.get("/{pollId}/ratio", response_model=PollRatioReadResponse)
async def getPollRateEndpoint(
    pollId: int,
    db: Session = Depends(getDb)
):
    resultData, statusMsg = getPollRatio(db=db, pollId=pollId)

    if statusMsg == "POLL_NOT_FOUND":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="존재하지 않는 투표입니다."
        )

    if statusMsg == "NO_STATS":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="투표율이 아직 계산되지 않았습니다."
        )

    assert resultData is not None

    return PollRatioReadResponse(
        message="투표율 조회 성공",
        pollId=pollId,
        totalVotes=resultData["totalVotes"],
        optionARatio=resultData["optionARatio"],
        optionBRatio=resultData["optionBRatio"],
    )