from fastapi import APIRouter, Depends, HTTPException, status

from db import SessionDep
from db.models import AuthUser
from schemas.user import UserResponse
from utils.jwt import validate_access_token

router = APIRouter(tags=["UserInfo"])


@router.get("/", summary="取得使用者資訊", response_model=UserResponse)
async def get_user_info(session: SessionDep, token_claims: dict = Depends(validate_access_token)):
    user_id: str = token_claims.get("sub", "")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token 中缺少使用者 ID (sub)"
        )

    user = await session.get(AuthUser, user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="找不到該使用者")

    return user
