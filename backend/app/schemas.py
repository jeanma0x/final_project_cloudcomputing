from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, EmailStr, Field

# ------- Request models -------
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str | None = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# ------- Response models -------
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in_minutes: int

class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str | None = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True  # permite convertir desde ORM (SQLAlchemy)


class BackupResponse(BaseModel):
    status: Literal["ok"] = "ok"
    file: str
    size_bytes: int
    created_at: datetime
    triggered_by: EmailStr


class AuditLogOut(BaseModel):
    id: int
    action: str
    actor_email: str | None = None
    payload: dict[str, Any] | None = None
    created_at: datetime

    class Config:
        from_attributes = True
