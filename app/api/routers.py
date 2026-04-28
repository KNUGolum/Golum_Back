from fastapi import APIRouter
from app.api.endpoints import (
    auth,
    poll,
    vote,
    bet,
    poll_result,
    payout,
    websocket,
    poll_ratio_update,
    poll_ratio_read,
    poll_result_read,
)

apiRouter = APIRouter()

apiRouter.include_router(auth.router, prefix="/auth", tags=["auth"])
apiRouter.include_router(poll.router, prefix="/poll", tags=["poll"])
apiRouter.include_router(vote.router, prefix="/vote", tags=["vote"])
apiRouter.include_router(bet.router, prefix="/bets", tags=["bet"])
apiRouter.include_router(poll_result.router, prefix="/poll", tags=["pollResult"])
apiRouter.include_router(payout.router, prefix="/payout", tags=["payout"])
apiRouter.include_router(websocket.router, tags=["WebSocket"])
apiRouter.include_router(poll_ratio_update.router, prefix="/poll", tags=["pollRatio"])
apiRouter.include_router(poll_ratio_read.router, prefix="/polls", tags=["polls"])
apiRouter.include_router(poll_result_read.router, prefix="/polls", tags=["polls"])
