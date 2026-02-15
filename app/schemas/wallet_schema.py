from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class WalletCreate(BaseModel):
    currency: str = "INR"


class DepositRequest(BaseModel):
    amount: float = Field(gt=0)


class WithdrawRequest(BaseModel):
    amount: float = Field(gt=0)


class Transaction(BaseModel):
    user_email: str
    amount: float
    type: str
    currency: str
    created_at: datetime = datetime.utcnow()
