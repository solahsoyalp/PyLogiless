# 実際の在庫サマリ (Actual Inventory Summary) API

このAPIでは、現在の物理的な在庫数量に関する情報を取得できます。

## エンドポイント

`GET /api/v1/actual_inventory_summary`

## 認証

このAPIを使用するには、適切なアクセス権を持つOAuth2アクセストークンが必要です。認証の詳細については、[認証ガイド](../concepts/authentication.md)を参照してください。

## リクエストパラメータ

| パラメータ名 | 型 | 必須 | 説明 |
|------------|------|------|------|
| article_code | string | いいえ | 商品コードでフィルタリング |
| warehouse_code | string | いいえ | 倉庫コードでフィルタリング |
| location_code | string | いいえ | ロケーションコードでフィルタリング |
| batch_code | string | いいえ | バッチコードでフィルタリング |
| has_stock | boolean | いいえ | 在庫がある商品のみフィルタリング (`true`の場合) |
| limit | integer | いいえ | 取得する結果の最大数（デフォルト: 100, 最大: 1000） |
| offset | integer | いいえ | 結果セットの開始オフセット（ページング用、デフォルト: 0） |
| sort | string | いいえ | ソートフィールドとソート順（例: `article_code:asc`, `stock_quantity:desc`） |

## レスポンスフィールド

| フィールド名 | 型 | 説明 |
|------------|------|------|
| id | string | 在庫サマリの一意のID |
| article_code | string | 商品コード |
| article_name | string | 商品名 |
| warehouse_code | string | 倉庫コード |
| warehouse_name | string | 倉庫名 |
| location_code | string | ロケーションコード（存在する場合） |
| batch_code | string | バッチコード（存在する場合） |
| stock_quantity | number | 在庫数量 |
| allocated_quantity | number | 引当済み数量 |
| available_quantity | number | 利用可能数量（stock_quantity - allocated_quantity） |
| unit_of_measure | string | 単位（個、ケース、パレットなど） |
| last_updated_at | string | 最終更新日時（ISO 8601形式） |
| created_at | string | 作成日時（ISO 8601形式） |

## レスポンス例

```json
{
  "items": [
    {
      "id": "inv_12345",
      "article_code": "ARTICLE001",
      "article_name": "テスト商品1",
      "warehouse_code": "WH001",
      "warehouse_name": "東京倉庫",
      "location_code": "A-01-01",
      "batch_code": "LOT20230601",
      "stock_quantity": 100,
      "allocated_quantity": 20,
      "available_quantity": 80,
      "unit_of_measure": "個",
      "last_updated_at": "2023-06-01T10:30:00+09:00",
      "created_at": "2023-01-15T09:00:00+09:00"
    },
    {
      "id": "inv_12346",
      "article_code": "ARTICLE002",
      "article_name": "テスト商品2",
      "warehouse_code": "WH001",
      "warehouse_name": "東京倉庫",
      "location_code": "A-01-02",
      "batch_code": null,
      "stock_quantity": 50,
      "allocated_quantity": 0,
      "available_quantity": 50,
      "unit_of_measure": "個",
      "last_updated_at": "2023-06-01T10:30:00+09:00",
      "created_at": "2023-01-15T09:00:00+09:00"
    }
  ],
  "total_count": 2,
  "limit": 100,
  "offset": 0
}
```

## エラーコード

| ステータスコード | エラーコード | 説明 |
|---------------|-------------|------|
| 400 | validation_error | リクエストパラメータが無効です |
| 401 | unauthorized | アクセストークンが無効または期限切れです |
| 403 | forbidden | このリソースへのアクセス権がありません |
| 500 | internal_server_error | サーバー内部エラーが発生しました |

詳細なエラーコードについては、[エラーコードリファレンス](../concepts/errors.md)を参照してください。

## 使用例

### Pythonでの使用例（pylogilessライブラリ使用）

```python
from pylogiless import LogilessClient

# クライアントの初期化
client = LogilessClient(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    redirect_uri="YOUR_REDIRECT_URI"
)
client.set_token(access_token="YOUR_ACCESS_TOKEN", refresh_token="YOUR_REFRESH_TOKEN")

# 在庫情報の取得
inventory_list = client.actual_inventory_summary.list(
    article_code="ARTICLE001",
    warehouse_code="WH001",
    limit=10
)

# 特定の在庫情報の取得
inventory = client.actual_inventory_summary.get("inv_12345")

# 結果の表示
for item in inventory_list.get("items", []):
    print(f"商品: {item.get('article_name')}, 在庫数: {item.get('stock_quantity')} {item.get('unit_of_measure')}")
```

## 関連リソース

- [論理的な在庫サマリ (Logical Inventory Summary)](logical_inventory_summary.md)
- [日次在庫サマリ (Daily Inventory Summary)](daily_inventory_summary.md)
- [商品 (Article)](article.md)
- [倉庫 (Warehouse)](warehouse.md)
- [ロケーション (Location)](location.md) 