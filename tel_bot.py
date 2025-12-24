import feedparser
import requests
import json
import os
import time
import logging
import traceback
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

YOUTUBE_FEED = (
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCN0DC6fbpIG2Gz95UVgG6jw"
)

# Token must come from environment
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Channel or chat where new videos are posted
TELEGRAM_CHAT_ID = "@YurikTrader"

# Admin chat for error notifications
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

STATE_FILE = os.path.join(BASE_DIR, "last_video.json")
LOG_FILE = os.path.join(BASE_DIR, "bot.log")
HEARTBEAT_FILE = os.path.join(BASE_DIR, "last_heartbeat.txt")

# === LOGGING WITH ROTATION ===
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Rotate log at 5 MB, keep 5 backups
file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=5)
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)
logger.addHandler(file_handler)

# Console output (useful for journalctl)
console_handler = logging.StreamHandler()
console_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)
logger.addHandler(console_handler)


def get_last_saved_video_id():
    if not os.path.exists(STATE_FILE):
        logging.info("State file not found, starting fresh.")
        return None
    try:
        with open(STATE_FILE, "r") as f:
            data = json.load(f)
            return data.get("last_video_id")
    except Exception as e:
        logging.warning("Failed to read state file: %s", e)
        return None


def save_last_video_id(video_id):
    try:
        with open(STATE_FILE, "w") as f:
            json.dump({"last_video_id": video_id}, f)
        logging.info("Saved last video ID: %s", video_id)
    except Exception as e:
        logging.error("Failed to write state file: %s", e)


def send_raw_telegram_message(chat_id, text, disable_notification=False):
    if not TELEGRAM_TOKEN:
        logging.error("TELEGRAM_TOKEN is not set.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}

    if disable_notification:
        payload["disable_notification"] = True

    for attempt in range(1, 4):
        try:
            response = requests.post(url, data=payload, timeout=10)
            if response.status_code == 200:
                logging.info("Message sent successfully.")
                return
            else:
                logging.warning(
                    "Telegram error %s: %s", response.status_code, response.text
                )
        except Exception as e:
            logging.warning("Network error: %s", e)

        time.sleep(3)

    logging.error("Failed to send message after retries.")


def notify_admin(error_message):
    text = f"⚠️ Bot error:\n{error_message}"
    send_raw_telegram_message(ADMIN_CHAT_ID, text, disable_notification=True)


def send_to_telegram(title, link):
    message = f"🔥 New YouTube video!\n\n{title}\n{link}"
    send_raw_telegram_message(TELEGRAM_CHAT_ID, message)


def send_heartbeat():
    """Send a daily 'bot is alive' message."""
    message = "💡 Bot is alive and running normally."
    send_raw_telegram_message(ADMIN_CHAT_ID, message, disable_notification=True)
    logging.info("Heartbeat sent.")

    with open(HEARTBEAT_FILE, "w") as f:
        f.write(str(time.time()))


def should_send_heartbeat():
    """Return True if 24 hours passed since last heartbeat."""
    if not os.path.exists(HEARTBEAT_FILE):
        return True

    try:
        with open(HEARTBEAT_FILE, "r") as f:
            last = float(f.read().strip())
    except:
        return True

    return (time.time() - last) >= 86400  # 24 hours


def check_and_post_latest_video():
    logging.info("Checking YouTube feed...")

    feed = feedparser.parse(YOUTUBE_FEED)

    if not feed.entries:
        logging.warning("Feed is empty or failed to load.")
        return

    latest = feed.entries[0]

    video_id = getattr(latest, "yt_videoid", None)
    title = getattr(latest, "title", None)
    link = getattr(latest, "link", None)

    if not video_id or not link:
        logging.warning("Invalid feed entry.")
        return

    last_saved = get_last_saved_video_id()

    if video_id != last_saved:
        logging.info("New video detected: %s", title)
        send_to_telegram(title, link)
        save_last_video_id(video_id)
    else:
        logging.info("No new videos.")


if __name__ == "__main__":
    logging.info("Bot started.")

    while True:
        try:
            check_and_post_latest_video()

            if should_send_heartbeat():
                send_heartbeat()

        except Exception as e:
            error_text = f"{type(e).__name__}: {e}\n\n{traceback.format_exc()}"
            logging.exception("Unhandled error.")
            notify_admin(error_text)

        time.sleep(1800)  # 30 minutes
