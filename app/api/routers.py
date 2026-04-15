from fastapi import APIRouter
from app.api.endpoints import auth, vote, bet

apiRouter = APIRouter()

apiRouter.include_router(auth.router, prefix="/auth", tags=["auth"])
apiRouter.include_router(vote.router, prefix="/poll", tags=["Vote"])
apiRouter.include_router(bet.router, prefix="/bets", tags=["bet"])