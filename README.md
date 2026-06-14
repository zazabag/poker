# ♠️ BLACKWOOD POKER CLUB

Telegram Mini App + Bot + API для покерного клуба.

## Архитектура

- **Bot** (`bot/`) — Telegram бот (aiogram). Приветствие + кнопка открытия Mini App + уведомления.
- **API** (`api/`) — FastAPI backend. Турниры, регистрации, результаты, лидерборд, статистика.
- **Database** (`database/`) — SQLite. Юзеры, турниры, регистрации, результаты, ачивки.
- **WebApp** (`webapp/` + `docs/`) — Telegram Mini App. HTML/CSS/JS в стиле Blackwood.

## Запуск локально

### 1. API
```bash
cd blackwood-poker-bot
python3 -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Bot
```bash
python3 -m bot.main
```

### 3. WebApp
Открыть `webapp/index.html` в браузере или через Telegram бота.

## Деплой

### WebApp (GitHub Pages)
Веб-ап лежит в папке `docs/`. Настрой GitHub Pages в репозитории:
- Settings → Pages → Source: Deploy from a branch
- Branch: `main` → Folder: `/docs`

URL будет: `https://zazabag.github.io/poker/`

### API (Render / Railway / VPS)
API нужно задеплоить отдельно. Рекомендуется [Render](https://render.com) (бесплатно).
Поменяй `API_URL` в `webapp/app.js` на свой URL.

## Функционал

- 📅 Расписание турниров
- ✍️ Запись на турниры (с лимитом мест)
- 🏆 Лидерборд (очки, победы, финалы)
- 👤 Профиль игрока (статистика, история)
- 🎖 Ачивки (бейджи)
- 📊 Админка ввода результатов (через API)

## Счёт очков

- 1 место: 100 очков
- 2 место: 80
- 3 место: 60
- 4 место: 40
- 5 место: 20
- Остальные: 10
- За каждый ребай: +5 очков

---

Made for BLACKWOOD POKER CLUB 🃏
