"""
SKUマッピング更新のサンプルコード
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
        # 既存のSKUマッピングを確認（デバッグ用）
        print("\n=== 既存のSKUマッピング ===")
        article_maps = client.article_map.list(limit=5)
        print(f"SKUマッピング: {article_maps}")

        # SKUマッピングを更新する例
        # 注意: 以下の値は実際の環境に合わせて変更してください
        article_map_id = "実際のマッピングID"  # 更新したいマッピングのID
        
        update_data = {
            "article_id": "商品ID",  # 商品ID - 必須
            "sku": "SKU1234",      # SKU - 必須
            "item_code": "ITEM001", # 商品コード - 必須
            "barcode": "バーコード",  # バーコード（オプション）
            "external_id": "外部ID",  # 外部システムのID（オプション）
            # 他の更新したいフィールドを追加
        }
        
        # マッピングの更新を実行
        updated_map = client.article_map.update(article_map_id, update_data)
        print(f"\n更新されたSKUマッピング: {updated_map}")

    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
        # より詳細なエラー情報を表示
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 