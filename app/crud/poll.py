from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import desc
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
    
def getPolls(
    db: Session, 
    status: str = "ongoing", 
    sort: str = "latest", 
    page: int = 1, 
    limit: int = 10
):
    try:
        currentTime = datetime.now()
        
        # Poll과 PollStat 조인 (정렬 및 전체 투표수 조회를 위해 outerjoin 사용)
        query = db.query(Poll, PollStat).outerjoin(PollStat, Poll.id == PollStat.poll_id)
        
        if status == "ongoing":
            query = query.filter(Poll.status == 'ONGOING')
        elif status == "ended":
            query = query.filter(Poll.status == 'ENDED')
            
        if sort == "popular":
            query = query.order_by(desc(PollStat.total_votes))
        else:
            query = query.order_by(desc(Poll.created_at))
            
        totalCount = query.count()
        
        offset = (page - 1) * limit
        # query.all() 반환값은 (Poll, PollStat) 형태의 튜플 리스트입니다.
        pollRecords = query.offset(offset).limit(limit).all()
        
        # 데이터가 없으면 빈 리스트를 빠르게 반환
        if not pollRecords:
            return totalCount, []

        # N+1 쿼리 성능 저하를 막기 위해, 조회된 투표들의 ID만 모아서 선택지(Option)를 한 번에 DB에서 가져옵니다.
        pollIds = [poll.id for poll, stat in pollRecords]
        dbOptions = db.query(PollOption).filter(PollOption.poll_id.in_(pollIds)).all()
        
        # poll_id를 key로 하여 선택지 리스트를 그룹화합니다. (빠른 매핑 용도)
        optionMap = {}
        for option in dbOptions:
            if option.poll_id not in optionMap:
                optionMap[option.poll_id] = []
            optionMap[option.poll_id].append(option.option_text)

        # 프론트엔드 응답 규격(PollListItem)에 맞게 최종 데이터 조립
        pollList = []
        for poll, stat in pollRecords:
            options = optionMap.get(poll.id, [])
            optionA = options[0] if len(options) > 0 else ""
            optionB = options[1] if len(options) > 1 else ""
            
            pollList.append({
                "pollId": poll.id,
                "title": poll.title,
                "optionA": optionA,
                "optionB": optionB,
                "status": poll.status,
                "totalVotes": stat.total_votes if stat else 0,
                # "creatorId": poll.creator_id,
                "endTime": poll.end_time,
                "createdAt": poll.created_at
            })

        return totalCount, pollList

    except SQLAlchemyError as databaseError:
        raise databaseError