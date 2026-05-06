from fastapi import APIRouter
from app.api.endpoints import auth, vote, bet, poll_result, payout, websocket

apiRouter = APIRouter()

apiRouter.include_router(auth.router, prefix="/auth", tags=["auth"])
apiRouter.include_router(vote.router, prefix="/poll", tags=["Vote"])
apiRouter.include_router(bet.router, prefix="/bets", tags=["bet"])
apiRouter.include_router(poll_result.router, prefix="/poll", tags=["pollResult"])
apiRouter.include_router(payout.router, prefix="/payout", tags=["payout"])
apiRouter.include_router(websocket.router, tags=["WebSocket"])