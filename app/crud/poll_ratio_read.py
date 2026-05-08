from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.poll import Poll, PollStat


def getPollRatio(db: Session, pollId: int):
    try:
        poll = db.query(Poll).filter(Poll.id == pollId).first()
        if not poll:
            return None, "POLL_NOT_FOUND"                    
        
        pollStat = db.query(PollStat).filter(PollStat.poll_id == 
        pollId).first()

        if not pollStat:
            return None, "NO_STATS"

        resultData = {
            "totalVotes": pollStat.total_votes,
            "optionARatio": pollStat.option1_ratio,
            "optionBRatio": pollStat.option2_ratio
        }

        return resultData, "SUCCESS"

    except SQLAlchemyError as e:
        db.rollback()
        raise e