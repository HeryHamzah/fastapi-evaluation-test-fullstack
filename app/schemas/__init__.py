"""
Pydantic schemas for request/response validation.
"""
from app.schemas.user import (
    UserCreate, UserUpdate, UserResponse, UserListResponse
)
from app.schemas.product import (
    ProductCreate, ProductUpdate, ProductResponse, ProductListResponse,
    ProductStatusUpdate, ProductStockUpdate
)
from app.schemas.auth import (
    Token, TokenData, LoginRequest, LoginResponse
)
from app.schemas.common import (
    PaginationParams, PaginatedResponse, MessageResponse
)

__all__ = [
    "UserCreate", "UserUpdate", "UserResponse", "UserListResponse",
    "ProductCreate", "ProductUpdate", "ProductResponse", "ProductListResponse",
    "ProductStatusUpdate", "ProductStockUpdate",
    "Token", "TokenData", "LoginRequest", "LoginResponse",
    "PaginationParams", "PaginatedResponse", "MessageResponse"
]
