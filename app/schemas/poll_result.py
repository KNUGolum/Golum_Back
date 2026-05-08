from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime

class PollResultStatus(str, Enum):
    FINISHED = "FINISHED"  
    DRAW = "DRAW"         
    INVALID = "INVALID"    

class EvaluatePollResponse(BaseModel):
    message: str = Field(..., description="처리 결과 메시지")
    pollId: int
    pollResultStatus: PollResultStatus = Field(..., description="최종 판정 상태")
    winningOptionId: Optional[int] = Field(None, description="승리한 선택지 ID")
    totalVoteCount: int = Field(0, description="총 투표 수")
    
    evaluatedAt: datetime = Field(default_factory=datetime.now, description="판정 완료 시간")

    class Config:
        from_attributes = True