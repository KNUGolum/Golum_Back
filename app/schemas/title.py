from pydantic import BaseModel
from typing import List, Optional

class ShopTitle(BaseModel):
    titleId: int
    name: str
    grade: str
    price: int

class TitleShopListResponse(BaseModel):
    message: str
    titles: List[ShopTitle]

class PurchaseTitleResponse(BaseModel):
    message: str
    currentCredit: int

class EquipTitleRequest(BaseModel):
    titleId: Optional[int] = None


class EquipTitleResponse(BaseModel):
    message: str
    equippedTitleId: Optional[int] = None