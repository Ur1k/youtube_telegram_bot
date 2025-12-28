import logging

from telegram_poster import send_public_message, send_admin_message
from facebook_poster import post_to_facebook
from instagram_poster import post_to_instagram


def notify_all(video):
    """
    video: dict with keys:
        - id
        - title
        - url
        - thumbnail_url
    """
    title = video["title"]
    url = video["url"]
    thumb = video.get("thumbnail_url")

    # Telegram
    try:
        public_text = f"🔥 <b>Нове YouTube відео!</b>\n{title}\n{url}"
        send_public_message(public_text)

    except Exception as e:
        logging.error(f"Error notifying Telegram: {e}")

    # Facebook
    try:
        post_to_facebook(url, title)
    except Exception as e:
        logging.error(f"Error posting to Facebook: {e}")

    # Instagram
    try:
        if thumb:
            post_to_instagram(thumb, title, url)
        else:
            logging.warning("No thumbnail URL provided, skipping Instagram.")
    except Exception as e:
        logging.error(f"Error posting to Instagram: {e}")
