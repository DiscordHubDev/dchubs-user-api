from fastapi import APIRouter

from app.api.v1.endpoints import me

# 建立 v1 的總路由器
v1_router = APIRouter()

v1_router.include_router(me.router, prefix="/me")
