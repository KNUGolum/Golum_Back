from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.bet import Bet, Vote
from app.models.user import User
from app.models.poll import PollOption

def createBet(db: Session, userId: int, pollId: int, optionId: int, amount: int):
    try:
        user = db.query(User).filter(User.id == userId).first()
        
        if not user:
            return None, "USER_NOT_FOUND"
        
        # PR 피드백 반영 - A/B 선택
        options = db.query(PollOption).filter(PollOption.poll_id == pollId).order_by(PollOption.id).all()
        if len(options) < 2:
            return None, "INVALID_POLL_OPTIONS"
        
        realOptionId = options[0].id if optionId == "A" else options[1].id
    
        # PR 피드백 반영 - 투표 참여 여부 확인
        hasVoted = db.query(Vote).filter(
            Vote.user_id == userId, 
            Vote.poll_id == pollId
        ).first()

        if not hasVoted:
            return None, "NOT_VOTED"
        
        if user.credit < amount:
            return None, "INSUFFICIENT_CREDIT"

        user.credit -= amount

        newBet = Bet(
            user_id=userId,
            poll_id=pollId,
            option_id=realOptionId,
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