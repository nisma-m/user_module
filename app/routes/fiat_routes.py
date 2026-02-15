from fastapi import APIRouter
from pydantic import BaseModel
from app.services.notification_service import manager

router = APIRouter()

class DepositRequest(BaseModel):
    user_id: str
    amount: float

@router.post("/deposit")
async def create_deposit(data: DepositRequest):

    print(f"Deposit received from {data.user_id} for {data.amount}")

    # 🔥 Send WebSocket notification
    await manager.send_message(
        data.user_id,
        {
            "type": "deposit",
            "status": "success",
            "user_id": data.user_id,
            "amount": data.amount,
            "message": f"Deposit of {data.amount} successful"
        }
    )

    return {
        "message": "Deposit Successful",
        "user_id": data.user_id,
        "amount": data.amount
    }
