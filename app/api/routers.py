from fastapi import APIRouter
<<<<<<< HEAD
from app.api.endpoints import auth, poll, vote
=======
from app.api.endpoints import auth, vote, bet
>>>>>>> pr-34

apiRouter = APIRouter()

apiRouter.include_router(auth.router, prefix="/auth", tags=["auth"])
<<<<<<< HEAD
apiRouter.include_router(poll.router, prefix="/poll", tags=["poll"])
apiRouter.include_router(vote.router, prefix="/vote", tags=["vote"])
=======
apiRouter.include_router(vote.router, prefix="/poll", tags=["Vote"])
apiRouter.include_router(bet.router, prefix="/bets", tags=["bet"])
>>>>>>> pr-34
