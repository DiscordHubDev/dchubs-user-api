from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends, HTTPException
import jwt

from config import get_settings

# 匯入你提供的工具與常數
from utils.jwt import (
    REFRESH_TOKEN_EXPIRE_SECONDS,
    generate_access_token,
    generate_refresh_token,
    validate_refresh_token,
)
from utils.redis import get_redis_client

if TYPE_CHECKING:
    import redis.asyncio as aioredis

settings = get_settings()

router = APIRouter(tags=["Authentication"])

IS_DEV = settings.app_env == "local"


@router.post("/refresh", summary="刷新存取令牌")
async def refresh_token(
    token_claims: dict = Depends(validate_refresh_token),
    redis: aioredis.Redis = Depends(get_redis_client),
):
    user_id = token_claims.get("sub")
    old_jti = token_claims.get("jti")

    if not user_id or not isinstance(user_id, str):
        raise HTTPException(
            status_code=401, detail="Invalid token payload: missing or invalid subject"
        )

    redis_key = f"user_refresh_token:{user_id}:{old_jti}"
    token_exists = await redis.exists(redis_key)

    if not token_exists:
        if IS_DEV:
            print(f"⚠️ [DEV MODE] 允許未知 Token (jti: {old_jti}), 這在 Prod 會被阻擋!")
        else:
            raise HTTPException(status_code=401, detail="Token has already been used or revoked")

    new_access_token = generate_access_token(user_id)
    new_refresh_token = generate_refresh_token(user_id)

    new_claims = jwt.decode(new_refresh_token, options={"verify_signature": False})
    new_jti = new_claims.get("jti")

    await redis.delete(redis_key)

    new_redis_key = f"user_refresh_token:{user_id}:{new_jti}"

    await redis.set(new_redis_key, "valid", ex=REFRESH_TOKEN_EXPIRE_SECONDS)
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }
