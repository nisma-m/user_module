from fastapi import APIRouter, HTTPException, Depends

from app.services import wallet_service as services
from app.schemas import wallet_schema as schemas
from app.dependencies.auth_dependency import get_current_user


router = APIRouter(
    prefix="/wallet",
    tags=["Wallet Management"]
)


# -------------------------
# Create Wallet
# -------------------------
@router.post("/create", response_model=schemas.WalletResponse)
async def create_wallet(
    data: schemas.WalletCreate,
    user: dict = Depends(get_current_user)
):
    try:
        wallet = await services.create_wallet(
            user_id=user["user_id"],
            currency=data.currency,
            wallet_type=data.wallet_type
        )
        return wallet

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# -------------------------
# Get Wallet Details
# -------------------------
@router.get("/{currency}", response_model=schemas.WalletResponse)
async def get_wallet(
    currency: str,
    user: dict = Depends(get_current_user)
):
    wallet = await services.get_wallet(user["user_id"], currency)

    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")

    wallet["_id"] = str(wallet["_id"])
    return wallet


# -------------------------
# Credit Wallet
# -------------------------
@router.post("/credit/{currency}")
async def credit_wallet(
    currency: str,
    data: schemas.AmountRequest,
    user: dict = Depends(get_current_user)
):
    try:
        await services.credit_wallet(
            user["user_id"],
            currency,
            data.amount
        )
        return {"message": "Wallet credited successfully"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# -------------------------
# Debit Wallet
# -------------------------
@router.post("/debit/{currency}")
async def debit_wallet(
    currency: str,
    data: schemas.AmountRequest,
    user: dict = Depends(get_current_user)
):
    try:
        await services.debit_wallet(
            user["user_id"],
            currency,
            data.amount
        )
        return {"message": "Wallet debited successfully"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# -------------------------
# Lock Balance
# -------------------------
@router.post("/lock/{currency}")
async def lock_wallet(
    currency: str,
    data: schemas.AmountRequest,
    user: dict = Depends(get_current_user)
):
    try:
        await services.lock_balance(
            user["user_id"],
            currency,
            data.amount
        )
        return {"message": "Amount locked successfully"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# -------------------------
# Unlock Balance
# -------------------------
@router.post("/unlock/{currency}")
async def unlock_wallet(
    currency: str,
    data: schemas.AmountRequest,
    user: dict = Depends(get_current_user)
):
    try:
        await services.unlock_balance(
            user["user_id"],
            currency,
            data.amount
        )
        return {"message": "Amount unlocked successfully"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# -------------------------
# Transaction History
# -------------------------
@router.get("/transactions/{currency}")
async def get_transactions(
    currency: str,
    user: dict = Depends(get_current_user)
):
    try:
        transactions = await services.get_transactions(
            user["user_id"],
            currency
        )

        for txn in transactions:
            txn["_id"] = str(txn["_id"])

        return transactions

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
