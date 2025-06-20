import json
import requests
from datetime import datetime, timedelta
import psycopg2
from dotenv import load_dotenv
import os

# 環境変数を読み込み
load_dotenv()

class AmazonSPAPITest:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'port': '5432',
            'user': 'postgres',
            'password': 'kyokaden',
            'database': 'order_management'
        }
        
        # Amazon SP-API設定（環境変数から取得）
        self.sp_api_config = {
            'refresh_token': os.getenv('AMAZON_REFRESH_TOKEN', ''),
            'lwa_app_id': os.getenv('AMAZON_LWA_APP_ID', ''),
            'lwa_client_secret': os.getenv('AMAZON_LWA_CLIENT_SECRET', ''),
            'aws_access_key': os.getenv('AMAZON_AWS_ACCESS_KEY', ''),
            'aws_secret_key': os.getenv('AMAZON_AWS_SECRET_KEY', ''),
            'role_arn': os.getenv('AMAZON_ROLE_ARN', ''),
            'marketplace_ids': [os.getenv('AMAZON_MARKETPLACE_ID', 'ATVPDKIKX0DER')],  # US marketplace
            'region': os.getenv('AMAZON_REGION', 'us-east-1')
        }
    
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
            """, (external_order_id, external_system, order_data, 'pending'))
            
            conn.commit()
            print(f"インターフェーステーブルに保存: {external_order_id}")
            return True
            
        except Exception as e:
            print(f"データベース保存エラー: {e}")
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()
    
    def test_sp_api_orders_simulation(self):
        """Amazon SP-API Orders API のシミュレーションテスト"""
        print("=== Amazon Selling Partner API Orders テスト ===")
        
        # SP-APIの実際のレスポンス形式に基づくテストデータ
        test_orders = [
            {
                "orderId": "SP-ORDER-001",
                "orderStatus": "Shipped",
                "orderTotal": {
                    "amount": "39.99",
                    "currency": "USD"
                },
                "buyerInfo": {
                    "buyerEmail": "buyer1@example.com",
                    "buyerName": "Buyer One",
                    "buyerCounty": "US"
                },
                "shippingAddress": {
                    "name": "Buyer One",
                    "addressLine1": "789 Pine St",
                    "addressLine2": "Apt 4B",
                    "city": "Chicago",
                    "stateOrRegion": "IL",
                    "postalCode": "60601",
                    "countryCode": "US",
                    "phone": "+1-555-123-4567"
                },
                "items": [
                    {
                        "asin": "B08N5WRWNW",
                        "title": "Amazon Echo Dot (4th Gen)",
                        "quantityOrdered": 1,
                        "itemPrice": {
                            "amount": "39.99",
                            "currency": "USD"
                        },
                        "itemTax": {
                            "amount": "3.20",
                            "currency": "USD"
                        }
                    }
                ],
                "orderDate": "2024-01-15T10:30:00Z",
                "lastUpdateDate": "2024-01-16T14:45:00Z"
            },
            {
                "orderId": "SP-ORDER-002",
                "orderStatus": "Pending",
                "orderTotal": {
                    "amount": "89.98",
                    "currency": "USD"
                },
                "buyerInfo": {
                    "buyerEmail": "buyer2@example.com",
                    "buyerName": "Buyer Two",
                    "buyerCounty": "US"
                },
                "shippingAddress": {
                    "name": "Buyer Two",
                    "addressLine1": "456 Oak Ave",
                    "city": "Los Angeles",
                    "stateOrRegion": "CA",
                    "postalCode": "90210",
                    "countryCode": "US",
                    "phone": "+1-555-987-6543"
                },
                "items": [
                    {
                        "asin": "B08N5WRWNW",
                        "title": "Kindle Paperwhite",
                        "quantityOrdered": 1,
                        "itemPrice": {
                            "amount": "89.98",
                            "currency": "USD"
                        },
                        "itemTax": {
                            "amount": "7.20",
                            "currency": "USD"
                        }
                    }
                ],
                "orderDate": "2024-01-17T09:15:00Z",
                "lastUpdateDate": "2024-01-17T09:15:00Z"
            },
            {
                "orderId": "SP-ORDER-003",
                "orderStatus": "Canceled",
                "orderTotal": {
                    "amount": "25.99",
                    "currency": "USD"
                },
                "buyerInfo": {
                    "buyerEmail": "buyer3@example.com",
                    "buyerName": "Buyer Three",
                    "buyerCounty": "US"
                },
                "shippingAddress": {
                    "name": "Buyer Three",
                    "addressLine1": "123 Main St",
                    "city": "New York",
                    "stateOrRegion": "NY",
                    "postalCode": "10001",
                    "countryCode": "US",
                    "phone": "+1-555-456-7890"
                },
                "items": [
                    {
                        "asin": "B08N5WRWNW",
                        "title": "Amazon Basics USB Cable",
                        "quantityOrdered": 2,
                        "itemPrice": {
                            "amount": "12.99",
                            "currency": "USD"
                        },
                        "itemTax": {
                            "amount": "1.04",
                            "currency": "USD"
                        }
                    }
                ],
                "orderDate": "2024-01-14T16:20:00Z",
                "lastUpdateDate": "2024-01-15T11:30:00Z"
            }
        ]
        
        # 各注文をインターフェーステーブルに保存
        for order in test_orders:
            external_order_id = f"SP-{order['orderId']}"
            external_system = "Amazon SP-API"
            order_data = json.dumps(order, ensure_ascii=False, indent=2)
            
            success = self.save_to_interface_table(external_order_id, external_system, order_data)
            if success:
                print(f"✓ 注文 {order['orderId']} ({order['orderStatus']}) を保存しました")
            else:
                print(f"✗ 注文 {order['orderId']} の保存に失敗しました")
    
    def test_sp_api_orders_by_date_range(self):
        """日付範囲での注文取得テスト（シミュレーション）"""
        print("\n=== 日付範囲での注文取得テスト ===")
        
        # 過去7日間の注文データ（シミュレーション）
        from datetime import datetime, timedelta
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        print(f"取得期間: {start_date.strftime('%Y-%m-%d')} から {end_date.strftime('%Y-%m-%d')}")
        
        # 期間内の注文データ
        recent_orders = [
            {
                "orderId": "SP-RECENT-001",
                "orderStatus": "Shipped",
                "orderTotal": {"amount": "59.99", "currency": "USD"},
                "orderDate": (end_date - timedelta(days=2)).isoformat() + "Z",
                "items": [
                    {
                        "asin": "B08N5WRWNW",
                        "title": "Recent Product 1",
                        "quantityOrdered": 1,
                        "itemPrice": {"amount": "59.99", "currency": "USD"}
                    }
                ]
            },
            {
                "orderId": "SP-RECENT-002",
                "orderStatus": "Pending",
                "orderTotal": {"amount": "29.99", "currency": "USD"},
                "orderDate": (end_date - timedelta(days=1)).isoformat() + "Z",
                "items": [
                    {
                        "asin": "B08N5WRWNW",
                        "title": "Recent Product 2",
                        "quantityOrdered": 1,
                        "itemPrice": {"amount": "29.99", "currency": "USD"}
                    }
                ]
            }
        ]
        
        for order in recent_orders:
            external_order_id = f"SP-{order['orderId']}"
            external_system = "Amazon SP-API (Date Range)"
            order_data = json.dumps(order, ensure_ascii=False, indent=2)
            
            success = self.save_to_interface_table(external_order_id, external_system, order_data)
            if success:
                print(f"✓ 最近の注文 {order['orderId']} を保存しました")
    
    def run_sp_api_tests(self):
        """Amazon SP-API のテストを実行"""
        print("Amazon Selling Partner API テスト環境の実行を開始します...")
        print("=" * 60)
        
        # 注文データのテストを実行
        self.test_sp_api_orders_simulation()
        self.test_sp_api_orders_by_date_range()
        
        print("\n" + "=" * 60)
        print("Amazon SP-API テストが完了しました！")
        print("インターフェーステーブル（external_orders）に注文データが保存されています。")

if __name__ == "__main__":
    # テスト実行
    sp_api_test = AmazonSPAPITest()
    sp_api_test.run_sp_api_tests() 