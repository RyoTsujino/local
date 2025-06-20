import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database():
    """PostgreSQLデータベースを作成する"""
    
    try:
        # PostgreSQLサーバーに接続（データベース名を指定しない）
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            user="postgres",
            password="kyokaden",
            database="postgres"  # デフォルトデータベース
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # データベースが存在するかチェック
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", ("order_management",))
        exists = cursor.fetchone()
        
        if not exists:
            # データベースを作成
            cursor.execute('CREATE DATABASE "order_management"')
            print("データベース 'order_management' を作成しました。")
        else:
            print("データベース 'order_management' は既に存在します。")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"データベース作成エラー: {e}")
        print("PostgreSQLサーバーが起動しているか確認してください。")

if __name__ == "__main__":
    create_database() 