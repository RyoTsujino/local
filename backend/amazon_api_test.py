import json
import requests
from datetime import datetime
import psycopg2
from dotenv import load_dotenv
import os

# 環境変数を読み込み
load_dotenv()

class AmazonAPITest:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'port': '5432',
            'user': 'postgres',
            'password': 'kyokaden',
            'database': 'order_management'
        }
        
        # Amazon API設定（環境変数から取得）
        self.amazon_config = {
            'access_key': os.getenv('AMAZON_ACCESS_KEY', ''),
            'secret_key': os.getenv('AMAZON_SECRET_KEY', ''),
            'seller_id': os.getenv('AMAZON_SELLER_ID', ''),
            'marketplace_id': os.getenv('AMAZON_MARKETPLACE_ID', ''),
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
    
    def test_amazon_mws_orders(self):
        """Amazon MWS Orders API のテスト"""
        print("=== Amazon MWS Orders API テスト ===")
        
        # テスト用の注文データ（実際のAPIレスポンスを模擬）
        test_orders = [
            {
                "AmazonOrderId": "AMZ-ORDER-001",
                "OrderStatus": "Shipped",
                "OrderTotal": {"Amount": "29.99", "CurrencyCode": "USD"},
                "ShippingAddress": {
                    "Name": "John Doe",
                    "AddressLine1": "123 Main St",
                    "City": "New York",
                    "StateOrRegion": "NY",
                    "PostalCode": "10001",
                    "CountryCode": "US"
                },
                "OrderItems": [
                    {
                        "ASIN": "B08N5WRWNW",
                        "Title": "Test Product 1",
                        "QuantityOrdered": 2,
                        "ItemPrice": {"Amount": "14.99", "CurrencyCode": "USD"}
                    }
                ]
            },
            {
                "AmazonOrderId": "AMZ-ORDER-002",
                "OrderStatus": "Pending",
                "OrderTotal": {"Amount": "49.99", "CurrencyCode": "USD"},
                "ShippingAddress": {
                    "Name": "Jane Smith",
                    "AddressLine1": "456 Oak Ave",
                    "City": "Los Angeles",
                    "StateOrRegion": "CA",
                    "PostalCode": "90210",
                    "CountryCode": "US"
                },
                "OrderItems": [
                    {
                        "ASIN": "B08N5WRWNW",
                        "Title": "Test Product 2",
                        "QuantityOrdered": 1,
                        "ItemPrice": {"Amount": "49.99", "CurrencyCode": "USD"}
                    }
                ]
            }
        ]
        
        # 各注文をインターフェーステーブルに保存
        for order in test_orders:
            external_order_id = f"AMZ-{order['AmazonOrderId']}"
            external_system = "Amazon MWS"
            order_data = json.dumps(order, ensure_ascii=False, indent=2)
            
            success = self.save_to_interface_table(external_order_id, external_system, order_data)
            if success:
                print(f"✓ 注文 {order['AmazonOrderId']} を保存しました")
            else:
                print(f"✗ 注文 {order['AmazonOrderId']} の保存に失敗しました")
    
    def test_amazon_sp_api_orders(self):
        """Amazon Selling Partner API のテスト"""
        print("\n=== Amazon Selling Partner API テスト ===")
        
        # テスト用の注文データ（SP-APIレスポンスを模擬）
        test_orders = [
            {
                "orderId": "SP-ORDER-001",
                "orderStatus": "Shipped",
                "orderTotal": {"amount": "39.99", "currency": "USD"},
                "buyerInfo": {
                    "buyerEmail": "buyer1@example.com",
                    "buyerName": "Buyer One"
                },
                "shippingAddress": {
                    "name": "Buyer One",
                    "addressLine1": "789 Pine St",
                    "city": "Chicago",
                    "stateOrRegion": "IL",
                    "postalCode": "60601",
                    "countryCode": "US"
                },
                "items": [
                    {
                        "asin": "B08N5WRWNW",
                        "title": "SP API Test Product 1",
                        "quantityOrdered": 1,
                        "itemPrice": {"amount": "39.99", "currency": "USD"}
                    }
                ]
            }
        ]
        
        # 各注文をインターフェーステーブルに保存
        for order in test_orders:
            external_order_id = f"SP-{order['orderId']}"
            external_system = "Amazon SP-API"
            order_data = json.dumps(order, ensure_ascii=False, indent=2)
            
            success = self.save_to_interface_table(external_order_id, external_system, order_data)
            if success:
                print(f"✓ 注文 {order['orderId']} を保存しました")
            else:
                print(f"✗ 注文 {order['orderId']} の保存に失敗しました")
    
    def test_amazon_product_api(self):
        """Amazon Product Advertising API のテスト"""
        print("\n=== Amazon Product Advertising API テスト ===")
        
        # テスト用の商品データ
        test_products = [
            {
                "ASIN": "B08N5WRWNW",
                "Title": "Amazon Echo Dot (4th Gen)",
                "Price": {"Amount": "49.99", "CurrencyCode": "USD"},
                "Features": ["Smart speaker", "Alexa enabled"],
                "Rating": 4.5,
                "ReviewCount": 125000
            },
            {
                "ASIN": "B08N5WRWNW",
                "Title": "Kindle Paperwhite",
                "Price": {"Amount": "139.99", "CurrencyCode": "USD"},
                "Features": ["Waterproof", "8GB storage"],
                "Rating": 4.7,
                "ReviewCount": 89000
            }
        ]
        
        # 各商品をインターフェーステーブルに保存
        for product in test_products:
            external_order_id = f"PROD-{product['ASIN']}"
            external_system = "Amazon Product API"
            order_data = json.dumps(product, ensure_ascii=False, indent=2)
            
            success = self.save_to_interface_table(external_order_id, external_system, order_data)
            if success:
                print(f"✓ 商品 {product['ASIN']} を保存しました")
            else:
                print(f"✗ 商品 {product['ASIN']} の保存に失敗しました")
    
    def run_all_tests(self):
        """すべてのテストを実行"""
        print("Amazon API テスト環境の実行を開始します...")
        print("=" * 50)
        
        # 各APIのテストを実行
        self.test_amazon_mws_orders()
        self.test_amazon_sp_api_orders()
        self.test_amazon_product_api()
        
        print("\n" + "=" * 50)
        print("すべてのテストが完了しました！")
        print("インターフェーステーブル（external_orders）にデータが保存されています。")

if __name__ == "__main__":
    # テスト実行
    amazon_test = AmazonAPITest()
    amazon_test.run_all_tests() 