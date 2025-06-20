from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models, crud, schemas
from datetime import datetime

# データベーステーブルを作成
models.Base.metadata.create_all(bind=engine)

def create_test_data():
    db = SessionLocal()
    try:
        # ===== マスターテーブル（マスタ）のテストデータ作成 =====
        
        # 顧客マスタ
        customers_data = [
            {"customer_code": "CUST001", "customer_name": "田中太郎", "email": "tanaka@example.com", "phone": "090-1234-5678", "address": "東京都渋谷区..."},
            {"customer_code": "CUST002", "customer_name": "佐藤花子", "email": "sato@example.com", "phone": "090-2345-6789", "address": "大阪府大阪市..."},
            {"customer_code": "CUST003", "customer_name": "鈴木一郎", "email": "suzuki@example.com", "phone": "090-3456-7890", "address": "愛知県名古屋市..."},
        ]
        
        for customer_data in customers_data:
            if not db.query(models.Customer).filter(models.Customer.customer_code == customer_data["customer_code"]).first():
                customer = schemas.CustomerCreate(**customer_data)
                crud.create_customer(db=db, customer=customer)
                print(f"顧客 {customer_data['customer_name']} を作成しました")
        
        # 商品マスタ
        products_data = [
            {"product_code": "PROD001", "product_name": "商品A", "price": 1000.0, "description": "高品質な商品A"},
            {"product_code": "PROD002", "product_name": "商品B", "price": 2000.0, "description": "人気の商品B"},
            {"product_code": "PROD003", "product_name": "商品C", "price": 1500.0, "description": "お得な商品C"},
        ]
        
        for product_data in products_data:
            if not db.query(models.Product).filter(models.Product.product_code == product_data["product_code"]).first():
                product = schemas.ProductCreate(**product_data)
                crud.create_product(db=db, product=product)
                print(f"商品 {product_data['product_name']} を作成しました")
        
        # 注文ステータスマスタ
        statuses_data = [
            {"status_code": "PENDING", "status_name": "処理中", "description": "注文処理中"},
            {"status_code": "COMPLETED", "status_name": "完了", "description": "注文完了"},
            {"status_code": "CANCELLED", "status_name": "キャンセル", "description": "注文キャンセル"},
        ]
        
        for status_data in statuses_data:
            if not db.query(models.OrderStatus).filter(models.OrderStatus.status_code == status_data["status_code"]).first():
                status = schemas.OrderStatusCreate(**status_data)
                crud.create_order_status(db=db, status=status)
                print(f"ステータス {status_data['status_name']} を作成しました")
        
        # ===== トランザクションテーブル（トラン）のテストデータ作成 =====
        
        # 顧客・商品・ステータスのIDを取得
        customer1 = db.query(models.Customer).filter(models.Customer.customer_code == "CUST001").first()
        customer2 = db.query(models.Customer).filter(models.Customer.customer_code == "CUST002").first()
        customer3 = db.query(models.Customer).filter(models.Customer.customer_code == "CUST003").first()
        
        product1 = db.query(models.Product).filter(models.Product.product_code == "PROD001").first()
        product2 = db.query(models.Product).filter(models.Product.product_code == "PROD002").first()
        product3 = db.query(models.Product).filter(models.Product.product_code == "PROD003").first()
        
        status_pending = db.query(models.OrderStatus).filter(models.OrderStatus.status_code == "PENDING").first()
        status_completed = db.query(models.OrderStatus).filter(models.OrderStatus.status_code == "COMPLETED").first()
        
        # 注文データ
        orders_data = [
            {
                "order_number": "ORD001",
                "customer_id": customer1.id,
                "product_id": product1.id,
                "quantity": 2,
                "unit_price": product1.price,
                "total_price": product1.price * 2,
                "status_id": status_pending.id,
                "notes": "急ぎの注文"
            },
            {
                "order_number": "ORD002",
                "customer_id": customer2.id,
                "product_id": product2.id,
                "quantity": 1,
                "unit_price": product2.price,
                "total_price": product2.price * 1,
                "status_id": status_completed.id,
                "notes": ""
            },
            {
                "order_number": "ORD003",
                "customer_id": customer3.id,
                "product_id": product3.id,
                "quantity": 3,
                "unit_price": product3.price,
                "total_price": product3.price * 3,
                "status_id": status_pending.id,
                "notes": "大量注文"
            },
        ]
        
        for order_data in orders_data:
            if not db.query(models.Order).filter(models.Order.order_number == order_data["order_number"]).first():
                order = schemas.OrderCreate(**order_data)
                crud.create_order(db=db, order=order)
                print(f"注文 {order_data['order_number']} を作成しました")
        
        # ===== インターフェーステーブル（インターフェース）のテストデータ作成 =====
        
        external_orders_data = [
            {
                "external_order_id": "EXT001",
                "external_system": "ECサイトA",
                "order_data": '{"customer": "外部顧客A", "product": "外部商品A", "quantity": 1}'
            },
            {
                "external_order_id": "EXT002",
                "external_system": "ECサイトB",
                "order_data": '{"customer": "外部顧客B", "product": "外部商品B", "quantity": 2}'
            },
        ]
        
        for ext_order_data in external_orders_data:
            if not db.query(models.ExternalOrder).filter(models.ExternalOrder.external_order_id == ext_order_data["external_order_id"]).first():
                ext_order = schemas.ExternalOrderCreate(**ext_order_data)
                crud.create_external_order(db=db, external_order=ext_order)
                print(f"外部注文 {ext_order_data['external_order_id']} を作成しました")
        
        # ===== ワークテーブル（ワーク）のテストデータ作成 =====
        
        # 注文IDを取得
        order1 = db.query(models.Order).filter(models.Order.order_number == "ORD001").first()
        
        order_works_data = [
            {
                "batch_id": "BATCH001",
                "order_id": order1.id,
                "process_type": "注文処理"
            },
        ]
        
        for work_data in order_works_data:
            work = schemas.OrderWorkCreate(**work_data)
            crud.create_order_work(db=db, order_work=work)
            print(f"ワークデータ {work_data['batch_id']} を作成しました")
        
        print("=== テストデータの作成が完了しました ===")
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_data() 