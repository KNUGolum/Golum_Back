from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from app.db.session import SessionLocal 
from app.models.poll import Poll
from app.crud.poll_result import evaluatePollResult

 # PR 피드백 반영 - 수동 판정 대신 end_time 기반 자동 판정 로직 구현
def check_and_evaluate_polls():
    db = SessionLocal()
    try:
        now = datetime.now()
        expired_polls = db.query(Poll).filter(
            Poll.status == 'ONGOING',
            Poll.end_time <= now
        ).all()

        if not expired_polls:
            return

        for poll in expired_polls:
            print(f"[Scheduler] 투표 종료 감지: Poll ID {poll.id} - 자동 판정 시작")
            result, msg = evaluatePollResult(db=db, pollId=poll.id)
            print(f"[Scheduler] Poll ID {poll.id} 결과: {msg}")

    except Exception as e:
        print(f"[Scheduler] 오류 발생: {e}")
    finally:
        db.close()

scheduler = BackgroundScheduler()
# 간격(minutes)은 조정 가능. 임의값 60분으로 설정함.
scheduler.add_job(check_and_evaluate_polls, 'interval', minutes=60)