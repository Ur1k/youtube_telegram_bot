import requests

TOKEN = "8500535296:AAHj2lZAAygkCdBD70YpLoyfWZMtZUZh7Iw"
CHAT = "@YurikTrader"

requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    json={"chat_id": CHAT, "text": "Test message from bot"},
)
