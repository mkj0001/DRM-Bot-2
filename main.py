import os
import asyncio
import logging
from pyrogram import Client as ARK
from pyrogram.errors import BadRequest, FloodWait

# ====== CONFIGURATION ======
class Config(object):
    # 👉 यहां अपने असली credentials भरें:
    BOT_TOKEN = "8496276598:AAFzxd8pBJcpEAWvR0Itow8p_xYBi2iZwDw"  # <-- आपका बॉट टोकन
    API_ID = 17640565                                    # <-- आपका API_ID (इंटीजर)
    API_HASH = "ff67816c19a48aff1f86204ff61ce786"         # <-- आपका API_HASH (स्ट्रिंग)
    DOWNLOAD_LOCATION = "./DOWNLOADS"
    SESSION = ".SESSION"  # session file path
    # 👉 अपने User IDs / Group IDs भरें (comma separated):
    AUTH_USERS = ["7959404410", "7959404410"]  # <-- User IDs
    GROUPS = ["-1002806996269"]              # <-- Group IDs

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(name)

# ====== CLIENT ======
PRO = ARK(
    Config.SESSION,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    workers=4
)

# ====== CHAT IDS (users + groups) ======
chat_ids = []
for g in Config.GROUPS:
    try:
        chat_ids.append(int(g))
    except Exception:
        pass

for u in Config.AUTH_USERS:
    try:
        chat_ids.append(int(u))
    except Exception:
        pass

# ====== SAFE SEND FUNCTION ======
async def safe_send_message(chat_id, text):
    try:
        await PRO.send_message(chat_id, text)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        try:
            await PRO.send_message(chat_id, text)
        except Exception as e2:
            LOGGER.warning(f"Retry failed in chat {chat_id}: {e2}")
    except BadRequest as e:
        LOGGER.warning(f"BadRequest in chat {chat_id}: {e}")
    except Exception as e:
        LOGGER.warning(f"Message send failed in chat {chat_id}: {e}")

# ====== MAIN ======
async def main():
    await PRO.start()
    bot_info = await PRO.get_me()
    LOGGER.info(f"Bot @{bot_info.username} started ✅")

    # startup message to all chats
    for cid in chat_ids:
        asyncio.create_task(safe_send_message(cid, f"Bot @{bot_info.username} started ✅"))

    # Keep alive loop so pingtask/nettask not stopped
    while True:
        await asyncio.sleep(60)

if name == "main":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        LOGGER.info("Bot stopped by user")
    except Exception as e:
        LOGGER.error(f"Bot crashed: {e}")
