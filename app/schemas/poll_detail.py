from datetime import datetime
from typing import Literal

from pydantic import BaseModel


PollStatus = Literal["ONGOING", "ENDED", "INVALID"]


class PollOptionDetail(BaseModel):
    id: int
    option_text: str | None
    vote_count: int
    vote_ratio: float
    bet_credits: int

    class Config:
        orm_mode = True


class PollDetailResponse(BaseModel):
    id: int
    title: str
    status: PollStatus
    end_time: datetime | None
    remaining_seconds: int
    participant_count: int
    total_bet_credits: int
    options: list[PollOptionDetail]
    results_visible: bool
    can_vote: bool
    can_bet: bool
    winner_option_id: int | None = None
    is_draw: bool = False

    class Config:
        orm_mode = True
