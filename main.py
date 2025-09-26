import os
import asyncio
import logging
from pyrogram import Client, idle, errors
from tglogging import TelegramLogHandler

# ---------------- Config ----------------
class Config(object):
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "8496276598:AAFzxd8pBJcpEAWvR0Itow8p_xYBi2iZwDw")
    API_ID = int(os.environ.get("API_ID", "17640565"))
    API_HASH = os.environ.get("API_HASH", "ff67816c19a48aff1f86204ff61ce786")

    DOWNLOAD_LOCATION = "./DOWNLOADS"
    SESSIONS = "./SESSIONS"

    # SESSION_STRING env में है तो उसी का यूज़ करेंगे
    SESSION_STRING = os.environ.get("SESSION_STRING", None)

    AUTH_USERS = list(map(int, os.environ.get('AUTH_USERS', '7959404410').split(',')))
    GROUPS = list(map(int, os.environ.get('GROUPS', '-1002806996269').split(',')))
    LOG_CH = os.environ.get("LOG_CH", "-1003166167318")

# ---------------- Logger ----------------
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
            pending_logs=200000
        ),
        logging.StreamHandler()
    ]
)
LOGGER = logging.getLogger(name)
LOGGER.info("live log streaming to telegram.")

# ---------------- Client (Session Safe) ----------------
if Config.SESSION_STRING:
    PRO = Client(
        session_name=Config.SESSION_STRING,  # env session
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        bot_token=Config.BOT_TOKEN,
        sleep_threshold=120,
        workdir=Config.SESSIONS,
        workers=4,
    )
else:
    PRO = Client(
        "AFK-DL",
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        bot_token=Config.BOT_TOKEN,
        sleep_threshold=120,
        workdir=Config.SESSIONS,
        workers=4,
    )

chat_id_list = Config.GROUPS + Config.AUTH_USERS

# ---------------- Main Async ----------------
async def main():
    if not os.path.isdir(Config.DOWNLOAD_LOCATION):
        os.makedirs(Config.DOWNLOAD_LOCATION)
    if not os.path.isdir(Config.SESSIONS):
        os.makedirs(Config.SESSIONS)

    await PRO.start()
    bot_info = await PRO.get_me()
    LOGGER.info(f"<--- @{bot_info.username} Started --->")

    # Broadcast to groups/users with floodwait handle
    for cid in chat_id_list:
        try:
            await PRO.send_message(chat_id=cid, text="Bot Started! ♾ /pro")
        except errors.FloodWait as fw:
            LOGGER.warning(f"FloodWait {fw.value} sec for {cid}, sleeping...")
            await asyncio.sleep(fw.value)
            try:
                await PRO.send_message(chat_id=cid, text="Bot Started! ♾ /pro")
            except Exception as e:
                LOGGER.warning(f"After FloodWait still failed {cid}: {e}")
        except Exception as e:
            LOGGER.warning(f"Failed to send start msg to {cid}: {e}")
            continue

    # Run forever (PingTask/NetTask never stops)
    while True:
        try:
            await idle()
        except Exception as e:
            LOGGER.error(f"Idle loop error: {e}")
            await asyncio.sleep(5)

# ---------------- Auto Restart Wrapper ----------------
if name == "main":
    async def runner():
        while True:
            try:
                await main()
            except Exception as e:
                LOGGER.error(f"Main loop crashed: {e}")
                LOGGER.info("Restarting bot in 5 seconds...")
                await asyncio.sleep(5)  # restart delay

    asyncio.get_event_loop().run_until_complete(runner())
    LOGGER.info("<---Bot Stopped--->")
