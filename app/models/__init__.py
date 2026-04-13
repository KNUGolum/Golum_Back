# app/models/__init__.py
# 생성된 모델들을 이곳에서 임포트하여, 다른 곳에서 app.models만 임포트해도 모든 모델이 인식되도록 합니다.
from app.db.base import Base  # Base를 먼저 가져와야 함
from app.models.user import User
from app.models.poll import Poll
from app.models.bet import Bet