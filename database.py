import sqlite3
from datetime import datetime

conn = sqlite3.connect("bot.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    limit_count INTEGER,
    last_reset TEXT,
    premium INTEGER DEFAULT 0
)
""")
conn.commit()

def get_user(user_id, free_limit):
    cur.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user = cur.fetchone()

    today = str(datetime.now().date())

    if not user:
        cur.execute("INSERT INTO users VALUES (?, ?, ?, ?)",
                    (user_id, free_limit, today, 0))
        conn.commit()
        return free_limit, 0

    limit_count, last_reset, premium = user[1], user[2], user[3]

    if last_reset != today:
        limit_count = free_limit
        cur.execute("UPDATE users SET limit_count=?, last_reset=? WHERE user_id=?",
                    (limit_count, today, user_id))
        conn.commit()

    return limit_count, premium

def reduce_limit(user_id):
    cur.execute("UPDATE users SET limit_count = limit_count - 1 WHERE user_id=?", (user_id,))
    conn.commit()

def set_premium(user_id):
    cur.execute("UPDATE users SET premium=1 WHERE user_id=?", (user_id,))
    conn.commit()
