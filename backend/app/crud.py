from sqlalchemy.orm import Session
from . import models, schemas
from .auth import get_password_hash, verify_password

# ユーザー関連のCRUD操作
def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
        is_admin=user.is_admin
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# マスターテーブル関連のCRUD操作
def get_customer(db: Session, customer_id: int):
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()

def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Customer).offset(skip).limit(limit).all()

def create_customer(db: Session, customer: schemas.CustomerCreate):
    db_customer = models.Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_order_status(db: Session, status_id: int):
    return db.query(models.OrderStatus).filter(models.OrderStatus.id == status_id).first()

def get_order_statuses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.OrderStatus).offset(skip).limit(limit).all()

def create_order_status(db: Session, status: schemas.OrderStatusCreate):
    db_status = models.OrderStatus(**status.dict())
    db.add(db_status)
    db.commit()
    db.refresh(db_status)
    return db_status

# 注文関連のCRUD操作
def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Order).offset(skip).limit(limit).all()

def create_order(db: Session, order: schemas.OrderCreate):
    db_order = models.Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def update_order(db: Session, order_id: int, order: schemas.OrderUpdate):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order:
        update_data = order.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_order, field, value)
        db.commit()
        db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: int):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order:
        db.delete(db_order)
        db.commit()
    return db_order

# インターフェーステーブル関連のCRUD操作
def get_external_order(db: Session, external_order_id: int):
    return db.query(models.ExternalOrder).filter(models.ExternalOrder.id == external_order_id).first()

def get_external_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ExternalOrder).offset(skip).limit(limit).all()

def create_external_order(db: Session, external_order: schemas.ExternalOrderCreate):
    db_external_order = models.ExternalOrder(**external_order.dict())
    db.add(db_external_order)
    db.commit()
    db.refresh(db_external_order)
    return db_external_order

# ワークテーブル関連のCRUD操作
def get_order_work(db: Session, work_id: int):
    return db.query(models.OrderWork).filter(models.OrderWork.id == work_id).first()

def get_order_works(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.OrderWork).offset(skip).limit(limit).all()

def create_order_work(db: Session, order_work: schemas.OrderWorkCreate):
    db_order_work = models.OrderWork(**order_work.dict())
    db.add(db_order_work)
    db.commit()
    db.refresh(db_order_work)
    return db_order_work 