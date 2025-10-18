"""
Upload related schemas.
"""
from typing import List
from pydantic import BaseModel, Field


class FileUploadResponse(BaseModel):
    """
    Response for single file upload.
    
    Example:
        {
            "filename": "product_image.jpg",
            "url": "/uploads/abc123.jpg",
            "size": 102400
        }
    """
    filename: str = Field(description="Original filename")
    url: str = Field(description="File URL path")
    size: int = Field(description="File size in bytes")


class MultipleFileUploadResponse(BaseModel):
    """
    Response for multiple file upload.
    
    Example:
        {
            "files": [
                {
                    "filename": "image1.jpg",
                    "url": "/uploads/abc123.jpg",
                    "size": 102400
                },
                {
                    "filename": "image2.jpg",
                    "url": "/uploads/def456.jpg",
                    "size": 204800
                }
            ],
            "count": 2
        }
    """
    files: List[FileUploadResponse] = Field(description="List of uploaded files")
    count: int = Field(description="Number of files uploaded")
