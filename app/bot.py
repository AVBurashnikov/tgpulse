import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ChatAction
from aiogram.filters import Command
from dotenv import load_dotenv

from app.telethon_client import get_recent_messages

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("❌ Не найден TELEGRAM_BOT_TOKEN в .env файле")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

connected_channels = {}

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет 👋 Я TG Pulse бот! Пока я просто здороваюсь :)")

@dp.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer("Доступные команды:\n/start - запустить бота\n/help - справка")

@dp.message(Command("connect"))
async def connect_channel(message: types.Message):
    args = message.text.split()
    if len(args) < 2:
        await message.reply("❌ Укажи канал, например: /connect @examplechannel")
        return

    channel_username = args[1]
    if not channel_username.startswith("@"):
        await message.reply("❌ Канал должен начинаться с @, пример: /connect @example")
        return

    user_id = message.from_user.id
    if user_id not in connected_channels:
        connected_channels[user_id] = []

    connected_channels[user_id].append(channel_username)
    await message.reply(f"✅ Канал {channel_username} подключён!")

@dp.message(Command("list"))
async def list_channels(message: types.Message):
    user_id = message.from_user.id
    channels = connected_channels.get(user_id, [])
    if not channels:
        await message.reply("У тебя пока нет подключённых каналов.")
        return

    formatted = "\n".join(channels)
    await message.reply(f"📋 Твои каналы:\n{formatted}")

@dp.message(Command("report"))
async def report_channel(message: types.Message):
    try:
        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
        args = message.text.split()
        if len(args) < 2:
            await message.reply("❌ Укажи канал, например: /report @examplechannel")
            return

        channel_username = args[1]
        if not channel_username.startswith("@"):
            await message.reply("❌ Канал должен начинаться с @, пример: /report @example")
            return

        data = await get_recent_messages(channel_username, limit=10)
        if not data:
            await message.reply("⚠️ Не удалось получить статистику. Возможно, канал приватный.")
            return

        await message.reply(
            f"📊 Отчёт по каналу {data.get('title', channel_username)}\n\n"
            f"📬 Сообщений: {data['count']}\n"
            f"👀 Средние просмотры: {data['avg_views']}"
        )

    except Exception as e:
        await message.reply("😬 Что-то пошло не так, попробуй позже.")
        print(f"Ошибка в /report: {e}")

async def main():
    print("Бот запущен ✅")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен ❌")
