# Database Documentation

## Overview

SQLite database for Blackwood Poker Club. Simple, file-based, no server needed. Good for MVP and small-scale usage.

## Database File

- **Location:** `database/blackwood.db` (auto-created on first run)
- **Type:** SQLite 3
- **Connection:** Via `sqlite3` module (Python standard library)

## Tables

### 1. `users`

Registered players. Linked to Telegram accounts.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PK | Auto-increment ID |
| telegram_id | INTEGER UNIQUE | Telegram user ID |
| username | TEXT | Telegram username or display name |
| nickname | TEXT UNIQUE | Player's chosen nickname |
| created_at | TIMESTAMP | Registration date |

### 2. `tournaments`

Scheduled poker tournaments.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PK | Auto-increment ID |
| title | TEXT | Tournament name (e.g., "Friday Night Poker") |
| date | TEXT | Date (format: DD.MM.YYYY) |
| time | TEXT | Time (format: HH:MM) |
| format | TEXT | Game format (default: "Texas Hold'em Classic") |
| max_players | INTEGER | Maximum participants (default: 40) |
| reentry_cost | INTEGER | Cost in rubles (default: 1500) |
| addon_cost | INTEGER | Add-on cost in rubles (default: 3000) |
| status | TEXT | `open`, `closed`, `completed` (default: `open`) |
| created_at | TIMESTAMP | Creation date |

### 3. `registrations`

Player registrations for tournaments.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PK | Auto-increment ID |
| tournament_id | INTEGER FK | Reference to tournaments.id |
| user_id | INTEGER FK | Reference to users.id |
| registered_at | TIMESTAMP | Registration date |
| **Unique constraint:** | | `(tournament_id, user_id)` |

### 4. `results`

Tournament results with points calculation.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PK | Auto-increment ID |
| tournament_id | INTEGER FK | Reference to tournaments.id |
| user_id | INTEGER FK | Reference to users.id |
| place | INTEGER | Final place (1, 2, 3, etc.) |
| points | INTEGER | Calculated points (base + reentry bonus) |
| reentries | INTEGER | Number of reentries (default: 0) |

### 5. `achievements`

Player achievements / badges.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PK | Auto-increment ID |
| user_id | INTEGER FK | Reference to users.id |
| badge_code | TEXT | Achievement identifier (e.g., "first_win", "rebuy_master") |
| earned_at | TIMESTAMP | Achievement date |

## Points System

### Base Points by Place

| Place | Points |
|-------|--------|
| 1 | 100 |
| 2 | 80 |
| 3 | 60 |
| 4 | 40 |
| 5 | 20 |
| 6+ | 10 |

### Reentry Bonus

+5 points per reentry (motivates players to rebuy rather than quit)

### Total Points Formula

```
total_points = base_points(place) + (reentries * 5)
```

## Key Functions

All functions are in `database/db.py`:

- `init_db()` — Creates all tables if not exist
- `add_user(telegram_id, username, nickname)` — Register new user
- `get_user_by_telegram_id(telegram_id)` — Find user by Telegram ID
- `create_tournament(title, date, time, ...)` — Create tournament
- `get_tournaments(status)` — List tournaments (optional filter)
- `register_user(tournament_id, user_id)` — Register for tournament
- `unregister_user(tournament_id, user_id)` — Cancel registration
- `get_registration_count(tournament_id)` — Count registrations
- `add_result(tournament_id, user_id, place, reentries)` — Record result + auto-calc points
- `get_leaderboard(limit)` — Get ranked list of players
- `get_user_stats(user_id)` — Get player stats + history
- `add_achievement(user_id, badge_code)` — Grant achievement
- `get_user_achievements(user_id)` — Get player's achievements

## Initialization

```python
from database.db import init_db
init_db()  # Creates blackwood.db with all tables
```

## Future Improvements

- Add `waitlist` table for tournaments at capacity
- Add `seasons` table for season-based leaderboards
- Add `rewards` table for tracking non-monetary prizes
- Add `banned` flag for users
- Add `tournament_notes` for admin comments
- Add `registration_status` (confirmed, pending, cancelled)
- Migrate to PostgreSQL for concurrent access and production scale
