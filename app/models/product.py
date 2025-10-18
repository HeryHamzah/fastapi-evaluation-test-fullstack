"""
Product ORM model.
"""
from datetime import datetime
from sqlalchemy import String, Text, Float, Integer, DateTime, Enum as SQLEnum, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base
import enum


class ProductStatus(str, enum.Enum):
    """Product status enumeration."""
    AKTIF = "aktif"
    NONAKTIF = "nonaktif"
    MENIPIS = "menipis"


class Product(Base):
    """
    Product model for product management.
    
    Attributes:
        id: Primary key
        nama_produk: Product name
        kategori: Product category
        deskripsi: Product description
        harga_satuan: Unit price
        stok_awal: Initial stock
        stok: Current stock (updated from stok_awal)
        gambar: List of image URLs (stored as JSON)
        status_produk: Product status (aktif/nonaktif/menipis)
        threshold_stok: Minimum stock threshold for "menipis" status
        diskon: Discount percentage (0-100)
        rating: Product rating (0-5)
        jumlah_terjual: Number of units sold
        created_at: Timestamp when product was created
        updated_at: Timestamp when product was last updated
    """
    
    __tablename__ = "products"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nama_produk: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    kategori: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    deskripsi: Mapped[str] = mapped_column(Text, nullable=True)
    harga_satuan: Mapped[float] = mapped_column(Float, nullable=False)
    stok_awal: Mapped[int] = mapped_column(Integer, nullable=False)
    stok: Mapped[int] = mapped_column(Integer, nullable=False)
    gambar: Mapped[list] = mapped_column(JSON, nullable=True, default=list)
    status_produk: Mapped[ProductStatus] = mapped_column(
        SQLEnum(ProductStatus, native_enum=False, length=20),
        default=ProductStatus.AKTIF,
        nullable=False,
        index=True
    )
    threshold_stok: Mapped[int] = mapped_column(Integer, nullable=True)
    
    # Optional fields for display
    diskon: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    rating: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    jumlah_terjual: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
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
        return f"<Product(id={self.id}, nama={self.nama_produk}, stok={self.stok})>"
    
    @property
    def harga_setelah_diskon(self) -> float:
        """Calculate price after discount."""
        if self.diskon > 0:
            return self.harga_satuan * (1 - self.diskon / 100)
        return self.harga_satuan
