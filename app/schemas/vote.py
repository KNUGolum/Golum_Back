from pydantic import BaseModel, Field

class VoteRequest(BaseModel):
    selection: str = Field(..., pattern="^[AB]$")

class VoteDetails(BaseModel):
    pollId: int
    selectedOption: str

class VoteResponse(BaseModel):
    message: str
    earnedCredit: int
    voteDetails: VoteDetails