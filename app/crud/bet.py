from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.crud import poll_detail as pollDetailCrud
from app.models.bet import Bet, Vote
from app.models.poll import Poll, PollOption
from app.models.user import User

BET_PARTICIPATION_REWARD_CREDIT = 100


def createBet(db: Session, userId: int, pollId: int, optionId: str, amount: int):
    try:
        user = db.query(User).filter(User.id == userId).first()
        if not user:
            return None, "USER_NOT_FOUND"

        if amount < 0:
            return None, "INVALID_AMOUNT"

        poll = db.query(Poll).filter(Poll.id == pollId).first()
        if not poll:
            return None, "POLL_NOT_FOUND"

        if not pollDetailCrud.isPollActive(poll):
            return None, "POLL_CLOSED"

        options = (
            db.query(PollOption)
            .filter(PollOption.poll_id == pollId)
            .order_by(PollOption.id)
            .all()
        )
        selectedOption = pollDetailCrud.resolveOptionBySelection(options, optionId)
        if selectedOption is None:
            return None, "INVALID_POLL_OPTIONS"

        vote = (
            db.query(Vote)
            .filter(Vote.user_id == userId, Vote.poll_id == pollId)
            .first()
        )
        if not vote:
            return None, "NOT_VOTED"

        if vote.option_id != selectedOption.id:
            return None, "VOTE_OPTION_MISMATCH"

        alreadyBet = (
            db.query(Bet)
            .filter(Bet.user_id == userId, Bet.poll_id == pollId)
            .first()
        )
        if alreadyBet:
            return None, "ALREADY_BET"

        if user.credit < amount:
            return None, "INSUFFICIENT_CREDIT"

        user.credit -= amount

        newBet = Bet(
            user_id=userId,
            poll_id=pollId,
            option_id=selectedOption.id,
            amount=amount,
        )
        db.add(newBet)

        if amount > 0:
            user.credit += BET_PARTICIPATION_REWARD_CREDIT

        db.commit()
        db.refresh(newBet)

        return newBet, "SUCCESS"

    except SQLAlchemyError as databaseError:
        db.rollback()
        raise databaseError

def getBetHistoryByUserId(db: Session, userId: int):
    return db.query(Bet).filter(Bet.user_id == userId).order_by(Bet.created_at.desc()).all()