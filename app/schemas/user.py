"""
User schemas for request/response validation.
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from app.models.user import UserRole, UserStatus


class UserBase(BaseModel):
    """Base user schema with common fields."""
    nama: str = Field(min_length=1, max_length=255, description="User's full name")
    no_telepon: str = Field(min_length=10, max_length=20, description="Phone number")
    email: EmailStr = Field(description="Email address")


class UserCreate(UserBase):
    """
    Schema for creating a new user.
    
    Example:
        {
            "nama": "John Doe",
            "no_telepon": "081234567890",
            "email": "john@example.com",
            "password": "password123",
            "role": "user",
            "status_user": "aktif",
            "photo_profile": "https://example.com/photo.jpg"
        }
    """
    password: str = Field(min_length=6, description="User password")
    role: UserRole = Field(default=UserRole.USER, description="User role")
    status_user: UserStatus = Field(default=UserStatus.AKTIF, description="User status")
    photo_profile: Optional[str] = Field(None, description="Profile photo URL")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nama": "John Doe",
                "no_telepon": "081234567890",
                "email": "john@example.com",
                "password": "password123",
                "role": "user",
                "status_user": "aktif",
                "photo_profile": "https://example.com/photo.jpg"
            }
        }
    )


class UserUpdate(BaseModel):
    """
    Schema for updating a user (all fields optional).
    
    Example:
        {
            "nama": "John Updated",
            "status_user": "nonaktif"
        }
    """
    nama: Optional[str] = Field(None, min_length=1, max_length=255)
    no_telepon: Optional[str] = Field(None, min_length=10, max_length=20)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)
    role: Optional[UserRole] = None
    status_user: Optional[UserStatus] = None
    photo_profile: Optional[str] = None
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nama": "John Updated",
                "status_user": "nonaktif"
            }
        }
    )


class UserResponse(UserBase):
    """
    Schema for user response.
    
    Example:
        {
            "id": 1,
            "nama": "John Doe",
            "no_telepon": "081234567890",
            "email": "john@example.com",
            "role": "user",
            "status_user": "aktif",
            "photo_profile": "https://example.com/photo.jpg",
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00"
        }
    """
    id: int
    role: UserRole
    status_user: UserStatus
    photo_profile: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class UserListResponse(BaseModel):
    """
    Simplified user response for list views.
    """
    id: int
    nama: str
    email: EmailStr
    no_telepon: str
    role: UserRole
    status_user: UserStatus
    photo_profile: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
