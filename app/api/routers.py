from fastapi import APIRouter
from app.api.endpoints import auth, poll, vote, bet
# 나중에 polls, bets 라우터도 만들면 여기서 import 합니다.
# from app.api.endpoints import polls, bets

apiRouter = APIRouter()

apiRouter.include_router(auth.router, prefix="/auth", tags=["auth"])
apiRouter.include_router(vote.router, prefix="/poll", tags=["Vote"])
apiRouter.include_router(bet.router, prefix="/bets", tags=["bet"])
# apiRouter.include_router(polls.router, prefix="/polls", tags=["polls"])
# apiRouter.include_router(bets.router, prefix="/bets", tags=["bets"])
apiRouter.include_router(poll.router, prefix="/poll", tags=["poll"])
# apiRouter.include_router(bets.router, prefix="/bets", tags=["bets"])
