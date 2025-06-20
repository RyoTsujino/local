from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# ===== マスターテーブル用スキーマ =====
class CustomerBase(BaseModel):
    customer_code: str
    customer_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    product_code: str
    product_name: str
    price: float
    description: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class OrderStatusBase(BaseModel):
    status_code: str
    status_name: str
    description: Optional[str] = None

class OrderStatusCreate(OrderStatusBase):
    pass

class OrderStatus(OrderStatusBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# ===== トランザクションテーブル用スキーマ =====
class OrderBase(BaseModel):
    order_number: str
    customer_id: int
    product_id: int
    quantity: int
    unit_price: float
    total_price: float
    status_id: int
    notes: Optional[str] = None

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    order_number: Optional[str] = None
    customer_id: Optional[int] = None
    product_id: Optional[int] = None
    quantity: Optional[int] = None
    unit_price: Optional[float] = None
    total_price: Optional[float] = None
    status_id: Optional[int] = None
    notes: Optional[str] = None

class Order(OrderBase):
    id: int
    order_date: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None
    customer: Customer
    product: Product
    status: OrderStatus

    class Config:
        from_attributes = True

# ===== インターフェーステーブル用スキーマ =====
class ExternalOrderBase(BaseModel):
    external_order_id: str
    external_system: str
    order_data: str

class ExternalOrderCreate(ExternalOrderBase):
    pass

class ExternalOrder(ExternalOrderBase):
    id: int
    status: str
    processed_at: Optional[datetime] = None
    created_at: datetime
    error_message: Optional[str] = None

    class Config:
        from_attributes = True

# ===== ワークテーブル用スキーマ =====
class OrderWorkBase(BaseModel):
    batch_id: str
    order_id: int
    process_type: str

class OrderWorkCreate(OrderWorkBase):
    pass

class OrderWork(OrderWorkBase):
    id: int
    status: str
    created_at: datetime
    processed_at: Optional[datetime] = None
    error_message: Optional[str] = None

    class Config:
        from_attributes = True

# ===== 認証用スキーマ（既存） =====
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class UserBase(BaseModel):
    username: str
    email: str
    full_name: str
    is_admin: bool = False

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True 