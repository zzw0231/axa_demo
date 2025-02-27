from datetime import datetime

import pytz
from pydantic import BaseModel, EmailStr, Field, field_validator

from app.utils.sanitization import sanitize_input


class BaseUserSchema(BaseModel):
    """Base schema with shared validation logic"""

    name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Name must be between 1 and 50 characters",
    )
    email: EmailStr

    @field_validator("email", mode="before")
    @classmethod
    def to_lowercase(cls, value: str) -> str:
        """Convert email to lowercase before EmailStr validation"""
        if not value:
            return value
        return value.lower()

    @field_validator("name", mode="before")
    @classmethod
    def sanitize_name(cls, value: str) -> str:
        """Sanitizes input and removes extra spaces"""
        if value is None:
            return value

        return sanitize_input(value.strip())

    @field_validator("name", mode="before")
    @classmethod
    def name_must_not_be_empty(cls, value: str) -> str:
        """Ensure name is not empty after stripping spaces"""
        if value is None:
            return value

        if not value.strip():
            raise ValueError("Name cannot be empty or just spaces")
        return value


# Schema for creating a new user (API Request)
class UserCreate(BaseUserSchema):
    pass


# Schema for updating a user (API Request)
class UserUpdate(BaseUserSchema):
    name: str | None = Field(
        None,
        min_length=1,
        max_length=50,
        description="Name must be between 1 and 50 characters",
    )
    email: EmailStr | None = None


# Schema for API Response (Returning user data)
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

    @field_validator("created_at", mode="before")
    def convert_timezone(cls, value):
        """Convert UTC timestamp to America/New_York before returning"""
        local_tz = pytz.timezone("America/New_York")
        return value.astimezone(local_tz)

    class Config:
        from_attributes = True  # Allows SQLAlchemy ORM to Pydantic conversion
