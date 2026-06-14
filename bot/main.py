import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message, InlineKeyboardMarkup, InlineKeyboardButton, 
    WebAppInfo, CallbackQuery, FSInputFile
)
from aiogram.filters import CommandStart
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from database import db

BOT_TOKEN = "8919857648:AAEF19yjCIA-u54uYuMGMONTq-l6ehdUEXY"
WEBAPP_URL = "https://zazabag.github.io/poker/"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

AVATAR_PATH = os.path.join(os.path.dirname(__file__), 'avatar1.jpg')

RULES_TEXT = (
    "📋 <b>Правила клуба BlackWood</b>\n\n"
    "BlackWood — клуб спортивного покера легального формата, где игра проводится "
    "<b>без денежных ставок, денежных выигрышей и поощрительных призов</b>. "
    "Это пространство для интеллектуального досуга, развития игровых навыков и общения в кругу единомышленников.\n\n"
    "<b>Условия допуска к игре:</b>\n"
    "• К участию допускаются лица старше 18 лет.\n"
    "• Игрок должен иметь базовое представление о правилах покера.\n"
    "• Для гостей, не знакомых с правилами игры, предусмотрено бесплатное обучение.\n"
    "• Клуб оставляет за собой право отказать в посещении без объяснения причин.\n"
    "• Каждый участник обязан соблюдать правила клуба, проявлять уважение к персоналу и другим гостям.\n"
    "• Агрессия, оскорбления, конфликтное поведение — недопустимы.\n"
    "• Попытки получить преимущество нечестным путем строго запрещены. "
    "Повторное нарушение влечет исключение из клуба.\n\n"
    "<b>Формат:</b> Texas Hold'em Classic\n"
    "<b>Вход:</b> Бесплатный\n"
    "<b>Re-Entry:</b> 1500₽ | <b>Add-on:</b> 3000₽\n\n"
    "Соблюдение правил — обязательно для всех участников. 🃏"
)


@dp.message(CommandStart())
async def start(message: Message):
    telegram_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    
    user = db.get_user_by_telegram_id(telegram_id)
    if not user:
        db.add_user(telegram_id, username, username)
        user = db.get_user_by_telegram_id(telegram_id)
    
    welcome_text = (
        "♠️ Добро пожаловать в <b>BLACKWOOD POKER CLUB</b>! 🃏\n\n"
        "Клуб спортивного покера легального формата. Игра без денежных ставок и выигрышей — "
        "только интеллект, навыки и атмосфера.\n\n"
        "🍸 <b>Welcome drink</b>, кальяны и приятная компания\n"
        "📅 <b>Турниры</b> — запись, статистика, ачивки и топы\n"
        "🔞 <b>Вход с 18 лет.</b> Базовые знания покера приветствуются\n\n"
        "<i>Открывай приложение — записывайся на турниры, следи за таблицей лидеров и копи очки.</i>"
    )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="♠️ Открыть BLACKWOOD APP",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )],
        [
            InlineKeyboardButton(text="📋 Правила клуба", callback_data="rules"),
            InlineKeyboardButton(text="📅 Турниры", callback_data="tournaments"),
        ]
    ])
    
    # Try to send photo with caption, fallback to plain text
    try:
        if os.path.exists(AVATAR_PATH):
            photo = FSInputFile(AVATAR_PATH)
            await message.answer_photo(
                photo=photo,
                caption=welcome_text,
                reply_markup=keyboard,
                parse_mode="HTML"
            )
        else:
            await message.answer(welcome_text, reply_markup=keyboard, parse_mode="HTML")
    except Exception as e:
        print(f"Photo send failed: {e}")
        await message.answer(welcome_text, reply_markup=keyboard, parse_mode="HTML")


@dp.callback_query(F.data == "rules")
async def show_rules(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="♠️ Открыть приложение",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )]
    ])
    await callback.message.answer(RULES_TEXT, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()


@dp.callback_query(F.data == "tournaments")
async def show_tournaments(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="📅 Открыть календарь турниров",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )]
    ])
    await callback.message.answer(
        "📅 <b>Расписание турниров</b>\n\n"
        "Все актуальные турниры, запись и статус мест — в приложении.\n\n"
        "Нажми кнопку ниже, чтобы открыть календарь.",
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await callback.answer()


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
