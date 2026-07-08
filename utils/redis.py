# utils/redis.py
import redis.asyncio as aioredis

from config import get_settings

settings = get_settings()

redis_pool: aioredis.ConnectionPool | None = None


def init_redis_pool():
    global redis_pool
    redis_pool = aioredis.ConnectionPool(
        host=settings.redis_host,
        port=settings.redis_port,
        db=settings.redis_db,
        password=settings.redis_password,
        decode_responses=True,
    )
    print("Redis connection pool initialized.")


async def close_redis_pool():
    """在 FastAPI 關閉時呼叫，優雅釋放資源"""
    global redis_pool
    if redis_pool:
        await redis_pool.disconnect()
        print("Redis connection pool closed.")


async def get_redis_client():
    if redis_pool is None:
        raise RuntimeError("Redis pool is not initialized. Call init_redis_pool first.")

    async with aioredis.Redis(connection_pool=redis_pool) as client:
        yield client
