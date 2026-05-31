from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.time import now_kst_naive
from app.crud import poll_detail as pollDetailCrud
from app.models.bet import Bet, Settlement
from app.models.poll import Poll
from app.models.user import User

DEFAULT_DIVIDEND_MULTIPLIER = 1.5


def calculateRewardAmount(
    betAmount: int,
    isDraw: bool,
    multiplier: float = DEFAULT_DIVIDEND_MULTIPLIER,
) -> int:
    if isDraw:
        return betAmount

    return int(betAmount * multiplier)


def payoutDividends(
    db: Session,
    pollId: int,
    multiplier: float = DEFAULT_DIVIDEND_MULTIPLIER,
):
    try:
        alreadySettled = (
            db.query(Settlement)
            .filter(Settlement.poll_id == pollId, Settlement.status == "COMPLETED")
            .first()
        )
        if alreadySettled:
            return None, "ALREADY_SETTLED"

        poll = db.query(Poll).filter(Poll.id == pollId).first()
        if not poll:
            return None, "POLL_NOT_FOUND"

        if poll.status != pollDetailCrud.POLL_STATUS_ENDED:
            return None, "POLL_NOT_ENDED"

        options = pollDetailCrud.getPollOptions(db, pollId)
        if not pollDetailCrud.hasBinaryOptions(options):
            return None, "INVALID_POLL_OPTIONS"

        winningOptionId, isDraw = pollDetailCrud.calculatePollResult(
            options=options,
            isEnded=True,
        )
        bets = db.query(Bet).filter(Bet.poll_id == pollId).all()

        totalPayoutAmount = 0
        payoutUserCount = 0

        for bet in bets:
            isWinningBet = isDraw or bet.option_id == winningOptionId
            if not isWinningBet:
                bet.result = "LOSE"
                bet.reward_amount = 0
                continue

            rewardAmount = calculateRewardAmount(bet.amount, isDraw, multiplier)
            user = (
                db.query(User)
                .filter(User.id == bet.user_id)
                .with_for_update()
                .first()
            )
            if user:
                user.credit += rewardAmount

            bet.result = "WIN"
            bet.reward_amount = rewardAmount
            totalPayoutAmount += rewardAmount
            payoutUserCount += 1

        settlement = db.query(Settlement).filter(Settlement.poll_id == pollId).first()
        if not settlement:
            settlement = Settlement(poll_id=pollId)
            db.add(settlement)

        settlement.status = "COMPLETED"
        settlement.completed_at = now_kst_naive()

        db.commit()

        return {
            "pollId": pollId,
            "winningOptionId": winningOptionId,
            "totalPayoutAmount": totalPayoutAmount,
            "payoutUserCount": payoutUserCount,
            "dividendRate": 1.0 if isDraw else multiplier,
        }, "SUCCESS"

    except SQLAlchemyError as databaseError:
        db.rollback()
        raise databaseError
