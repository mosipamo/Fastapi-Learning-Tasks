from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


def _now() -> datetime:
    return datetime.now(timezone.utc)


class User(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=False)
    created_at: datetime = Field(default_factory=_now)


class UserCreate(SQLModel):
    username: str
    email: str
