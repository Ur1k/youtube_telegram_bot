import logging
import requests
from config import FB_PAGE_ID, FB_PAGE_ACCESS_TOKEN


def post_to_facebook(video_url: str, title: str, thumbnail_url: str):
    """Post a Facebook photo with caption + YouTube link."""

    if not FB_PAGE_ID or not FB_PAGE_ACCESS_TOKEN:
        logging.warning("Facebook credentials not set, skipping Facebook post.")
        return

    # 1. Download thumbnail
    try:
        img_data = requests.get(thumbnail_url, timeout=10).content
    except Exception as e:
        logging.error(f"Failed to download thumbnail: {e}")
        return

    # 2. Upload photo to Facebook
    upload_endpoint = f"https://graph.facebook.com/v24.0/{FB_PAGE_ID}/photos"

    caption = f"🔥 New YouTube video is live!\n\n{title}\n\n{video_url}"
    caption = caption.encode("utf-8", errors="ignore").decode("utf-8")

    files = {"source": ("thumbnail.jpg", img_data, "image/jpeg")}

    payload = {
        "caption": caption,
        "access_token": FB_PAGE_ACCESS_TOKEN,
    }

    try:
        resp = requests.post(upload_endpoint, data=payload, files=files, timeout=15)
        logging.info(f"Facebook response: {resp.text}")
        resp.raise_for_status()
        logging.info("Posted photo to Facebook successfully.")
    except Exception as e:
        logging.error(f"Failed to post photo to Facebook: {e}")
