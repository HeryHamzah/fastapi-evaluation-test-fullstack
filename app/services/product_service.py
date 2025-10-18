"""
Product service for business logic operations.
"""
from typing import List, Tuple, Optional
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.product import Product, ProductStatus
from app.repositories.product_repository import ProductRepository
from app.schemas.product import (
    ProductCreate, ProductUpdate, ProductResponse, ProductListResponse,
    ProductStatusUpdate, ProductStockUpdate
)
import math


class ProductService:
    """Service for product management operations."""
    
    def __init__(self, db: AsyncSession):
        """
        Initialize service with database session.
        
        Args:
            db: Async database session
        """
        self.db = db
        self.product_repo = ProductRepository(db)
    
    def _calculate_status(self, product: Product) -> ProductStatus:
        """
        Calculate product status based on stock and threshold.
        
        Args:
            product: Product instance
            
        Returns:
            ProductStatus: Calculated status
        """
        # If manually set to nonaktif, keep it
        if product.status_produk == ProductStatus.NONAKTIF:
            return ProductStatus.NONAKTIF
        
        # Check if stock is low (menipis)
        if product.threshold_stok is not None and product.stok <= product.threshold_stok:
            return ProductStatus.MENIPIS
        
        # Otherwise aktif
        return ProductStatus.AKTIF
    
    async def create_product(self, product_data: ProductCreate) -> ProductResponse:
        """
        Create a new product.
        
        Args:
            product_data: Product creation data
            
        Returns:
            ProductResponse: Created product
        """
        # Create product model
        product = Product(
            nama_produk=product_data.nama_produk,
            kategori=product_data.kategori,
            deskripsi=product_data.deskripsi,
            harga_satuan=product_data.harga_satuan,
            stok_awal=product_data.stok_awal,
            stok=product_data.stok_awal,  # Initialize stok with stok_awal
            gambar=product_data.gambar or [],
            status_produk=product_data.status_produk,
            threshold_stok=product_data.threshold_stok,
            diskon=product_data.diskon or 0.0,
            rating=product_data.rating or 0.0,
            jumlah_terjual=product_data.jumlah_terjual or 0
        )
        
        # Calculate initial status
        product.status_produk = self._calculate_status(product)
        
        # Save to database
        product = await self.product_repo.create(product)
        
        return ProductResponse.model_validate(product)
    
    async def get_products(
        self,
        page: int = 1,
        limit: int = 10,
        kategori: Optional[str] = None,
        status_filter: Optional[str] = None,
        search: Optional[str] = None,
        sort_by: str = "nama_produk",
        sort_order: str = "asc"
    ) -> Tuple[List[ProductListResponse], int, int]:
        """
        Get all products with pagination and filtering.
        
        Args:
            page: Page number
            limit: Items per page
            kategori: Filter by category
            status_filter: Filter by status
            search: Search by name
            sort_by: Sort field
            sort_order: Sort order
            
        Returns:
            Tuple[List[ProductListResponse], int, int]: Products, total count, total pages
        """
        skip = (page - 1) * limit
        
        products, total = await self.product_repo.get_all(
            skip=skip,
            limit=limit,
            kategori=kategori,
            status_filter=status_filter,
            search=search,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        total_pages = math.ceil(total / limit) if total > 0 else 0
        
        return [ProductListResponse.model_validate(product) for product in products], total, total_pages
    
    async def get_product_by_id(self, product_id: int) -> ProductResponse:
        """
        Get product by ID.
        
        Args:
            product_id: Product ID
            
        Returns:
            ProductResponse: Product data with harga_setelah_diskon
            
        Raises:
            HTTPException: If product not found
        """
        product = await self.product_repo.get_by_id(product_id)
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produk tidak ditemukan"
            )
        
        return ProductResponse.model_validate(product)
    
    async def update_product(self, product_id: int, product_data: ProductUpdate) -> ProductResponse:
        """
        Full update of product.
        
        Args:
            product_id: Product ID to update
            product_data: Updated product data
            
        Returns:
            ProductResponse: Updated product
            
        Raises:
            HTTPException: If product not found
        """
        product = await self.product_repo.get_by_id(product_id)
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produk tidak ditemukan"
            )
        
        # Update fields
        update_data = product_data.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            if value is not None:
                setattr(product, field, value)
        
        # Recalculate status if not explicitly set
        if "status_produk" not in update_data:
            product.status_produk = self._calculate_status(product)
        
        product = await self.product_repo.update(product)
        
        return ProductResponse.model_validate(product)
    
    async def update_product_status(
        self,
        product_id: int,
        status_data: ProductStatusUpdate
    ) -> ProductResponse:
        """
        Update only product status.
        
        Args:
            product_id: Product ID
            status_data: New status
            
        Returns:
            ProductResponse: Updated product
            
        Raises:
            HTTPException: If product not found
        """
        product = await self.product_repo.get_by_id(product_id)
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produk tidak ditemukan"
            )
        
        product.status_produk = status_data.status_produk
        product = await self.product_repo.update(product)
        
        return ProductResponse.model_validate(product)
    
    async def update_product_stock(
        self,
        product_id: int,
        stock_data: ProductStockUpdate
    ) -> ProductResponse:
        """
        Update product stock (add or subtract).
        
        Args:
            product_id: Product ID
            stock_data: Stock adjustment data
            
        Returns:
            ProductResponse: Updated product
            
        Raises:
            HTTPException: If product not found or insufficient stock
        """
        product = await self.product_repo.get_by_id(product_id)
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produk tidak ditemukan"
            )
        
        # Validate stock operation
        if stock_data.operation == "subtract" and product.stok < stock_data.adjustment:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Stok tidak mencukupi. Stok tersedia: {product.stok}"
            )
        
        # Update stock
        product = await self.product_repo.update_stock(
            product, stock_data.adjustment, stock_data.operation
        )
        
        # Recalculate status based on new stock
        product.status_produk = self._calculate_status(product)
        product = await self.product_repo.update(product)
        
        return ProductResponse.model_validate(product)
    
    async def delete_product(self, product_id: int) -> None:
        """
        Delete product.
        
        Args:
            product_id: Product ID to delete
            
        Raises:
            HTTPException: If product not found
        """
        product = await self.product_repo.get_by_id(product_id)
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produk tidak ditemukan"
            )
        
        await self.product_repo.delete(product)
