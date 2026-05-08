from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.bet import Vote
from app.models.poll import PollOption, PollStat
from app.models.user import User

# from app.crud import poll as crudPoll
# from app.crud import user as crudUser

def createVote(db: Session, pollId: int, userId: int, selection: str):
    try:
        # 1. 중복 투표 체크 (Vote 도메인 고유 로직이므로 직접 쿼리)
        alreadyVoted = db.query(Vote).filter(Vote.poll_id == pollId, Vote.user_id == userId).first()
        if alreadyVoted:
            return None, "ALREADY_VOTED"

        # 2. 선택지 ID 매핑 (A/B 선택을 실제 DB의 Option ID로 변환)
        # options = crudPoll.getPollOptions(db, pollId=pollId)
        options = db.query(PollOption).filter(PollOption.poll_id == pollId).order_by(PollOption.id).all()
        
        if not options or len(options) < 2:
            return None, "INVALID_POLL"
        
        targetOptionId = options[0].id if selection == "A" else options[1].id

        # 3. 투표 기록 생성
        newVote = Vote(user_id=userId, poll_id=pollId, option_id=targetOptionId)
        db.add(newVote)

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