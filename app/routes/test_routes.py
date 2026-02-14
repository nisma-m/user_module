from fastapi import APIRouter, Depends
from app.utils.security import get_current_user

router = APIRouter(prefix="/test", tags=["Test"])

@router.get("/protected")
async def protected_route(user=Depends(get_current_user)):
    return {"msg": "Access granted", "user": user}