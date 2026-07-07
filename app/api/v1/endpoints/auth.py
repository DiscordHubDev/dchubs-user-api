from fastapi import APIRouter, Depends, HTTPException

from app.utils.jwt import create_access_token, get_refresh_user

auth_router = APIRouter(tags=["Authentication"])


@auth_router.post("/refresh", summary="使用 Refresh Token 換取新 Access Token")
async def refresh_token(token_claims: dict = Depends(get_refresh_user)):
    user_id = token_claims.get("sub")

    if not user_id or not isinstance(user_id, str):
        raise HTTPException(
            status_code=401, detail="Invalid token payload: missing or invalid subject"
        )

    new_access_token = create_access_token(user_id)
    return {"access_token": new_access_token, "token_type": "bearer"}
