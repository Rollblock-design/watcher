import os
import threading
from flask import Flask
from telethon import TelegramClient, events

# === TELEGRAM CONFIG ===
api_id = 33087118
api_hash = "30849ab507d1216cd299e714d23757cf"

ADMIN_ID = 795990315  

KEYWORDS = ["crypto", "airdrop", "spam"]

client = TelegramClient("watcher_session", api_id, api_hash)

# === WATCHER LOGIC ===
async def send_alert(message):
    await client.send_message(ADMIN_ID, message)

@client.on(events.NewMessage)
async def handler(event):
    if event.is_private:
        return

    text = event.raw_text.lower()

    sender = await event.get_sender()
    username = sender.username if sender and sender.username else "No username"

    # 👤 Join detection (groups only, limited)
    if not event.is_channel:
        if "joined the group" in text or "joined" in text:
            await send_alert(
                f"👤 Join Detected\nUser: @{username}\nChat: {event.chat.title}"
            )

    # ⚠️ Keyword detection
    if any(word in text for word in KEYWORDS):
        await send_alert(
            f"⚠️ Keyword Alert\nChat: {event.chat.title}\nUser: @{username}\nMessage: {event.raw_text}"
        )

def start_telegram():
    client.start()
    print("👀 Watcher running...")
    client.run_until_disconnected()

# === FLASK SERVER (FOR RENDER) ===
app = Flask(__name__)

@app.route("/")
def home():
    return "Watcher is running!"

if __name__ == "__main__":
    # Run Telegram in background thread
    t = threading.Thread(target=start_telegram)
    t.start()

    # Run web server (required by Render)
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
