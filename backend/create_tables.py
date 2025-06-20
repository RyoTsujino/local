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
    # マスターテーブル（マスタ）
    
    # 顧客テーブル
    cur.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id SERIAL PRIMARY KEY,
            customer_code VARCHAR UNIQUE NOT NULL,
            customer_name VARCHAR NOT NULL,
            email VARCHAR,
            phone VARCHAR,
            address TEXT,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE
        );
    """)
    
    # 商品テーブル
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
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
    
    # 注文ステータステーブル
    cur.execute("""
        CREATE TABLE IF NOT EXISTS order_statuses (
            id SERIAL PRIMARY KEY,
            status_code VARCHAR UNIQUE NOT NULL,
            status_name VARCHAR NOT NULL,
            description TEXT,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    # トランザクションテーブル（トラン）
    
    # 注文テーブル（既存のordersテーブルを更新）
    cur.execute("""
        DROP TABLE IF EXISTS orders CASCADE;
        CREATE TABLE orders (
            id SERIAL PRIMARY KEY,
            order_number VARCHAR UNIQUE NOT NULL,
            customer_id INTEGER REFERENCES customers(id),
            product_id INTEGER REFERENCES products(id),
            quantity INTEGER NOT NULL,
            unit_price DECIMAL(10,2) NOT NULL,
            total_price DECIMAL(10,2) NOT NULL,
            status_id INTEGER REFERENCES order_statuses(id),
            order_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE,
            notes TEXT
        );
    """)
    
    # インターフェーステーブル（インターフェース）
    
    # 外部注文テーブル
    cur.execute("""
        CREATE TABLE IF NOT EXISTS external_orders (
            id SERIAL PRIMARY KEY,
            external_order_id VARCHAR UNIQUE NOT NULL,
            external_system VARCHAR NOT NULL,
            order_data TEXT NOT NULL,
            status VARCHAR DEFAULT 'pending',
            processed_at TIMESTAMP WITH TIME ZONE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            error_message TEXT
        );
    """)
    
    # ワークテーブル（ワーク）
    
    # 注文ワークテーブル
    cur.execute("""
        CREATE TABLE IF NOT EXISTS order_works (
            id SERIAL PRIMARY KEY,
            batch_id VARCHAR NOT NULL,
            order_id INTEGER REFERENCES orders(id),
            process_type VARCHAR NOT NULL,
            status VARCHAR DEFAULT 'pending',
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            processed_at TIMESTAMP WITH TIME ZONE,
            error_message TEXT
        );
    """)
    
    conn.commit()
    print("テーブルの作成が完了しました。")
    
except Exception as e:
    print(f"エラー: {e}")
    conn.rollback()
finally:
    cur.close()
    conn.close() 