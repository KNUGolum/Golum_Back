from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import getCurrentUser, getDb
from app.core.time import now_kst_naive
from app.crud import poll_detail as pollDetailCrud
from app.models.bet import Bet, Vote
from app.models.user import User
from app.schemas.poll_detail import PollDetailResponse, PollOptionDetail

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
    effectiveStatus = pollDetailCrud.getEffectiveStatus(poll, isEnded)
    remainingSeconds = pollDetailCrud.getRemainingSeconds(poll, isEnded, now)

    participantCount = pollDetailCrud.getParticipantCount(databaseSession, pollId)
    totalBetCredits = pollDetailCrud.getTotalBetCredits(databaseSession, pollId)
    betCreditsByOption = pollDetailCrud.getBetCreditsByOption(
        databaseSession,
        pollId,
    )
    optionDetails = buildOptionDetails(options, betCreditsByOption)
    winnerOptionId, isDraw = pollDetailCrud.calculatePollResult(options, isEnded)

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
    actionState = pollDetailCrud.getPollActionState(
        poll=poll,
        userId=currentUser.id,
        myVote=myVote,
        myBet=myBet,
        now=now,
    )
    mySelection = (
        None
        if actionState["isCreator"]
        else pollDetailCrud.getMySelection(options, myVote)
    )

    return PollDetailResponse(
        id=poll.id,
        title=poll.title,
        status=effectiveStatus,
        endTime=poll.end_time,
        remainingSeconds=remainingSeconds,
        participantCount=participantCount,
        totalBetCredits=totalBetCredits,
        options=optionDetails,
        resultsVisible=actionState["resultsVisible"],
        canVote=actionState["canVote"],
        canBet=actionState["canBet"],
        hasVoted=actionState["hasVoted"],
        hasBet=actionState["hasBet"],
        isCreator=actionState["isCreator"],
        mySelection=mySelection,
        winnerOptionId=winnerOptionId,
        isDraw=isDraw,
    )


def buildOptionDetails(
    options,
    betCreditsByOption: dict[int, int],
) -> list[PollOptionDetail]:
    totalVotes = sum(option.vote_count or 0 for option in options)
    optionDetails = []

    for option in options:
        voteCount = option.vote_count or 0
        voteRatio = pollDetailCrud.calculateVoteRatio(voteCount, totalVotes)
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
