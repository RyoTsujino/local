from app.database import SessionLocal
from app import crud, schemas

def add_test_user():
    db = SessionLocal()
    try:
        test_user = schemas.UserCreate(
            username="testUser1",
            email="testuser1@example.com",
            full_name="テストユーザー1",
            password="password"
        )
        if not crud.get_user(db, username="testUser1"):
            crud.create_user(db=db, user=test_user)
            print("testUser1 を追加しました")
        else:
            print("testUser1 は既に存在します")
    finally:
        db.close()

if __name__ == "__main__":
    add_test_user() 