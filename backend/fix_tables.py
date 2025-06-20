import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    user="postgres",
    password="kyokaden",
    database="order_management"
)

cur = conn.cursor()
try:
    # 問題のあるテーブルを削除して再作成
    cur.execute("DROP TABLE IF EXISTS products CASCADE;")
    cur.execute("DROP TABLE IF EXISTS order_items CASCADE;")
    
    # 商品テーブルを正しく作成
    cur.execute("""
        CREATE TABLE products (
            id SERIAL PRIMARY KEY,
            product_code VARCHAR UNIQUE NOT NULL,
            product_name VARCHAR NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            description TEXT,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE
        );
    """)
    
    # usersテーブルも修正
    cur.execute("DROP TABLE IF EXISTS users CASCADE;")
    cur.execute("""
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            username VARCHAR UNIQUE NOT NULL,
            email VARCHAR UNIQUE NOT NULL,
            full_name VARCHAR NOT NULL,
            hashed_password VARCHAR NOT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            is_admin BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    conn.commit()
    print("テーブルの修正が完了しました。")
    
except Exception as e:
    print(f"エラー: {e}")
    conn.rollback()
finally:
    cur.close()
    conn.close() 