from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# -------------------------
# Create Wallet Schema
# -------------------------
class WalletCreate(BaseModel):
    currency: str = "INR"
    wallet_type: str = "spot"


# -------------------------
# Common Amount Schema
# -------------------------
class AmountRequest(BaseModel):
    amount: float = Field(gt=0)


# -------------------------
# Wallet Response Schema
# -------------------------
class WalletResponse(BaseModel):
    user_id: str
    currency: str
    wallet_type: str
    balance: float
    locked_balance: float

    class Config:
        from_attributes = True


# -------------------------
# Transaction Schema
# -------------------------
class Transaction(BaseModel):
    user_email: Optional[str] = None
    amount: float
    type: str
    currency: str
    created_at: datetime = datetime.utcnow()
