# トランザクションログ API

トランザクションログAPIは、在庫の増減を記録したログ情報を取得するためのインターフェースを提供します。

## 概要

トランザクションログは、在庫の変動を引き起こすすべての取引（入荷、出荷、在庫調整など）の記録を保持します。このAPIを使用することで、特定の商品や倉庫に関する在庫変動の履歴を追跡し、監査証跡として活用することができます。

## API エンドポイント

### トランザクションログ一覧の取得

```
GET /api/v1/transaction_log
```

#### 認証

このAPIを使用するには、OAuth2アクセストークンが必要です。

#### リクエストパラメータ

| パラメータ | 型 | 必須 | 説明 |
|------|------|------|------|
| `article_code` | string | いいえ | 商品コードでフィルタリング |
| `warehouse_code` | string | いいえ | 倉庫コードでフィルタリング |
| `location_code` | string | いいえ | ロケーションコードでフィルタリング |
| `batch_code` | string | いいえ | バッチコードでフィルタリング |
| `transaction_type` | string | いいえ | トランザクションタイプでフィルタリング |
| `reference_document` | string | いいえ | 参照ドキュメント番号でフィルタリング |
| `created_by` | string | いいえ | 作成者でフィルタリング |
| `date_from` | string | いいえ | この日時以降のログを取得（ISO 8601形式） |
| `date_to` | string | いいえ | この日時以前のログを取得（ISO 8601形式） |
| `limit` | integer | いいえ | 1ページあたりの最大件数（デフォルト: 100） |
| `offset` | integer | いいえ | 取得開始位置（デフォルト: 0） |
| `sort` | string | いいえ | 並び順（例：`-created_at`、`article_code`） |

#### レスポンスフィールド

| フィールド | 型 | 説明 |
|------|------|------|
| `items` | array | トランザクションログの配列 |
| `total_count` | integer | 検索条件に一致する総件数 |
| `limit` | integer | 1ページあたりの最大件数 |
| `offset` | integer | 取得開始位置 |

`items`配列の各要素には、以下のフィールドが含まれます：

| フィールド | 型 | 説明 |
|------|------|------|
| `id` | string | トランザクションログID |
| `article_code` | string | 商品コード |
| `article_name` | string | 商品名 |
| `warehouse_code` | string | 倉庫コード |
| `warehouse_name` | string | 倉庫名 |
| `location_code` | string | ロケーションコード |
| `location_name` | string | ロケーション名 |
| `batch_code` | string | バッチコード |
| `transaction_type` | string | トランザクションタイプ |
| `quantity` | number | 数量（増加はプラス、減少はマイナス） |
| `unit_of_measure` | string | 単位 |
| `reference_document` | string | 参照ドキュメント番号 |
| `note` | string | 備考 |
| `created_at` | string | 作成日時（ISO 8601形式） |
| `created_by` | string | 作成者 |

#### レスポンス例

```json
{
  "items": [
    {
      "id": "TL123456",
      "article_code": "GADGET001",
      "article_name": "スマートウォッチ",
      "warehouse_code": "WH001",
      "warehouse_name": "東京倉庫",
      "location_code": "A-01-01",
      "location_name": "エリアA 棚01 段01",
      "batch_code": "LOT202301",
      "transaction_type": "INBOUND_DELIVERY",
      "quantity": 100,
      "unit_of_measure": "EA",
      "reference_document": "ID12345",
      "note": "定期入荷",
      "created_at": "2023-06-01T10:00:00+09:00",
      "created_by": "user123"
    },
    {
      "id": "TL123457",
      "article_code": "GADGET001",
      "article_name": "スマートウォッチ",
      "warehouse_code": "WH001",
      "warehouse_name": "東京倉庫",
      "location_code": "A-01-01",
      "location_name": "エリアA 棚01 段01",
      "batch_code": "LOT202301",
      "transaction_type": "OUTBOUND_DELIVERY",
      "quantity": -30,
      "unit_of_measure": "EA",
      "reference_document": "OD67890",
      "note": "通常出荷",
      "created_at": "2023-06-10T15:30:00+09:00",
      "created_by": "user456"
    }
  ],
  "total_count": 2,
  "limit": 100,
  "offset": 0
}
```

