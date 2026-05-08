from pydantic import BaseModel, Field
from datetime import datetime


class PollRatioReadResponse(BaseModel):
    message: str
    pollId: int
    totalVotes: int
    optionARatio: float
    optionBRatio: float
    updatedAt: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True