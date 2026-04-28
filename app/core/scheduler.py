import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from app.db.session import SessionLocal
from app.models.poll import Poll
from app.models.bet import Bet
from app.crud.poll_result import evaluatePollResult
from app.crud.payout import payoutDividends
from app.core.websocket import manager


async def send_notifications(db, poll_id, result_data):
    await manager.broadcast({
        "type": "POLL_END",
        "pollId": poll_id,
        "winningOptionId": result_data["winningOptionId"],
        "message": "투표가 종료되었습니다."
    })

    if result_data["winningOptionId"]:
        winners = db.query(Bet).filter(
            Bet.poll_id == poll_id,
            Bet.option_id == result_data["winningOptionId"]
        ).all()

        for winner in winners:
            await manager.send_personal_message({
                "type": "PAYOUT_COMPLETE",
                "pollId": poll_id,
                "amount": winner.reward_amount,
                "message": f"축하합니다 {winner.reward_amount} 크레딧이 정산되었습니다."
            }, winner.user_id)


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
            print(f"[Scheduler] 작업 시작: Poll ID {poll.id}")

            eval_result, eval_msg = evaluatePollResult(db=db, pollId=poll.id)

            if eval_msg == "SUCCESS":
                payout_result, payout_msg = payoutDividends(db=db, pollId=poll.id)

                if payout_msg == "SUCCESS":
                    print(f"[Scheduler] Poll ID {poll.id} - 정산 완료")
                    asyncio.run(send_notifications(db, poll.id, payout_result))
                else:
                    print(f"[Scheduler] Poll ID {poll.id} - 정산 실패: {payout_msg}")
            else:
                print(f"[Scheduler] Poll ID {poll.id} - 판정 실패: {eval_msg}")

    except Exception as e:
        print(f"[Scheduler] 오류 발생: {e}")
    finally:
        db.close()


scheduler = BackgroundScheduler()
scheduler.add_job(check_and_evaluate_polls, 'interval', minutes=60)