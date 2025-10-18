"""
Product repository for database operations.
"""
from typing import List, Optional, Tuple
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.product import Product, ProductStatus


class ProductRepository:
    """Repository for Product database operations."""
    
    def __init__(self, db: AsyncSession):
        """
        Initialize repository with database session.
        
        Args:
            db: Async database session
        """
        self.db = db
    
    async def create(self, product: Product) -> Product:
        """
        Create a new product.
        
        Args:
            product: Product model instance
            
        Returns:
            Product: Created product
        """
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product
    
    async def get_by_id(self, product_id: int) -> Optional[Product]:
        """
        Get product by ID.
        
        Args:
            product_id: Product ID
            
        Returns:
            Optional[Product]: Product if found, None otherwise
        """
        result = await self.db.execute(
            select(Product).where(Product.id == product_id)
        )
        return result.scalar_one_or_none()
    
    async def get_all(
        self,
        skip: int = 0,
        limit: int = 10,
        kategori: Optional[str] = None,
        status_filter: Optional[str] = None,
        search: Optional[str] = None,
        sort_by: str = "nama_produk",
        sort_order: str = "asc"
    ) -> Tuple[List[Product], int]:
        """
        Get all products with filtering, searching, sorting and pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            kategori: Filter by category
            status_filter: Filter by status (aktif/nonaktif/menipis)
            search: Search term for product name
            sort_by: Field to sort by
            sort_order: Sort order (asc/desc)
            
        Returns:
            Tuple[List[Product], int]: List of products and total count
        """
        # Base query
        query = select(Product)
        count_query = select(func.count(Product.id))
        
        # Apply filters
        if kategori:
            query = query.where(Product.kategori == kategori)
            count_query = count_query.where(Product.kategori == kategori)
        
        if status_filter:
            # Handle special "menipis" status
            if status_filter == "menipis":
                query = query.where(
                    Product.status_produk == ProductStatus.AKTIF,
                    Product.threshold_stok.isnot(None),
                    Product.stok <= Product.threshold_stok
                )
                count_query = count_query.where(
                    Product.status_produk == ProductStatus.AKTIF,
                    Product.threshold_stok.isnot(None),
                    Product.stok <= Product.threshold_stok
                )
            else:
                query = query.where(Product.status_produk == status_filter)
                count_query = count_query.where(Product.status_produk == status_filter)
        
        if search:
            search_filter = Product.nama_produk.ilike(f"%{search}%")
            query = query.where(search_filter)
            count_query = count_query.where(search_filter)
        
        # Apply sorting
        sort_column = getattr(Product, sort_by, Product.nama_produk)
        if sort_order.lower() == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())
        
        # Apply pagination
        query = query.offset(skip).limit(limit)
        
        # Execute queries
        result = await self.db.execute(query)
        products = result.scalars().all()
        
        count_result = await self.db.execute(count_query)
        total = count_result.scalar()
        
        return list(products), total
    
    async def update(self, product: Product) -> Product:
        """
        Update a product.
        
        Args:
            product: Product model instance with updated data
            
        Returns:
            Product: Updated product
        """
        await self.db.commit()
        await self.db.refresh(product)
        return product
    
    async def delete(self, product: Product) -> None:
        """
        Delete a product.
        
        Args:
            product: Product model instance to delete
        """
        await self.db.delete(product)
        await self.db.commit()
    
    async def update_stock(self, product: Product, adjustment: int, operation: str) -> Product:
        """
        Update product stock.
        
        Args:
            product: Product to update
            adjustment: Amount to adjust
            operation: 'add' or 'subtract'
            
        Returns:
            Product: Updated product
        """
        if operation == "add":
            product.stok += adjustment
        elif operation == "subtract":
            product.stok -= adjustment
        
        await self.db.commit()
        await self.db.refresh(product)
        return product
