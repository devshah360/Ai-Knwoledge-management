from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["knowledge-management"]
chat_collection = db["chat_memory"]


def save_chat_memory(user_id, question, answer):
    chat_collection.insert_one({
        "user_id": user_id,
        "question": question,
        "answer": answer
    })


def get_chat_memory(user_id, limit=5):
    return list(
        chat_collection.find(
            {"user_id": user_id}
        ).sort("_id", -1).limit(limit)
    )


def build_memory_context(chats):
    context = ""

    for chat in chats:
        context += f"User: {chat['question']}\n"
        context += f"Assistant: {chat['answer']}\n\n"

    return context