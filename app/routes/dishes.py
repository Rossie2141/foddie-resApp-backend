from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.models.dish import Dish
from app.schemas.dish import DishResponse
from app.deps import get_db

router = APIRouter(prefix="/dishes", tags=["Dishes"])


@router.get("/", response_model=List[DishResponse])
def get_all_dishes(
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Dish)

    if category:
        query = query.filter(Dish.category == category)

    return query.all()


@router.get("/popular", response_model=List[DishResponse])
def get_popular_dishes(db: Session = Depends(get_db)):
    return db.query(Dish).filter(Dish.is_popular == True).all()


@router.get("/new", response_model=List[DishResponse])
def get_new_dishes(db: Session = Depends(get_db)):
    return db.query(Dish).filter(Dish.is_new == True).all()
