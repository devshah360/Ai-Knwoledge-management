from fastapi import APIRouter, HTTPException
from bson import ObjectId

from app.services.mongo_service import chat_collection

router = APIRouter(
    prefix="/chat/history",
    tags=["History"]
)


@router.get("/")
def history():

    chats = list(

        chat_collection

        .find()

        .sort("created_at", -1)

    )

    return [

        {

            "id": str(chat["_id"]),

            "title": chat["title"],

            "created_at": chat["created_at"]

        }

        for chat in chats

    ]


@router.get("/{chat_id}")
def get_chat(chat_id: str):

    chat = chat_collection.find_one(

        {

            "_id": ObjectId(chat_id)

        }

    )

    if not chat:

        raise HTTPException(

            status_code=404,

            detail="Chat not found"

        )

    return {

        "_id": str(chat["_id"]),

        "title": chat["title"],

        "messages": chat["messages"],

        "created_at": chat["created_at"]

    }


@router.delete("/{chat_id}")

def delete_chat(chat_id: str):

    result = chat_collection.delete_one(

        {

            "_id": ObjectId(chat_id)

        }

    )

    if result.deleted_count == 0:

        raise HTTPException(

            status_code=404,

            detail="Chat not found"

        )

    return {

        "message": "Chat deleted successfully"

    }