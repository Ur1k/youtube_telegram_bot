import feedparser
import requests
import json
import os
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# === CONFIG ===
YOUTUBE_FEED = "https://www.youtube.com/feeds/videos.xml?channel_id=UCN0DC6fbpIG2Gz95UVgG6jw"
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = "@YurikTrader"

STATE_FILE = os.path.join(BASE_DIR, "last_video.json")


def get_last_saved_video_id():
    """Load last posted video ID from file."""
    if not os.path.exists(STATE_FILE):
        return None
    try:
        with open(STATE_FILE, "r") as f:
            data = json.load(f)
            return data.get("last_video_id")
    except:
        return None


def save_last_video_id(video_id):
    """Save last posted video ID to file."""
    with open(STATE_FILE, "w") as f:
        json.dump({"last_video_id": video_id}, f)


def send_to_telegram(title, link):
    """Send message to Telegram channel."""
    if not TELEGRAM_TOKEN:
        print("ERROR: TELEGRAM_TOKEN is not set in environment variables.")
        return

    message = f"🔥 New YouTube video!\n\n{title}\n{link}"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, data=payload)


def check_and_post_latest_video():
    """Check RSS feed and post only if new video exists."""
    feed = feedparser.parse(YOUTUBE_FEED)

    if not feed.entries:
        print("Feed is empty or failed to load.")
        return

    latest = feed.entries[0]

    video_id = latest.yt_videoid
    title = latest.title
    link = latest.link

    last_saved = get_last_saved_video_id()

    if video_id != last_saved:
        print(f"New video detected: {title}")
        send_to_telegram(title, link)
        save_last_video_id(video_id)
    else:
        print("No new videos. Nothing to post.")


if __name__ == "__main__":
    while True:
        check_and_post_latest_video()
        time.sleep(1800)  # 1800 seconds = 30 minutes