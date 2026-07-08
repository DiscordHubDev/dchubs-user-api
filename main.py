from contextlib import asynccontextmanager
from importlib.metadata import PackageNotFoundError, version

from fastapi import FastAPI

from api.v1.router import v1_router
from config import get_settings
from db import async_engine, create_db_and_tables
from utils.redis import close_redis_pool, init_redis_pool

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_redis_pool()
    await create_db_and_tables()
    yield
    await close_redis_pool()
    await async_engine.dispose()


try:
    __version__ = version("dchubs-api")
except PackageNotFoundError:
    __version__ = "0.0.0-dev"


app = FastAPI(
    title=settings.app_name,
    version=__version__,
    debug=settings.app_debug,
    lifespan=lifespan,
)


@app.get("/health", status_code=200, include_in_schema=False)
async def health_check():
    return {"status": "ok"}


app.include_router(v1_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app", host=settings.app_host, port=settings.app_port, reload=settings.app_debug
    )
