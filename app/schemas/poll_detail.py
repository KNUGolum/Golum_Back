from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class PollStatus(str, Enum):
    ONGOING = "ONGOING"
    ENDED = "ENDED"
    INVALID = "INVALID"


class PollOptionDetail(BaseModel):
    id: int
    optionText: str | None
    voteCount: int
    voteRatio: float
    betCredits: int

    class Config:
        orm_mode = True


class PollDetailResponse(BaseModel):
    id: int
    title: str
    status: PollStatus
    endTime: datetime | None
    remainingSeconds: int
    participantCount: int
    totalBetCredits: int
    options: list[PollOptionDetail]
    resultsVisible: bool
    canVote: bool
    canBet: bool
    winnerOptionId: int | None = None
    isDraw: bool = False

    class Config:
        orm_mode = True
