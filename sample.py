"""
LOGILESS APIを使用したサンプルコード
"""
import os
from dotenv import load_dotenv
from pylogiless import LogilessClient

def main():
    # .envファイルから環境変数を読み込む
    load_dotenv()
    
    # 環境変数から認証情報を取得
    access_token = os.getenv("LOGILESS_ACCESS_TOKEN")
    merchant_id = os.getenv("LOGILESS_MERCHANT_ID")

    if not access_token or not merchant_id:
        print("環境変数 LOGILESS_ACCESS_TOKEN と LOGILESS_MERCHANT_ID を設定してください。")
        return

    # クライアントの初期化
    client = LogilessClient(access_token, merchant_id)

    try:
        # 実在庫サマリの取得
        print("\n=== 実在庫サマリ ===")
        actual_inventory = client.actual_inventory_summary.list()
        print(f"実在庫サマリ: {actual_inventory}")

        # 論理在庫サマリの取得
        print("\n=== 論理在庫サマリ ===")
        logical_inventory = client.logical_inventory_summary.list()
        print(f"論理在庫サマリ: {logical_inventory}")

        # 商品一覧の取得
        print("\n=== 商品一覧 ===")
        articles = client.article.list()
        print(f"商品一覧: {articles}")

    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")

if __name__ == "__main__":
    main() 