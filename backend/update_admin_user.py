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
    cur.execute("UPDATE users SET is_admin = TRUE WHERE username = 'admin';")
    conn.commit()
    print("adminユーザーを管理者に設定しました。")
except Exception as e:
    print(f"エラー: {e}")
finally:
    cur.close()
    conn.close() 