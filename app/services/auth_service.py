"""
Authentication service for login/logout operations.
"""
from typing import Optional, Dict, Any
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User, UserStatus
from app.repositories.user_repository import UserRepository
from app.core.security import verify_password, create_access_token, create_refresh_token
from app.schemas.auth import LoginRequest, LoginResponse


class AuthService:
    """Service for authentication operations."""
    
    def __init__(self, db: AsyncSession):
        """
        Initialize service with database session.
        
        Args:
            db: Async database session
        """
        self.db = db
        self.user_repo = UserRepository(db)
    
    async def login(self, login_data: LoginRequest) -> LoginResponse:
        """
        Authenticate user and generate JWT tokens.
        
        Args:
            login_data: Login credentials
            
        Returns:
            LoginResponse: Access token and user info
            
        Raises:
            HTTPException: If credentials are invalid or user is inactive
        """
        # Get user by email
        user = await self.user_repo.get_by_email(login_data.email)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email atau password salah"
            )
        
        # Verify password
        if not verify_password(login_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email atau password salah"
            )
        
        # Check if user is active
        if user.status_user == UserStatus.NONAKTIF:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Akun Anda tidak aktif. Hubungi administrator."
            )
        
        # Create tokens
        token_data = {
            "sub": user.email,
            "user_id": user.id,
            "role": user.role.value
        }
        
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)
        
        # Prepare user info
        user_info = {
            "id": user.id,
            "email": user.email,
            "nama": user.nama,
            "role": user.role.value,
            "status_user": user.status_user.value
        }
        
        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user=user_info
        )
    
    async def logout(self, user_id: int) -> Dict[str, str]:
        """
        Logout user (placeholder for token blacklist implementation).
        
        Args:
            user_id: User ID to logout
            
        Returns:
            Dict: Success message
            
        Note:
            In production, implement token blacklist or use Redis for revocation
        """
        # In a real implementation, you would:
        # 1. Add token to blacklist
        # 2. Use Redis to store revoked tokens
        # 3. Check blacklist on each authenticated request
        
        return {"message": "Logout berhasil"}
