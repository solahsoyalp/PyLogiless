"""
在庫情報を取得するサンプルコード
"""
import os
from dotenv import load_dotenv
from pylogiless.api.client import LogilessClient

def main():
    # .envファイルから環境変数を読み込む
    load_dotenv()
    
    # 認証情報を取得
    access_token = os.getenv("LOGILESS_ACCESS_TOKEN")
    merchant_id = os.getenv("LOGILESS_MERCHANT_ID")
    
    if not access_token or not merchant_id:
        print("エラー: .envファイルにLOGILESS_ACCESS_TOKENとLOGILESS_MERCHANT_IDを設定してください。")
        return
    
    try:
        # クライアントを初期化
        client = LogilessClient(access_token, merchant_id)
        
        # 実在庫サマリを取得
        print("実在庫サマリを取得中...")
        inventory = client.actual_inventory_summary.list()
        print("\n実在庫サマリ:")
        print(f"総アイテム数: {len(inventory.get('items', []))}")
        for item in inventory.get('items', []):
            print(f"- 商品ID: {item.get('article_id')}")
            print(f"  在庫数: {item.get('quantity')}")
            print(f"  倉庫ID: {item.get('warehouse_id')}")
            print()
        
        # 論理在庫サマリを取得
        print("\n論理在庫サマリを取得中...")
        logical_inventory = client.logical_inventory_summary.list()
        print("\n論理在庫サマリ:")
        print(f"総アイテム数: {len(logical_inventory.get('items', []))}")
        for item in logical_inventory.get('items', []):
            print(f"- 商品ID: {item.get('article_id')}")
            print(f"  在庫数: {item.get('quantity')}")
            print(f"  倉庫ID: {item.get('warehouse_id')}")
            print()
            
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")

if __name__ == "__main__":
    main() 