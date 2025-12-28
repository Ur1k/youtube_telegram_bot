import logging
import requests
from config import FB_PAGE_ID, FB_PAGE_ACCESS_TOKEN


def post_to_facebook(video_url: str, title: str):
    """Post a link to a Facebook Page feed."""
    if not FB_PAGE_ID or not FB_PAGE_ACCESS_TOKEN:
        logging.warning("Facebook credentials not set, skipping Facebook post.")
        return

    endpoint = f"https://graph.facebook.com/v19.0/{FB_PAGE_ID}/feed"

    message = f"New YouTube video is live!\n\n{title}\n\n{video_url}"

    payload = {
        "message": message,
        "link": video_url,
        "access_token": FB_PAGE_ACCESS_TOKEN,
    }

    try:
        resp = requests.post(endpoint, data=payload, timeout=10)
        resp.raise_for_status()
        logging.info("Posted to Facebook successfully.")
    except Exception as e:
        logging.error(f"Failed to post to Facebook: {e}")
