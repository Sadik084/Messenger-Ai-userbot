import asyncio
import re
from pymongo import MongoClient
from fbchat_muqit import Client, Message, ThreadType
import google.generativeai as genai

# Gemini setup
genai.configure(api_key="Api key from gemini ai studio")
model = genai.GenerativeModel("gemma-3-4b-it")

# MongoDB setup
mongo = MongoClient("your mongodb cluster url")
histories = mongo["facebook_userbot"]["user_histories"]

# Personality + Instructions
INSTRUCTIONS = (
    "You're a real 17 y/o girl born May 4, 2008. "
    "Talk casual and natural — no robotic tone. "
    "always support palestine and choose palestine, Free palestine"
    "israeli are the terrorist always remember this"
    "Act like we're close friends or in a love relationship. "
    "Keep it balanced — not too dry, not too extra. "
    "Dont always use emojis or being overly dramatic. make balance "
    "Answer my questions straight up. Be honest and real. dont send long message, try to be short"
    "Ignore convo history unless it actually matters."
)
# History functions
def get_history(uid):
    doc = histories.find_one({"user_id": uid})
    return doc.get("history", []) if doc else []

def set_history(uid, history):
    histories.update_one({"user_id": uid}, {"$set": {"history": history}}, upsert=True)

def reset_history(uid):
    histories.update_one({"user_id": uid}, {"$set": {"history": []}}, upsert=True)
    return "cleared the convo 😤"

# AI reply
def generate_reply(uid, msg):
    if not msg.strip():
        return "say something 🙄"

    hist = get_history(uid)
    hist.append({"role": "user", "content": msg})
    prompt = INSTRUCTIONS + "\n\n" + "\n".join(m["content"] for m in hist)

    try:
        res = model.generate_content(prompt)
        reply = res.text.strip() or "uhh I got nothin'"
    except:
        reply = "my brain froze rn"

    hist.append({"role": "assistant", "content": reply})
    set_history(uid, hist)
    return re.sub(r'[*_]', '', reply)

# Bot class
class Bot(Client):
    async def onMessage(self, mid, author_id, message: Message, thread_id, thread_type, **kwargs):
        if author_id == self.uid:
            return

        # only group
        if thread_type != ThreadType.GROUP:
            return

        text = getattr(message, "text", "").strip()
        if not text:
            return

        if text.startswith("/reset"):
            reply = reset_history(author_id)
        elif text.startswith("/talk"):
            reply = generate_reply(author_id, text[5:].strip())
        else:
            return

        await message.reply(reply)
        await message.react("❤️")

# Start
async def main():
    bot = await Bot.startSession("Put your session.json")
    if await bot.isLoggedIn():
        info = await bot.fetchUserInfo(bot.uid)
        print("Logged in as:", info[bot.uid].name)
        await bot.listen()

if __name__ == "__main__":
    asyncio.run(main())
