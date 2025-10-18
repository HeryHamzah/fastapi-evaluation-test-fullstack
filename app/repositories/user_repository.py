"""
User repository for database operations.
"""
from typing import List, Optional, Tuple
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User, UserStatus


class UserRepository:
    """Repository for User database operations."""
    
    def __init__(self, db: AsyncSession):
        """
        Initialize repository with database session.
        
        Args:
            db: Async database session
        """
        self.db = db
    
    async def create(self, user: User) -> User:
        """
        Create a new user.
        
        Args:
            user: User model instance
            
        Returns:
            User: Created user
        """
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Get user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            Optional[User]: User if found, None otherwise
        """
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email.
        
        Args:
            email: User email
            
        Returns:
            Optional[User]: User if found, None otherwise
        """
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
    
    async def get_all(
        self,
        skip: int = 0,
        limit: int = 10,
        status_filter: Optional[UserStatus] = None,
        search: Optional[str] = None,
        sort_by: str = "nama",
        sort_order: str = "asc"
    ) -> Tuple[List[User], int]:
        """
        Get all users with filtering, searching, sorting and pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            status_filter: Filter by user status
            search: Search term for name
            sort_by: Field to sort by
            sort_order: Sort order (asc/desc)
            
        Returns:
            Tuple[List[User], int]: List of users and total count
        """
        # Base query
        query = select(User)
        count_query = select(func.count(User.id))
        
        # Apply filters
        if status_filter:
            query = query.where(User.status_user == status_filter)
            count_query = count_query.where(User.status_user == status_filter)
        
        if search:
            search_filter = User.nama.ilike(f"%{search}%")
            query = query.where(search_filter)
            count_query = count_query.where(search_filter)
        
        # Apply sorting
        sort_column = getattr(User, sort_by, User.nama)
        if sort_order.lower() == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())
        
        # Apply pagination
        query = query.offset(skip).limit(limit)
        
        # Execute queries
        result = await self.db.execute(query)
        users = result.scalars().all()
        
        count_result = await self.db.execute(count_query)
        total = count_result.scalar()
        
        return list(users), total
    
    async def update(self, user: User) -> User:
        """
        Update a user.
        
        Args:
            user: User model instance with updated data
            
        Returns:
            User: Updated user
        """
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def delete(self, user: User) -> None:
        """
        Delete a user.
        
        Args:
            user: User model instance to delete
        """
        await self.db.delete(user)
        await self.db.commit()
    
    async def exists_by_email(self, email: str, exclude_id: Optional[int] = None) -> bool:
        """
        Check if user with email exists.
        
        Args:
            email: Email to check
            exclude_id: Optional user ID to exclude from check
            
        Returns:
            bool: True if exists, False otherwise
        """
        query = select(func.count(User.id)).where(User.email == email)
        if exclude_id:
            query = query.where(User.id != exclude_id)
        
        result = await self.db.execute(query)
        count = result.scalar()
        return count > 0
