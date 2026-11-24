
import asyncio
import os
from aiogram import Bot
from dotenv import load_dotenv

load_dotenv()

async def main():
    bot = Bot(token=os.getenv("BOT_TOKEN"))

    chat = await bot.get_chat("@your_channel_username")

    print("Channel ID:", chat.id)
    print("Channel title:", chat.title)

    await bot.session.close()

asyncio.run(main())
