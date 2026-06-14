import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "blackwood.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE,
            username TEXT,
            nickname TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Tournaments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tournaments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            format TEXT DEFAULT "Texas Hold'em Classic",
            max_players INTEGER DEFAULT 40,
            reentry_cost INTEGER DEFAULT 1500,
            addon_cost INTEGER DEFAULT 3000,
            status TEXT DEFAULT 'open',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Registrations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tournament_id INTEGER,
            user_id INTEGER,
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tournament_id) REFERENCES tournaments(id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE(tournament_id, user_id)
        )
    """)
    
    # Results table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tournament_id INTEGER,
            user_id INTEGER,
            place INTEGER,
            points INTEGER DEFAULT 0,
            reentries INTEGER DEFAULT 0,
            FOREIGN KEY (tournament_id) REFERENCES tournaments(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    # Achievements table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            badge_code TEXT,
            earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    conn.commit()
    conn.close()

def add_user(telegram_id, username, nickname):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (telegram_id, username, nickname) VALUES (?, ?, ?)",
            (telegram_id, username, nickname)
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def get_user_by_telegram_id(telegram_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None

def get_user_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None

def create_tournament(title, date, time, max_players=40, reentry_cost=1500, addon_cost=3000):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tournaments (title, date, time, max_players, reentry_cost, addon_cost) VALUES (?, ?, ?, ?, ?, ?)",
        (title, date, time, max_players, reentry_cost, addon_cost)
    )
    conn.commit()
    tid = cursor.lastrowid
    conn.close()
    return tid

def get_tournaments(status=None):
    conn = get_connection()
    cursor = conn.cursor()
    if status:
        cursor.execute("SELECT * FROM tournaments WHERE status = ? ORDER BY date, time", (status,))
    else:
        cursor.execute("SELECT * FROM tournaments ORDER BY date, time")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_tournament(tournament_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tournaments WHERE id = ?", (tournament_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def register_user(tournament_id, user_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO registrations (tournament_id, user_id) VALUES (?, ?)",
            (tournament_id, user_id)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def unregister_user(tournament_id, user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM registrations WHERE tournament_id = ? AND user_id = ?",
        (tournament_id, user_id)
    )
    conn.commit()
    conn.close()

def get_registrations(tournament_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.id, u.nickname, u.username, r.registered_at 
        FROM registrations r 
        JOIN users u ON r.user_id = u.id 
        WHERE r.tournament_id = ?
    """, (tournament_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def is_registered(tournament_id, user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT 1 FROM registrations WHERE tournament_id = ? AND user_id = ?",
        (tournament_id, user_id)
    )
    result = cursor.fetchone()
    conn.close()
    return result is not None

def get_registration_count(tournament_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as cnt FROM registrations WHERE tournament_id = ?", (tournament_id,))
    result = cursor.fetchone()
    conn.close()
    return result["cnt"] if result else 0

def add_result(tournament_id, user_id, place, reentries=0):
    conn = get_connection()
    cursor = conn.cursor()
    points = calculate_points(place, reentries)
    cursor.execute(
        "INSERT INTO results (tournament_id, user_id, place, points, reentries) VALUES (?, ?, ?, ?, ?)",
        (tournament_id, user_id, place, points, reentries)
    )
    conn.commit()
    conn.close()
    return points

def calculate_points(place, reentries):
    base_points = {1: 100, 2: 80, 3: 60, 4: 40, 5: 20}.get(place, 10)
    return base_points + (reentries * 5)

def get_leaderboard(limit=50):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.id, u.nickname, u.username,
               COUNT(r.id) as games,
               SUM(r.points) as total_points,
               SUM(CASE WHEN r.place = 1 THEN 1 ELSE 0 END) as wins,
               SUM(CASE WHEN r.place <= 3 THEN 1 ELSE 0 END) as finals,
               SUM(r.reentries) as total_reentries,
               AVG(r.place) as avg_place
        FROM results r
        JOIN users u ON r.user_id = u.id
        GROUP BY u.id
        ORDER BY total_points DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_user_stats(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            COUNT(r.id) as games,
            SUM(r.points) as total_points,
            SUM(CASE WHEN r.place = 1 THEN 1 ELSE 0 END) as wins,
            SUM(CASE WHEN r.place <= 3 THEN 1 ELSE 0 END) as finals,
            SUM(r.reentries) as total_reentries,
            AVG(r.place) as avg_place
        FROM results r
        WHERE r.user_id = ?
    """, (user_id,))
    stats = cursor.fetchone()
    
    cursor.execute("""
        SELECT t.title, t.date, r.place, r.points
        FROM results r
        JOIN tournaments t ON r.tournament_id = t.id
        WHERE r.user_id = ?
        ORDER BY t.date DESC
        LIMIT 10
    """, (user_id,))
    history = cursor.fetchall()
    
    conn.close()
    return {
        "stats": dict(stats) if stats else None,
        "history": [dict(row) for row in history]
    }

def add_achievement(user_id, badge_code):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO achievements (user_id, badge_code) VALUES (?, ?)",
            (user_id, badge_code)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_user_achievements(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT badge_code, earned_at FROM achievements WHERE user_id = ?",
        (user_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

if __name__ == "__main__":
    init_db()
    print("Database initialized!")
