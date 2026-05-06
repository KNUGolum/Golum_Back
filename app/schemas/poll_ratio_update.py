from pydantic import BaseModel, Field
from datetime import datetime


class PollRatioUpdateRequest(BaseModel):
    optionId: int = Field(..., description="투표할 선택지 ID")

class PollRatioUpdateResponse(BaseModel):
    message: str
    pollId: int
    totalVotes: int
    optionARatio: float
    optionBRatio: float
    updatedAt: datetime = Field(default_factory=datetime.now, description="갱신 시간")
