from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models, crud, schemas

# データベーステーブルを作成
models.Base.metadata.create_all(bind=engine)

def create_initial_data():
    db = SessionLocal()
    try:
        # 管理者ユーザーの作成
        admin_user = schemas.UserCreate(
            username="admin",
            email="admin@example.com",
            full_name="管理者",
            password="admin123",
            is_admin=True
        )
        
        # 一般ユーザーの作成
        user = schemas.UserCreate(
            username="user",
            email="user@example.com",
            full_name="一般ユーザー",
            password="user123",
            is_admin=False
        )
        
        # ユーザーが存在しない場合のみ作成
        if not crud.get_user(db, username="admin"):
            crud.create_user(db=db, user=admin_user)
            print("管理者ユーザーを作成しました")
        
        if not crud.get_user(db, username="user"):
            crud.create_user(db=db, user=user)
            print("一般ユーザーを作成しました")
        
        # サンプル注文データの作成
        sample_orders = [
            schemas.OrderCreate(
                customer_name="田中太郎",
                product_name="商品A",
                quantity=2,
                price=1000.0,
                notes="急ぎの注文"
            ),
            schemas.OrderCreate(
                customer_name="佐藤花子",
                product_name="商品B",
                quantity=1,
                price=2000.0,
                notes=""
            ),
            schemas.OrderCreate(
                customer_name="鈴木一郎",
                product_name="商品C",
                quantity=3,
                price=1500.0,
                notes="大量注文"
            )
        ]
        
        for order_data in sample_orders:
            crud.create_order(db=db, order=order_data)
        
        print("サンプル注文データを作成しました")
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_initial_data()
    print("初期データの作成が完了しました") 