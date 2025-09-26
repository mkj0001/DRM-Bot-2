import os
import asyncio
import logging
import time
import tgcrypto
from pyrogram import Client as AFK, idle, errors
from pyromod import listen
from tglogging import TelegramLogHandler

# -------- helpers ----------
def parse_id_list(env_name: str, default: str):
    s = os.environ.get(env_name, default or "")
    if not s:
        return []
    parts = [p.strip() for p in s.split(',') if p.strip()]
    ids = []
    for p in parts:
        try:
            ids.append(int(p))
        except ValueError:
            logging.warning("Invalid id in %s: %r (skipping)", env_name, p)
    return ids

def parse_single_id(env_name: str, default: str):
    v = os.environ.get(env_name, default)
    if not v:
        return None
    try:
        return int(v)
    except Exception:
        logging.warning("Invalid single id for %s: %r", env_name, v)
        return None

# -------- Config ----------
class Config(object):
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    API_ID = int(os.environ.get("API_ID", "0") or 0)
    API_HASH = os.environ.get("API_HASH", "")
    DOWNLOAD_LOCATION = os.environ.get("DOWNLOAD_LOCATION", "./DOWNLOADS")
    SESSIONS = os.environ.get("SESSIONS", "./SESSIONS")

    AUTH_USERS = parse_id_list('AUTH_USERS', '7959404410')
    GROUPS = parse_id_list('GROUPS', '-1002806996269')

    LOG_CH = parse_single_id("LOG_CH", "-1003166167318")

# -------- Logging ----------
# try to use TelegramLogHandler but don't crash if it fails
handlers = [logging.StreamHandler()]
try:
    if Config.BOT_TOKEN and Config.LOG_CH:
        handlers.insert(0, TelegramLogHandler(
            token=Config.BOT_TOKEN,
            log_chat_id=Config.LOG_CH,
            update_interval=2,
            minimum_lines=1,
            pending_logs=200000
        ))
except Exception as e:
    print("TelegramLogHandler init failed:", e)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=handlers
)

LOGGER = logging.getLogger(name)
LOGGER.info("Logger initialized.")

# -------- Client plugins ----------
plugins = dict(root="plugins")


# -------- Core run logic ----------
async def run_bot_once():
    # ensure folders exist
    os.makedirs(Config.DOWNLOAD_LOCATION, exist_ok=True)
    os.makedirs(Config.SESSIONS, exist_ok=True)

    # Build recipients list (groups first then auth users)
    recipients = []
    recipients.extend(Config.GROUPS)
    recipients.extend(Config.AUTH_USERS)

    # Create client
    PRO = AFK(
        "AFK-DL",
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        bot_token=Config.BOT_TOKEN,
        plugins=plugins,
        workdir=f"{Config.SESSIONS}/",
        workers=2,
    )

    try:
        await PRO.start()
        me = await PRO.get_me()
        LOGGER.info(f"<--- @{getattr(me, 'username', 'bot')} Started --->")

        # send startup messages with flood handling
        for cid in recipients:
            try:
                await PRO.send_message(chat_id=cid, text="✅ Bot Started! ♾ /pro")
                await asyncio.sleep(0.5)  # gentle delay to reduce flooding
            except errors.FloodWait as e:
                # many pyrogram versions store wait in e.value or e.x
                wait = getattr(e, "value", None) or getattr(e, "x", None) or getattr(e, "wait", None)
                wait = int(wait) if wait else 5
                LOGGER.warning(f"FloodWait caught. Sleeping for {wait} seconds...")
                await asyncio.sleep(wait)
            except errors.MessageNotModified:
                LOGGER.debug("Message not modified. Skipping update.")
            except Exception as exc:
                LOGGER.exception("Failed to send startup message to %s: %s", cid, exc)

        # Idle until stopped
        await idle()

    finally:
        try:
            await PRO.stop()
        except Exception as e:
            LOGGER.exception("Error while stopping client: %s", e)
        LOGGER.info("Client stopped.")
        async def main_loop():
    # continuous restart loop
    while True:
        try:
            LOGGER.info("Starting bot instance...")
            await run_bot_once()
        except Exception as e:
            LOGGER.exception("Unhandled exception in run_bot_once(): %s", e)
        LOGGER.info("Bot will restart in 2 seconds...")
        await asyncio.sleep(2)


if name == "main":
    # sanity checks for required config
    if not Config.BOT_TOKEN:
        LOGGER.error("BOT_TOKEN is empty. Set BOT_TOKEN environment variable.")
        raise SystemExit(1)
    if not Config.API_ID or not Config.API_HASH:
        LOGGER.error("API_ID/API_HASH missing. Set API_ID and API_HASH environment variables.")
        raise SystemExit(1)

    asyncio.run(main_loop())
