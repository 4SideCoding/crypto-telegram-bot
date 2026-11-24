
import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is missing from your .env file")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

PLANS = {
    "7days": ("7 Days", 5),
    "30days": ("30 Days", 10),
    "90days": ("90 Days", 20),
    "1year": ("1 Year", 40),
    "lifetime": ("Lifetime", 60),
}


@dp.message(CommandStart())
async def start(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Buy Access", callback_data="buy")]
        ]
    )

    await message.answer(
        "Welcome!\n\nChoose Buy Access to see our membership plans.",
        reply_markup=keyboard
    )


@dp.callback_query(lambda query: query.data == "buy")
async def show_plans(query: CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{name} — {amount} USDT",
                    callback_data=f"plan:{plan_id}"
                )
            ]
            for plan_id, (name, amount) in PLANS.items()
        ]
    )

    await query.message.answer(
        "Please choose your membership plan:",
        reply_markup=keyboard
    )
    await query.answer()


@dp.callback_query(lambda query: query.data.startswith("plan:"))
async def choose_plan(query: CallbackQuery):
    plan_id = query.data.split(":", 1)[1]

    if plan_id not in PLANS:
        await query.answer("Invalid plan.", show_alert=True)
        return

    name, amount = PLANS[plan_id]

    await query.message.answer(
        f"You selected: {name}\n"
        f"Price: {amount} USDT\n\n"
        "Checkout setup is our next step. "
        "No payment has been requested or verified yet."
    )
    await query.answer()


async def main():
    print("Bot is running...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
