from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    ForeignKey,
    Float,
    Enum,
    UniqueConstraint,
    DateTime,
    func,
)
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.db.database import Base

# ---------- ENUMS ----------

class SizeEnum(PyEnum):
    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"
    XXL = "XXL"


# ---------- MODELS ----------

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text, nullable=False)
    lifetime_guarantee = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

    variants = relationship(
        "ProductVariant",
        back_populates="product",
        cascade="all, delete"
    )

    images = relationship(
        "ProductImage",
        back_populates="product",
        cascade="all, delete"
    )

    # Products this product recommends
    recommendations = relationship(
        "ProductRecommendation",
        foreign_keys="[ProductRecommendation.base_product_id]",
        back_populates="base_product",
        cascade="all, delete",
    )

    # Products that recommend this product
    recommended_in = relationship(
        "ProductRecommendation",
        foreign_keys="[ProductRecommendation.recommended_product_id]",
        back_populates="recommended_product",
        cascade="all, delete",
    )

    def __repr__(self):
        return f"<Product(name='{self.name}', price={self.price})>"


class ProductVariant(Base):
    __tablename__ = "product_variants"
    __table_args__ = (UniqueConstraint("product_id", "color", "size", name="uq_variant"),)

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    color = Column(String(50), nullable=False)
    size = Column(Enum(SizeEnum), nullable=False)
    in_stock = Column(Boolean, default=False)

    product = relationship("Product", back_populates="variants")

    def __repr__(self):
        return f"<ProductVariant(product={self.product_id}, color={self.color}, size={self.size})>"


class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    color = Column(String(50), nullable=True)
    image_url = Column(String(255), nullable=False)

    product = relationship("Product", back_populates="images")

    def __repr__(self):
        return f"<ProductImage(product={self.product_id}, color={self.color})>"


class ProductRecommendation(Base):
    __tablename__ = "product_recommendations"
    __table_args__ = (
        UniqueConstraint("base_product_id", "recommended_product_id", name="uq_recommendation"),
    )

    id = Column(Integer, primary_key=True)
    base_product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    recommended_product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))

    base_product = relationship(
        "Product",
        foreign_keys=[base_product_id],
        back_populates="recommendations",
    )

    recommended_product = relationship(
        "Product",
        foreign_keys=[recommended_product_id],
        back_populates="recommended_in",
    )

    def __repr__(self):
        return f"<ProductRecommendation(base={self.base_product_id}, rec={self.recommended_product_id})>"


class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True)
    session_id = Column(String(128), nullable=False, unique=True)
    created_at = Column(DateTime, server_default=func.now())

    items = relationship("CartItem", back_populates="cart", cascade="all, delete")

    def __repr__(self):
        return f"<Cart(session='{self.session_id}')>"


class CartItem(Base):
    __tablename__ = "cart_items"
    __table_args__ = (UniqueConstraint("cart_id", "variant_id", name="uq_cart_item"),)

    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey("carts.id", ondelete="CASCADE"))
    variant_id = Column(Integer, ForeignKey("product_variants.id", ondelete="CASCADE"))
    quantity = Column(Integer, default=1)

    cart = relationship("Cart", back_populates="items")
    variant = relationship("ProductVariant")

    def __repr__(self):
        return f"<CartItem(variant={self.variant_id}, qty={self.quantity})>"
