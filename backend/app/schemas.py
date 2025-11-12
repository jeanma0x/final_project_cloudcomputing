from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

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
