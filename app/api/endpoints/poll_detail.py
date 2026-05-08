from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import getCurrentUser, getDb
from app.core.time import now_kst_naive
from app.crud import poll_detail as pollDetailCrud
from app.models.bet import Bet, Vote
from app.models.poll import Poll, PollOption
from app.models.user import User
from app.schemas.poll_detail import PollDetailResponse, PollOptionDetail, PollStatus

POLL_STATUS_ONGOING = "ONGOING"

router = APIRouter()


@router.get("/{pollId}", response_model=PollDetailResponse)
def readPollDetail(
    pollId: int,
    databaseSession: Session = Depends(getDb),
    currentUser: User = Depends(getCurrentUser),
):
    poll = pollDetailCrud.getPoll(databaseSession, pollId)
    if poll is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Poll not found",
        )

    options = pollDetailCrud.getPollOptions(databaseSession, pollId)
    if len(options) != 2:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Poll detail requires exactly two options",
        )

    now = now_kst_naive()
    isEnded = pollDetailCrud.isPollEnded(poll, now)
    effectiveStatus = getEffectiveStatus(poll, isEnded)
    remainingSeconds = getRemainingSeconds(poll, isEnded, now)

    participantCount = pollDetailCrud.getParticipantCount(databaseSession, pollId)
    totalBetCredits = pollDetailCrud.getTotalBetCredits(databaseSession, pollId)
    betCreditsByOption = pollDetailCrud.getBetCreditsByOption(
        databaseSession,
        pollId,
    )
    optionDetails = buildOptionDetails(options, betCreditsByOption)
    winnerOptionId, isDraw = getPollResult(options, isEnded)

    isActive = not isEnded and poll.status == POLL_STATUS_ONGOING
    isCreator = poll.creator_id == currentUser.id
    myVote = (
        databaseSession.query(Vote)
        .filter(Vote.poll_id == pollId, Vote.user_id == currentUser.id)
        .first()
    )
    myBet = (
        databaseSession.query(Bet)
        .filter(Bet.poll_id == pollId, Bet.user_id == currentUser.id)
        .first()
    )
    hasVoted = myVote is not None and not isCreator
    hasBet = myBet is not None and not isCreator
    mySelection = None if isCreator else getMySelection(options, myVote)

    return PollDetailResponse(
        id=poll.id,
        title=poll.title,
        status=effectiveStatus,
        endTime=poll.end_time,
        remainingSeconds=remainingSeconds,
        participantCount=participantCount,
        totalBetCredits=totalBetCredits,
        options=optionDetails,
        resultsVisible=isEnded or hasBet,
        canVote=isActive and not hasVoted and not isCreator,
        canBet=isActive and hasVoted and not hasBet,
        hasVoted=hasVoted,
        hasBet=hasBet,
        isCreator=isCreator,
        mySelection=mySelection,
        winnerOptionId=winnerOptionId,
        isDraw=isDraw,
    )


def getEffectiveStatus(poll: Poll, isEnded: bool) -> PollStatus:
    if isEnded and poll.status == POLL_STATUS_ONGOING:
        return PollStatus.ENDED

    return PollStatus(poll.status)


def getRemainingSeconds(poll: Poll, isEnded: bool, now: datetime) -> int:
    if poll.end_time is None or isEnded:
        return 0

    return max(int((poll.end_time - now).total_seconds()), 0)


def buildOptionDetails(
    options: list[PollOption],
    betCreditsByOption: dict[int, int],
) -> list[PollOptionDetail]:
    totalVotes = sum(option.vote_count or 0 for option in options)
    optionDetails = []

    for option in options:
        voteCount = option.vote_count or 0
        voteRatio = calculateVoteRatio(voteCount, totalVotes)
        optionDetails.append(
            PollOptionDetail(
                id=option.id,
                optionText=option.option_text,
                voteCount=voteCount,
                voteRatio=voteRatio,
                betCredits=betCreditsByOption.get(option.id, 0),
            )
        )

    return optionDetails


def calculateVoteRatio(voteCount: int, totalVotes: int) -> float:
    if not totalVotes:
        return 0.0

    return round((voteCount / totalVotes) * 100, 2)


def getMySelection(options: list[PollOption], myVote: Vote | None) -> str | None:
    if myVote is None:
        return None

    if myVote.option_id == options[0].id:
        return "A"
    if myVote.option_id == options[1].id:
        return "B"
    return None


def getPollResult(
    options: list[PollOption],
    isEnded: bool,
) -> tuple[int | None, bool]:
    if not isEnded:
        return None, False

    firstVoteCount = options[0].vote_count or 0
    secondVoteCount = options[1].vote_count or 0

    if firstVoteCount == secondVoteCount:
        return None, True

    winnerOptionId = (
        options[0].id
        if firstVoteCount > secondVoteCount
        else options[1].id
    )
    return winnerOptionId, False
