import aiohttp
from settings import env


async def send_telegram_message(message: str) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"https://api.telegram.org/bot{env.str('TELEGRAM_BOT_TOKEN')}/sendMessage",
            data={
                "chat_id": env.str("TELEGRAM_CHAT_ID"),
                "text": message,
                "parse_mode": "HTML",
            },
        ) as response:
            return response
