from pydantic import BaseModel
from typing import Optional


class DishResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    rating: Optional[float]
    category: str
    image_url: Optional[str]
    is_new: bool
    is_popular: bool

    class Config:
        orm_mode = True
