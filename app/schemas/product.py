"""
Product schemas for request/response validation.
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, field_validator
from app.models.product import ProductStatus


class ProductBase(BaseModel):
    """Base product schema with common fields."""
    nama_produk: str = Field(min_length=1, max_length=255, description="Product name")
    kategori: str = Field(min_length=1, max_length=100, description="Product category")
    deskripsi: Optional[str] = Field(None, description="Product description")
    harga_satuan: float = Field(gt=0, description="Unit price")


class ProductCreate(ProductBase):
    """
    Schema for creating a new product.
    
    Example:
        {
            "nama_produk": "Laptop ASUS ROG",
            "kategori": "Electronics",
            "deskripsi": "Gaming laptop with RTX 4060",
            "harga_satuan": 15000000,
            "stok_awal": 10,
            "gambar": ["https://example.com/img1.jpg", "https://example.com/img2.jpg"],
            "status_produk": "aktif",
            "threshold_stok": 5,
            "diskon": 10.0,
            "rating": 4.5
        }
    """
    stok_awal: int = Field(ge=0, description="Initial stock quantity")
    gambar: Optional[List[str]] = Field(default=[], description="List of image URLs")
    status_produk: ProductStatus = Field(default=ProductStatus.AKTIF, description="Product status")
    threshold_stok: Optional[int] = Field(None, ge=0, description="Minimum stock threshold")
    diskon: Optional[float] = Field(0.0, ge=0, le=100, description="Discount percentage (0-100)")
    rating: Optional[float] = Field(0.0, ge=0, le=5, description="Product rating (0-5)")
    jumlah_terjual: Optional[int] = Field(0, ge=0, description="Number of units sold")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nama_produk": "Laptop ASUS ROG",
                "kategori": "Electronics",
                "deskripsi": "Gaming laptop with RTX 4060",
                "harga_satuan": 15000000.0,
                "stok_awal": 10,
                "gambar": ["https://example.com/img1.jpg"],
                "status_produk": "aktif",
                "threshold_stok": 5,
                "diskon": 10.0,
                "rating": 4.5
            }
        }
    )


class ProductUpdate(BaseModel):
    """
    Schema for full product update (all fields optional).
    
    Example:
        {
            "nama_produk": "Updated Product Name",
            "harga_satuan": 16000000,
            "diskon": 15.0
        }
    """
    nama_produk: Optional[str] = Field(None, min_length=1, max_length=255)
    kategori: Optional[str] = Field(None, min_length=1, max_length=100)
    deskripsi: Optional[str] = None
    harga_satuan: Optional[float] = Field(None, gt=0)
    stok_awal: Optional[int] = Field(None, ge=0)
    stok: Optional[int] = Field(None, ge=0)
    gambar: Optional[List[str]] = None
    status_produk: Optional[ProductStatus] = None
    threshold_stok: Optional[int] = Field(None, ge=0)
    diskon: Optional[float] = Field(None, ge=0, le=100)
    rating: Optional[float] = Field(None, ge=0, le=5)
    jumlah_terjual: Optional[int] = Field(None, ge=0)
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nama_produk": "Updated Product Name",
                "harga_satuan": 16000000.0,
                "diskon": 15.0
            }
        }
    )


class ProductStatusUpdate(BaseModel):
    """
    Schema for updating only product status.
    
    Example:
        {
            "status_produk": "nonaktif"
        }
    """
    status_produk: ProductStatus = Field(description="Product status")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status_produk": "nonaktif"
            }
        }
    )


class ProductStockUpdate(BaseModel):
    """
    Schema for updating product stock.
    
    Example:
        {
            "adjustment": -5,
            "operation": "subtract"
        }
    """
    adjustment: int = Field(description="Stock adjustment amount")
    operation: str = Field(description="Operation: 'add' or 'subtract'")
    
    @field_validator('operation')
    @classmethod
    def validate_operation(cls, v: str) -> str:
        if v not in ['add', 'subtract']:
            raise ValueError("operation must be 'add' or 'subtract'")
        return v
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "adjustment": 5,
                "operation": "add"
            }
        }
    )


class ProductResponse(ProductBase):
    """
    Schema for product response.
    
    Example:
        {
            "id": 1,
            "nama_produk": "Laptop ASUS ROG",
            "kategori": "Electronics",
            "deskripsi": "Gaming laptop",
            "harga_satuan": 15000000,
            "stok_awal": 10,
            "stok": 8,
            "gambar": ["https://example.com/img1.jpg"],
            "status_produk": "aktif",
            "threshold_stok": 5,
            "diskon": 10.0,
            "rating": 4.5,
            "jumlah_terjual": 2,
            "harga_setelah_diskon": 13500000.0,
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00"
        }
    """
    id: int
    stok_awal: int
    stok: int
    gambar: List[str]
    status_produk: ProductStatus
    threshold_stok: Optional[int] = None
    diskon: float
    rating: float
    jumlah_terjual: int
    harga_setelah_diskon: float
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ProductListResponse(BaseModel):
    """
    Simplified product response for list views with calculated fields.
    """
    id: int
    nama_produk: str
    kategori: str
    harga_satuan: float
    stok: int
    status_produk: ProductStatus
    diskon: float
    rating: float
    jumlah_terjual: int
    harga_setelah_diskon: float
    gambar: List[str]
    
    model_config = ConfigDict(from_attributes=True)
