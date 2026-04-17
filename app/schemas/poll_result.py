from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime

# 테스트를 위한 임의의 고정 배수 설정 (추후 수정 예정)
# 수수료 미적용 / 승리 시 1.5배 지급 / 무승부 시 1.0배(원금) / 패배 시 0배 지급 기준
FIXED_WIN_MULTIPLIER = 1.5

class PollResultStatus(str, Enum):
    FINISHED = "FINISHED"
    DRAW = "DRAW"
    INVALID = "INVALID"

class EvaluatePollResponse(BaseModel):
    message: str = Field(..., description="처리 결과 메시지")
    pollId: int
    pollResultStatus: PollResultStatus = Field(..., description="최종 마감 상태")
    winningOptionId: Optional[int] = Field(None, description="승리한 선택지 ID")
    totalVoteCount: int = Field(0, description="총 투표 수")
    totalPoolAmount: int = Field(0, description="총 배팅 크레딧")
    
    dividendRate: float = Field(default=FIXED_WIN_MULTIPLIER, description="적용된 고정 배당률")
    
    settledAt: datetime = Field(default_factory=datetime.now, description="정산 완료 시간")

    class Config:
        from_attributes = True