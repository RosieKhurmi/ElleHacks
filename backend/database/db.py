import sqlite3
from pathlib import Path
from typing import Optional
import hashlib
import secrets

# Database file path
DB_PATH = Path(__file__).parent / "app.db"

_db_initialized = False

def get_db_connection():
    """Get a database connection"""
    global _db_initialized
    if not _db_initialized:
        init_db()
        _db_initialized = True
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with required tables"""
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Favorites table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            place_id TEXT NOT NULL,
            place_name TEXT NOT NULL,
            place_address TEXT,
            place_rating REAL,
            place_data TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
            UNIQUE(user_id, place_id)
        )
    """)
    
    # Sessions table for authentication
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            token TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    """)
    
    conn.commit()
    conn.close()
    print("Database initialized successfully")

def hash_password(password: str) -> str:
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username: str, email: str, password: str) -> Optional[int]:
    """Create a new user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        password_hash = hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, password_hash)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id
    except sqlite3.IntegrityError:
        conn.close()
        return None

def verify_user(username: str, password: str) -> Optional[dict]:
    """Verify user credentials"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    password_hash = hash_password(password)
    cursor.execute(
        "SELECT id, username, email FROM users WHERE username = ? AND password_hash = ?",
        (username, password_hash)
    )
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return dict(user)
    return None

def create_session(user_id: int) -> str:
    """Create a session token for a user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    token = secrets.token_urlsafe(32)
    cursor.execute(
        "INSERT INTO sessions (user_id, token, expires_at) VALUES (?, ?, datetime('now', '+7 days'))",
        (user_id, token)
    )
    conn.commit()
    conn.close()
    
    return token

def verify_session(token: str) -> Optional[int]:
    """Verify a session token and return user_id"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT user_id FROM sessions WHERE token = ? AND expires_at > datetime('now')",
        (token,)
    )
    session = cursor.fetchone()
    conn.close()
    
    if session:
        return session['user_id']
    return None

def delete_session(token: str):
    """Delete a session (logout)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sessions WHERE token = ?", (token,))
    conn.commit()
    conn.close()

def add_favorite(user_id: int, place_data: dict) -> bool:
    """Add a place to user's favorites"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        import json
        cursor.execute(
            """INSERT INTO favorites 
               (user_id, place_id, place_name, place_address, place_rating, place_data) 
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                user_id,
                place_data.get('place_id'),
                place_data.get('name'),
                place_data.get('formatted_address', place_data.get('vicinity')),
                place_data.get('rating'),
                json.dumps(place_data)
            )
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

def remove_favorite(user_id: int, place_id: str) -> bool:
    """Remove a place from user's favorites"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM favorites WHERE user_id = ? AND place_id = ?",
        (user_id, place_id)
    )
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

def get_favorites(user_id: int) -> list:
    """Get all favorites for a user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT id, place_id, place_name, place_address, place_rating, place_data, created_at 
           FROM favorites WHERE user_id = ? ORDER BY created_at DESC""",
        (user_id,)
    )
    favorites = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    # Parse JSON data
    import json
    for fav in favorites:
        if fav['place_data']:
            fav['place_data'] = json.loads(fav['place_data'])
    
    return favorites

def is_favorite(user_id: int, place_id: str) -> bool:
    """Check if a place is in user's favorites"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT 1 FROM favorites WHERE user_id = ? AND place_id = ?",
        (user_id, place_id)
    )
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Database will be initialized when first accessed
# init_db() is called by the first function that needs the database
