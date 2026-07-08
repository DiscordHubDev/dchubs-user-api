import datetime
import enum
from typing import Optional

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Double,
    Enum,
    ForeignKeyConstraint,
    Index,
    Integer,
    PrimaryKeyConstraint,
    Table,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, TIMESTAMP
from sqlmodel import Field, Relationship, SQLModel


class Emailpriority(enum.StrEnum):
    SUCCESS = "success"
    INFO = "info"
    WARNING = "warning"
    DANGER = "danger"


class Reportseverity(enum.StrEnum):
    SEVERE = "severe"
    MODERATE = "moderate"
    LOW = "low"
    UNTAGGED = "untagged"


class Reportstatus(enum.StrEnum):
    PENDING = "pending"
    RESOLVED = "resolved"
    REJECTED = "rejected"


class Reporttype(enum.StrEnum):
    BOT = "bot"
    SERVER = "server"


class Status(enum.StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class Votetype(enum.StrEnum):
    SERVER = "server"
    BOT = "bot"


class BotCommand(SQLModel, table=True):
    __tablename__ = "BotCommand"
    __table_args__ = (
        ForeignKeyConstraint(
            ["botId"],
            ["Bot.id"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="BotCommand_botId_fkey",
        ),
        PrimaryKeyConstraint("id", name="BotCommand_pkey"),
        Index("BotCommand_botId_idx", "botId"),
        Index("BotCommand_category_idx", "category"),
        Index("BotCommand_name_idx", "name"),
    )

    id: str = Field(sa_column=Column("id", Text, primary_key=True))
    name: str = Field(sa_column=Column("name", Text, nullable=False))
    description: str = Field(sa_column=Column("description", Text, nullable=False))
    usage: str = Field(sa_column=Column("usage", Text, nullable=False))
    botId: str = Field(sa_column=Column("botId", Text, nullable=False))
    category: str | None = Field(default=None, sa_column=Column("category", Text))

    Bot_: "Bot" = Relationship(back_populates="BotCommand_")


class Review(SQLModel, table=True):
    __tablename__ = "Review"
    __table_args__ = (
        ForeignKeyConstraint(
            ["botId"], ["Bot.id"], ondelete="SET NULL", onupdate="CASCADE", name="Review_botId_fkey"
        ),
        ForeignKeyConstraint(
            ["serverId"],
            ["Server.id"],
            ondelete="SET NULL",
            onupdate="CASCADE",
            name="Review_serverId_fkey",
        ),
        PrimaryKeyConstraint("id", name="Review_pkey"),
        Index("Review_botId_idx", "botId"),
        Index("Review_botId_rating_idx", "botId", "rating"),
        Index("Review_createdAt_idx", "createdAt"),
        Index("Review_rating_idx", "rating"),
        Index("Review_serverId_idx", "serverId"),
        Index("Review_serverId_rating_idx", "serverId", "rating"),
        Index("Review_userId_botId_key", "userId", "botId", unique=True),
        Index("Review_userId_idx", "userId"),
        Index("Review_userId_serverId_key", "userId", "serverId", unique=True),
    )

    id: str = Field(sa_column=Column("id", Text, primary_key=True))
    rating: float = Field(
        sa_column=Column("rating", Double(53), nullable=False, server_default=text("0"))
    )
    vote: int = Field(sa_column=Column("vote", Integer, nullable=False))
    createdAt: datetime.datetime = Field(
        sa_column=Column(
            "createdAt",
            TIMESTAMP(precision=3),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )
    userId: str = Field(sa_column=Column("userId", Text, nullable=False))
    comment: str | None = Field(default=None, sa_column=Column("comment", Text))
    botId: str | None = Field(default=None, sa_column=Column("botId", Text))
    serverId: str | None = Field(default=None, sa_column=Column("serverId", Text))

    Bot_: Optional["Bot"] = Relationship(back_populates="Review_")
    Server_: Optional["Server"] = Relationship(back_populates="Review_")


class Administrators(SQLModel, table=True):
    __tablename__ = "Administrators"
    __table_args__ = (PrimaryKeyConstraint("id", name="Administrators_pkey"),)

    id: str = Field(sa_column=Column("id", Text, primary_key=True))


class ApiToken(SQLModel, table=True):
    __tablename__ = "ApiToken"
    __table_args__ = (
        PrimaryKeyConstraint("userId", name="ApiToken_pkey"),
        Index("ApiToken_accessToken_key", "accessToken", unique=True),
        Index("ApiToken_refreshToken_key", "refreshToken", unique=True),
    )

    userId: str = Field(sa_column=Column("userId", Text, primary_key=True))
    accessToken: str = Field(sa_column=Column("accessToken", Text, nullable=False))
    refreshToken: str = Field(sa_column=Column("refreshToken", Text, nullable=False))


class Notification(SQLModel, table=True):
    __tablename__ = "Notification"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="Notification_pkey"),
        Index("Notification_createdAt_idx", "createdAt"),
        Index("Notification_read_idx", "read"),
        Index("Notification_userId_idx", "userId"),
        Index("Notification_userId_read_idx", "userId", "read"),
    )

    id: str = Field(sa_column=Column("id", Text, primary_key=True))
    name: str = Field(sa_column=Column("name", Text, nullable=False))
    createdAt: datetime.datetime = Field(
        sa_column=Column(
            "createdAt",
            TIMESTAMP(precision=3),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )
    subject: str = Field(sa_column=Column("subject", Text, nullable=False))
    teaser: str = Field(sa_column=Column("teaser", Text, nullable=False))
    priority: Emailpriority = Field(
        sa_column=Column(
            "priority",
            Enum(
                Emailpriority,
                values_callable=lambda cls: [member.value for member in cls],
                name="EmailPriority",
            ),
            nullable=False,
            server_default=text("'info'::\"EmailPriority\""),
        )
    )
    isSystem: bool = Field(
        sa_column=Column("isSystem", Boolean, nullable=False, server_default=text("false"))
    )
    read: bool = Field(
        sa_column=Column("read", Boolean, nullable=False, server_default=text("false"))
    )
    content: str = Field(sa_column=Column("content", Text, nullable=False))
    userId: str | None = Field(default=None, sa_column=Column("userId", Text))


class Announcements(SQLModel, table=True):
    __table_args__ = (PrimaryKeyConstraint("id", name="announcements_pkey"),)

    id: int = Field(sa_column=Column("id", Integer, primary_key=True, autoincrement=True))
    content: str = Field(sa_column=Column("content", Text, nullable=False))
    is_active: bool = Field(
        sa_column=Column("is_active", Boolean, nullable=False, server_default=text("true"))
    )
    updated_at: datetime.datetime = Field(
        sa_column=Column("updated_at", DateTime, nullable=False, server_default=text("now()"))
    )


class AuthVerification(SQLModel, table=True):
    __tablename__ = "auth_verification"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="auth_verification_pkey"),
        Index("authVerification_identifier_idx", "identifier"),
    )

    id: str = Field(sa_column=Column("id", Text, primary_key=True))
    identifier: str = Field(sa_column=Column("identifier", Text, nullable=False))
    value: str = Field(sa_column=Column("value", Text, nullable=False))
    expires_at: datetime.datetime = Field(
        sa_column=Column("expires_at", TIMESTAMP(precision=3), nullable=False)
    )
    created_at: datetime.datetime = Field(
        sa_column=Column(
            "created_at",
            TIMESTAMP(precision=3),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )
    updated_at: datetime.datetime = Field(
        sa_column=Column("updated_at", TIMESTAMP(precision=3), nullable=False)
    )


class Jwks(SQLModel, table=True):
    __table_args__ = (PrimaryKeyConstraint("id", name="jwks_pkey"),)

    id: str = Field(sa_column=Column("id", Text, primary_key=True))
    publicKey: str = Field(sa_column=Column("publicKey", Text, nullable=False))
    privateKey: str = Field(sa_column=Column("privateKey", Text, nullable=False))
    createdAt: datetime.datetime = Field(
        sa_column=Column(
            "createdAt",
            TIMESTAMP(precision=3),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )
    expiresAt: datetime.datetime | None = Field(
        default=None, sa_column=Column("expiresAt", TIMESTAMP(precision=3))
    )


class ApiKey(SQLModel, table=True):
    __tablename__ = "ApiKey"
    __table_args__ = (
        ForeignKeyConstraint(
            ["userId"],
            ["auth_user.id"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="ApiKey_userId_fkey",
        ),
        PrimaryKeyConstraint("id", name="ApiKey_pkey"),
        Index("ApiKey_key_idx", "key"),
        Index("ApiKey_key_key", "key", unique=True),
        Index("ApiKey_userId_idx", "userId"),
        Index("ApiKey_userId_key", "userId", unique=True),
    )

    id: str = Field(sa_column=Column("id", Text, primary_key=True))
    userId: str = Field(sa_column=Column("userId", Text, nullable=False))
    key: str = Field(sa_column=Column("key", Text, nullable=False))
    name: str = Field(sa_column=Column("name", Text, nullable=False))
    isActive: bool = Field(
        sa_column=Column("isActive", Boolean, nullable=False, server_default=text("true"))
    )
    createdAt: datetime.datetime = Field(
        sa_column=Column(
            "createdAt",
            TIMESTAMP(precision=3),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )
    lastUsed: datetime.datetime = Field(
        sa_column=Column(
            "lastUsed",
            TIMESTAMP(precision=3),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )
    expiresAt: datetime.datetime | None = Field(
        default=None, sa_column=Column("expiresAt", TIMESTAMP(precision=3))
    )

    auth_user: "AuthUser" = Relationship(back_populates="ApiKey_")


class Bot(SQLModel, table=True):
    __tablename__ = "Bot"
    __table_args__ = (
        ForeignKeyConstraint(
            ["handledById"],
            ["auth_user.id"],
            ondelete="SET NULL",
            onupdate="CASCADE",
            name="Bot_handledById_fkey",
        ),
        PrimaryKeyConstraint("id", name="Bot_pkey"),
        Index("Bot_approvedAt_idx", "approvedAt"),
        Index("Bot_createdAt_idx", "createdAt"),
        Index("Bot_featured_idx", "featured"),
        Index("Bot_featured_upvotes_idx", "featured", "upvotes"),
        Index("Bot_handledById_idx", "handledById"),
        Index("Bot_nsfw_idx", "nsfw"),
        Index("Bot_pin_idx", "pin"),
        Index("Bot_servers_idx", "servers"),
        Index("Bot_status_createdAt_idx", "status", "createdAt"),
        Index("Bot_status_featured_idx", "status", "featured"),
        Index("Bot_status_idx", "status"),
        Index("Bot_upvotes_idx", "upvotes"),
        Index("Bot_users_idx", "users"),
        Index("Bot_verified_idx", "verified"),
        Index("Bot_verified_upvotes_idx", "verified", "upvotes"),
    )

    id: str = Field(sa_column=Column("id", Text, primary_key=True))
    name: str = Field(sa_column=Column("name", Text, nullable=False))
    description: str = Field(sa_column=Column("description", Text, nullable=False))
    servers: int = Field(sa_column=Column("servers", Integer, nullable=False))
    users: int = Field(sa_column=Column("users", Integer, nullable=False))
    upvotes: int = Field(sa_column=Column("upvotes", Integer, nullable=False))
    featured: bool = Field(
        sa_column=Column("featured", Boolean, nullable=False, server_default=text("false"))
    )
    createdAt: datetime.datetime = Field(
        sa_column=Column(
            "createdAt",
            TIMESTAMP(precision=3),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )
    verified: bool = Field(
        sa_column=Column("verified", Boolean, nullable=False, server_default=text("false"))
    )
    status: Status = Field(
        sa_column=Column(
            "status",
            Enum(
                Status, values_callable=lambda cls: [member.value for member in cls], name="Status"
            ),
            nullable=False,
            server_default=text("'pending'::\"Status\""),
        )
    )
    isAdmin: bool = Field(
        sa_column=Column("isAdmin", Boolean, nullable=False, server_default=text("false"))
    )
    pin: bool = Field(
        sa_column=Column("pin", Boolean, nullable=False, server_default=text("false"))
    )
    nsfw: bool = Field(
        sa_column=Column("nsfw", Boolean, nullable=False, server_default=text("false"))
    )
    updatedAt: datetime.datetime = Field(
        sa_column=Column(
            "updatedAt",
            TIMESTAMP(precision=3),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )
    longDescription: str | None = Field(default=None, sa_column=Column("longDescription", Text))
    tags: list[str] | None = Field(default=None, sa_column=Column("tags", ARRAY(Text())))
    icon: str | None = Field(default=None, sa_column=Column("icon", Text))
    banner: str | None = Field(default=None, sa_column=Column("banner", Text))
    approvedAt: datetime.datetime | None = Field(
        default=None, sa_column=Column("approvedAt", TIMESTAMP(precision=3))
    )
    prefix: str | None = Field(default=None, sa_column=Column("prefix", Text))
    website: str | None = Field(default=None, sa_column=Column("website", Text))
    inviteUrl: str | None = Field(default=None, sa_column=Column("inviteUrl", Text))
    supportServer: str | None = Field(default=None, sa_column=Column("supportServer", Text))
    features: list[str] | None = Field(default=None, sa_column=Column("features", ARRAY(Text())))
    screenshots: list[str] | None = Field(
        default=None, sa_column=Column("screenshots", ARRAY(Text()))
    )
    handledAt: datetime.datetime | None = Field(
        default=None, sa_column=Column("handledAt", TIMESTAMP(precision=3))
    )
    handledById: str | None = Field(default=None, sa_column=Column("handledById", Text))
    rejectionReason: str | None = Field(default=None, sa_column=Column("rejectionReason", Text))
    VoteNotificationURL: str | None = Field(
        default=None, sa_column=Column("VoteNotificationURL", Text)
    )
    secret: str | None = Field(default=None, sa_column=Column("secret", Text))
    pinExpiry: datetime.datetime | None = Field(
        default=None, sa_column=Column("pinExpiry", TIMESTAMP(precision=3))
    )
    custom_field: dict | None = Field(default=None, sa_column=Column("custom_field", JSONB))
    terms_of_service_url: str | None = Field(
        default=None, sa_column=Column("terms_of_service_url", Text)
    )
    privacy_policy_url: str | None = Field(
        default=None, sa_column=Column("privacy_policy_url", Text)
    )

    auth_user: Optional["AuthUser"] = Relationship(back_populates="Bot_")
    auth_user__BotDevelopers: list["AuthUser"] = Relationship(
        back_populates="Bot__BotDevelopers", sa_relationship_kwargs={"secondary": "_BotDevelopers"}
    )
    auth_user__UserFavoriteBots: list["AuthUser"] = Relationship(
        back_populates="Bot__UserFavoriteBots",
        sa_relationship_kwargs={"secondary": "_UserFavoriteBots"},
    )
    BotCommand_: list[BotCommand] = Relationship(back_populates="Bot_")
    Review_: list[Review] = Relationship(back_populates="Bot_")


class Report(SQLModel, table=True):
    __tablename__ = "Report"
    __table_args__ = (
        ForeignKeyConstraint(
            ["handledById"],
            ["auth_user.id"],
            ondelete="SET NULL",
            onupdate="CASCADE",
            name="Report_handledById_fkey",
        ),
        ForeignKeyConstraint(
            ["reportedById"],
            ["auth_user.id"],
            ondelete="RESTRICT",
            onupdate="CASCADE",
            name="Report_reportedById_fkey",
        ),
        PrimaryKeyConstraint("id", name="Report_pkey"),
        Index("Report_handledById_idx", "handledById"),
        Index("Report_itemId_idx", "itemId"),
        Index("Report_reportedAt_idx", "reportedAt"),
        Index("Report_reportedById_idx", "reportedById"),
        Index("Report_severity_idx", "severity"),
        Index("Report_status_idx", "status"),
        Index("Report_status_reportedAt_idx", "status", "reportedAt"),
        Index("Report_status_severity_idx", "status", "severity"),
        Index("Report_type_idx", "type"),
        Index("Report_type_itemId_idx", "type", "itemId"),
    )

    id: str = Field(sa_column=Column("id", Text, primary_key=True))
    subject: str = Field(sa_column=Column("subject", Text, nullable=False))
    content: str = Field(sa_column=Column("content", Text, nullable=False))
    reportedAt: datetime.datetime = Field(
        sa_column=Column(
            "reportedAt",
            TIMESTAMP(precision=3),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )
    status: Reportstatus = Field(
        sa_column=Column(
            "status",
            Enum(
                Reportstatus,
                values_callable=lambda cls: [member.value for member in cls],
                name="ReportStatus",
            ),
            nullable=False,
            server_default=text("'pending'::\"ReportStatus\""),
        )
    )
    severity: Reportseverity = Field(
        sa_column=Column(
            "severity",
            Enum(
                Reportseverity,
                values_callable=lambda cls: [member.value for member in cls],
                name="ReportSeverity",
            ),
            nullable=False,
            server_default=text("'untagged'::\"ReportSeverity\""),
        )
    )
    type: Reporttype = Field(
        sa_column=Column(
            "type",
            Enum(
                Reporttype,
                values_callable=lambda cls: [member.value for member in cls],
                name="ReportType",
            ),
            nullable=False,
        )
    )
    itemId: str = Field(sa_column=Column("itemId", Text, nullable=False))
    itemName: str = Field(sa_column=Column("itemName", Text, nullable=False))
    reportedById: str = Field(sa_column=Column("reportedById", Text, nullable=False))
    attachments: dict = Field(sa_column=Column("attachments", JSONB, nullable=False))
    reasons: dict = Field(
        sa_column=Column("reasons", JSONB, nullable=False, server_default=text("'[]'::jsonb"))
    )
    handledAt: datetime.datetime | None = Field(
        default=None, sa_column=Column("handledAt", TIMESTAMP(precision=3))
    )
    handledById: str | None = Field(default=None, sa_column=Column("handledById", Text))
    resolutionNote: str | None = Field(default=None, sa_column=Column("resolutionNote", Text))

    auth_user: Optional["AuthUser"] = Relationship(
        back_populates="Report_handledById",
        sa_relationship_kwargs={"foreign_keys": "[Report.handledById]"},
    )
    auth_user_: "AuthUser" = Relationship(
        back_populates="Report_reportedById",
        sa_relationship_kwargs={"foreign_keys": "[Report.reportedById]"},
    )


class Server(SQLModel, table=True):
    __tablename__ = "Server"
    __table_args__ = (
        ForeignKeyConstraint(
            ["ownerId"],
            ["auth_user.discord_id"],
            ondelete="SET NULL",
            onupdate="CASCADE",
            name="Server_ownerId_fkey",
        ),
        PrimaryKeyConstraint("id", name="Server_pkey"),
        Index("Server_createdAt_idx", "createdAt"),
        Index("Server_createdAt_upvotes_idx", "createdAt", "upvotes"),
        Index("Server_featured_idx", "featured"),
        Index("Server_featured_upvotes_idx", "featured", "upvotes"),
        Index("Server_id_ownerId_key", "id", "ownerId", unique=True),
        Index("Server_members_idx", "members"),
        Index("Server_nsfw_idx", "nsfw"),
        Index("Server_ownerId_idx", "ownerId"),
        Index("Server_pin_idx", "pin"),
        Index("Server_upvotes_idx", "upvotes"),
    )

    id: str = Field(sa_column=Column("id", Text, primary_key=True))
    name: str = Field(sa_column=Column("name", Text, nullable=False))
    description: str = Field(sa_column=Column("description", Text, nullable=False))
    members: int = Field(sa_column=Column("members", Integer, nullable=False))
    upvotes: int = Field(sa_column=Column("upvotes", Integer, nullable=False))
    featured: bool = Field(
        sa_column=Column("featured", Boolean, nullable=False, server_default=text("false"))
    )
    createdAt: datetime.datetime = Field(
        sa_column=Column(
            "createdAt",
            TIMESTAMP(precision=3),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )
    ownerId: str = Field(sa_column=Column("ownerId", Text, nullable=False))
    pin: bool = Field(
        sa_column=Column("pin", Boolean, nullable=False, server_default=text("false"))
    )
    nsfw: bool = Field(
        sa_column=Column("nsfw", Boolean, nullable=False, server_default=text("false"))
    )
    longDescription: str | None = Field(default=None, sa_column=Column("longDescription", Text))
    tags: list[str] | None = Field(default=None, sa_column=Column("tags", ARRAY(Text())))
    online: int | None = Field(default=None, sa_column=Column("online", Integer))
    icon: str | None = Field(default=None, sa_column=Column("icon", Text))
    banner: str | None = Field(default=None, sa_column=Column("banner", Text))
    website: str | None = Field(default=None, sa_column=Column("website", Text))
    inviteUrl: str | None = Field(default=None, sa_column=Column("inviteUrl", Text))
    rules: list[str] | None = Field(default=None, sa_column=Column("rules", ARRAY(Text())))
    features: list[str] | None = Field(default=None, sa_column=Column("features", ARRAY(Text())))
    screenshots: list[str] | None = Field(
        default=None, sa_column=Column("screenshots", ARRAY(Text()))
    )
    VoteNotificationURL: str | None = Field(
        default=None, sa_column=Column("VoteNotificationURL", Text)
    )
    secret: str | None = Field(default=None, sa_column=Column("secret", Text))
    pinExpiry: datetime.datetime | None = Field(
        default=None, sa_column=Column("pinExpiry", TIMESTAMP(precision=3))
    )
    custom_field: dict | None = Field(default=None, sa_column=Column("custom_field", JSONB))

    auth_user: "AuthUser" = Relationship(back_populates="Server_")
    auth_user__ServerAdmins: list["AuthUser"] = Relationship(
        back_populates="Server__ServerAdmins", sa_relationship_kwargs={"secondary": "_ServerAdmins"}
    )
    auth_user__UserFavoriteServers: list["AuthUser"] = Relationship(
        back_populates="Server__UserFavoriteServers",
        sa_relationship_kwargs={"secondary": "_UserFavoriteServers"},
    )
    Review_: list[Review] = Relationship(back_populates="Server_")


class Vote(SQLModel, table=True):
    __tablename__ = "Vote"
    __table_args__ = (
        ForeignKeyConstraint(
            ["userId"],
            ["auth_user.id"],
            ondelete="RESTRICT",
            onupdate="CASCADE",
            name="Vote_userId_fkey",
        ),
        PrimaryKeyConstraint("id", name="Vote_pkey"),
        Index("Vote_createdAt_idx", "createdAt"),
        Index("Vote_itemId_idx", "itemId"),
        Index("Vote_itemType_idx", "itemType"),
        Index("Vote_userId_idx", "userId"),
        Index("Vote_userId_itemId_itemType_idx", "userId", "itemId", "itemType"),
    )

    id: str = Field(sa_column=Column("id", Text, primary_key=True))
    userId: str = Field(sa_column=Column("userId", Text, nullable=False))
    itemId: str = Field(sa_column=Column("itemId", Text, nullable=False))
    itemType: Votetype = Field(
        sa_column=Column(
            "itemType",
            Enum(
                Votetype,
                values_callable=lambda cls: [member.value for member in cls],
                name="VoteType",
            ),
            nullable=False,
        )
    )
    createdAt: datetime.datetime = Field(
        sa_column=Column(
            "createdAt",
            TIMESTAMP(precision=3),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )

    auth_user: "AuthUser" = Relationship(back_populates="Vote_")


class AuthAccount(SQLModel, table=True):
    __tablename__ = "auth_account"
    __table_args__ = (
        ForeignKeyConstraint(
            ["user_id"],
            ["auth_user.id"],
            ondelete="CASCADE",
            name="auth_account_user_id_auth_user_id_fk",
        ),
        PrimaryKeyConstraint("id", name="auth_account_pkey"),
        Index("authAccount_userId_idx", "user_id"),
    )

    id: str = Field(sa_column=Column("id", Text, primary_key=True))
    user_id: str = Field(sa_column=Column("user_id", Text, nullable=False))
    account_id: str = Field(sa_column=Column("account_id", Text, nullable=False))
    provider_id: str = Field(sa_column=Column("provider_id", Text, nullable=False))
    created_at: datetime.datetime = Field(
        sa_column=Column(
            "created_at",
            TIMESTAMP(precision=3),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )
    updated_at: datetime.datetime = Field(
        sa_column=Column("updated_at", TIMESTAMP(precision=3), nullable=False)
    )
    access_token: str | None = Field(default=None, sa_column=Column("access_token", Text))
    refresh_token: str | None = Field(default=None, sa_column=Column("refresh_token", Text))
    access_token_expires_at: datetime.datetime | None = Field(
        default=None, sa_column=Column("access_token_expires_at", TIMESTAMP(precision=3))
    )
    refresh_token_expires_at: datetime.datetime | None = Field(
        default=None, sa_column=Column("refresh_token_expires_at", TIMESTAMP(precision=3))
    )
    scope: str | None = Field(default=None, sa_column=Column("scope", Text))
    id_token: str | None = Field(default=None, sa_column=Column("id_token", Text))
    password: str | None = Field(default=None, sa_column=Column("password", Text))
    profile: dict | None = Field(default=None, sa_column=Column("profile", JSONB))

    user: "AuthUser" = Relationship(back_populates="auth_account")


class AuthSession(SQLModel, table=True):
    __tablename__ = "auth_session"
    __table_args__ = (
        ForeignKeyConstraint(
            ["user_id"],
            ["auth_user.id"],
            ondelete="CASCADE",
            name="auth_session_user_id_auth_user_id_fk",
        ),
        PrimaryKeyConstraint("id", name="auth_session_pkey"),
        UniqueConstraint("token", name="auth_session_token_unique"),
        Index("authSession_userId_idx", "user_id"),
    )

    id: str = Field(sa_column=Column("id", Text, primary_key=True))
    user_id: str = Field(sa_column=Column("user_id", Text, nullable=False))
    token: str = Field(sa_column=Column("token", Text, nullable=False))
    expires_at: datetime.datetime = Field(
        sa_column=Column("expires_at", TIMESTAMP(precision=3), nullable=False)
    )
    created_at: datetime.datetime = Field(
        sa_column=Column(
            "created_at",
            TIMESTAMP(precision=3),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )
    updated_at: datetime.datetime = Field(
        sa_column=Column("updated_at", TIMESTAMP(precision=3), nullable=False)
    )
    ip_address: str | None = Field(default=None, sa_column=Column("ip_address", Text))
    user_agent: str | None = Field(default=None, sa_column=Column("user_agent", Text))
    impersonated_by: str | None = Field(default=None, sa_column=Column("impersonated_by", Text))

    user: "AuthUser" = Relationship(back_populates="auth_session")


class AuthUser(SQLModel, table=True):
    __tablename__ = "auth_user"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="auth_user_pkey"),
        UniqueConstraint("discord_id", name="auth_user_discord_id_unique"),
        UniqueConstraint("email", name="auth_user_email_unique"),
        Index("auth_user_created_at_idx", "created_at"),
    )

    id: str = Field(sa_column=Column("id", Text, primary_key=True))
    name: str = Field(sa_column=Column("name", Text, nullable=False))
    email: str = Field(sa_column=Column("email", Text, nullable=False))
    email_verified: bool = Field(
        sa_column=Column("email_verified", Boolean, nullable=False, server_default=text("false"))
    )
    discord_id: str = Field(sa_column=Column("discord_id", Text, nullable=False))
    username: str = Field(
        sa_column=Column(
            "username", Text, nullable=False, server_default=text("'未知使用者'::text")
        )
    )
    avatar: str = Field(
        sa_column=Column(
            "avatar",
            Text,
            nullable=False,
            server_default=text("'https://cdn.discordapp.com/embed/avatars/0.png'::text"),
        )
    )
    created_at: str = Field(
        sa_column=Column("created_at", Text, nullable=False, server_default=text("now()"))
    )
    updated_at: str = Field(
        sa_column=Column("updated_at", Text, nullable=False, server_default=text("now()"))
    )
    global_name: str = Field(
        sa_column=Column(
            "global_name", Text, nullable=False, server_default=text("'未知使用者'::text")
        )
    )
    nsfw: bool = Field(
        sa_column=Column("nsfw", Boolean, nullable=False, server_default=text("true"))
    )
    image: str | None = Field(default=None, sa_column=Column("image", Text))
    banner: str | None = Field(default=None, sa_column=Column("banner", Text))
    banner_color: str | None = Field(default=None, sa_column=Column("banner_color", Text))
    role: str | None = Field(default=None, sa_column=Column("role", Text))
    banned: bool | None = Field(
        default=None, sa_column=Column("banned", Boolean, server_default=text("false"))
    )
    ban_reason: str | None = Field(default=None, sa_column=Column("ban_reason", Text))
    ban_expires: datetime.datetime | None = Field(
        default=None, sa_column=Column("ban_expires", DateTime)
    )
    bio: str | None = Field(default=None, sa_column=Column("bio", Text))
    social: dict | None = Field(default=None, sa_column=Column("social", JSONB))

    ApiKey_: list[ApiKey] = Relationship(back_populates="auth_user")
    Bot_: list[Bot] = Relationship(back_populates="auth_user")
    Bot__BotDevelopers: list[Bot] = Relationship(
        back_populates="auth_user__BotDevelopers",
        sa_relationship_kwargs={"secondary": "_BotDevelopers"},
    )
    Bot__UserFavoriteBots: list[Bot] = Relationship(
        back_populates="auth_user__UserFavoriteBots",
        sa_relationship_kwargs={"secondary": "_UserFavoriteBots"},
    )
    Report_handledById: list[Report] = Relationship(
        back_populates="auth_user", sa_relationship_kwargs={"foreign_keys": "[Report.handledById]"}
    )
    Report_reportedById: list[Report] = Relationship(
        back_populates="auth_user_",
        sa_relationship_kwargs={"foreign_keys": "[Report.reportedById]"},
    )
    Server_: list[Server] = Relationship(back_populates="auth_user")
    Server__ServerAdmins: list[Server] = Relationship(
        back_populates="auth_user__ServerAdmins",
        sa_relationship_kwargs={"secondary": "_ServerAdmins"},
    )
    Server__UserFavoriteServers: list[Server] = Relationship(
        back_populates="auth_user__UserFavoriteServers",
        sa_relationship_kwargs={"secondary": "_UserFavoriteServers"},
    )
    Vote_: list[Vote] = Relationship(back_populates="auth_user")
    auth_account: list[AuthAccount] = Relationship(back_populates="user")
    auth_session: list[AuthSession] = Relationship(back_populates="user")


t__BotDevelopers = Table(
    "_BotDevelopers",
    SQLModel.metadata,
    Column("A", Text, primary_key=True),
    Column("B", Text, primary_key=True),
    ForeignKeyConstraint(
        ["A"], ["Bot.id"], ondelete="CASCADE", onupdate="CASCADE", name="_BotDevelopers_A_fkey"
    ),
    ForeignKeyConstraint(
        ["B"],
        ["auth_user.id"],
        ondelete="CASCADE",
        onupdate="CASCADE",
        name="_BotDevelopers_B_fkey",
    ),
    PrimaryKeyConstraint("A", "B", name="_BotDevelopers_AB_pkey"),
    Index("_BotDevelopers_B_index", "B"),
)


t__ServerAdmins = Table(
    "_ServerAdmins",
    SQLModel.metadata,
    Column("A", Text, primary_key=True),
    Column("B", Text, primary_key=True),
    ForeignKeyConstraint(
        ["A"], ["Server.id"], ondelete="CASCADE", onupdate="CASCADE", name="_ServerAdmins_A_fkey"
    ),
    ForeignKeyConstraint(
        ["B"], ["auth_user.id"], ondelete="CASCADE", onupdate="CASCADE", name="_ServerAdmins_B_fkey"
    ),
    PrimaryKeyConstraint("A", "B", name="_ServerAdmins_AB_pkey"),
    Index("_ServerAdmins_B_index", "B"),
)


t__UserFavoriteBots = Table(
    "_UserFavoriteBots",
    SQLModel.metadata,
    Column("A", Text, primary_key=True),
    Column("B", Text, primary_key=True),
    ForeignKeyConstraint(
        ["A"], ["Bot.id"], ondelete="CASCADE", onupdate="CASCADE", name="_UserFavoriteBots_A_fkey"
    ),
    ForeignKeyConstraint(
        ["B"],
        ["auth_user.id"],
        ondelete="CASCADE",
        onupdate="CASCADE",
        name="_UserFavoriteBots_B_fkey",
    ),
    PrimaryKeyConstraint("A", "B", name="_UserFavoriteBots_AB_pkey"),
    Index("_UserFavoriteBots_B_index", "B"),
)


t__UserFavoriteServers = Table(
    "_UserFavoriteServers",
    SQLModel.metadata,
    Column("A", Text, primary_key=True),
    Column("B", Text, primary_key=True),
    ForeignKeyConstraint(
        ["A"],
        ["Server.id"],
        ondelete="CASCADE",
        onupdate="CASCADE",
        name="_UserFavoriteServers_A_fkey",
    ),
    ForeignKeyConstraint(
        ["B"],
        ["auth_user.id"],
        ondelete="CASCADE",
        onupdate="CASCADE",
        name="_UserFavoriteServers_B_fkey",
    ),
    PrimaryKeyConstraint("A", "B", name="_UserFavoriteServers_AB_pkey"),
    Index("_UserFavoriteServers_B_index", "B"),
)
