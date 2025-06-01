import sqlite3
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_FILENAME = "database.db"
DB_PATH = os.path.join(BASE_DIR, DB_FILENAME)

SQL_FILE = os.path.join(os.path.dirname(__file__), "classroom.sql")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DB_PATH):
        open(DB_PATH, "a").close()

    conn = get_db_connection()
    cursor = conn.cursor()

    # Kiểm tra bảng 'classes'
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='classes';"
    )
    if cursor.fetchone() is None:
        # Nếu chưa có, đọc classroom.sql và chạy
        with open(SQL_FILE, "r", encoding="utf-8") as f:
            sql_script = f.read()
        cursor.executescript(sql_script)
        conn.commit()

    cursor.close()
    conn.close()
