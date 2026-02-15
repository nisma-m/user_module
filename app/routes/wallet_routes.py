from fastapi import APIRouter, Depends, HTTPException
from app.dependencies.auth_dependency import get_current_user
from app.models.wallet_schema import WalletCreate, DepositRequest, WithdrawRequest
from app.services.wallet_service import (
    create_wallet,
    deposit_money,
    withdraw_money,
    get_wallet,
    get_transactions
)

router = APIRouter(prefix="/wallet", tags=["Wallet"])


@router.post("/create")
async def create_user_wallet(
    data: WalletCreate,
    user=Depends(get_current_user)
):
    wallet = await create_wallet(user["email"], data.currency)
    return wallet


@router.get("/balance")
async def wallet_balance(user=Depends(get_current_user)):
    wallet = await get_wallet(user["email"])
    return wallet


@router.post("/deposit")
async def deposit(
    data: DepositRequest,
    user=Depends(get_current_user)
):
    await deposit_money(user["email"], data.amount)
    return {"message": "Deposit successful"}


@router.post("/withdraw")
async def withdraw(
    data: WithdrawRequest,
    user=Depends(get_current_user)
):
    try:
        await withdraw_money(user["email"], data.amount)
        return {"message": "Withdraw successful"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/transactions")
async def transactions(user=Depends(get_current_user)):
    txns = await get_transactions(user["email"])
    return txns
