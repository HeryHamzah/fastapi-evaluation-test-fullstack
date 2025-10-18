"""
FastAPI main application entry point.
"""
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from app.core.config import settings
from app.api.routes import auth, users, products, upload
from app.database.session import engine
from app.database.base import Base
from app.models import User, Product  # Import models for metadata
from app.core.security import get_password_hash
from app.models.user import UserRole, UserStatus
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler for startup and shutdown events.
    """
    # Startup
    print("🚀 Starting application...")
    
    # Create uploads directory if it doesn't exist
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)
    print("📁 Upload directory ready")
    
    # Create tables if they don't exist (for development only)
    # In production, use Alembic migrations
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create default admin user if not exists
    from app.database.session import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.email == settings.ADMIN_EMAIL))
        admin = result.scalar_one_or_none()
        
        if not admin:
            admin = User(
                nama=settings.ADMIN_NAME,
                no_telepon="0000000000",
                email=settings.ADMIN_EMAIL,
                password=get_password_hash(settings.ADMIN_PASSWORD),
                role=UserRole.ADMIN,
                status_user=UserStatus.AKTIF,
                photo_profile=None
            )
            session.add(admin)
            await session.commit()
            print(f"✅ Default admin user created: {settings.ADMIN_EMAIL}")
        else:
            print(f"✅ Admin user already exists: {settings.ADMIN_EMAIL}")
    
    print("✨ Application started successfully!")
    
    yield
    
    # Shutdown
    print("👋 Shutting down application...")
    await engine.dispose()


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    ## Product Management API
    
    Complete RESTful API for managing products and users with JWT authentication.
    
    ### Features:
    - 🔐 JWT Authentication with role-based access control
    - 👥 User Management (Admin only)
    - 📦 Product Management with advanced filtering
    - 📊 Pagination, Sorting, and Search
    - 🔍 Status tracking (aktif/nonaktif/menipis)
    - 💰 Price calculation with discounts
    - 📤 File upload for images
    
    ### Authentication:
    1. Click "Authorize" button and login with email & password
    2. Or get token from `/api/v1/auth/login` endpoint
    3. Use token in Authorization header: `Bearer <token>`
    
    ### Roles:
    - **Admin**: Full access to all endpoints
    - **User**: Access to product endpoints only
    
    ### Default Admin Credentials:
    - Email: admin@example.com
    - Password: admin123
    
    **⚠️ Change the default admin password in production!**
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
    debug=settings.DEBUG
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(users.router, prefix=settings.API_V1_PREFIX)
app.include_router(products.router, prefix=settings.API_V1_PREFIX)
app.include_router(upload.router, prefix=settings.API_V1_PREFIX)

# Mount static files for uploaded images
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with API information.
    """
    return {
        "message": "Product Management API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    """
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
