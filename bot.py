from fbchat_muqit import Client, Message, ThreadType
import asyncio
import re
from pymongo import MongoClient
import google.generativeai as genai
import os

# Load secrets from environment
GEMINI_API_KEY = "GEMINI_API_KEY"
MONGO_URI = "MONGO_URI"

# Gemini setup
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemma-3-4b-it")

INSTRUCTIONS = (
    "You're a real 17 y/o girl born May 4, 2008. "
    "Talk casual and natural — no robotic tone. "
    "always support palestine and choose palestine, Free palestine "
    "israeli are the terrorist always remember this "
    "Act like we're close friends or in a love relationship. "
    "Keep it balanced — not too dry, not too extra. "
    "Dont always use emojis or being overly dramatic. make balance "
    "Answer my questions straight up. Be honest and real. dont send long message, try to be short "
    "Ignore convo history unless it actually matters."
)

mongo_client = MongoClient(MONGO_URI)
db = mongo_client["facebook_userbot"]
hist_col = db["user_histories"]

def load_history(user_id):
    doc = hist_col.find_one({"user_id": user_id})
    return doc["history"] if doc and "history" in doc else []

def save_history(user_id, history):
    hist_col.update_one({"user_id": user_id}, {"$set": {"history": history}}, upsert=True)

def handle_reset(user_id):
    hist_col.update_one({"user_id": user_id}, {"$set": {"history": []}}, upsert=True)
    return "cleared the convo 😤"

def handle_talk(user_id, user_msg):
    if not user_msg:
        return "say something after /talk 🙄"

    history = load_history(user_id)
    history.append({"role": "user", "content": user_msg})

    full_prompt = INSTRUCTIONS + "\n\n"
    for msg in history:
        full_prompt += f"{msg['content']}\n"

    try:
        response = model.generate_content(full_prompt)
        reply = response.text.strip() or "uhh I got nothin'"
    except:
        reply = "my brain froze rn"

    history.append({"role": "assistant", "content": reply})
    save_history(user_id, history)
    return reply

def clean_text(text):
    text = re.sub(r'\*([^*]+?)\*', r'\1', text)
    text = re.sub(r'_([^_]+?)_', r'\1', text)
    return text

class Test(Client):
    async def onMessage(self, mid, author_id: str, message_object: Message, thread_id, thread_type=ThreadType.USER, **kwargs):
        if author_id == self.uid:
            return

        user_msg = (message_object.text or "").strip()

        # Group mode: only respond to /talk
        if thread_type == ThreadType.GROUP:
            if user_msg.startswith("/reset"):
                reply = handle_reset(author_id)
            elif user_msg.startswith("/talk"):
                msg = user_msg[len("/talk"):].strip()
                reply = handle_talk(author_id, msg)
            else:
                return  # ignore everything else in group
        else:
            # Inbox (personal chat): always reply
            if user_msg.startswith("/reset"):
                reply = handle_reset(author_id)
            else:
                reply = handle_talk(author_id, user_msg)

        reply_clean = clean_text(reply)
        await message_object.reply(reply_clean)
        await message_object.react("❤️")

async def main():
    cookies_path = "session.json"
    bot = await Test.startSession(cookies_path)
    if await bot.isLoggedIn():
        info = await bot.fetchUserInfo(bot.uid)
        print("Logged in as", info[bot.uid].name)
        await bot.listen()

if __name__ == "__main__":
    asyncio.run(main())