### 特定のトランザクションログの取得

```
GET /api/v1/transaction_log/{transaction_log_id}
```

#### 認証

このAPIを使用するには、OAuth2アクセストークンが必要です。

#### パスパラメータ

| パラメータ | 型 | 必須 | 説明 |
|------|------|------|------|
| `transaction_log_id` | string | はい | トランザクションログID |

#### レスポンスフィールド

特定のトランザクションログの詳細情報が返されます。フィールドは「トランザクションログ一覧の取得」のレスポンスの`items`配列の要素と同じです。

## トランザクションタイプ

トランザクションログに記録されるトランザクションタイプには以下のものがあります：

| 値 | 説明 | 在庫への影響 |
|------|------|------|
| `INBOUND_DELIVERY` | 入荷配送 | 増加 |
| `OUTBOUND_DELIVERY` | 出荷配送 | 減少 |
| `TRANSFER_IN` | 倉庫内転入 | 増加（特定のロケーションにおいて） |
| `TRANSFER_OUT` | 倉庫内転出 | 減少（特定のロケーションにおいて） |
| `ADJUSTMENT_PLUS` | 在庫調整（増加） | 増加 |
| `ADJUSTMENT_MINUS` | 在庫調整（減少） | 減少 |
| `RETURN` | 返品 | 増加 |
| `RETURN_TO_SUPPLIER` | 仕入先返品 | 減少 |
| `PRODUCTION` | 生産 | 増加 |
| `CONSUMPTION` | 消費 | 減少 |
| `SCRAP` | 廃棄 | 減少 |
| `INITIAL_LOAD` | 初期ロード | 増加 |

詳細については、[トランザクションタイプ](../types/transaction_type.md)を参照してください。

## エラーコード

| ステータスコード | 説明 |
|------|------|
| `400` | リクエストパラメータが無効 |
| `401` | 認証エラー |
| `403` | アクセス権限がない |
| `404` | 指定されたリソースが存在しない |
| `500` | サーバーエラー |

## 使用例（Python pylogilessライブラリ使用）

```python
from pylogiless import LogilessClient
from datetime import datetime, timedelta

client = LogilessClient(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    redirect_uri="YOUR_REDIRECT_URI"
)
client.set_token(access_token="YOUR_ACCESS_TOKEN", refresh_token="YOUR_REFRESH_TOKEN")

# 過去7日間の特定商品の在庫トランザクションを取得
seven_days_ago = datetime.now() - timedelta(days=7)
seven_days_ago_str = seven_days_ago.strftime("%Y-%m-%d")

transactions = client.transaction_log.list(
    article_code="GADGET001",
    date_from=seven_days_ago_str,
    sort="-created_at"
)

# 結果の表示
for transaction in transactions.get("items", []):
    print(f"トランザクションID: {transaction.get('id')}")
    print(f"商品: {transaction.get('article_code')} - {transaction.get('article_name')}")
    print(f"倉庫: {transaction.get('warehouse_code')} - {transaction.get('warehouse_name')}")
    print(f"ロケーション: {transaction.get('location_code')}")
    print(f"トランザクションタイプ: {transaction.get('transaction_type')}")
    print(f"数量: {transaction.get('quantity')} {transaction.get('unit_of_measure')}")
    print(f"参照ドキュメント: {transaction.get('reference_document')}")
    print(f"作成日時: {transaction.get('created_at')}")
    print("---")

# 特定の参照ドキュメントに関連するトランザクションを取得
document_transactions = client.transaction_log.list(
    reference_document="OD67890"
)

print(f"ドキュメント OD67890 に関連するトランザクション数: {document_transactions.get('total_count')}")
```

## 関連リソース

- [トランザクションタイプ (Transaction Type)](../types/transaction_type.md)
- [実在庫サマリー (Actual Inventory Summary) API](actual_inventory_summary.md)
- [論理在庫サマリー (Logical Inventory Summary) API](logical_inventory_summary.md)
- [入荷配送 (Inbound Delivery) API](inbound_delivery.md)
- [出荷配送 (Outbound Delivery) API](outbound_delivery.md) 