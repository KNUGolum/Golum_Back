from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.api.deps import getDb
from app.schemas.payout import DividendPayoutResponse
from app.crud.payout import payoutDividends

router = APIRouter()

@router.post("/{pollId}/payout", response_model=DividendPayoutResponse, status_code=status.HTTP_200_OK)
async def processPayout(
    pollId: int,
    db: Session = Depends(getDb)
):
    try:
        resultData, statusMsg = payoutDividends(db=db, pollId=pollId)
        
        if statusMsg == "ALREADY_SETTLED":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="이미 정산이 완료된 투표입니다."
            )
        if statusMsg == "POLL_NOT_FOUND":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="존재하지 않는 투표 정보입니다."
            )
        if statusMsg == "POLL_NOT_ENDED":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="아직 종료되지 않은 투표입니다. 판정(Evaluate)을 먼저 진행해 주세요."
            )
        if statusMsg == "INVALID_POLL_OPTIONS":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="투표 선택지 정보가 부족하여 정산할 수 없습니다."
            )

        return DividendPayoutResponse(
            message="배당금 정산 및 크레딧 지급이 성공적으로 완료되었습니다.",
            pollId=pollId,
            pollResultStatus="FINISHED" if resultData["winningOptionId"] else "DRAW",
            winningOptionId=resultData["winningOptionId"],
            status="COMPLETED",
            dividendRate=resultData["dividendRate"],
            totalPayoutAmount=resultData["totalPayoutAmount"],
            payoutUserCount=resultData["payoutUserCount"]
        )

    except SQLAlchemyError as databaseError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"데이터베이스 처리 중 오류가 발생했습니다: {str(databaseError)}"
        )
    except Exception as unexpectedError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"서버 내부 오류가 발생했습니다: {str(unexpectedError)}"
        )