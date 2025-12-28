import os
from dotenv import load_dotenv


# Load environment variables from .env if present
load_dotenv()

# --- Telegram ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_PUBLIC_CHAT_ID = os.getenv("TELEGRAM_PUBLIC_CHAT_ID", "@YurikTrader")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

# --- Facebook ---
FB_PAGE_ID = os.getenv("FB_PAGE_ID")
FB_PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")

# --- Instagram ---
IG_USER_ID = os.getenv(
    "IG_USER_ID"
)  # Instagram Business/Creator user ID (not username)
IG_ACCESS_TOKEN = os.getenv("IG_ACCESS_TOKEN")  # Long-lived IG token

# --- YouTube ---
YOUTUBE_CHANNEL_ID = os.getenv(
    "YOUTUBE_CHANNEL_ID"
)  # Optional, if you want dynamic feeds

# You can also hard-code a feed URL instead:
YOUTUBE_FEED_URL = os.getenv(
    "YOUTUBE_FEED_URL",
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCN0DC6fbpIG2Gz95UVgG6jw",
)

# --- Bot behavior ---
CHECK_INTERVAL_SECONDS = int(os.getenv("CHECK_INTERVAL_SECONDS", "1800"))  # 30 minutes
HEARTBEAT_INTERVAL_HOURS = int(os.getenv("HEARTBEAT_INTERVAL_HOURS", "24"))
LOG_FILE = os.getenv("LOG_FILE", "bot.log")
LOG_RETENTION_DAYS = int(os.getenv("LOG_RETENTION_DAYS", "7"))

# --- Files ---
LAST_VIDEO_FILE = os.getenv("LAST_VIDEO_FILE", "last_video.json")
LAST_HEARTBEAT_FILE = os.getenv("LAST_HEARTBEAT_FILE", "last_heartbeat.txt")
