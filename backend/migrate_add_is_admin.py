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
    cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS is_admin BOOLEAN DEFAULT FALSE;")
    conn.commit()
    print("is_adminカラムを追加しました。")
except Exception as e:
    print(f"エラー: {e}")
finally:
    cur.close()
    conn.close() 