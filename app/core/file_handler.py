"""
File handling utilities for upload and storage.
"""
import os
import uuid
from typing import List, Optional
from pathlib import Path
from fastapi import UploadFile, HTTPException, status
from app.core.config import settings


# Allowed image extensions
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


def get_upload_dir() -> Path:
    """Get or create upload directory."""
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)
    return upload_dir


def get_file_extension(filename: str) -> str:
    """Get file extension from filename."""
    return Path(filename).suffix.lower()


def is_valid_image(filename: str) -> bool:
    """Check if file is a valid image."""
    ext = get_file_extension(filename)
    return ext in ALLOWED_IMAGE_EXTENSIONS


def generate_unique_filename(original_filename: str) -> str:
    """Generate unique filename with UUID."""
    ext = get_file_extension(original_filename)
    unique_id = uuid.uuid4().hex
    return f"{unique_id}{ext}"


async def save_upload_file(file: UploadFile) -> str:
    """
    Save uploaded file and return the file URL.
    
    Args:
        file: UploadFile from FastAPI
        
    Returns:
        str: Relative URL path to the uploaded file
        
    Raises:
        HTTPException: If file validation fails
    """
    # Validate file type
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename tidak valid"
        )
    
    if not is_valid_image(file.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Format file tidak didukung. Gunakan: {', '.join(ALLOWED_IMAGE_EXTENSIONS)}"
        )
    
    # Read file content
    content = await file.read()
    file_size = len(content)
    
    # Validate file size
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ukuran file terlalu besar. Maksimal {MAX_FILE_SIZE / (1024*1024)}MB"
        )
    
    # Generate unique filename
    unique_filename = generate_unique_filename(file.filename)
    
    # Save file
    upload_dir = get_upload_dir()
    file_path = upload_dir / unique_filename
    
    with open(file_path, "wb") as f:
        f.write(content)
    
    # Return URL path
    return f"/uploads/{unique_filename}"


async def save_multiple_files(files: List[UploadFile]) -> List[str]:
    """
    Save multiple uploaded files.
    
    Args:
        files: List of UploadFile from FastAPI
        
    Returns:
        List[str]: List of relative URL paths
    """
    if len(files) > 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maksimal 10 file per upload"
        )
    
    urls = []
    for file in files:
        url = await save_upload_file(file)
        urls.append(url)
    
    return urls


def delete_file(file_url: str) -> bool:
    """
    Delete file from storage.
    
    Args:
        file_url: Relative URL path (e.g., "/uploads/abc123.jpg")
        
    Returns:
        bool: True if deleted, False if file not found
    """
    try:
        # Extract filename from URL
        filename = Path(file_url).name
        file_path = get_upload_dir() / filename
        
        if file_path.exists():
            file_path.unlink()
            return True
        return False
    except Exception:
        return False


def delete_multiple_files(file_urls: List[str]) -> int:
    """
    Delete multiple files from storage.
    
    Args:
        file_urls: List of relative URL paths
        
    Returns:
        int: Number of files successfully deleted
    """
    deleted_count = 0
    for url in file_urls:
        if delete_file(url):
            deleted_count += 1
    return deleted_count
