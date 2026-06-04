from sqlalchemy import Column, BigInteger, String, Integer, ForeignKey, DateTime

from app.core.time import now_kst_naive
from app.db.base import Base


class Title(Base):
    __tablename__ = "titles"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    grade = Column(String(20), nullable=False)
    price = Column(Integer, nullable=False)

class UserTitle(Base):
    __tablename__ = "user_titles"

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    title_id = Column(BigInteger, ForeignKey("titles.id"), nullable=False)
    acquired_at = Column(DateTime, default=now_kst_naive)