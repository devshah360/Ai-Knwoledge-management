from app.models.chat_model import ChatHistory


chat_memory = []

def save_message(role,content):
        chat_memory.append({"role":role,"content":content})

def get_memory():
        return chat_memory[-10:]

def get_recent_memory(db,user_id,limit=5):
        chats = (db.query(ChatHistory).filter(ChatHistory.user_id == user_id).order_by(ChatHistory.id.desc()).limit(limit).all())

        return chats

def memory_to_text(chats):
        memory = ""

        for chat in chats:

                memory += (
                        f"User : {chat.question}\n"
                )

                memory += (
                        f"Assitant : {chat.answer}\n\n"
                )

        return memory
