from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime



class PollResultStatus(str, Enum):
    FINISHED = "FINISHED"
    DRAW = "DRAW"
    INVALID = "INVALID"


class PollResultReadResponse(BaseModel):
    message: str
    pollId: int
    resultStatus: PollResultStatus
    winningOptionId: Optional[int]
    winningOptionText: Optional[str]
    totalVotes: int
    checkedAt: datetime = Field(default_factory=datetime.now)


    class Config:
        from_attributes = True