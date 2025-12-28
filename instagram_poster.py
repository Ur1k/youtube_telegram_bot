import logging
import time
import requests
from config import IG_USER_ID, IG_ACCESS_TOKEN


def post_to_instagram(thumbnail_url: str, title: str, video_url: str):
    """
    Post an image with caption to Instagram.
    Note: Links in captions are not clickable on Instagram.
    """
    if not IG_USER_ID or not IG_ACCESS_TOKEN:
        logging.warning("Instagram credentials not set, skipping Instagram post.")
        return

    caption = f"New YouTube video is live!\n\n{title}\n\n{video_url}"

    # Step 1: Create media object
    create_url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media"
    create_payload = {
        "image_url": thumbnail_url,
        "caption": caption,
        "access_token": IG_ACCESS_TOKEN,
    }

    try:
        create_resp = requests.post(create_url, data=create_payload, timeout=15)
        create_resp.raise_for_status()
        creation_id = create_resp.json().get("id")
        if not creation_id:
            logging.error(f"Instagram media creation failed: {create_resp.text}")
            return
        logging.info(f"Instagram media created: {creation_id}")
    except Exception as e:
        logging.error(f"Failed to create Instagram media: {e}")
        return

    # Optional: brief delay before publish
    time.sleep(2)

    # Step 2: Publish media
    publish_url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media_publish"
    publish_payload = {
        "creation_id": creation_id,
        "access_token": IG_ACCESS_TOKEN,
    }

    try:
        publish_resp = requests.post(publish_url, data=publish_payload, timeout=15)
        publish_resp.raise_for_status()
        logging.info("Posted to Instagram successfully.")
    except Exception as e:
        logging.error(f"Failed to publish Instagram media: {e}")
