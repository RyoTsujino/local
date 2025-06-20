from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# ===== マスターテーブル（マスタ） =====
class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    customer_code = Column(String, unique=True, index=True)
    customer_name = Column(String, index=True)
    email = Column(String)
    phone = Column(String)
    address = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    product_code = Column(String, unique=True, index=True)
    product_name = Column(String, index=True)
    price = Column(Float)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class OrderStatus(Base):
    __tablename__ = "order_statuses"

    id = Column(Integer, primary_key=True, index=True)
    status_code = Column(String, unique=True, index=True)
    status_name = Column(String)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# ===== トランザクションテーブル（トラン） =====
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String, unique=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    unit_price = Column(Float)
    total_price = Column(Float)
    status_id = Column(Integer, ForeignKey("order_statuses.id"))
    order_date = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    notes = Column(Text, nullable=True)
    
    # リレーションシップ
    customer = relationship("Customer")
    product = relationship("Product")
    status = relationship("OrderStatus")

# ===== インターフェーステーブル（インターフェース） =====
class ExternalOrder(Base):
    __tablename__ = "external_orders"

    id = Column(Integer, primary_key=True, index=True)
    external_order_id = Column(String, unique=True, index=True)
    external_system = Column(String)  # 外部システム名
    order_data = Column(Text)  # JSON形式の外部データ
    status = Column(String, default="pending")  # pending, processed, error
    processed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    error_message = Column(Text, nullable=True)

# ===== ワークテーブル（ワーク） =====
class OrderWork(Base):
    __tablename__ = "order_works"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(String, index=True)  # バッチ処理ID
    order_id = Column(Integer, ForeignKey("orders.id"))
    process_type = Column(String)  # 処理種別
    status = Column(String, default="pending")  # pending, processing, completed, error
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)
    error_message = Column(Text, nullable=True)
    
    # リレーションシップ
    order = relationship("Order") 