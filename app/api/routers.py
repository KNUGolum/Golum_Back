from fastapi import APIRouter
# from app.api.endpoints import auth
# 나중에 polls, bets 라우터도 만들면 여기서 import 합니다.
# from app.api.endpoints import polls, bets

apiRouter = APIRouter()

# 각각의 엔드포인트를 중앙 라우터에 꽂아줍니다.
# apiRouter.include_router(auth.router, prefix="/auth", tags=["auth"])
# apiRouter.include_router(polls.router, prefix="/polls", tags=["polls"])
# apiRouter.include_router(bets.router, prefix="/bets", tags=["bets"])