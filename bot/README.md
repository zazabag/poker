# Bot Documentation

## Overview

Telegram bot for Blackwood Poker Club built with aiogram 3.x. The bot serves as the entry point for the Telegram Mini App — it sends a welcome message with a button that opens the web application.

## Tech Stack

- **Framework:** aiogram >= 3.0.0
- **Language:** Python 3.9+
- **Integration:** Uses `telegram-web-app.js` for Mini App support

## Running the Bot

```bash
cd blackwood-poker-bot
pip install -r requirements.txt
python3 -m bot.main
```

## Bot Configuration

All settings are in `bot/main.py`:

```python
BOT_TOKEN = "8919857648:AAEF19yjCIA-u54uYuMGMONTq-l6ehdUEXY"  # Your bot token
WEBAPP_URL = "https://zazabag.github.io/poker/"  # GitHub Pages URL
```

## Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome message + opens Web App button |
| `test` (text) | Simple test response to verify bot is running |

## How It Works

1. User sends `/start` to the bot
2. Bot checks if user exists in database (creates if not)
3. Bot sends welcome message with a button that opens the Mini App
4. The Mini App receives the user's Telegram ID via `window.Telegram.WebApp.initDataUnsafe.user.id`

## Mini App Integration

The bot uses `WebAppInfo` to create a button that opens the web app directly in Telegram's in-app browser. The web app then uses the Telegram Web App API to identify the user.

```python
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton

keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text="♠️ Открыть BLACKWOOD APP",
        web_app=WebAppInfo(url=WEBAPP_URL)
    )]
])
```

## Notifications

The bot has a helper function `notify_user(telegram_id, text)` that can be used to send push notifications to users (e.g., tournament reminders, registration confirmations).

## Future Features

- Scheduled reminders before tournaments
- "Tournament full" notifications for waitlist
- Achievement unlocked notifications
- Admin broadcast messages
- /help command with club info
- /rules command showing poker rules

## Files

- `bot/main.py` — Main bot logic and handlers
- `bot/__init__.py` — Package marker (empty)
