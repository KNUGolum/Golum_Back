from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.bet import Vote
from app.models.poll import Poll, PollOption, PollStat
from app.models.user import User

# from app.crud import poll as crudPoll
# from app.crud import user as crudUser

POLL_STATUS_ONGOING = "ONGOING"

def createVote(db: Session, pollId: int, userId: int, selection: str):
    try:
        poll = db.query(Poll).filter(Poll.id == pollId).first()
        if not poll:
            return None, "INVALID_POLL"
        isPollEnded = poll.end_time and poll.end_time <= datetime.now()
        if poll.status != POLL_STATUS_ONGOING or isPollEnded:
            return None, "POLL_CLOSED"

        # 1. 중복 투표 체크 (Vote 도메인 고유 로직이므로 직접 쿼리)
        alreadyVoted = db.query(Vote).filter(Vote.poll_id == pollId, Vote.user_id == userId).first()
        if alreadyVoted:
            return None, "ALREADY_VOTED"

        # 2. 선택지 ID 매핑 (A/B 선택을 실제 DB의 Option ID로 변환)
        # options = crudPoll.getPollOptions(db, pollId=pollId)
        options = db.query(PollOption).filter(PollOption.poll_id == pollId).order_by(PollOption.id).all()
        
        if not options or len(options) < 2:
            return None, "INVALID_POLL"
        
        targetOption = options[0] if selection == "A" else options[1]

        # 3. 투표 기록 생성
        newVote = Vote(user_id=userId, poll_id=pollId, option_id=targetOption.id)
        db.add(newVote)
        targetOption.vote_count = (targetOption.vote_count or 0) + 1

        # 4. 유저 크레딧 지급 (참여 보상 +100)
        # crudUser.addCredit(db, userId=userId, amount=100) 
        user = db.query(User).filter(User.id == userId).first()
        if user:
            user.credit += 100

        # 5. 투표 통계 업데이트 (총 투표수 증가)
        # crudPoll.incrementTotalVotes(db, pollId=pollId)
        stat = db.query(PollStat).filter(PollStat.poll_id == pollId).first()
        if stat:
            stat.total_votes += 1

        # 한 번의 트랜잭션으로 안전하게 저장
        db.commit()
        return newVote, "SUCCESS"

    except SQLAlchemyError as databaseError:
        db.rollback()
        raise databaseError
