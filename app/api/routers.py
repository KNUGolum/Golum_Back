from fastapi import APIRouter
from app.api.endpoints import auth, poll, vote, bet, poll_result, payout, websocket
# 나중에 polls, bets 라우터도 만들면 여기서 import 합니다.
# from app.api.endpoints import polls, bets
from app.api.endpoints import poll_ratio_update, poll_ratio_read, poll_result_read, poll_detail

apiRouter = APIRouter()

apiRouter.include_router(auth.router, prefix="/auth", tags=["auth"])
apiRouter.include_router(vote.router, prefix="/poll", tags=["Vote"])
apiRouter.include_router(bet.router, prefix="/bets", tags=["bet"])
apiRouter.include_router(poll_result.router, prefix="/poll", tags=["pollResult"])
apiRouter.include_router(payout.router, prefix="/payout", tags=["payout"])
apiRouter.include_router(websocket.router, tags=["WebSocket"])
apiRouter.include_router(poll.router, prefix="/poll", tags=["poll"])
apiRouter.include_router(poll_ratio_update.router, prefix="/poll", tags=["poll"])
apiRouter.include_router(poll_ratio_read.router, prefix="/polls", tags=["polls"])
apiRouter.include_router(poll_result_read.router, prefix="/polls", tags=["polls"])
apiRouter.include_router(poll_detail.router, prefix="/polls", tags=["polls"])




