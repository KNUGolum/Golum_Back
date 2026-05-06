from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import Optional
# 나중에 주석 해제
# from app.schemas.poll_result import PollResultStatus

class SettlementStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class DividendPayoutResponse(BaseModel):
    message: str = Field(..., description="처리 결과 메시지")
    pollId: int = Field(..., description="투표 ID")
    
    # pollResultStatus: PollResultStatus = Field(..., description="판정 상태")
    winningOptionId: Optional[int] = Field(None, description="승리한 선택지 ID")
    
    status: SettlementStatus = Field(..., description="정산 최종 상태")
    dividendRate: float = Field(..., description="적용된 고정 배수")
    totalPayoutAmount: int = Field(0, description="총 지급된 배당금 합계")
    payoutUserCount: int = Field(0, description="배당금을 받은 유저 수")
    
    paidAt: datetime = Field(default_factory=datetime.now, description="지급 완료 시간")

    class Config:
        from_attributes = True