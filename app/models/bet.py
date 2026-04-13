from sqlalchemy import Column, BigInteger, ForeignKey, Enum, Integer, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class Vote(Base):
    __tablename__ = "votes"
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"))
    poll_id = Column(BigInteger, ForeignKey("polls.id"))
    option_id = Column(BigInteger, ForeignKey("poll_options.id"))
    created_at = Column(DateTime, server_default=func.now())

class Bet(Base):
    __tablename__ = "bets"
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"))
    poll_id = Column(BigInteger, ForeignKey("polls.id"))
    option_id = Column(BigInteger, ForeignKey("poll_options.id"))
    amount = Column(Integer, nullable=False)
    result = Column(Enum('PENDING', 'WIN', 'LOSE', name='bet_result_enum'), default='PENDING')
    reward_amount = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())

class Settlement(Base):
    __tablename__ = "settlements"
    id = Column(BigInteger, primary_key=True, index=True)
    poll_id = Column(BigInteger, ForeignKey("polls.id"), unique=True)
    status = Column(Enum('PENDING', 'COMPLETED', 'FAILED', name='settlement_status_enum'), default='PENDING')
    created_at = Column(DateTime, server_default=func.now())
    completed_at = Column(DateTime)