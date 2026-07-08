# app/api/v1/router.py

from fastapi import APIRouter

from api.v1.endpoints import auth, me

v1_router = APIRouter()

# 3. 註冊子路由
v1_router.include_router(me.router, prefix="/me")
v1_router.include_router(auth.router, prefix="/auth")
