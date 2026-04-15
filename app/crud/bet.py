from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.bet import Bet
from app.models.user import User

def createBet(db: Session, userId: int, pollId: int, optionId: int, amount: int):
    try:
        user = db.query(User).filter(User.id == userId).first()
        
        if not user:
            return None, "USER_NOT_FOUND"

        if user.credit < amount:
            return None, "INSUFFICIENT_CREDIT"

        user.credit -= amount

        newBet = Bet(
            user_id=userId,
            poll_id=pollId,
            option_id=optionId,
            amount=amount
        )
        db.add(newBet)

        # 배팅 참여 크레딧 지급 (임시로 100포인트 설정함)
        user.credit += 100

        db.commit()
        db.refresh(newBet)
        
        return newBet, "SUCCESS"

    except SQLAlchemyError as databaseError:
        db.rollback()
        raise databaseError