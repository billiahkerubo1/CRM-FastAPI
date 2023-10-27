# auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.security import create_access_token, get_password_hash, verify_password

router = APIRouter()

# User registration
@router.post("/register")
def register_user(user_data: dict, db: Session = Depends(get_db)):
    # Check if the user already exists
    if db.query(User).filter(User.email == user_data['email']).first():
        raise HTTPException(status_code=400, detail="User with this email already registered")
    
    # Create a new user
    new_user = User(**user_data, hashed_password=get_password_hash(user_data['password']))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}

# User login
@router.post("/login")
def login_user(credentials: dict, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials['email']).first()
    if user is None:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    if not verify_password(credentials['password'], user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    # Generate an authentication token
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Sample function to get the current user
@router.get("/user/me", response_model=User)
def get_current_user(current_user: User ):
    return current_user
