from app.config import settings
import asyncpg

_db_pool = None


async def connect_db():
    global _db_pool
    _db_pool = await asyncpg.create_pool(
        dsn=settings.DATABASE_URL,
        min_size=1,
        max_size=10,
    )
    print("✅ Database connected")


async def disconnect_db():
    global _db_pool
    if _db_pool:
        await _db_pool.close()
        print("❌ Database disconnected")


async def get_db():
    async with _db_pool.acquire() as conn:
        yield conn
