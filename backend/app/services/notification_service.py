from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017")

db = client["knowledge-management"]

notification_collection = db["notifications"]


def create_notification(
    message: str,
    notification_type: str = "info"
):
    notification = {
        "message": message,
        "type": notification_type,
        "read": False,
        "timestamp": datetime.utcnow()
    }

    notification_collection.insert_one(
        notification
    )

    return notification


def get_notifications():
    notifications = list(
        notification_collection
        .find()
        .sort("timestamp", -1)
        .limit(100)
    )

    for item in notifications:
        item["id"] = str(item["_id"])
        del item["_id"]

    return notifications


def mark_as_read(notification_id):

    from bson import ObjectId

    notification_collection.update_one(
        {"_id": ObjectId(notification_id)},
        {"$set": {"read": True}}
    )

    return True