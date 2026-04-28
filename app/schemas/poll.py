from pydantic import BaseModel, Field
from datetime import datetime

class PollCreateRequest(BaseModel):
    title: str = Field(..., example="탕수육은 부먹인가 찍먹인가?")
    optionA: str = Field(..., example="부먹")
    optionB: str = Field(..., example="찍먹")
    durationHours: int = Field(..., ge=1, le=24, description="투표 진행 시간 (1~24시간)")

class PollCreateResponse(BaseModel):
    message: str
    pollId: int
    # creatorId: int
    endTime: datetime

class PollListItem(BaseModel):
    pollId: int
    title: str
    optionA: str
    optionB: str
    status: str
    totalVotes: int
    # creatorId: int
    endTime: datetime
    createdAt: datetime

class PollListResponse(BaseModel):
    totalCount: int
    currentPage: int
    polls: list[PollListItem]