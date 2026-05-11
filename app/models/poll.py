from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey, Enum, Integer, Float
from app.core.time import now_kst_naive
from app.db.base import Base

class Poll(Base):
    __tablename__ = "polls"
    id = Column(BigInteger, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    creator_id = Column(BigInteger, ForeignKey("users.id"))
    status = Column(Enum('ONGOING', 'ENDED', 'INVALID', name='poll_status_enum'), default='ONGOING')
    end_time = Column(DateTime)
    created_at = Column(DateTime, default=now_kst_naive)

class PollOption(Base):
    __tablename__ = "poll_options"
    id = Column(BigInteger, primary_key=True, index=True)
    poll_id = Column(BigInteger, ForeignKey("polls.id"))
    option_text = Column(String(255))
    vote_count = Column(Integer, default=0)

class PollStat(Base):
    __tablename__ = "poll_stats"
    poll_id = Column(BigInteger, ForeignKey("polls.id"), primary_key=True)
    total_votes = Column(Integer, default=0)
    option1_ratio = Column(Float, default=0.0)
    option2_ratio = Column(Float, default=0.0)
    updated_at = Column(DateTime, default=now_kst_naive, onupdate=now_kst_naive)
