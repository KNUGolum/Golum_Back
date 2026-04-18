from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import getDb
from app.schemas.poll_ratio_update import PollRatioUpdateResponse
from app.crud.poll_ratio_update import updatePollRatio

router = APIRouter()

@router.post("/{pollId}/ratio", response_model=PollRatioUpdateResponse, status_code=status.HTTP_200_OK)
async def updatePollRateEndpoint(
    pollId: int,
    db: Session = Depends(getDb)
):
    resultData, statusMsg = updatePollRatio(db=db, pollId=pollId)

    if statusMsg == "POLL_NOT_FOUND":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="존재하지 않는 투표입니다."
        )

    if statusMsg == "NO_VOTES":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="투표가 없어 투표율을 계산할 수 없습니다."
        )
    if statusMsg != "SUCCESS":
        raise HTTPException(
        status_code=500,
        detail="알 수 없는 오류"
    )
    if resultData is None:
        raise HTTPException(
        status_code=500,
        detail="데이터 처리 오류"
    )

    return PollRatioUpdateResponse(
    message="투표율 갱신이 완료되었습니다.",
    pollId=pollId,
    totalVotes=resultData["totalVoteCount"],
    optionARatio=resultData["option1Ratio"],
    optionBRatio=resultData["option2Ratio"],
)