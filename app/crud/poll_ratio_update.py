from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from datetime import datetime

from app.models.poll import Poll, PollOption, PollStat
from app.models.bet import Vote


def updatePollRatio(db: Session, pollId: int):
    try:
        # 1 poll 확인
        poll = db.query(Poll).filter(Poll.id == pollId).first()
        if not poll:
            return None, "POLL_NOT_FOUND"

        # 2 옵션 조회
        options = db.query(PollOption).filter(PollOption.poll_id == 
        pollId).order_by(PollOption.id).all()

        optionA, optionB = options[0], options[1]

        # 3️ 투표 수 계산 
        voteCountA = db.query(func.count(Vote.id)).filter(Vote.poll_id == 
        pollId, Vote.option_id == optionA.id).scalar() or 0

        voteCountB = db.query(func.count(Vote.id)).filter(Vote.poll_id == 
        pollId, Vote.option_id == optionB.id).scalar() or 0

        totalVotes = voteCountA + voteCountB

        if totalVotes == 0:
            return None, "NO_VOTES"

        # 4 비율 계산
        option1Ratio = round((voteCountA / totalVotes),2)
        option2Ratio = round((voteCountB / totalVotes),2)

        # 5 poll_stats 업데이트
        pollStat = db.query(PollStat).filter(PollStat.poll_id ==
        pollId).first()

        if not pollStat:
            pollStat = PollStat(
                poll_id=pollId,
                total_votes=totalVotes,
                option1_ratio=option1Ratio,
                option2_ratio=option2Ratio,
                updated_at=datetime.now()
            )
            db.add(pollStat)
        else:
            pollStat.total_votes = totalVotes # type: ignore
            pollStat.option1_ratio = option1Ratio # type: ignore
            pollStat.option2_ratio = option2Ratio # type: ignore
            pollStat.updated_at = datetime.now() # type: ignore

        db.commit()

        resultData = {
            "totalVoteCount": totalVotes,
            "option1Ratio": option1Ratio,
            "option2Ratio": option2Ratio
        }

        return resultData, "SUCCESS"

    except SQLAlchemyError as databaseError:
        db.rollback()
        raise databaseError