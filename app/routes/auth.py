import bcrypt # Import direct library
from fastapi import APIRouter, Request, HTTPException, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.database import get_db
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])

# --- Pydantic Schemas ---
class SignUpRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

# --- New Direct Hashing Functions ---
def hash_password(password: str) -> str:
    # Convert password to bytes, generate salt, and hash
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8') # Store as string in DB

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Compare plain text against the stored hash
    password_byte_enc = plain_password.encode('utf-8')
    hashed_byte_enc = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_byte_enc, hashed_byte_enc)

# --- Routes ---

@router.post("/signup")
def signup(details: SignUpRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == details.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username taken")

    new_user = User(
        username=details.username,
        email=details.email,
        hashed_password=hash_password(details.password) # Uses new function
    )
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}

@router.post("/login")
def login(request: Request, details: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == details.username).first()
    
    # Check if user exists and password matches
    if not user or not verify_password(details.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Set Session
    request.session["user_id"] = user.id
    return {"message": "Logged in successfully"}


@router.get("/me")
def me(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401)
    return {"id": user_id}
