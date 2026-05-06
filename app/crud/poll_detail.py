from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.bet import Bet, Vote
from app.models.poll import Poll, PollOption


def get_poll(db: Session, poll_id: int) -> Poll | None:
    return db.query(Poll).filter(Poll.id == poll_id).first()


def get_poll_options(db: Session, poll_id: int) -> list[PollOption]:
    return (
        db.query(PollOption)
        .filter(PollOption.poll_id == poll_id)
        .order_by(PollOption.id.asc())
        .all()
    )


def get_participant_count(db: Session, poll_id: int) -> int:
    return (
        db.query(func.count(func.distinct(Vote.user_id)))
        .filter(Vote.poll_id == poll_id)
        .scalar()
        or 0
    )


def get_total_bet_credits(db: Session, poll_id: int) -> int:
    return (
        db.query(func.coalesce(func.sum(Bet.amount), 0))
        .filter(Bet.poll_id == poll_id)
        .scalar()
        or 0
    )


def get_bet_credits_by_option(db: Session, poll_id: int) -> dict[int, int]:
    rows = (
        db.query(Bet.option_id, func.coalesce(func.sum(Bet.amount), 0))
        .filter(Bet.poll_id == poll_id)
        .group_by(Bet.option_id)
        .all()
    )
    return {option_id: amount for option_id, amount in rows}


def is_poll_ended(poll: Poll, now: datetime | None = None) -> bool:
    if poll.status == "ENDED":
        return True
    if poll.status in {"INVALID"}:
        return True
    if poll.end_time is None:
        return False
    now = now or datetime.utcnow()
    return poll.end_time <= now
