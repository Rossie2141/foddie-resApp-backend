from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database import Base

# class Dish(Base):
#     __tablename__ = "dishes"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     description = Column(String)
#     price = Column(Float)
#     category = Column(String)
#     rating = Column(Float, nullable=True)

class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("dishes.id"))
    quantity = Column(Integer, default=1)

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("dishes.id"))