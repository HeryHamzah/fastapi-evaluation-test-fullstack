"""
User service for business logic operations.
"""
from typing import List, Tuple, Optional
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User, UserStatus, UserRole
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.core.security import get_password_hash
import math


class UserService:
    """Service for user management operations."""
    
    def __init__(self, db: AsyncSession):
        """
        Initialize service with database session.
        
        Args:
            db: Async database session
        """
        self.db = db
        self.user_repo = UserRepository(db)
    
    async def create_user(self, user_data: UserCreate) -> UserResponse:
        """
        Create a new user.
        
        Args:
            user_data: User creation data
            
        Returns:
            UserResponse: Created user
            
        Raises:
            HTTPException: If email already exists
        """
        # Check if email already exists
        if await self.user_repo.exists_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email sudah terdaftar"
            )
        
        # Create user model
        user = User(
            nama=user_data.nama,
            no_telepon=user_data.no_telepon,
            email=user_data.email,
            password=get_password_hash(user_data.password),
            role=user_data.role,
            status_user=user_data.status_user,
            photo_profile=user_data.photo_profile
        )
        
        # Save to database
        user = await self.user_repo.create(user)
        
        return UserResponse.model_validate(user)
    
    async def get_users(
        self,
        page: int = 1,
        limit: int = 10,
        status_filter: Optional[UserStatus] = None,
        search: Optional[str] = None,
        sort_by: str = "nama",
        sort_order: str = "asc"
    ) -> Tuple[List[UserResponse], int, int]:
        """
        Get all users with pagination and filtering.
        
        Args:
            page: Page number
            limit: Items per page
            status_filter: Filter by status
            search: Search by name
            sort_by: Sort field
            sort_order: Sort order
            
        Returns:
            Tuple[List[UserResponse], int, int]: Users, total count, total pages
        """
        skip = (page - 1) * limit
        
        users, total = await self.user_repo.get_all(
            skip=skip,
            limit=limit,
            status_filter=status_filter,
            search=search,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        total_pages = math.ceil(total / limit) if total > 0 else 0
        
        return [UserResponse.model_validate(user) for user in users], total, total_pages
    
    async def get_user_by_id(self, user_id: int) -> UserResponse:
        """
        Get user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            UserResponse: User data
            
        Raises:
            HTTPException: If user not found
        """
        user = await self.user_repo.get_by_id(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User tidak ditemukan"
            )
        
        return UserResponse.model_validate(user)
    
    async def update_user(self, user_id: int, user_data: UserUpdate) -> UserResponse:
        """
        Update user.
        
        Args:
            user_id: User ID to update
            user_data: Updated user data
            
        Returns:
            UserResponse: Updated user
            
        Raises:
            HTTPException: If user not found or email already exists
        """
        user = await self.user_repo.get_by_id(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User tidak ditemukan"
            )
        
        # Check email uniqueness if email is being updated
        if user_data.email and user_data.email != user.email:
            if await self.user_repo.exists_by_email(user_data.email, exclude_id=user_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email sudah terdaftar"
                )
        
        # Update fields
        update_data = user_data.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            if field == "password" and value:
                # Hash password if being updated
                setattr(user, field, get_password_hash(value))
            elif value is not None:
                setattr(user, field, value)
        
        user = await self.user_repo.update(user)
        
        return UserResponse.model_validate(user)
    
    async def delete_user(self, user_id: int) -> None:
        """
        Delete user.
        
        Args:
            user_id: User ID to delete
            
        Raises:
            HTTPException: If user not found
        """
        user = await self.user_repo.get_by_id(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User tidak ditemukan"
            )
        
        await self.user_repo.delete(user)
