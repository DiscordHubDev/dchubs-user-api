from datetime import datetime
import json
import logging
from typing import Any

from pydantic import Field, field_validator

from schemas import BaseResponseModel

logger = logging.getLogger(__name__)


class UserResponse(BaseResponseModel):
    """
    使用者資訊回應模型

    這個說明會顯示在 FastAPI 文件的 Schema 描述中，用來表示回傳的使用者完整資料。
    """

    name: str = Field(
        ..., description="使用者的全域顯示名稱或使用者名稱", examples=["鰻頭(`・ω・´)"]
    )
    email: str = Field(..., description="使用者的電子郵件信箱", examples=["user@example.com"])
    email_verified: bool = Field(..., description="標示該電子郵件是否已完成驗證", examples=[True])
    discord_id: str = Field(..., description="Discord 帳號ID", examples=["123456789012345678"])
    username: str = Field(
        ..., description="登入用的使用者名稱 (不含空格)", examples=["mantouisyummy"]
    )
    avatar: str = Field(
        ..., description="使用者頭貼網址", examples=["https://cdn.discordapp.com/avatars/..."]
    )
    created_at: datetime = Field(
        ..., description="帳號建立的 ISO 8601 時間字串", examples=["2025-04-06T14:29:47.501000"]
    )
    updated_at: datetime = Field(
        ...,
        description="帳號最後更新的 ISO 8601 時間字串",
        examples=["2026-07-07T08:27:25.342000Z"],
    )
    nsfw: bool = Field(..., description="帳號是否標記為成人內容 (NSFW)", examples=[True])

    banner: str | None = Field(
        default=None,
        description="使用者的 Discord 橫幅圖片網址",
        examples=["https://cdn.discordapp.com/banners/..."],
    )
    banner_color: str | None = Field(
        default=None, description="橫幅的十六進位主題色碼 (沒有橫幅時才使用)", examples=["#5865F2"]
    )
    bio: str | None = Field(
        default=None, description="使用者的自我介紹", examples=["這是一段自我介紹。"]
    )
    social: dict[str, Any] | None = Field(
        default=None,
        description="社群媒體連結與相關資料 (JSON 格式)",
        examples=[{"github": "https://github.com/daming", "twitter": "https://twitter.com/daming"}],
    )

    @staticmethod
    def _try_parse_json(raw: str) -> dict[str, Any] | None:
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            return None
        return parsed if isinstance(parsed, dict) else None

    @field_validator("social", mode="before")
    @classmethod
    def parse_social_data(cls, v: Any) -> dict[str, Any] | None:
        if v is None or isinstance(v, dict):
            return v

        if isinstance(v, str):
            result = cls._try_parse_json(v)
            if result is None:
                logger.warning("Failed to parse social field as JSON: %r", v)
            return result

        if isinstance(v, list):
            for item in v:
                if isinstance(item, str) and item.strip().startswith("{"):
                    result = cls._try_parse_json(item)
                    if result is not None:
                        return result
            logger.warning("No parsable dict found in social list: %r", v)
            return None

        logger.warning("Unexpected type for social field: %r", type(v))
        return None
