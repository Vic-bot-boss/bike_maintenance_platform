from fastapi import APIRouter, HTTPException, Depends
from passlib.context import CryptContext
from app.models.user import UserCreate, UserLogin
from app.auth.auth import create_access_token, get_current_user
import os
import json
from pathlib import Path


router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
users_path = Path("app/data/users.json")
users_path.parent.mkdir(parents=True, exist_ok=True)

# Load or initialize users file
if not users_path.exists() or users_path.stat().st_size == 0:
    with open(users_path, "w") as f:
        json.dump([], f)


def load_users():
    try:
        with open(users_path, "r") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except Exception as e:
        print("Error reading users file:", e)
        return []


def save_users(users):
    with open(users_path, "w") as f:
        json.dump(users, f, indent=2)

@router.post("/register")
def register(user: UserCreate):
    users = load_users()
    if any(u["email"] == user.email for u in users):
        raise HTTPException(status_code=400, detail="User already exists")
    
    hashed = pwd_context.hash(user.password)
    users.append({"email": user.email, "password": hashed})
    save_users(users)
    return {"msg": "User created successfully"}

@router.post("/login")
def login(user: UserLogin):
    users = load_users()
    user_data = next((u for u in users if u["email"] == user.email), None)
    if not user_data or not pwd_context.verify(user.password, user_data["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
def get_me(user_email: str = Depends(get_current_user)):
    return {"email": user_email}