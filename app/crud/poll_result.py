from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from datetime import datetime

from app.models.poll import Poll, PollOption
from app.models.bet import Vote

def evaluatePollResult(db: Session, pollId: int):
    try:
        poll = db.query(Poll).filter(Poll.id == pollId).first()
        if not poll:
            return None, "POLL_NOT_FOUND"
        
        if poll.status in ["ENDED", "INVALID"]: 
            return None, "ALREADY_EVALUATED"
        
        # PR 피드백 반영 - 종료 후 판정
        currentTime = datetime.now()
        if currentTime < poll.end_time:
            return None, "POLL_STILL_ONGOING"

        options = db.query(PollOption).filter(PollOption.poll_id == pollId).order_by(PollOption.id).all()
        if len(options) < 2:
            return None, "NOT_ENOUGH_OPTIONS"
        
        optionA, optionB = options[0], options[1]

        voteCountA = db.query(func.count(Vote.id)).filter(Vote.poll_id == pollId, Vote.option_id == optionA.id).scalar() or 0
        voteCountB = db.query(func.count(Vote.id)).filter(Vote.poll_id == pollId, Vote.option_id == optionB.id).scalar() or 0
        totalVotes = voteCountA + voteCountB

        resultStatus = None
        winningOptionId = None

        if totalVotes == 0:
            resultStatus = "INVALID"
            poll.status = "INVALID"
        elif voteCountA == voteCountB:
            resultStatus = "DRAW"
            poll.status = "ENDED"
        else:
            resultStatus = "FINISHED"
            poll.status = "ENDED"
            winningOptionId = optionA.id if voteCountA > voteCountB else optionB.id

        db.commit()

        return {
            "pollResultStatus": resultStatus,
            "winningOptionId": winningOptionId,
            "totalVoteCount": totalVotes
        }, "SUCCESS"

    except SQLAlchemyError as databaseError:
        db.rollback()
        raise databaseError