import sqlite3
from pathlib import Path

DB_PATH = Path("database") / "zzdd.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_database():
    DB_PATH.parent.mkdir(exist_ok=True)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS albums (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS photos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            album_id INTEGER NOT NULL,
            file_path TEXT NOT NULL,
            title TEXT,
            description TEXT,
            taken_at TEXT,
            uploaded_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (album_id) REFERENCES albums(id)
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM albums")
    count = cursor.fetchone()[0]

    if count == 0:
        default_albums = [
            ("WoW",),
            ("IT TAKES TWO",),
            ("Life",)
        ]

        cursor.executemany(
            "INSERT INTO albums (name) VALUES (?)",
            default_albums
        )

    conn.commit()
    conn.close()
    
def get_all_albums():
    conn = get_connection()
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, created_at
        FROM albums
        ORDER BY id
    """)

    albums = cursor.fetchall()
    conn.close()

    return albums

def get_album_by_id(album_id):
    conn = get_connection()
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, created_at FROM albums WHERE id = ?",
        (album_id,)
    )

    album = cursor.fetchone()
    conn.close()

    return album


def add_photo(album_id, file_path, title, description, taken_at):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO photos (album_id, file_path, title, description, taken_at)
        VALUES (?, ?, ?, ?, ?)
    """, (album_id, file_path, title, description, taken_at))

    conn.commit()
    conn.close()


def get_photos_by_album(album_id):
    conn = get_connection()
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, album_id, file_path, title, description, taken_at, uploaded_at
        FROM photos
        WHERE album_id = ?
        ORDER BY id DESC
    """, (album_id,))

    photos = cursor.fetchall()
    conn.close()

    return photos