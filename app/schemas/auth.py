"""
Authentication related schemas.
"""
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, ConfigDict


class LoginRequest(BaseModel):
    """
    Login request payload.
    
    Example:
        {
            "email": "user@example.com",
            "password": "password123"
        }
    """
    email: EmailStr = Field(description="User email address")
    password: str = Field(min_length=6, description="User password")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "admin@example.com",
                "password": "admin123"
            }
        }
    )


class Token(BaseModel):
    """
    JWT token response.
    
    Example:
        {
            "access_token": "eyJ...",
            "token_type": "bearer"
        }
    """
    access_token: str = Field(description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")


class TokenData(BaseModel):
    """
    Decoded token data.
    """
    email: Optional[str] = None
    role: Optional[str] = None
    user_id: Optional[int] = None


class LoginResponse(BaseModel):
    """
    Complete login response with user info.
    
    Example:
        {
            "access_token": "eyJ...",
            "token_type": "bearer",
            "user": {
                "id": 1,
                "email": "user@example.com",
                "nama": "John Doe",
                "role": "admin"
            }
        }
    """
    access_token: str = Field(description="JWT access token")
    refresh_token: Optional[str] = Field(None, description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Token type")
    user: dict = Field(description="User information")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user": {
                    "id": 1,
                    "email": "admin@example.com",
                    "nama": "Administrator",
                    "role": "admin"
                }
            }
        }
    )
