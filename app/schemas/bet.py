from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class BetResult(str, Enum):
    PENDING = "PENDING"
    WIN = "WIN"
    LOSE = "LOSE"

class BetCreate(BaseModel):
    optionId: str = Field(..., pattern="^[AB]$")
    amount: int = Field(..., gt=0)

class BetResponse(BaseModel):
    id: int
    userId: int
    pollId: int
    optionId: int
    amount: int
    result: BetResult = BetResult.PENDING  
    rewardAmount: int = 0              
    createdAt: datetime

    class Config:
        from_attributes = True

class BetActionResponse(BaseModel):
    message: str
    betDetails: Optional[BetResponse] = None