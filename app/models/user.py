"""
User ORM model.
"""
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base
import enum


class UserRole(str, enum.Enum):
    """User role enumeration."""
    ADMIN = "admin"
    USER = "user"


class UserStatus(str, enum.Enum):
    """User status enumeration."""
    AKTIF = "aktif"
    NONAKTIF = "nonaktif"


class User(Base):
    """
    User model for authentication and user management.
    
    Attributes:
        id: Primary key
        nama: User's full name
        no_telepon: Phone number
        email: Email address (unique)
        password: Hashed password
        role: User role (admin/user)
        status_user: Account status (aktif/nonaktif)
        photo_profile: URL or path to profile photo
        created_at: Timestamp when user was created
        updated_at: Timestamp when user was last updated
    """
    
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nama: Mapped[str] = mapped_column(String(255), nullable=False)
    no_telepon: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole, native_enum=False, length=20),
        default=UserRole.USER,
        nullable=False
    )
    status_user: Mapped[UserStatus] = mapped_column(
        SQLEnum(UserStatus, native_enum=False, length=20),
        default=UserStatus.AKTIF,
        nullable=False
    )
    photo_profile: Mapped[str] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
