"""
File upload routes.
"""
from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, status
from app.schemas.upload import FileUploadResponse, MultipleFileUploadResponse
from app.core.file_handler import save_upload_file, save_multiple_files
from app.api.deps.auth import get_current_active_user
from app.models.user import User


router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post(
    "/image",
    response_model=FileUploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload Single Image",
    description="""
    Upload single image file.
    
    **Supported formats:** JPG, JPEG, PNG, GIF, WEBP, SVG  
    **Max size:** 5MB
    
    **Response:**
    - `filename`: Original filename
    - `url`: File URL path (use this for photo_profile or gambar field)
    - `size`: File size in bytes
    
    **Authentication:** Required
    """
)
async def upload_single_image(
    file: UploadFile = File(..., description="Image file to upload"),
    current_user: User = Depends(get_current_active_user)
):
    """
    Upload a single image file.
    Returns the URL that can be used in photo_profile or gambar fields.
    """
    url = await save_upload_file(file)
    
    return FileUploadResponse(
        filename=file.filename or "unknown",
        url=url,
        size=file.size or 0
    )


@router.post(
    "/images",
    response_model=MultipleFileUploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload Multiple Images",
    description="""
    Upload multiple image files at once (max 10 files).
    
    **Supported formats:** JPG, JPEG, PNG, GIF, WEBP, SVG  
    **Max size per file:** 5MB  
    **Max files:** 10
    
    **Response:**
    - `files`: Array of uploaded file info
    - `count`: Number of files uploaded
    
    **Use case:** Upload product images
    
    **Authentication:** Required
    """
)
async def upload_multiple_images(
    files: List[UploadFile] = File(..., description="Multiple image files"),
    current_user: User = Depends(get_current_active_user)
):
    """
    Upload multiple image files.
    Returns array of URLs that can be used in product gambar field.
    """
    urls = await save_multiple_files(files)
    
    file_responses = [
        FileUploadResponse(
            filename=file.filename or "unknown",
            url=url,
            size=file.size or 0
        )
        for file, url in zip(files, urls)
    ]
    
    return MultipleFileUploadResponse(
        files=file_responses,
        count=len(file_responses)
    )
