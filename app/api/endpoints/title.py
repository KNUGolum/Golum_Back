from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import getDb
from app.crud import title 
from app.schemas.title import ShopTitle, TitleShopListResponse

router = APIRouter()


@router.get("/shop", response_model=TitleShopListResponse)
async def getTitleShopList(db: Session = Depends(getDb)):
    titles = title.getShopTitles(db)

    return TitleShopListResponse(
        message="상점 목록 조회가 완료되었습니다.",
        titles=[
            ShopTitle(
                titleId=title.id,
                name=title.name,
                grade=title.grade,
                price=title.price
            )
            for title in titles
        ]
    )