"""
User management routes (Admin only).
"""
from typing import Optional
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserListResponse
from app.schemas.common import PaginatedResponse, MessageResponse
from app.services.user_service import UserService
from app.api.deps.auth import get_current_admin_user
from app.models.user import User, UserStatus


router = APIRouter(prefix="/users", tags=["User Management"])


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create User (Admin Only)",
    description="""
    Create a new user. Only accessible by admin users.
    
    **Request Body:**
    - `nama`: Full name (required)
    - `no_telepon`: Phone number (required)
    - `email`: Email address (required, unique)
    - `password`: Password (required, min 6 characters)
    - `role`: User role (admin/user, default: user)
    - `status_user`: User status (aktif/nonaktif, default: aktif)
    - `photo_profile`: Profile photo URL (optional)
    """
)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """
    Create a new user (admin only).
    """
    user_service = UserService(db)
    return await user_service.create_user(user_data)


@router.get(
    "",
    response_model=PaginatedResponse[UserListResponse],
    status_code=status.HTTP_200_OK,
    summary="Get All Users (Admin Only)",
    description="""
    Get paginated list of users with filtering and sorting.
    
    **Query Parameters:**
    - `page`: Page number (default: 1)
    - `limit`: Items per page (default: 10, max: 100)
    - `status`: Filter by status (aktif/nonaktif)
    - `search`: Search by name
    - `sort_by`: Sort field (nama, email, created_at)
    - `sort_order`: Sort order (asc/desc, default: asc)
    
    **Response:**
    - Paginated list with total count and page info
    """
)
async def get_users(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    status: Optional[UserStatus] = Query(None, description="Filter by status"),
    search: Optional[str] = Query(None, description="Search by name"),
    sort_by: str = Query("nama", description="Sort by field"),
    sort_order: str = Query("asc", description="Sort order (asc/desc)"),
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """
    Get all users with pagination and filtering (admin only).
    """
    user_service = UserService(db)
    users, total, total_pages = await user_service.get_users(
        page=page,
        limit=limit,
        status_filter=status,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order
    )
    
    return PaginatedResponse(
        items=users,
        total=total,
        page=page,
        limit=limit,
        pages=total_pages
    )


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get User by ID (Admin Only)",
    description="""
    Get detailed information about a specific user by ID.
    """
)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """
    Get user by ID (admin only).
    """
    user_service = UserService(db)
    return await user_service.get_user_by_id(user_id)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Update User (Admin Only)",
    description="""
    Update user information. All fields are optional.
    
    **Request Body (all optional):**
    - `nama`: Full name
    - `no_telepon`: Phone number
    - `email`: Email address (must be unique)
    - `password`: New password (will be hashed)
    - `role`: User role
    - `status_user`: User status
    - `photo_profile`: Profile photo URL
    """
)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """
    Update user (admin only).
    """
    user_service = UserService(db)
    return await user_service.update_user(user_id, user_data)


@router.delete(
    "/{user_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete User (Admin Only)",
    description="""
    Delete a user by ID.
    """
)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """
    Delete user (admin only).
    """
    user_service = UserService(db)
    await user_service.delete_user(user_id)
    return MessageResponse(message="User berhasil dihapus")
