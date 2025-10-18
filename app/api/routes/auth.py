"""
Authentication routes for login and logout.
"""
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.schemas.auth import LoginRequest, LoginResponse, Token
from app.schemas.common import MessageResponse
from app.services.auth_service import AuthService
from app.api.deps.auth import get_current_active_user
from app.models.user import User


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/token",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="OAuth2 Token (for Swagger UI)",
    description="""
    OAuth2 compatible token endpoint for Swagger UI Authorize button.
    
    **Form Data:**
    - `username`: User email address (use email here)
    - `password`: User password
    
    **Response:**
    - `access_token`: JWT token for authentication
    - `token_type`: Always "bearer"
    
    **Note:** Use email as username. This endpoint is for Swagger UI compatibility.
    For programmatic access, use `/login` endpoint instead.
    """
)
async def get_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    OAuth2 password flow token endpoint (for Swagger UI).
    Username field should contain the email address.
    """
    # Create LoginRequest from form data (username is actually email)
    login_data = LoginRequest(
        email=form_data.username,  # Swagger UI sends email as username
        password=form_data.password
    )
    
    auth_service = AuthService(db)
    result = await auth_service.login(login_data)
    
    # Return only token data (OAuth2 standard)
    return Token(
        access_token=result.access_token,
        token_type=result.token_type
    )


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="User Login",
    description="""
    Authenticate user and receive JWT access token.
    
    **Request Body:**
    - `email`: User email address
    - `password`: User password
    
    **Response:**
    - `access_token`: JWT token for authentication
    - `refresh_token`: JWT refresh token
    - `token_type`: Always "bearer"
    - `user`: User information (id, email, nama, role)
    
    **Example:**
    ```json
    {
        "email": "admin@example.com",
        "password": "admin123"
    }
    ```
    """
)
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Login endpoint for user authentication.
    """
    auth_service = AuthService(db)
    return await auth_service.login(login_data)


@router.post(
    "/logout",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="User Logout",
    description="""
    Logout current user.
    
    **Note:** This is a placeholder endpoint. In production, implement token blacklist
    or use Redis for token revocation.
    
    **Headers:**
    - `Authorization`: Bearer {access_token}
    """
)
async def logout(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Logout endpoint (placeholder for token revocation).
    """
    auth_service = AuthService(db)
    result = await auth_service.logout(current_user.id)
    return MessageResponse(message=result["message"])
