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

class RealAmazonSPAPITest:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'port': '5432',
            'user': 'postgres',
            'password': 'kyokaden',
            'database': 'order_management'
        }
        
        # Amazon SP-API設定
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
        
        # 設定の検証
        self.validate_config()
    
    def validate_config(self):
        """設定の検証"""
        required_fields = [
            'refresh_token', 'lwa_app_id', 'lwa_client_secret',
            'aws_access_key', 'aws_secret_key', 'role_arn'
        ]
        
        missing_fields = []
        for field in required_fields:
            if not self.sp_api_config.get(field):
                missing_fields.append(field)
        
        if missing_fields:
            print(f"⚠️  以下の環境変数が設定されていません: {', '.join(missing_fields)}")
            print("⚠️  .env ファイルを確認してください。")
            return False
        
        print("✅ 設定の検証が完了しました")
        return True
    
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
            """, (external_order_id, external_system, order_data, 'processed'))
            
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
        """SP-API接続のテスト"""
        if not SP_API_AVAILABLE:
            return False
        
        try:
            print("=== Amazon SP-API 接続テスト ===")
            
            # Access Token の取得テスト
            auth_client = AccessTokenClient(
                refresh_token=self.sp_api_config['refresh_token'],
                lwa_app_id=self.sp_api_config['lwa_app_id'],
                lwa_client_secret=self.sp_api_config['lwa_client_secret'],
                aws_access_key=self.sp_api_config['aws_access_key'],
                aws_secret_key=self.sp_api_config['aws_secret_key'],
                role_arn=self.sp_api_config['role_arn']
            )
            
            # アクセストークンを取得
            access_token = auth_client.get_access_token()
            print(f"✅ アクセストークンの取得に成功しました")
            print(f"   トークン: {access_token[:20]}...")
            
            return True
            
        except Exception as e:
            print(f"❌ SP-API接続エラー: {e}")
            return False
    
    def get_real_amazon_orders(self):
        """実際のAmazon注文データを取得"""
        if not SP_API_AVAILABLE:
            print("❌ SP-API クライアントが利用できません")
            return None
        
        try:
            print("\n=== 実際のAmazon注文データ取得 ===")
            
            # Orders API クライアントの初期化
            orders_api = Orders(
                refresh_token=self.sp_api_config['refresh_token'],
                lwa_app_id=self.sp_api_config['lwa_app_id'],
                lwa_client_secret=self.sp_api_config['lwa_client_secret'],
                aws_access_key=self.sp_api_config['aws_access_key'],
                aws_secret_key=self.sp_api_config['aws_secret_key'],
                role_arn=self.sp_api_config['role_arn']
            )
            
            # 過去7日間の注文を取得
            end_date = datetime.now()
            start_date = end_date - timedelta(days=7)
            
            print(f"取得期間: {start_date.strftime('%Y-%m-%d')} から {end_date.strftime('%Y-%m-%d')}")
            
            # 実際のAPI呼び出し
            response = orders_api.get_orders(
                MarketplaceIds=self.sp_api_config['marketplace_ids'],
                CreatedAfter=start_date.isoformat() + 'Z',
                OrderStatuses=['Shipped', 'Pending', 'Unshipped']
            )
            
            if response.payload and 'Orders' in response.payload:
                orders = response.payload['Orders']
                print(f"✅ {len(orders)}件の注文を取得しました")
                return orders
            else:
                print("ℹ️  注文データが見つかりませんでした")
                return []
                
        except SellingApiException as e:
            print(f"❌ SP-API エラー: {e}")
            return None
        except Exception as e:
            print(f"❌ 予期しないエラー: {e}")
            return None
    
    def process_real_orders(self, orders):
        """実際の注文データを処理"""
        if not orders:
            print("ℹ️  処理する注文データがありません")
            return
        
        print(f"\n=== {len(orders)}件の注文データを処理中 ===")
        
        for order in orders:
            try:
                # 注文IDを取得
                order_id = order.get('AmazonOrderId', 'Unknown')
                external_order_id = f"REAL-SP-{order_id}"
                external_system = "Amazon SP-API (Real)"
                
                # 注文データをJSON形式で保存
                order_data = json.dumps(order, ensure_ascii=False, indent=2)
                
                # データベースに保存
                success = self.save_to_interface_table(external_order_id, external_system, order_data)
                
                if success:
                    order_status = order.get('OrderStatus', 'Unknown')
                    print(f"✅ 注文 {order_id} ({order_status}) を処理しました")
                else:
                    print(f"❌ 注文 {order_id} の処理に失敗しました")
                    
            except Exception as e:
                print(f"❌ 注文処理エラー: {e}")
    
    def run_real_api_test(self):
        """実際のAPIテストを実行"""
        print("Amazon Selling Partner API 実際のテストを開始します...")
        print("=" * 60)
        
        # 設定の検証
        if not self.validate_config():
            print("❌ 設定が不完全です。.env ファイルを確認してください。")
            return
        
        # SP-API接続テスト
        if not self.test_sp_api_connection():
            print("❌ SP-API接続に失敗しました。")
            return
        
        # 実際の注文データを取得
        orders = self.get_real_amazon_orders()
        
        # 取得したデータを処理
        self.process_real_orders(orders)
        
        print("\n" + "=" * 60)
        print("Amazon SP-API 実際のテストが完了しました！")

if __name__ == "__main__":
    # 実際のAPIテスト実行
    real_test = RealAmazonSPAPITest()
    real_test.run_real_api_test() 