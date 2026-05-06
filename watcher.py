from telethon import TelegramClient, events
import re

# === YOUR CREDENTIALS ===
api_id = 33087118
api_hash = "30849ab507d1216cd299e714d23757cf"

# Your Telegram user ID (you'll receive alerts here)
ADMIN_ID = 795990315  

# Keywords to monitor
KEYWORDS = ["crypto", "airdrop", "spam", "http"]

client = TelegramClient("watcher_session", api_id, api_hash)


# 🚨 Alert function
async def send_alert(message):
    await client.send_message(ADMIN_ID, message)


# 👀 Watch all incoming messages
@client.on(events.NewMessage)
async def handler(event):
    text = event.raw_text.lower()

    sender = await event.get_sender()
    username = sender.username if sender.username else "No username"
    name = f"{sender.first_name or ''} {sender.last_name or ''}"

    # 🔔 1. Detect join messages (if visible)
    if "joined the group" in text or "joined" in text:
        await send_alert(
            f"👤 Possible Join Detected\nName: {name}\nUsername: @{username}"
        )

    # ⚠️ 2. Keyword detection
    if any(word in text for word in KEYWORDS):
        await send_alert(
            f"⚠️ Keyword Detected\nUser: @{username}\nMessage: {event.raw_text}"
        )

    # 🔗 3. Link detection
    if re.search(r"http[s]?://", text):
        await send_alert(
            f"🔗 Link Posted\nUser: @{username}\nMessage: {event.raw_text}"
        )


print("👀 Userbot watcher is running...")
client.start()
client.run_until_disconnected()