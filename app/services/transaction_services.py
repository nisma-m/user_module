from app.config.database import db
from datetime import datetime

txn_collection = db.transactions


async def create_transaction(user_id, currency, amount, txn_type):

    txn = {
        "user_id": user_id,
        "currency": currency,
        "amount": amount,
        "txn_type": txn_type,
        "created_at": datetime.utcnow()
    }

    await txn_collection.insert_one(txn)
