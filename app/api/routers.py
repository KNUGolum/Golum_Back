from fastapi import APIRouter

from app.api.endpoints import auth, bet, poll, poll_detail, vote, websocket, title

apiRouter = APIRouter()

apiRouter.include_router(auth.router, prefix="/auth", tags=["auth"])
apiRouter.include_router(vote.router, prefix="/poll", tags=["Vote"])
apiRouter.include_router(bet.router, prefix="/bets", tags=["bet"])
apiRouter.include_router(websocket.router, tags=["WebSocket"])
apiRouter.include_router(poll.router, prefix="/poll", tags=["poll"])
apiRouter.include_router(poll_detail.router, prefix="/polls", tags=["polls"])
apiRouter.include_router(title.router, prefix="/titles", tags=["title"])



