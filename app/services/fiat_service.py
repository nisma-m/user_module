from app.database import wallet_collection
from app.utils.serializer import serialize_doc
from app.services.notification_service import manager


async def create_wallet(user_id: str):
    existing = await wallet_collection.find_one({"user_id": user_id})

    if existing:
        raise Exception("Wallet already exists")

    wallet = {
        "user_id": user_id,
        "balance": 0.0
    }

    result = await wallet_collection.insert_one(wallet)
    wallet["_id"] = result.inserted_id

    return serialize_doc(wallet)


async def fiat_deposit(user_id: str, amount: float):
    wallet = await wallet_collection.find_one({"user_id": user_id})

    if not wallet:
        raise Exception("Wallet not found")

    new_balance = wallet["balance"] + amount

    await wallet_collection.update_one(
        {"user_id": user_id},
        {"$set": {"balance": new_balance}}
    )

    wallet["balance"] = new_balance

    # 🔥 Send WebSocket update
    await manager.send_message(user_id, {
        "type": "deposit",
        "balance": new_balance
    })

    return serialize_doc(wallet)


async def fiat_withdraw(user_id: str, amount: float):
    wallet = await wallet_collection.find_one({"user_id": user_id})

    if not wallet:
        raise Exception("Wallet not found")

    if wallet["balance"] < amount:
        raise Exception("Insufficient balance")

    new_balance = wallet["balance"] - amount

    await wallet_collection.update_one(
        {"user_id": user_id},
        {"$set": {"balance": new_balance}}
    )

    wallet["balance"] = new_balance

    # 🔥 Send WebSocket update
    await manager.send_message(user_id, {
        "type": "withdraw",
        "balance": new_balance
    })

    return serialize_doc(wallet)
