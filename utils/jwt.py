import time
import uuid

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt

from config import get_settings

settings = get_settings()

JWT_SECRET_ACCESS = settings.jwt_secret_key
JWT_SECRET_REFRESH = settings.refresh_jwt_secret_key
JWT_ISSUER = settings.jwt_iss
JWT_AUDIENCE = settings.jwt_audience
JWT_ALGORITHM = settings.jwt_algorithm

# 定義時間常數（秒）
ACCESS_TOKEN_EXPIRE_SECONDS = 15 * 60  # 15 分鐘
REFRESH_TOKEN_EXPIRE_SECONDS = 7 * 24 * 60 * 60  # 7 天

security = HTTPBearer()


def decode_and_verify_token(token: str, secret: str, expected_type: str) -> dict:
    """驗證並解析 Token，確保型態正確"""
    try:
        payload = jwt.decode(
            token, secret, algorithms=[JWT_ALGORITHM], issuer=JWT_ISSUER, audience=JWT_AUDIENCE
        )
        if payload.get("typ") != expected_type:
            raise HTTPException(status_code=401, detail=f"Expected {expected_type} token")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired") from None
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token") from None


def validate_access_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """FastAPI 依賴項：攔截並驗證 Access Token，回傳其 Payload"""
    return decode_and_verify_token(credentials.credentials, JWT_SECRET_ACCESS, "access")


def validate_refresh_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """FastAPI 依賴項：攔截並驗證 Refresh Token，回傳其 Payload"""
    return decode_and_verify_token(credentials.credentials, JWT_SECRET_REFRESH, "refresh")


def generate_access_token(user_id: str) -> str:
    """核發新的 Access Token (15 分鐘有效)"""
    now = int(time.time())
    claims = {
        "sub": user_id,
        "typ": "access",
        "iss": JWT_ISSUER,
        "aud": JWT_AUDIENCE,
        "iat": now,
        "exp": now + ACCESS_TOKEN_EXPIRE_SECONDS,
        "jti": str(uuid.uuid4()),
    }
    return jwt.encode(claims, JWT_SECRET_ACCESS, algorithm=JWT_ALGORITHM)


def generate_refresh_token(user_id: str) -> str:
    """核發新的 Refresh Token (7 天有效)"""
    now = int(time.time())
    claims = {
        "sub": user_id,
        "typ": "refresh",  # 注意這裡型態改為 refresh
        "iss": JWT_ISSUER,
        "aud": JWT_AUDIENCE,
        "iat": now,
        "exp": now + REFRESH_TOKEN_EXPIRE_SECONDS,  # 設定 7 天過期
        "jti": str(uuid.uuid4()),
    }
    return jwt.encode(claims, JWT_SECRET_REFRESH, algorithm=JWT_ALGORITHM)
