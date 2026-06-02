from pydantic import BaseModel, Field
from datetime import datetime

class VoteRequest(BaseModel):
    selection: str = Field(..., pattern="^[AB]$")

class VoteDetails(BaseModel):
    pollId: int
    selectedOption: str

class VoteResponse(BaseModel):
    message: str
    earnedCredit: int
    voteDetails: VoteDetails

class VoteHistoryItem(BaseModel):
    id: int
    pollId: int
    optionId: int
    createdAt: datetime

    class Config:
        from_attributes = True