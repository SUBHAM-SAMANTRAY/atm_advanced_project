import sqlite3

DB_NAME = 'accounts.db'

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users(
            username TEXT PRIMARY KEY,
            pin TEXT,
            balance INTEGER)''')
        c.execute('''CREATE TABLE IF NOT EXISTS transactions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            info TEXT
        )''')
        conn.commit()

def add_user(username, pin):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO users(username, pin, balance) VALUES (?, ?, 0)", (username, pin))
        conn.commit()

def get_user(username):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT pin, balance FROM users WHERE username=?", (username,))
        return c.fetchone()

def change_balance(username, delta):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("UPDATE users SET balance=balance+? WHERE username=?", (delta, username))
        conn.commit()

def log_transaction(username, info):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO transactions(username, info) VALUES (?, ?)", (username, info))
        conn.commit()

def get_history(username):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT info FROM transactions WHERE username=?", (username,))
        return [row[0] for row in c.fetchall()]
