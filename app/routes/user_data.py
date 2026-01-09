from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.database import get_db
from app.models.user import User # Assuming your models are in app/models/
# You will need to create these models in your models file (see note below)
from app.models.data_models import CartItem, Favorite
from app.models.dish import Dish 

router = APIRouter(prefix="/user", tags=["User Data"])

# --- Pydantic Schemas for Validation ---
class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = 1

# --- Cart Logic ---

@router.get("/cart")
def get_cart(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    
    # If no user is logged in, return empty list instead of crashing
    if not user_id:
        return []

    try:
        # We join the Dish table and CartItem table
        # This allows us to get the price and name which aren't in the cart_items table
        results = db.query(Dish, CartItem.quantity).join(
            CartItem, Dish.id == CartItem.product_id
        ).filter(CartItem.user_id == user_id).all()

        # Format the data into a list of dictionaries
        cart_data = []
        for dish, qty in results:
            cart_data.append({
                "product_id": dish.id,
                "name": dish.name,
                "price": dish.price,
                "quantity": qty,
                "image": getattr(dish, 'image', None) # Safely get image if it exists
            })
        
        return cart_data

    except Exception as e:
        print(f"Error fetching cart: {e}")
        raise HTTPException(status_code=500, detail="Database join failed. Check if Dish and CartItem models are linked.")

@router.post("/cart/add")
def add_to_cart(item: CartItemCreate, request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Please login to add items")

    # Check if item already exists in cart for this user
    existing_item = db.query(CartItem).filter(
        CartItem.user_id == user_id, 
        CartItem.product_id == item.product_id
    ).first()

    if existing_item:
        existing_item.quantity += item.quantity
    else:
        new_cart_item = CartItem(
            user_id=user_id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(new_cart_item)
    
    db.commit()
    return {"message": "Cart updated"}

@router.delete("/cart/remove/{product_id}")
def remove_from_cart(product_id: int, request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    item = db.query(CartItem).filter(
        CartItem.user_id == user_id, 
        CartItem.product_id == product_id
    ).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found in cart")
    
    db.delete(item)
    db.commit()
    return {"message": "Item removed"}

# --- Favorites Logic ---

@router.get("/favorites")
def get_favorites(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authorized")
    
    # Fetches dish details for all items the user has favorited
    favs = db.query(Dish).join(Favorite).filter(Favorite.user_id == user_id).all()
    return favs

@router.post("/favorites/toggle/{product_id}")
def toggle_favorite(product_id: int, request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Login required")

    existing_fav = db.query(Favorite).filter(
        Favorite.user_id == user_id, 
        Favorite.product_id == product_id
    ).first()

    if existing_fav:
        db.delete(existing_fav)
        db.commit()
        return {"message": "Removed from favorites", "status": "unliked"}
    else:
        new_fav = Favorite(user_id=user_id, product_id=product_id)
        db.add(new_fav)
        db.commit()
        return {"message": "Added to favorites", "status": "liked"}