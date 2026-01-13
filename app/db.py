# app/db.py
import asyncpg
from app.config import DATABASE_URL

_db_pool: asyncpg.Pool | None = None


async def connect_db():
    """
    Runs ONCE when the app starts.
    Creates a connection pool.

    Pool = efficient + scalable.
    """
    global _db_pool
    _db_pool = await asyncpg.create_pool(
        DATABASE_URL,
        min_size=1,
        max_size=10,      # increase later
        command_timeout=60
    )


async def disconnect_db():
    """
    Runs ONCE when app shuts down.
    """
    global _db_pool
    if _db_pool:
        await _db_pool.close()


async def get_db():
    """
    This is what your routes will use.

    Gives ONE connection per request.
    """
    if not _db_pool:
        raise RuntimeError("DB not initialized")

    async with _db_pool.acquire() as connection:
        yield connection
