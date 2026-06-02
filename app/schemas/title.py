from pydantic import BaseModel
from typing import List


class ShopTitle(BaseModel):
    titleId: int
    name: str
    grade: str
    price: int


class TitleShopListResponse(BaseModel):
    message: str
    titles: List[ShopTitle]