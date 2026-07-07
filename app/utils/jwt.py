import time
import uuid

from config import get_settings
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt

settings = get_settings()

JWT_SECRET_ACCESS = settings.jwt_secret_key
JWT_SECRET_REFRESH = settings.refresh_jwt_secret_key
JWT_ISSUER = settings.jwt_iss
JWT_AUDIENCE = settings.jwt_audience
JWT_ALGORITHM = settings.jwt_algorithm

security = HTTPBearer()


def verify_token(token: str, secret: str, expected_type: str):
    """共用的 Token 驗證邏輯"""
    try:
        payload = jwt.decode(
            token, secret, algorithms=[JWT_ALGORITHM], issuer=JWT_ISSUER, audience=JWT_AUDIENCE
        )
        if payload.get("typ") != expected_type:
            raise HTTPException(status_code=401, detail=f"Expected {expected_type} token")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Access Token 攔截器"""
    return verify_token(credentials.credentials, JWT_SECRET_ACCESS, "access")


def get_refresh_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Refresh Token 攔截器"""
    return verify_token(credentials.credentials, JWT_SECRET_REFRESH, "refresh")


def create_access_token(user_id: str) -> str:
    """後端核發新的 Access Token (對齊前端邏輯)"""
    now = int(time.time())
    claims = {
        "sub": user_id,
        "typ": "access",
        "iss": JWT_ISSUER,
        "aud": JWT_AUDIENCE,
        "iat": now,
        "exp": now + 900,
        "jti": str(uuid.uuid4()),
    }
    return jwt.encode(claims, JWT_SECRET_ACCESS, algorithm=JWT_ALGORITHM)
