from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import getDb, getCurrentUser
from app.crud import title
from app.models.user import User
from app.schemas.title import ShopTitle, TitleShopListResponse, PurchaseTitleResponse, EquipTitleRequest, EquipTitleResponse

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

@router.post("/{titleId}/purchase", response_model=PurchaseTitleResponse)
async def purchaseTitle(
    titleId: int,
    db: Session = Depends(getDb),
    currentUser: User = Depends(getCurrentUser)
):
    user, result = title.purchaseTitle(db, currentUser.id, titleId)

    if result == "USER_NOT_FOUND":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="존재하지 않는 사용자입니다."
        )

    if result == "TITLE_NOT_FOUND":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="존재하지 않는 칭호입니다."
        )

    if result == "ALREADY_OWNED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 보유 중인 아이템입니다."
        )

    if result == "INSUFFICIENT_CREDIT":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="잔액이 부족합니다."
        )

    return PurchaseTitleResponse(
        message="칭호 구매가 완료되었습니다.",
        currentCredit=user.credit
    )

@router.put("/equipped", response_model=EquipTitleResponse)
async def updateEquippedTitle(
    request: EquipTitleRequest,
    db: Session = Depends(getDb),
    currentUser: User = Depends(getCurrentUser)
):
    if request.titleId is None:
        user, result = title.unequipTitle(db, currentUser.id)

        if result == "USER_NOT_FOUND":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="존재하지 않는 사용자입니다."
            )

        return EquipTitleResponse(
            message="칭호 장착이 해제되었습니다.",
            equippedTitleId=None
        )

    user, result = title.equipTitle(db, currentUser.id, request.titleId)

    if result == "USER_NOT_FOUND":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="존재하지 않는 사용자입니다."
        )

    if result == "TITLE_NOT_OWNED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="보유하지 않은 칭호입니다."
        )

    if result == "ALREADY_EQUIPPED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 장착한 칭호입니다."
        )

    return EquipTitleResponse(
        message="칭호 장착이 완료되었습니다.",
        equippedTitleId=user.equipped_title_id
    )