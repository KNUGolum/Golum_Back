from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

from app.models.poll import Poll, PollOption, PollStat
from app.schemas.poll import PollCreateRequest

def createPoll(db: Session, pollData: PollCreateRequest, endTime: datetime) -> Poll: # creatorId: int 추가할 예정
    try:
        dbPoll = Poll(
            title=pollData.title,
            end_time=endTime,
            # creator_id=creatorId
        )
        db.add(dbPoll)
        db.flush()

        optionA = PollOption(poll_id=dbPoll.id, option_text=pollData.optionA)
        optionB = PollOption(poll_id=dbPoll.id, option_text=pollData.optionB)
        db.add_all([optionA, optionB])

        dbStat = PollStat(poll_id=dbPoll.id)
        db.add(dbStat)

        db.commit()
        db.refresh(dbPoll)
        
        return dbPoll

    except SQLAlchemyError as databaseError:
        db.rollback()
        raise databaseError