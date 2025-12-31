from sqlalchemy import Column, Integer, String, Float, Boolean
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.database import Base

class Dish(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    rating = Column(Float)
    category = Column(String, index=True)  # main | salad | dessert
    image_url = Column(String)

    is_new = Column(Boolean, default=False)
    is_popular = Column(Boolean, default=False)
