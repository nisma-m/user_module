from fastapi import APIRouter, HTTPException
from app.config.database import db
from app.utils.hash_utils import hash_password, verify_password
from app.utils.jwt_handler import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
async def register(user: dict):
    existing_user = await db.users.find_one({"email": user["email"]})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed_password = hash_password(user["password"])

    new_user = {
        "email": user["email"],
        "password": hashed_password
    }

    await db.users.insert_one(new_user)

    return {"message": "User registered successfully"}


@router.post("/login")
async def login(user: dict):
    existing_user = await db.users.find_one({"email": user["email"]})

    if not existing_user:
        raise HTTPException(status_code=400, detail="Invalid email")

    if not verify_password(user["password"], existing_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid password")

    token = create_access_token({"sub": user["email"]})

    return {
        "access_token": token,
        "token_type": "bearer"
    }