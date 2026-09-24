from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    """Shared user fields."""

    email: EmailStr
    full_name: str


class UserCreate(UserBase):
    """Data required to create a user."""

    password: str = Field(min_length=8)


class UserResponse(UserBase):
    """Public user representation."""

    id: int
    role: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class Token(BaseModel):
    """JWT authentication response."""

    access_token: str
    token_type: str = "bearer"