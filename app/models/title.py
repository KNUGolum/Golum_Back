from sqlalchemy import Column, BigInteger, String, Integer
from app.db.base import Base


class Title(Base):
    __tablename__ = "titles"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    grade = Column(String(20), nullable=False)
    price = Column(Integer, nullable=False)