from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.time import now_kst_naive
from app.crud import poll_detail as pollDetailCrud
from app.models.poll import Poll


def evaluatePollResult(db: Session, pollId: int):
    try:
        poll = db.query(Poll).filter(Poll.id == pollId).first()
        if not poll:
            return None, "POLL_NOT_FOUND"

        if poll.status in [
            pollDetailCrud.POLL_STATUS_ENDED,
            pollDetailCrud.POLL_STATUS_INVALID,
        ]:
            return None, "ALREADY_EVALUATED"

        if poll.end_time is not None and now_kst_naive() < poll.end_time:
            return None, "POLL_STILL_ONGOING"

        options = pollDetailCrud.getPollOptions(db, pollId)
        if not pollDetailCrud.hasBinaryOptions(options):
            return None, "NOT_ENOUGH_OPTIONS"

        resultStatus, winningOptionId, totalVoteCount = (
            pollDetailCrud.calculatePollResultStatus(options)
        )

        if resultStatus == pollDetailCrud.POLL_RESULT_INVALID:
            poll.status = pollDetailCrud.POLL_STATUS_INVALID
        else:
            poll.status = pollDetailCrud.POLL_STATUS_ENDED

        db.commit()

        return {
            "pollResultStatus": resultStatus,
            "winningOptionId": winningOptionId,
            "totalVoteCount": totalVoteCount,
        }, "SUCCESS"

    except SQLAlchemyError as databaseError:
        db.rollback()
        raise databaseError
