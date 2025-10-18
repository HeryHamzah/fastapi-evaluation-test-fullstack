"""
Product management routes.
"""
from typing import Optional
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.schemas.product import (
    ProductCreate, ProductUpdate, ProductResponse, ProductListResponse,
    ProductStatusUpdate, ProductStockUpdate
)
from app.schemas.common import PaginatedResponse, MessageResponse
from app.services.product_service import ProductService
from app.api.deps.auth import get_current_active_user, get_current_admin_user
from app.models.user import User


router = APIRouter(prefix="/products", tags=["Product Management"])


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Product",
    description="""
    Create a new product.
    
    **Request Body:**
    - `nama_produk`: Product name (required)
    - `kategori`: Product category (required)
    - `deskripsi`: Product description (optional)
    - `harga_satuan`: Unit price (required, > 0)
    - `stok_awal`: Initial stock (required, >= 0)
    - `gambar`: List of image URLs (optional)
    - `status_produk`: Product status (aktif/nonaktif, default: aktif)
    - `threshold_stok`: Minimum stock threshold (optional)
    - `diskon`: Discount percentage 0-100 (optional, default: 0)
    - `rating`: Product rating 0-5 (optional, default: 0)
    - `jumlah_terjual`: Units sold (optional, default: 0)
    
    **Note:** Product status will be automatically calculated based on stock and threshold.
    """
)
async def create_product(
    product_data: ProductCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new product.
    """
    product_service = ProductService(db)
    return await product_service.create_product(product_data)


@router.get(
    "",
    response_model=PaginatedResponse[ProductListResponse],
    status_code=status.HTTP_200_OK,
    summary="Get All Products",
    description="""
    Get paginated list of products with filtering and sorting.
    
    **Query Parameters:**
    - `page`: Page number (default: 1)
    - `limit`: Items per page (default: 10, max: 100)
    - `kategori`: Filter by category
    - `status`: Filter by status (aktif/nonaktif/menipis)
    - `search`: Search by product name
    - `sort_by`: Sort field (nama_produk, harga_satuan, stok, kategori)
    - `sort_order`: Sort order (asc/desc, default: asc)
    
    **Response:**
    - Paginated list with calculated fields (harga_setelah_diskon, etc.)
    """
)
async def get_products(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    kategori: Optional[str] = Query(None, description="Filter by category"),
    status: Optional[str] = Query(None, description="Filter by status (aktif/nonaktif/menipis)"),
    search: Optional[str] = Query(None, description="Search by product name"),
    sort_by: str = Query("nama_produk", description="Sort by field"),
    sort_order: str = Query("asc", description="Sort order (asc/desc)"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get all products with pagination and filtering.
    """
    product_service = ProductService(db)
    products, total, total_pages = await product_service.get_products(
        page=page,
        limit=limit,
        kategori=kategori,
        status_filter=status,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order
    )
    
    return PaginatedResponse(
        items=products,
        total=total,
        page=page,
        limit=limit,
        pages=total_pages
    )


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Product by ID",
    description="""
    Get detailed information about a specific product by ID.
    
    **Response includes:**
    - All product fields
    - Calculated field: `harga_setelah_diskon`
    """
)
async def get_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get product by ID with calculated price after discount.
    """
    product_service = ProductService(db)
    return await product_service.get_product_by_id(product_id)


@router.put(
    "/{product_id}",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
    summary="Update Product (Full Update)",
    description="""
    Full update of product. All fields are optional.
    
    **Use cases:**
    1. Update all product information
    2. Update specific fields only
    
    **Request Body (all optional):**
    - `nama_produk`: Product name
    - `kategori`: Category
    - `deskripsi`: Description
    - `harga_satuan`: Unit price
    - `stok_awal`: Initial stock
    - `stok`: Current stock
    - `gambar`: Image URLs
    - `status_produk`: Status
    - `threshold_stok`: Stock threshold
    - `diskon`: Discount percentage
    - `rating`: Rating
    - `jumlah_terjual`: Units sold
    
    **Note:** Status will be recalculated if not explicitly set.
    """
)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Full update of product.
    """
    product_service = ProductService(db)
    return await product_service.update_product(product_id, product_data)


@router.patch(
    "/{product_id}/status",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
    summary="Update Product Status Only",
    description="""
    Update only the product status (aktif/nonaktif).
    
    **Request Body:**
    ```json
    {
        "status_produk": "nonaktif"
    }
    ```
    """
)
async def update_product_status(
    product_id: int,
    status_data: ProductStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update product status only.
    """
    product_service = ProductService(db)
    return await product_service.update_product_status(product_id, status_data)


@router.patch(
    "/{product_id}/stock",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
    summary="Update Product Stock",
    description="""
    Add or subtract product stock.
    
    **Request Body:**
    ```json
    {
        "adjustment": 5,
        "operation": "add"
    }
    ```
    
    **Operations:**
    - `add`: Increase stock
    - `subtract`: Decrease stock (will validate sufficient stock)
    
    **Note:** Status will be recalculated after stock update.
    """
)
async def update_product_stock(
    product_id: int,
    stock_data: ProductStockUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update product stock (add or subtract).
    """
    product_service = ProductService(db)
    return await product_service.update_product_stock(product_id, stock_data)


@router.delete(
    "/{product_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete Product",
    description="""
    Delete a product by ID.
    """
)
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete product.
    """
    product_service = ProductService(db)
    await product_service.delete_product(product_id)
    return MessageResponse(message="Produk berhasil dihapus")
