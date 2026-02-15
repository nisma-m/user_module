from app.config.database import db
from datetime import datetime


async def create_wallet(user_email, currency="INR"):
    wallet = await db.wallets.find_one({"user_email": user_email})

    if wallet:
        return wallet

    new_wallet = {
        "user_email": user_email,
        "currency": currency,
        "balance": 0.0,
        "created_at": datetime.utcnow()
    }

    await db.wallets.insert_one(new_wallet)
    return new_wallet


async def deposit_money(user_email, amount):
    await db.wallets.update_one(
        {"user_email": user_email},
        {"$inc": {"balance": amount}}
    )

    await db.transactions.insert_one({
        "user_email": user_email,
        "amount": amount,
        "type": "deposit",
        "currency": "INR",
        "created_at": datetime.utcnow()
    })


async def withdraw_money(user_email, amount):
    wallet = await db.wallets.find_one({"user_email": user_email})

    if wallet["balance"] < amount:
        raise Exception("Insufficient balance")

    await db.wallets.update_one(
        {"user_email": user_email},
        {"$inc": {"balance": -amount}}
    )

    await db.transactions.insert_one({
        "user_email": user_email,
        "amount": amount,
        "type": "withdraw",
        "currency": "INR",
        "created_at": datetime.utcnow()
    })


async def get_wallet(user_email):
    return await db.wallets.find_one({"user_email": user_email})


async def get_transactions(user_email):
    transactions = db.transactions.find({"user_email": user_email})
    return await transactions.to_list(100)
