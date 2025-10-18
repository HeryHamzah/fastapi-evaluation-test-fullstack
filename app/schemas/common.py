"""
Common schemas used across the application.
"""
from typing import TypeVar, Generic, List, Optional
from pydantic import BaseModel, Field, ConfigDict


T = TypeVar('T')


class PaginationParams(BaseModel):
    """
    Standard pagination parameters.
    
    Example:
        GET /api/v1/users?page=1&limit=10
    """
    page: int = Field(default=1, ge=1, description="Page number (starts from 1)")
    limit: int = Field(default=10, ge=1, le=100, description="Items per page")
    
    @property
    def offset(self) -> int:
        """Calculate offset from page and limit."""
        return (self.page - 1) * self.limit


class PaginatedResponse(BaseModel, Generic[T]):
    """
    Generic paginated response wrapper.
    
    Example response:
        {
            "items": [...],
            "total": 100,
            "page": 1,
            "limit": 10,
            "pages": 10
        }
    """
    items: List[T]
    total: int = Field(description="Total number of items")
    page: int = Field(description="Current page number")
    limit: int = Field(description="Items per page")
    pages: int = Field(description="Total number of pages")
    
    model_config = ConfigDict(from_attributes=True)


class MessageResponse(BaseModel):
    """
    Simple message response.
    
    Example:
        {"message": "Operation successful"}
    """
    message: str = Field(description="Response message")
    
    model_config = ConfigDict(from_attributes=True)
