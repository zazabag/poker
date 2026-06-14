import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import CommandStart
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from database import db

BOT_TOKEN = "8919857648:AAEF19yjCIA-u54uYuMGMONTq-l6ehdUEXY"
WEBAPP_URL = "https://blackwood-poker-app.pages.dev"  # placeholder

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    telegram_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    
    user = db.get_user_by_telegram_id(telegram_id)
    if not user:
        db.add_user(telegram_id, username, username)
        user = db.get_user_by_telegram_id(telegram_id)
    
    welcome_text = (
        "👑 Добро пожаловать в <b>BLACKWOOD POKER CLUB</b>!\n\n"
        "🎴 Здесь живёт настоящий покер. Турниры, статистика, ачивки и топы.\n\n"
        "Нажми кнопку ниже, чтобы открыть приложение клуба."
    )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="♠️ Открыть BLACKWOOD APP",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )]
    ])
    
    await message.answer(welcome_text, reply_markup=keyboard, parse_mode="HTML")

@dp.message(F.text == "test")
async def test(message: Message):
    await message.answer("Бот работает, блять! ✅")

async def notify_user(telegram_id: int, text: str):
    try:
        await bot.send_message(chat_id=telegram_id, text=text, parse_mode="HTML")
    except Exception as e:
        print(f"Failed to notify {telegram_id}: {e}")

async def main():
    db.init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
