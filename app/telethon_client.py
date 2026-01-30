import os
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

API_ID = int(os.getenv("TELETHON_API_ID"))
API_HASH = os.getenv("TELETHON_API_HASH")
SESSION = os.getenv("TELETHON_SESSION_NAME", "tgpulse_session")

async def get_recent_messages(username: str, limit: int = 10):
    async with TelegramClient(SESSION, API_ID, API_HASH) as client:
        entity = await client.get_entity(username)
        history = await client.get_messages(entity, limit=limit)
        # messages have .views for channels if available
        return history
