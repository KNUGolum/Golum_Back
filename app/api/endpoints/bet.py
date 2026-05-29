from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List

from app.api.deps import getDb, getCurrentUser
from app.schemas.bet import BetCreate, BetActionResponse, BetResponse
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

        if result == "POLL_CLOSED":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="종료된 투표에는 배팅할 수 없습니다."
            )

        if result == "INVALID_AMOUNT":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="배팅 금액은 0 이상이어야 합니다."
            )

        if result == "ALREADY_BET":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="이미 배팅에 참여한 투표입니다."
            )

        if result == "VOTE_OPTION_MISMATCH":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="투표한 선택지에만 배팅할 수 있습니다."
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

        if result == "POLL_NOT_FOUND":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="투표 정보를 찾을 수 없습니다."
            )

        if result == "INVALID_POLL_OPTIONS":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Poll requires exactly two options."
            )

        message = "배팅이 완료되었습니다." if bet.amount == 0 else "배팅 참여 보상으로 100 크레딧이 지급되었습니다."

        return BetActionResponse(
            message=message,
            betDetails=BetResponse(
            id=bet.id,
            userId=bet.user_id,      
            pollId=bet.poll_id,      
            optionId=bet.option_id,
            amount=bet.amount,
            result=bet.result,
            createdAt=bet.created_at 
            )
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

@router.get("/history", response_model=List[BetResponse], status_code=status.HTTP_200_OK)
def getMyBetHistory(db: Session = Depends(getDb), currentUser: User = Depends(getCurrentUser)):
    bets = crudBet.getBetHistoryByUserId(db=db, userId=currentUser.id)
    return [
        BetResponse(
            id=b.id,
            userId=b.user_id,
            pollId=b.poll_id,
            optionId=b.option_id,
            amount=b.amount,
            result=b.result,
            rewardAmount=b.reward_amount,
            createdAt=b.created_at
        ) for b in bets
    ]