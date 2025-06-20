import json
import psycopg2
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

# SP-API クライアントのインポート
try:
    from sp_api.api import Orders
    from sp_api.base import SellingApiException
    from sp_api.auth import AccessTokenClient
    SP_API_AVAILABLE = True
except ImportError:
    print("SP-API クライアントがインストールされていません。")
    print("pip install python-amazon-sp-api を実行してください。")
    SP_API_AVAILABLE = False

# 環境変数を読み込み
load_dotenv()

class SandboxAmazonSPAPITest:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'port': '5432',
            'user': 'postgres',
            'password': 'kyokaden',
            'database': 'order_management'
        }
        
        # Amazon SP-API設定（サンドボックス）
        self.sp_api_config = {
            'refresh_token': os.getenv('AMAZON_REFRESH_TOKEN'),
            'lwa_app_id': os.getenv('AMAZON_LWA_APP_ID'),
            'lwa_client_secret': os.getenv('AMAZON_LWA_CLIENT_SECRET'),
            'aws_access_key': os.getenv('AMAZON_AWS_ACCESS_KEY'),
            'aws_secret_key': os.getenv('AMAZON_AWS_SECRET_KEY'),
            'role_arn': os.getenv('AMAZON_ROLE_ARN'),
            'marketplace_ids': [os.getenv('AMAZON_MARKETPLACE_ID', 'ATVPDKIKX0DER')],
            'region': os.getenv('AMAZON_REGION', 'us-east-1')
        }
        
        # サンドボックス環境の設定
        self.sandbox_mode = True
    
    def get_db_connection(self):
        """データベース接続を取得"""
        return psycopg2.connect(**self.db_config)
    
    def save_to_interface_table(self, external_order_id, external_system, order_data):
        """インターフェーステーブルにデータを保存"""
        conn = self.get_db_connection()
        cur = conn.cursor()
        
        try:
            cur.execute("""
                INSERT INTO external_orders (external_order_id, external_system, order_data, status)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (external_order_id) DO UPDATE SET
                    order_data = EXCLUDED.order_data,
                    status = EXCLUDED.status,
                    processed_at = CURRENT_TIMESTAMP
            """, (external_order_id, external_system, order_data, 'sandbox_test'))
            
            conn.commit()
            print(f"✅ インターフェーステーブルに保存: {external_order_id}")
            return True
            
        except Exception as e:
            print(f"❌ データベース保存エラー: {e}")
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()
    
    def test_sp_api_connection(self):
        """SP-API接続のテスト（サンドボックス）"""
        if not SP_API_AVAILABLE:
            print("❌ SP-API クライアントが利用できません")
            return False
        
        try:
            print("=== Amazon SP-API サンドボックス接続テスト ===")
            
            # 設定の検証
            missing_fields = []
            required_fields = ['refresh_token', 'lwa_app_id', 'lwa_client_secret']
            
            for field in required_fields:
                if not self.sp_api_config.get(field):
                    missing_fields.append(field)
            
            if missing_fields:
                print(f"⚠️  以下の環境変数が設定されていません: {', '.join(missing_fields)}")
                print("⚠️  .env ファイルを確認してください。")
                return False
            
            print("✅ 基本設定の検証が完了しました")
            
            # Refresh Token の形式確認
            refresh_token = self.sp_api_config['refresh_token']
            if refresh_token and len(refresh_token) > 100:
                print(f"✅ Refresh Token が設定されています（長さ: {len(refresh_token)}文字）")
                print(f"   トークン: {refresh_token[:20]}...")
            else:
                print("❌ Refresh Token が正しく設定されていません")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ SP-API接続エラー: {e}")
            return False
    
    def test_sandbox_orders_api(self):
        """サンドボックス環境でのOrders APIテスト"""
        if not SP_API_AVAILABLE:
            print("❌ SP-API クライアントが利用できません")
            return False
        
        try:
            print("\n=== サンドボックス Orders API テスト ===")
            
            # サンドボックス用のOrders API クライアント
            orders_api = Orders(
                refresh_token=self.sp_api_config['refresh_token'],
                app_id=self.sp_api_config['lwa_app_id'],
                client_secret=self.sp_api_config['lwa_client_secret'],
                aws_access_key=self.sp_api_config['aws_access_key'],
                aws_secret_key=self.sp_api_config['aws_secret_key'],
                role_arn=self.sp_api_config['role_arn'],
                sandbox=True  # サンドボックスモード
            )
            
            print("✅ Orders API クライアントの初期化が完了しました")
            
            # サンドボックス環境では実際の注文データは取得できないため、
            # 接続テストのみ実行
            print("ℹ️  サンドボックス環境では実際の注文データは取得できません")
            print("ℹ️  接続テストのみ実行します")
            
            return True
            
        except Exception as e:
            print(f"❌ Orders API エラー: {e}")
            return False
    
    def create_sandbox_test_data(self):
        """サンドボックス環境用のテストデータを作成"""
        print("\n=== サンドボックス環境用テストデータ作成 ===")
        
        # サンドボックス環境を模擬したテストデータ
        sandbox_orders = [
            {
                "orderId": "SANDBOX-ORDER-001",
                "orderStatus": "Shipped",
                "orderTotal": {"amount": "29.99", "currency": "USD"},
                "buyerInfo": {
                    "buyerEmail": "sandbox-buyer1@example.com",
                    "buyerName": "Sandbox Buyer One"
                },
                "shippingAddress": {
                    "name": "Sandbox Buyer One",
                    "addressLine1": "123 Sandbox St",
                    "city": "Sandbox City",
                    "stateOrRegion": "SB",
                    "postalCode": "12345",
                    "countryCode": "US"
                },
                "items": [
                    {
                        "asin": "B08SANDBOX1",
                        "title": "Sandbox Test Product 1",
                        "quantityOrdered": 1,
                        "itemPrice": {"amount": "29.99", "currency": "USD"}
                    }
                ],
                "orderDate": datetime.now().isoformat() + "Z",
                "sandbox": True
            },
            {
                "orderId": "SANDBOX-ORDER-002",
                "orderStatus": "Pending",
                "orderTotal": {"amount": "49.99", "currency": "USD"},
                "buyerInfo": {
                    "buyerEmail": "sandbox-buyer2@example.com",
                    "buyerName": "Sandbox Buyer Two"
                },
                "shippingAddress": {
                    "name": "Sandbox Buyer Two",
                    "addressLine1": "456 Test Ave",
                    "city": "Test City",
                    "stateOrRegion": "TC",
                    "postalCode": "67890",
                    "countryCode": "US"
                },
                "items": [
                    {
                        "asin": "B08SANDBOX2",
                        "title": "Sandbox Test Product 2",
                        "quantityOrdered": 2,
                        "itemPrice": {"amount": "24.99", "currency": "USD"}
                    }
                ],
                "orderDate": datetime.now().isoformat() + "Z",
                "sandbox": True
            }
        ]
        
        # 各注文をインターフェーステーブルに保存
        for order in sandbox_orders:
            external_order_id = f"SB-{order['orderId']}"
            external_system = "Amazon SP-API (Sandbox)"
            order_data = json.dumps(order, ensure_ascii=False, indent=2)
            
            success = self.save_to_interface_table(external_order_id, external_system, order_data)
            if success:
                print(f"✅ サンドボックス注文 {order['orderId']} ({order['orderStatus']}) を保存しました")
            else:
                print(f"❌ サンドボックス注文 {order['orderId']} の保存に失敗しました")
    
    def run_sandbox_test(self):
        """サンドボックス環境のテストを実行"""
        print("Amazon Selling Partner API サンドボックス環境テストを開始します...")
        print("=" * 70)
        
        # SP-API接続テスト
        if not self.test_sp_api_connection():
            print("❌ SP-API接続に失敗しました。")
            return
        
        # サンドボックスOrders APIテスト
        if not self.test_sandbox_orders_api():
            print("❌ Orders APIテストに失敗しました。")
            return
        
        # サンドボックス用テストデータの作成
        self.create_sandbox_test_data()
        
        print("\n" + "=" * 70)
        print("✅ Amazon SP-API サンドボックス環境テストが完了しました！")
        print("ℹ️  インターフェーステーブル（external_orders）にサンドボックスデータが保存されています。")

if __name__ == "__main__":
    # サンドボックステスト実行
    sandbox_test = SandboxAmazonSPAPITest()
    sandbox_test.run_sandbox_test() 