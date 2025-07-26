# 💬 Messenger-AI-Userbot

[![Stars](https://img.shields.io/github/stars/Sadik084/Messenger-Ai-userbot?style=social)](https://github.com/Sadik084/Messenger-Ai-userbot)

A **Facebook Messenger userbot** powered by **Gemini AI Studio API**, designed to chat naturally like a real human.

---

## ⚙️ Features

- 🧠 Gemini AI 3-4B brain (fast + smart)
- 📱 Facebook group message support
- 🧵 Custom `/talk` & `/reset` commands
- 💬 Memory-based conversation
- ❤️ Auto reply & react to your message

---

## 🛠 Requirements

Install dependencies using:

```bash
pip install -r requirements.txt
```

> Make sure you're using **Python 3.9+**

---

## 📂 Get Your `session.json` (Login Cookie)

To login as a Facebook user, you need a valid session from your own account.

### 🔐 How to generate `session.json`:

1. Install [C3C Fbstate Utility Extension](https://chromewebstore.google.com/detail/c3c-fbstate-utility/nlgehefndkobdignlfhapfpggielmdph)
2. Go to [facebook.com](https://facebook.com) and login to your account
3. Click the extension → click **"Get fbstate"**
4. A file will download — rename it to `session.json`
5. Move that file to your project folder

---

## 🚀 Run the Bot

Before running the bot, make sure to:

- 🔑 Get your **Gemini AI API key** from [Google AI Studio](https://makersuite.google.com/app/apikey)
- 🌐 Get your **MongoDB cluster URI** from [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- 🔐 Place your `session.json` in the root folder

Then run:

```bash
python bot.py
```

If everything works, it’ll show:

```bash
Logged in as: Your Name
```

---

## 💬 How to Use

| Command    | What it does                         |
| ---------- | ------------------------------------ |
| `/talk hi` | Start a conversation with the bot    |
| `/reset`   | Clear previous memory (forget convo) |

> ⚠️ Only replies if your message **starts with `/talk`**  
> 💬 Works **only in group chats** (not inbox)

---

## 🧪 Example Chat

**You:** `/talk what's your name?`  
**Bot:** I'm just your bestie for now 😏💅

---

## 📦 requirements.txt

```txt
fbchat-muqit  
google-generativeai  
pymongo
```

---

## 🤝 Special Thanks

* 🧠 `fbchat_muqit` for the Messenger API → [github.com/togashigreat/fbchat-muqit](https://github.com/togashigreat/fbchat-muqit)
* 🧪 Google Gemini AI for the LLM API
* 🔒 C3C FBSTATE Extension for login cookies

---

## 🕊️ Always Free Palestine 🇵🇸

## ⭐ Star this repo

If you like this project, give it a ⭐ on GitHub:  
[https://github.com/Sadik084/Messenger-Ai-userbot](https://github.com/Sadik084/Messenger-Ai-userbot)
