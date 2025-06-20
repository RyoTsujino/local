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
    # ===== マスターテーブル（マスタ）のテストデータ挿入 =====
    
    # 顧客マスタ
    cur.execute("""
        INSERT INTO customers (customer_code, customer_name, email, phone, address) VALUES
        ('CUST001', '田中太郎', 'tanaka@example.com', '090-1234-5678', '東京都渋谷区...'),
        ('CUST002', '佐藤花子', 'sato@example.com', '090-2345-6789', '大阪府大阪市...'),
        ('CUST003', '鈴木一郎', 'suzuki@example.com', '090-3456-7890', '愛知県名古屋市...')
        ON CONFLICT (customer_code) DO NOTHING;
    """)
    print("顧客マスタのテストデータを挿入しました")
    
    # 商品マスタ
    cur.execute("""
        INSERT INTO products (product_code, product_name, price, description) VALUES
        ('PROD001', '商品A', 1000.00, '高品質な商品A'),
        ('PROD002', '商品B', 2000.00, '人気の商品B'),
        ('PROD003', '商品C', 1500.00, 'お得な商品C')
        ON CONFLICT (product_code) DO NOTHING;
    """)
    print("商品マスタのテストデータを挿入しました")
    
    # 注文ステータスマスタ
    cur.execute("""
        INSERT INTO order_statuses (status_code, status_name, description) VALUES
        ('PENDING', '処理中', '注文処理中'),
        ('COMPLETED', '完了', '注文完了'),
        ('CANCELLED', 'キャンセル', '注文キャンセル')
        ON CONFLICT (status_code) DO NOTHING;
    """)
    print("注文ステータスマスタのテストデータを挿入しました")
    
    # ===== トランザクションテーブル（トラン）のテストデータ挿入 =====
    
    # 注文データ
    cur.execute("""
        INSERT INTO orders (order_number, customer_id, product_id, quantity, unit_price, total_price, status_id, notes) VALUES
        ('ORD001', (SELECT id FROM customers WHERE customer_code = 'CUST001'), 
                (SELECT id FROM products WHERE product_code = 'PROD001'), 
                2, 1000.00, 2000.00, 
                (SELECT id FROM order_statuses WHERE status_code = 'PENDING'), 
                '急ぎの注文'),
        ('ORD002', (SELECT id FROM customers WHERE customer_code = 'CUST002'), 
                (SELECT id FROM products WHERE product_code = 'PROD002'), 
                1, 2000.00, 2000.00, 
                (SELECT id FROM order_statuses WHERE status_code = 'COMPLETED'), 
                ''),
        ('ORD003', (SELECT id FROM customers WHERE customer_code = 'CUST003'), 
                (SELECT id FROM products WHERE product_code = 'PROD003'), 
                3, 1500.00, 4500.00, 
                (SELECT id FROM order_statuses WHERE status_code = 'PENDING'), 
                '大量注文')
        ON CONFLICT (order_number) DO NOTHING;
    """)
    print("注文データのテストデータを挿入しました")
    
    # ===== インターフェーステーブル（インターフェース）のテストデータ挿入 =====
    
    # 外部注文データ
    cur.execute("""
        INSERT INTO external_orders (external_order_id, external_system, order_data) VALUES
        ('EXT001', 'ECサイトA', '{"customer": "外部顧客A", "product": "外部商品A", "quantity": 1}'),
        ('EXT002', 'ECサイトB', '{"customer": "外部顧客B", "product": "外部商品B", "quantity": 2}')
        ON CONFLICT (external_order_id) DO NOTHING;
    """)
    print("外部注文データのテストデータを挿入しました")
    
    # ===== ワークテーブル（ワーク）のテストデータ挿入 =====
    
    # 注文ワークデータ
    cur.execute("""
        INSERT INTO order_works (batch_id, order_id, process_type) VALUES
        ('BATCH001', (SELECT id FROM orders WHERE order_number = 'ORD001'), '注文処理')
        ON CONFLICT DO NOTHING;
    """)
    print("注文ワークデータのテストデータを挿入しました")
    
    conn.commit()
    print("=== すべてのテストデータの挿入が完了しました ===")
    
except Exception as e:
    print(f"エラー: {e}")
    conn.rollback()
finally:
    cur.close()
    conn.close() 