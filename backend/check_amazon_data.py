import psycopg2
import json

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    user="postgres",
    password="kyokaden",
    database="order_management"
)

cur = conn.cursor()
try:
    # インターフェーステーブルのデータを確認
    cur.execute("""
        SELECT external_order_id, external_system, status, created_at, 
               LEFT(order_data, 200) as order_data_preview
        FROM external_orders
        ORDER BY created_at DESC;
    """)
    
    results = cur.fetchall()
    
    print("=== Amazon API で保存されたデータ ===")
    print(f"総件数: {len(results)}")
    print("-" * 80)
    
    for row in results:
        external_order_id, external_system, status, created_at, order_data_preview = row
        print(f"ID: {external_order_id}")
        print(f"システム: {external_system}")
        print(f"ステータス: {status}")
        print(f"作成日時: {created_at}")
        print(f"データプレビュー: {order_data_preview}...")
        print("-" * 80)
    
    # システム別の件数
    cur.execute("""
        SELECT external_system, COUNT(*) as count
        FROM external_orders
        GROUP BY external_system
        ORDER BY count DESC;
    """)
    
    system_counts = cur.fetchall()
    print("\n=== システム別件数 ===")
    for system, count in system_counts:
        print(f"{system}: {count}件")
    
except Exception as e:
    print(f"エラー: {e}")
finally:
    cur.close()
    conn.close() 