import logging
import time
import requests
import xml.etree.ElementTree as ET
from telegram_poster import send_admin_message


from config import (
    YOUTUBE_FEED_URL,
    CHECK_INTERVAL_SECONDS,
    HEARTBEAT_INTERVAL_HOURS,
    LOG_RETENTION_DAYS,
)
from utils import (
    setup_logging,
    load_last_video_id,
    save_last_video_id,
    should_send_heartbeat,
    mark_heartbeat_sent,
    cleanup_old_logs,
)
from notifier import notify_all
from telegram_poster import send_telegram_message


def fetch_latest_video(feed_url: str):
    """
    Return latest video info from YouTube RSS feed as dict:
    {
        "id": str,
        "title": str,
        "url": str,
        "thumbnail_url": str or None
    }
    """
    resp = requests.get(feed_url, timeout=15)
    resp.raise_for_status()

    root = ET.fromstring(resp.content)

    # YouTube RSS uses Atom namespace
    ns = {
        "atom": "http://www.w3.org/2005/Atom",
        "media": "http://search.yahoo.com/mrss/",
    }

    entry = root.find("atom:entry", ns)
    if entry is None:
        return None

    video_id = entry.findtext("atom:id", default="", namespaces=ns)
    title = entry.findtext("atom:title", default="", namespaces=ns)

    link_elem = entry.find("atom:link[@rel='alternate']", ns)
    if link_elem is not None:
        url = link_elem.attrib.get("href", "")
    else:
        url = ""

    # Try to get thumbnail from media:thumbnail
    thumb_elem = entry.find(".//media:thumbnail", ns)
    thumbnail_url = thumb_elem.attrib.get("url") if thumb_elem is not None else None

    # Normalize video ID (YouTube Atom id often looks like "...:video:VIDEOID")
    if ":" in video_id:
        video_id = video_id.split(":")[-1]

    return {
        "id": video_id,
        "title": title,
        "url": url,
        "thumbnail_url": thumbnail_url,
    }


def send_heartbeat_and_cleanup():
    send_admin_message("💡 Bot is alive and running normally.", silent=True)
    logging.info("Heartbeat sent.")
    mark_heartbeat_sent()
    cleanup_old_logs(".", days=LOG_RETENTION_DAYS)


def main():
    setup_logging()
    logging.info("Bot started.")

    last_video_id = load_last_video_id()

    while True:
        try:
            logging.info("Checking YouTube feed...")
            video = fetch_latest_video(YOUTUBE_FEED_URL)

            if video is None:
                logging.warning("No entries found in YouTube feed.")
            else:
                if last_video_id is None:
                    # First run: just record the latest video
                    last_video_id = video["id"]
                    save_last_video_id(last_video_id)
                    logging.info(f"Initialized last_video_id with: {last_video_id}")
                elif video["id"] != last_video_id:
                    logging.info(f"New video detected: {video['title']}")
                    last_video_id = video["id"]
                    save_last_video_id(last_video_id)
                    notify_all(video)
                else:
                    logging.info("No new videos.")

            # Heartbeat logic
            if should_send_heartbeat(hours=HEARTBEAT_INTERVAL_HOURS):
                send_heartbeat_and_cleanup()

        except Exception as e:
            logging.exception(f"Error in main loop: {e}")
            # Try to notify via Telegram (best-effort)
            try:
                send_admin_message(f"❌ Bot error:\n{e}")
            except Exception:
                pass

        time.sleep(CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
