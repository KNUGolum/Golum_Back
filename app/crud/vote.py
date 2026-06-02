from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.crud import poll_detail as pollDetailCrud
from app.models.bet import Vote
from app.models.poll import Poll, PollOption, PollStat
from app.models.user import User

VOTE_REWARD_CREDIT = 100


def createVote(db: Session, pollId: int, userId: int, selection: str):
    try:
        poll = db.query(Poll).filter(Poll.id == pollId).first()
        if not poll:
            return None, "INVALID_POLL"

        if not pollDetailCrud.isPollActive(poll):
            return None, "POLL_CLOSED"

        if poll.creator_id == userId:
            return None, "CREATOR_CANNOT_VOTE"

        alreadyVoted = (
            db.query(Vote)
            .filter(Vote.poll_id == pollId, Vote.user_id == userId)
            .first()
        )
        if alreadyVoted:
            return None, "ALREADY_VOTED"

        options = (
            db.query(PollOption)
            .filter(PollOption.poll_id == pollId)
            .order_by(PollOption.id)
            .all()
        )
        targetOption = pollDetailCrud.resolveOptionBySelection(options, selection)
        if targetOption is None:
            return None, "INVALID_POLL"

        newVote = Vote(
            user_id=userId,
            poll_id=pollId,
            option_id=targetOption.id,
        )
        db.add(newVote)
        targetOption.vote_count = (targetOption.vote_count or 0) + 1

        user = db.query(User).filter(User.id == userId).first()
        if user:
            user.credit += VOTE_REWARD_CREDIT

        stat = db.query(PollStat).filter(PollStat.poll_id == pollId).first()
        if stat:
            stat.total_votes += 1

        db.commit()
        return newVote, "SUCCESS"

    except SQLAlchemyError as databaseError:
        db.rollback()
        raise databaseError

def getVoteHistoryByUserId(db: Session, userId: int):
    return db.query(Vote).filter(Vote.user_id == userId).order_by(Vote.created_at.desc()).all()