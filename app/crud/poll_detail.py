from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.bet import Bet, Vote
from app.models.poll import Poll, PollOption

POLL_STATUS_ENDED = "ENDED"
POLL_STATUS_INVALID = "INVALID"


def getPoll(databaseSession: Session, pollId: int) -> Poll | None:
    return databaseSession.query(Poll).filter(Poll.id == pollId).first()


def getPollOptions(databaseSession: Session, pollId: int) -> list[PollOption]:
    return (
        databaseSession.query(PollOption)
        .filter(PollOption.poll_id == pollId)
        .order_by(PollOption.id.asc())
        .all()
    )


def getParticipantCount(databaseSession: Session, pollId: int) -> int:
    return (
        databaseSession.query(func.count(func.distinct(Vote.user_id)))
        .filter(Vote.poll_id == pollId)
        .scalar()
        or 0
    )


def getTotalBetCredits(databaseSession: Session, pollId: int) -> int:
    return (
        databaseSession.query(func.coalesce(func.sum(Bet.amount), 0))
        .filter(Bet.poll_id == pollId)
        .scalar()
        or 0
    )


def getBetCreditsByOption(
    databaseSession: Session,
    pollId: int,
) -> dict[int, int]:
    betCreditsRows = (
        databaseSession.query(
            Bet.option_id,
            func.coalesce(func.sum(Bet.amount), 0),
        )
        .filter(Bet.poll_id == pollId)
        .group_by(Bet.option_id)
        .all()
    )
    return {optionId: amount for optionId, amount in betCreditsRows}


def isPollEnded(poll: Poll, now: datetime | None = None) -> bool:
    if poll.status == POLL_STATUS_ENDED:
        return True

    if poll.status == POLL_STATUS_INVALID:
        return True

    if poll.end_time is None:
        return False

    now = now or datetime.utcnow()
    return poll.end_time <= now
