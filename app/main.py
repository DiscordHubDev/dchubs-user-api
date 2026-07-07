from importlib.metadata import PackageNotFoundError, version

# 統一從 config 拿取
from config import get_settings
from fastapi import FastAPI

from app.api.v1.router import v1_router

try:
    __version__ = version("dchubs-api")
except PackageNotFoundError:
    __version__ = "0.0.0-dev"

settings = get_settings()

app = FastAPI(title="DcHubs User API", version=__version__)
app.include_router(v1_router, prefix="/api/v1")
