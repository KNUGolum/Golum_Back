from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func

from app.models.poll import Poll, PollOption, PollStat
from app.models.bet import Vote


def getPollResult(db: Session, pollId: int):
    try:
        poll = db.query(Poll).filter(
            Poll.id == pollId
        ).first()

        if not poll:
            return None, "POLL_NOT_FOUND"

        if poll.status in ["ONGOING"]:
            return None, "NOT_FINISHED"

        options = db.query(PollOption).filter(
            PollOption.poll_id == pollId
        ).order_by(PollOption.id).all()

        if len(options) < 2:
            return None, "NOT_ENOUGH_OPTIONS"

        optionA, optionB = options[0], options[1]

        voteCountA = db.query(func.count(Vote.id)).filter(
            Vote.poll_id == pollId,
            Vote.option_id == optionA.id
        ).scalar() or 0

        voteCountB = db.query(func.count(Vote.id)).filter(
            Vote.poll_id == pollId,
            Vote.option_id == optionB.id
        ).scalar() or 0

        totalVotes = voteCountA + voteCountB

        if totalVotes == 0:
            return {
                "resultStatus": "INVALID",
                "winningOptionId": None,
                "winningOptionText": None,
                "totalVotes": 0
            }, "SUCCESS"

        if voteCountA == voteCountB:
            return {
                "resultStatus": "DRAW",
                "winningOptionId": None,
                "winningOptionText": None,
                "totalVotes": totalVotes
            }, "SUCCESS"

        if voteCountA > voteCountB:
            winningOption = optionA 
        else:
            winningOption = optionB

        return {
            "resultStatus": "FINISHED",
            "winningOptionId": winningOption.id,
            "winningOptionText": winningOption.option_text,
            "totalVotes": totalVotes
        }, "SUCCESS"

    except SQLAlchemyError as e:
        db.rollback()
        raise e