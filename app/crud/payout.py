from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from app.models.poll import Poll, PollOption
from app.models.bet import Bet, Settlement
from app.models.user import User

# 정산 기본 배수 임의로 설정함
DEFAULT_DIVIDEND_MULTIPLIER = 1.5

def payoutDividends(db: Session, pollId: int, multiplier: float = DEFAULT_DIVIDEND_MULTIPLIER):
    try:
        # 중복 정산 체크
        alreadySettled = db.query(Settlement).filter(
            Settlement.poll_id == pollId, 
            Settlement.status == 'COMPLETED'
        ).first()
        if alreadySettled:
            return None, "ALREADY_SETTLED"

        poll = db.query(Poll).filter(Poll.id == pollId).first()
        if not poll:
            return None, "POLL_NOT_FOUND"
        if poll.status != 'ENDED':
            return None, "POLL_NOT_ENDED"

        options = db.query(PollOption).filter(PollOption.poll_id == pollId).all()
        if len(options) < 2:
            return None, "INVALID_POLL_OPTIONS"

        opt1, opt2 = options[0], options[1]
        
        if opt1.vote_count == opt2.vote_count:
            winningOptionId = None  
        else:
            winningOptionId = opt1.id if opt1.vote_count > opt2.vote_count else opt2.id

        bets = db.query(Bet).filter(Bet.poll_id == pollId).all()
        
        totalPayoutAmount = 0
        payoutUserCount = 0

        for bet in bets:
            # Case 1: 무승부일 경우 (전원 배팅액 1배 환불)
            if winningOptionId is None:
                rewardAmount = bet.amount # 1.0배
                
                user = db.query(User).filter(User.id == bet.user_id).with_for_update().first()
                if user:
                    user.credit += rewardAmount
                
                bet.result = 'WIN' # 돈을 돌려받았으므로 모델 Enum에 따라 WIN 처리
                bet.reward_amount = rewardAmount
                
                totalPayoutAmount += rewardAmount
                payoutUserCount += 1

            # Case 2: 승패가 갈린 경우
            else:
                if bet.option_id == winningOptionId:
                    # 적중: 승리 진영 (고정 배수 적용)
                    rewardAmount = int(bet.amount * multiplier)
                    
                    user = db.query(User).filter(User.id == bet.user_id).with_for_update().first()
                    if user:
                        user.credit += rewardAmount
                    
                    bet.result = 'WIN'
                    bet.reward_amount = rewardAmount
                    totalPayoutAmount += rewardAmount
                    payoutUserCount += 1
                else:
                    # 미적중: 패배 진영 (0원 처리)
                    bet.result = 'LOSE'
                    bet.reward_amount = 0

        settlement = db.query(Settlement).filter(Settlement.poll_id == pollId).first()
        if not settlement:
            settlement = Settlement(poll_id=pollId)
            db.add(settlement)
            
        settlement.status = 'COMPLETED'
        settlement.completed_at = datetime.now()

        db.commit()
        
        resultData = {
            "pollId": pollId,
            "winningOptionId": winningOptionId,
            "totalPayoutAmount": totalPayoutAmount,
            "payoutUserCount": payoutUserCount,
            "dividendRate": multiplier if winningOptionId else 1.0
        }
        
        return resultData, "SUCCESS"

    except SQLAlchemyError as databaseError:
        db.rollback()
        raise databaseError