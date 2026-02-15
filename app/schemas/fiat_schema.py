from pydantic import BaseModel
from typing import Optional

class WalletCreate(BaseModel):
    user_id: str


class DepositRequest(BaseModel):
    user_id: str
    amount: float


class WithdrawRequest(BaseModel):
    user_id: str
    amount: float


class WalletResponse(BaseModel):
    id: str
    user_id: str
    balance: float
