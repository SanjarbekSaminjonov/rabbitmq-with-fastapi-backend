import requests

from settings import env

def send_telegram_message(message: str) -> None:
    requests.post(
        env.str("TELEGRAM_BOT_API_URL"),
        data={
            "chat_id": env.str("TELEGRAM_CHAT_ID"),
            "text": message,
        },
    )
