import psycopg2
import os
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

def test_connection():
    """PostgreSQLへの接続をテストする"""
    
    try:
        # 直接接続情報を指定
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            user="postgres",
            password="kyokaden",
            database="postgres"
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"接続成功！PostgreSQLバージョン: {version[0]}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"接続エラー: {e}")
        return False

if __name__ == "__main__":
    test_connection() 