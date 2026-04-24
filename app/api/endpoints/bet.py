from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.api.deps import getDb, getCurrentUser
from app.schemas.bet import BetCreate, BetActionResponse
from app.crud import bet as crudBet
from app.models.user import User

router = APIRouter()

@router.post("/{pollId}/bet", response_model=BetActionResponse, status_code=status.HTTP_201_CREATED)
async def createBetParticipation(
    pollId: int,
    betData: BetCreate,
    db: Session = Depends(getDb),
    currentUser: User = Depends(getCurrentUser)
):
    try:
        bet, result = crudBet.createBet(
            db=db,
            userId=currentUser.id,
            pollId=pollId,
            optionId=betData.optionId,
            amount=betData.amount
        )

        # PR 피드백 반영 - 투표 미참여 유저 처리
        if result == "NOT_VOTED":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="투표에 참여한 유저만 배팅할 수 있습니다."
            )

        if result == "INSUFFICIENT_CREDIT":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="보유하신 크레딧이 부족합니다."
            )

        if result == "USER_NOT_FOUND":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="사용자 정보를 찾을 수 없습니다."
            )

        return BetActionResponse(
            message="배팅 참여 보상으로 100 크레딧이 지급되었습니다.",
            betDetails=bet
        )

    except SQLAlchemyError as databaseError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"데이터베이스 처리 중 오류가 발생했습니다: {str(databaseError)}"
        )
    except HTTPException:
        raise
    except Exception as unexpectedError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"서버 내부 오류가 발생했습니다: {str(unexpectedError)}"
        )