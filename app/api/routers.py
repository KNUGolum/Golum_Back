from fastapi import APIRouter
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
from app.api.endpoints import auth, poll, vote
=======
from app.api.endpoints import auth, vote, bet
>>>>>>> pr-34
=======
from app.api.endpoints import auth, vote, bet, poll_result
>>>>>>> pr-35
=======
from app.api.endpoints import auth, vote, bet, poll_result, payout, websocket
>>>>>>> pr-36

apiRouter = APIRouter()

apiRouter.include_router(auth.router, prefix="/auth", tags=["auth"])
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
apiRouter.include_router(poll.router, prefix="/poll", tags=["poll"])
apiRouter.include_router(vote.router, prefix="/vote", tags=["vote"])
=======
apiRouter.include_router(vote.router, prefix="/poll", tags=["Vote"])
apiRouter.include_router(bet.router, prefix="/bets", tags=["bet"])
>>>>>>> pr-34
=======
apiRouter.include_router(vote.router, prefix="/poll", tags=["Vote"])
apiRouter.include_router(bet.router, prefix="/bets", tags=["bet"])
apiRouter.include_router(
    poll_result.router,  
    prefix="/poll",      
    tags=["pollResult"]  
)
>>>>>>> pr-35
=======
apiRouter.include_router(vote.router, prefix="/poll", tags=["Vote"])
apiRouter.include_router(bet.router, prefix="/bets", tags=["bet"])
apiRouter.include_router(poll_result.router, prefix="/poll", tags=["pollResult"])
apiRouter.include_router(payout.router, prefix="/payout", tags=["payout"])
apiRouter.include_router(websocket.router, tags=["WebSocket"])
>>>>>>> pr-36
=======
#from app.api.endpoints import auth
# 나중에 polls, bets 라우터도 만들면 여기서 import 합니다.
# from app.api.endpoints import polls, bets
from app.api.endpoints import poll_ratio_update

apiRouter = APIRouter()

# 각각의 엔드포인트를 중앙 라우터에 꽂아줍니다.
#apiRouter.include_router(auth.router, prefix="/auth", tags=["auth"])
# apiRouter.include_router(polls.router, prefix="/polls", tags=["polls"])
# apiRouter.include_router(bets.router, prefix="/bets", tags=["bets"])
apiRouter.include_router(poll_ratio_update.router, prefix="/poll", tags=["poll"])
>>>>>>> pr-37
