import os

from dotenv import load_dotenv
from telethon import TelegramClient

load_dotenv()

API_ID = int(os.getenv("TELETHON_API_ID"))
API_HASH = os.getenv("TELETHON_API_HASH")
SESSION = os.getenv("TELETHON_SESSION_NAME", "tgpulse_session")

async def get_recent_messages(username: str, limit: int = 100) -> dict[str, str | int]:
    async with TelegramClient(SESSION, API_ID, API_HASH) as client:
        try:
            entity = await client.get_entity(username)
            messages = await client.get_messages(entity, limit=limit)
            views = [m.views for m in messages if m.views]
            avg_views = sum(views) / len(views) if views else 0
            return {
                "title": entity.title,
                "count": len(messages),
                "avg_views": round(avg_views)
            }
        except Exception as e:
            print(f"Ошибка Telethon: {e}")
            return None


