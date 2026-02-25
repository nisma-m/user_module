from app.config.database import db
from app.services.transaction_services import create_transaction

wallet_collection = db.wallets


# -------------------------
# Create Wallet
# -------------------------
async def create_wallet(user_id, currency, wallet_type):

    existing_wallet = await wallet_collection.find_one({
        "user_id": user_id,
        "currency": currency
    })

    if existing_wallet:
        raise Exception("Wallet already exists")

    wallet = {
        "user_id": user_id,
        "currency": currency,
        "wallet_type": wallet_type,
        "balance": 0.0,
        "locked_balance": 0.0
    }

    result = await wallet_collection.insert_one(wallet)
    wallet["_id"] = str(result.inserted_id)

    return wallet

# -------------------------
# Get Wallet
# -------------------------
async def get_wallet(user_id, currency):

    wallet = await wallet_collection.find_one({
        "user_id": user_id,
        "currency": currency
    })

    if not wallet:
        raise Exception("Wallet not found")

    return wallet


# -------------------------
# Credit Wallet
# -------------------------
async def credit_wallet(user_id, currency, amount):

    wallet = await get_wallet(user_id, currency)  # ensure exists

    await wallet_collection.update_one(
        {"user_id": user_id, "currency": currency},
        {"$inc": {"balance": amount}}
    )

    await create_transaction(user_id, currency, amount, "credit")

# -------------------------
# Debit Wallet
# -------------------------
async def debit_wallet(user_id, currency, amount):

    wallet = await get_wallet(user_id, currency)

    if wallet["balance"] < amount:
        raise Exception("Insufficient balance")

    await wallet_collection.update_one(
        {"user_id": user_id, "currency": currency},
        {"$inc": {"balance": -amount}}
    )

    # Transaction log
    await create_transaction(user_id, currency, amount, "debit")


# -------------------------
# Lock Balance
# -------------------------
async def lock_balance(user_id, currency, amount):

    wallet = await get_wallet(user_id, currency)

    if wallet["balance"] < amount:
        raise Exception("Insufficient balance")

    await wallet_collection.update_one(
        {"user_id": user_id, "currency": currency},
        {
            "$inc": {
                "balance": -amount,
                "locked_balance": amount
            }
        }
    )

    await create_transaction(user_id, currency, amount, "lock")


# -------------------------
# Unlock Balance
# -------------------------
async def unlock_balance(user_id, currency, amount):

    wallet = await get_wallet(user_id, currency)

    if wallet["locked_balance"] < amount:
        raise Exception("Insufficient locked balance")

    await wallet_collection.update_one(
        {"user_id": user_id, "currency": currency},
        {
            "$inc": {
                "balance": amount,
                "locked_balance": -amount
            }
        }
    )

    await create_transaction(user_id, currency, amount, "unlock")

from app.config.database import db

txn_collection = db.transactions

# -------------------------
# Get Transactions
# -------------------------
async def get_transactions(user_id, currency):
    transactions = await txn_collection.find({
        "user_id": user_id,
        "currency": currency
    }).to_list(length=100)

    return transactions