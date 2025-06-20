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
    # Amazon SP-APIで保存されたデータのみを確認
    cur.execute("""
        SELECT external_order_id, external_system, status, created_at, 
               LEFT(order_data, 300) as order_data_preview
        FROM external_orders
        WHERE external_system LIKE '%Amazon SP-API%'
        ORDER BY created_at DESC;
    """)
    
    results = cur.fetchall()
    
    print("=== Amazon SP-API で保存された注文データ ===")
    print(f"総件数: {len(results)}")
    print("-" * 100)
    
    for row in results:
        external_order_id, external_system, status, created_at, order_data_preview = row
        print(f"ID: {external_order_id}")
        print(f"システム: {external_system}")
        print(f"ステータス: {status}")
        print(f"作成日時: {created_at}")
        print(f"データプレビュー:")
        print(order_data_preview)
        print("-" * 100)
    
    # 注文ステータス別の件数
    cur.execute("""
        SELECT 
            CASE 
                WHEN order_data LIKE '%"orderStatus": "Shipped"%' THEN 'Shipped'
                WHEN order_data LIKE '%"orderStatus": "Pending"%' THEN 'Pending'
                WHEN order_data LIKE '%"orderStatus": "Canceled"%' THEN 'Canceled'
                ELSE 'Other'
            END as order_status,
            COUNT(*) as count
        FROM external_orders
        WHERE external_system LIKE '%Amazon SP-API%'
        GROUP BY 
            CASE 
                WHEN order_data LIKE '%"orderStatus": "Shipped"%' THEN 'Shipped'
                WHEN order_data LIKE '%"orderStatus": "Pending"%' THEN 'Pending'
                WHEN order_data LIKE '%"orderStatus": "Canceled"%' THEN 'Canceled'
                ELSE 'Other'
            END
        ORDER BY count DESC;
    """)
    
    status_counts = cur.fetchall()
    print("\n=== 注文ステータス別件数 ===")
    for status, count in status_counts:
        print(f"{status}: {count}件")
    
    # 総注文金額の計算（シミュレーション）
    print("\n=== 注文金額サマリー ===")
    cur.execute("""
        SELECT 
            SUM(
                CASE 
                    WHEN order_data LIKE '%"amount": "%' 
                    THEN CAST(
                        SUBSTRING(
                            order_data FROM '"amount": "([^"]+)"'
                        ) AS DECIMAL(10,2)
                    )
                    ELSE 0 
                END
            ) as total_amount
        FROM external_orders
        WHERE external_system LIKE '%Amazon SP-API%'
        AND order_data LIKE '%"amount": "%';
    """)
    
    total_result = cur.fetchone()
    if total_result and total_result[0]:
        print(f"総注文金額: ${total_result[0]:.2f} USD")
    else:
        print("注文金額の計算に失敗しました")
    
except Exception as e:
    print(f"エラー: {e}")
finally:
    cur.close()
    conn.close() 