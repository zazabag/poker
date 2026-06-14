# API Documentation

## Overview

FastAPI-based REST API for Blackwood Poker Club. Handles all backend logic: users, tournaments, registrations, results, leaderboard, and achievements.

## Tech Stack

- **Framework:** FastAPI
- **Server:** Uvicorn (ASGI)
- **Database:** SQLite (file-based, located in `database/blackwood.db`)
- **CORS:** Enabled for all origins (Telegram WebApp requirement)

## Running the API

```bash
cd blackwood-poker-bot
pip install -r requirements.txt
python3 -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

## API Endpoints

### Health Check
```
GET /
Response: {"message": "Blackwood Poker Club API", "status": "running"}
```

### Users
```
POST /users
Body: {"telegram_id": int, "username": str, "nickname": str}
Response: {"id": int, "message": "User created"}

GET /users/{telegram_id}
Response: {"id": int, "telegram_id": int, "username": str, "nickname": str, "created_at": str}
```

### Tournaments
```
GET /tournaments?status=open
Response: [{"id": int, "title": str, "date": str, "time": str, "format": str, "max_players": int, "reentry_cost": int, "addon_cost": int, "status": str}]

POST /tournaments
Body: {"title": str, "date": str, "time": str, "max_players": int, "reentry_cost": int, "addon_cost": int}
Response: {"id": int, "message": "Tournament created"}

GET /tournaments/{id}
Response: full tournament + registrations list + registered_count
```

### Registrations
```
POST /register
Body: {"tournament_id": int, "user_id": int}
Response: {"message": "Registered successfully"}

POST /unregister
Body: {"tournament_id": int, "user_id": int}
Response: {"message": "Unregistered"}
```

### Results & Leaderboard
```
POST /results
Body: {"tournament_id": int, "user_id": int, "place": int, "reentries": int}
Response: {"points": int, "message": "Result recorded"}

GET /leaderboard
Response: [{"id": int, "nickname": str, "username": str, "games": int, "total_points": int, "wins": int, "finals": int, "total_reentries": int, "avg_place": float}]

GET /users/{user_id}/stats
Response: {"stats": {...}, "history": [{"title": str, "date": str, "place": int, "points": int}]}

GET /users/{user_id}/achievements
Response: [{"badge_code": str, "earned_at": str}]
```

## Points Calculation

| Place | Base Points |
|-------|------------|
| 1     | 100        |
| 2     | 80         |
| 3     | 60         |
| 4     | 40         |
| 5     | 20         |
| Other | 10         |

**Bonus:** +5 points per reentry

## Database Schema

See `database/README.md` for full schema details.

## Admin Workflow (Manual via API)

1. Create tournament: `POST /tournaments`
2. After tournament ends: `POST /results` for each player
3. Leaderboard auto-updates

## Future Improvements

- Add admin authentication middleware
- Add tournament close endpoint
- Add achievement auto-check after result submission
- Migrate to PostgreSQL for production
- Add tournament brackets/structure
