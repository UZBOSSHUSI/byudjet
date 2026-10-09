import aiosqlite
import datetime

DB_PATH = "bot_database.db"

async def init_db():
    """Ma'lumotlar bazasi va jadvallarni yaratish"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS votes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                username TEXT,
                full_name TEXT,
                phone_number TEXT,
                verification_code TEXT,
                voted_at TIMESTAMP
            )
        """)
        await db.commit()

async def save_vote(user_id: int, username: str, full_name: str, phone_number: str, verification_code: str):
    """Ovoz berish ma'lumotlarini saqlash"""
    async with aiosqlite.connect(DB_PATH) as db:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await db.execute("""
            INSERT OR REPLACE INTO votes (user_id, username, full_name, phone_number, verification_code, voted_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, username, full_name, phone_number, verification_code, now))
        await db.commit()

async def has_user_voted(user_id: int) -> bool:
    """Foydalanuvchi ilgari ovoz berganmi yoki yo'qligini tekshirish"""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT 1 FROM votes WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            return row is not None

async def get_all_votes():
    """Barcha ovozlar statistikasini olish"""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT user_id, full_name, phone_number, verification_code, voted_at FROM votes ORDER BY id DESC") as cursor:
            return await cursor.fetchall()

async def get_votes_count() -> int:
    """Jami ovozlar sonini olish"""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT COUNT(*) FROM votes") as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0
