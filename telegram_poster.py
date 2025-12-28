import logging
import requests
from config import TELEGRAM_TOKEN, TELEGRAM_PUBLIC_CHAT_ID, ADMIN_CHAT_ID


def send_telegram_message(chat_id, text, disable_notification=False):
    if not TELEGRAM_TOKEN:
        logging.error("TELEGRAM_TOKEN is not set.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}

    if disable_notification:
        payload["disable_notification"] = True

    try:
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        logging.info(f"Telegram message sent to {chat_id}: {text[:50]}...")
    except Exception as e:
        logging.error(f"Failed to send Telegram message to {chat_id}: {e}")


def send_public_message(text):
    send_telegram_message(TELEGRAM_PUBLIC_CHAT_ID, text)


def send_admin_message(text, silent=True):
    send_telegram_message(ADMIN_CHAT_ID, text, disable_notification=silent)
