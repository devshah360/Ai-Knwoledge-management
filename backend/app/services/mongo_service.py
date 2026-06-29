from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime


client = MongoClient(

    "mongodb://localhost:27017"

)

db = client["knowledge-management"]

chat_collection = db["chat_memory"]


def create_conversation(

    title="New Chat"

):

    result = chat_collection.insert_one({

        "title": title,

        "messages": [],

        "created_at": datetime.utcnow()

    })

    return str(result.inserted_id)



def add_message(

    conversation_id,

    role,

    content

):

    chat_collection.update_one(

        {

            "_id":

            ObjectId(conversation_id)

        },

        {

            "$push": {

                "messages": {

                    "role": role,

                    "content": content,

                    "timestamp": datetime.utcnow()

                }

            }

        }

    )



def get_conversation(

    conversation_id

):

    chat = chat_collection.find_one(

        {

            "_id":

            ObjectId(conversation_id)

        }

    )

    if chat:

        chat["_id"] = str(chat["_id"])

    return chat