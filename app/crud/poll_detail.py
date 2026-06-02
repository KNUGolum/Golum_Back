from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.time import now_kst_naive
from app.models.bet import Bet, Vote
from app.models.poll import Poll, PollOption

POLL_STATUS_ONGOING = "ONGOING"
POLL_STATUS_ENDED = "ENDED"
POLL_STATUS_INVALID = "INVALID"
POLL_RESULT_DRAW = "DRAW"
POLL_RESULT_FINISHED = "FINISHED"
POLL_RESULT_INVALID = "INVALID"
SELECTION_OPTION_A = "A"
SELECTION_OPTION_B = "B"


def getPoll(databaseSession: Session, pollId: int) -> Poll | None:
    return databaseSession.query(Poll).filter(Poll.id == pollId).first()


def getPollOptions(databaseSession: Session, pollId: int) -> list[PollOption]:
    return (
        databaseSession.query(PollOption)
        .filter(PollOption.poll_id == pollId)
        .order_by(PollOption.id.asc())
        .all()
    )


def getParticipantCount(databaseSession: Session, pollId: int) -> int:
    return (
        databaseSession.query(func.count(func.distinct(Vote.user_id)))
        .filter(Vote.poll_id == pollId)
        .scalar()
        or 0
    )


def getTotalBetCredits(databaseSession: Session, pollId: int) -> int:
    return (
        databaseSession.query(func.coalesce(func.sum(Bet.amount), 0))
        .filter(Bet.poll_id == pollId)
        .scalar()
        or 0
    )


def getBetCreditsByOption(
    databaseSession: Session,
    pollId: int,
) -> dict[int, int]:
    betCreditsRows = (
        databaseSession.query(
            Bet.option_id,
            func.coalesce(func.sum(Bet.amount), 0),
        )
        .filter(Bet.poll_id == pollId)
        .group_by(Bet.option_id)
        .all()
    )
    return {optionId: amount for optionId, amount in betCreditsRows}


def hasBinaryOptions(options: list[PollOption]) -> bool:
    return len(options) == 2


def resolveOptionBySelection(
    options: list[PollOption],
    selection: str,
) -> PollOption | None:
    if not hasBinaryOptions(options):
        return None

    if selection == SELECTION_OPTION_A:
        return options[0]

    if selection == SELECTION_OPTION_B:
        return options[1]

    return None


def isPollEnded(poll: Poll, now: datetime | None = None) -> bool:
    if poll.status == POLL_STATUS_ENDED:
        return True

    if poll.status == POLL_STATUS_INVALID:
        return True

    if poll.end_time is None:
        return False

    now = now or now_kst_naive()
    return poll.end_time <= now


def isPollActive(poll: Poll, now: datetime | None = None) -> bool:
    return poll.status == POLL_STATUS_ONGOING and not isPollEnded(poll, now)


def getEffectiveStatus(poll: Poll, isEnded: bool) -> str:
    if isEnded and poll.status == POLL_STATUS_ONGOING:
        return POLL_STATUS_ENDED

    return poll.status


def getRemainingSeconds(poll: Poll, isEnded: bool, now: datetime) -> int:
    if poll.end_time is None or isEnded:
        return 0

    return max(int((poll.end_time - now).total_seconds()), 0)


def calculateVoteRatio(voteCount: int, totalVotes: int) -> float:
    if not totalVotes:
        return 0.0

    return round((voteCount / totalVotes) * 100, 2)


def calculatePollResult(
    options: list[PollOption],
    isEnded: bool,
) -> tuple[int | None, bool]:
    if not isEnded or not hasBinaryOptions(options):
        return None, False

    firstVoteCount = options[0].vote_count or 0
    secondVoteCount = options[1].vote_count or 0
    totalVoteCount = firstVoteCount + secondVoteCount

    if totalVoteCount == 0:
        return None, False

    if firstVoteCount == secondVoteCount:
        return None, True

    winnerOptionId = (
        options[0].id
        if firstVoteCount > secondVoteCount
        else options[1].id
    )
    return winnerOptionId, False


def calculatePollResultStatus(
    options: list[PollOption],
) -> tuple[str, int | None, int]:
    if not hasBinaryOptions(options):
        return POLL_RESULT_INVALID, None, 0

    firstVoteCount = options[0].vote_count or 0
    secondVoteCount = options[1].vote_count or 0
    totalVoteCount = firstVoteCount + secondVoteCount

    if totalVoteCount == 0:
        return POLL_RESULT_INVALID, None, totalVoteCount

    if firstVoteCount == secondVoteCount:
        return POLL_RESULT_DRAW, None, totalVoteCount

    winnerOptionId = (
        options[0].id
        if firstVoteCount > secondVoteCount
        else options[1].id
    )
    return POLL_RESULT_FINISHED, winnerOptionId, totalVoteCount


def getMySelection(
    options: list[PollOption],
    myVote: Vote | None,
) -> str | None:
    if myVote is None or not hasBinaryOptions(options):
        return None

    if myVote.option_id == options[0].id:
        return SELECTION_OPTION_A

    if myVote.option_id == options[1].id:
        return SELECTION_OPTION_B

    return None


def getPollActionState(
    poll: Poll,
    userId: int | None,
    myVote: Vote | None,
    myBet: Bet | None,
    now: datetime | None = None,
) -> dict[str, bool]:
    isEnded = isPollEnded(poll, now)
    isCreator = userId is not None and poll.creator_id == userId
    hasVoted = myVote is not None and not isCreator
    hasBet = myBet is not None and not isCreator
    isActive = poll.status == POLL_STATUS_ONGOING and not isEnded

    return {
        "isEnded": isEnded,
        "isCreator": isCreator,
        "hasVoted": hasVoted,
        "hasBet": hasBet,
        "resultsVisible": isEnded or hasBet,
        "canVote": isActive and not hasVoted and not isCreator,
        "canBet": isActive and hasVoted and not hasBet,
    }
