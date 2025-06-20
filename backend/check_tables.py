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
    # テーブル一覧を取得
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    tables = cur.fetchall()
    print("=== 作成されたテーブル一覧 ===")
    for table in tables:
        print(f"- {table[0]}")
    
    # 各テーブルの構造を確認
    for table in tables:
        table_name = table[0]
        print(f"\n=== {table_name} テーブルの構造 ===")
        cur.execute(f"""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_name = '{table_name}'
            ORDER BY ordinal_position;
        """)
        columns = cur.fetchall()
        for col in columns:
            print(f"  {col[0]}: {col[1]} (NULL: {col[2]}, DEFAULT: {col[3]})")
    
except Exception as e:
    print(f"エラー: {e}")
finally:
    cur.close()
    conn.close() 