from fastapi import APIRouter
from app.api.endpoints import auth, vote, bet, poll_result

apiRouter = APIRouter()

apiRouter.include_router(auth.router, prefix="/auth", tags=["auth"])
apiRouter.include_router(vote.router, prefix="/poll", tags=["Vote"])
apiRouter.include_router(bet.router, prefix="/bets", tags=["bet"])
apiRouter.include_router(
    poll_result.router,  
    prefix="/poll",      
    tags=["pollResult"]  
)