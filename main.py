import os
import asyncio
import logging
import tgcrypto
from pyrogram import Client as AFK, idle, errors
from pyrogram.enums import ChatMemberStatus, ChatMembersFilter
from pyrogram import enums
from pyrogram.types import ChatMember
from pyromod import listen
from tglogging import TelegramLogHandler

# Config
class Config(object):
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "8496276598:AAFzxd8pBJcpEAWvR0Itow8p_xYBi2iZwDw")
    API_ID = int(os.environ.get("API_ID", "17640565"))
    API_HASH = os.environ.get("API_HASH", "ff67816c19a48aff1f86204ff61ce786")
    DOWNLOAD_LOCATION = "./DOWNLOADS"
    SESSIONS = "./SESSIONS"

    AUTH_USERS = [int(x) for x in os.environ.get('AUTH_USERS', '7959404410').split(',')]
    GROUPS = [int(x) for x in os.environ.get('GROUPS', '-1002806996269').split(',')]
    LOG_CH = os.environ.get("LOG_CH", "-1003166167318")

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        TelegramLogHandler(
            token=Config.BOT_TOKEN,
            log_chat_id=Config.LOG_CH,
            update_interval=2,
            minimum_lines=1,
            pending_logs=200000),
        logging.StreamHandler()
    ]
)
LOGGER = logging.getLogger(name)
LOGGER.info("live log streaming to telegram.")

# Client
plugins = dict(root="plugins")

async def start_bot():
    if not os.path.isdir(Config.DOWNLOAD_LOCATION):
        os.makedirs(Config.DOWNLOAD_LOCATION)
    if not os.path.isdir(Config.SESSIONS):
        os.makedirs(Config.SESSIONS)

    PRO = AFK(
        "AFK-DL",
        bot_token=Config.BOT_TOKEN,
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        sleep_threshold=120,
        plugins=plugins,
        workdir=f"{Config.SESSIONS}/",
        workers=2,
    )

    chat_id = Config.GROUPS + Config.AUTH_USERS

    try:
        await PRO.start()
        bot_info = await PRO.get_me()
        LOGGER.info(f"<--- @{bot_info.username} Started --->")

        for i in chat_id:
            try:
                await PRO.send_message(chat_id=i, text="✅ Bot Started! ♾ /pro")
                await asyncio.sleep(0.5)  # to avoid flood
            except errors.FloodWait as e:
                LOGGER.warning(f"Flood wait for {e.value} seconds")
                await asyncio.sleep(e.value)
            except Exception as d:
                LOGGER.error(d)
                continue

        await idle()

    except Exception as e:
        LOGGER.error(f"Error in main: {e}")
    finally:
        await PRO.stop()
        LOGGER.info("Bot stopped")

# Auto-Restart loop
if name == "main":
    while True:
        asyncio.run(start_bot())
        LOGGER.info("Restarting bot in 2 seconds…")
        asyncio.sleep(2)
