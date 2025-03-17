# トランザクションタイプ (Transaction Type)

トランザクションタイプは、在庫の増減を引き起こす取引の種類を分類するために使用されます。

## 概要

トランザクションタイプは、在庫管理システム内で発生するさまざまな在庫移動の原因や性質を識別するためのラベルです。これにより、在庫増減の理由を明確に追跡し、適切な在庫管理と会計処理が可能になります。

## 使用できる値

| 値 | 説明 | 在庫への影響 |
|------|------|------|
| `INBOUND_DELIVERY` | 入荷配送。仕入先や他の倉庫からの商品受領。 | 増加 |
| `OUTBOUND_DELIVERY` | 出荷配送。顧客や他の倉庫への商品出荷。 | 減少 |
| `TRANSFER_IN` | 倉庫内転入。倉庫内の別のロケーションからの商品移動。 | 増加（特定のロケーションにおいて） |
| `TRANSFER_OUT` | 倉庫内転出。倉庫内の別のロケーションへの商品移動。 | 減少（特定のロケーションにおいて） |
| `ADJUSTMENT_PLUS` | 在庫調整（増加）。在庫の不足を補正するための調整。 | 増加 |
| `ADJUSTMENT_MINUS` | 在庫調整（減少）。在庫の過剰を補正するための調整。 | 減少 |
| `RETURN` | 返品。顧客からの商品返品。 | 増加 |
| `RETURN_TO_SUPPLIER` | 仕入先返品。仕入先への商品返品。 | 減少 |
| `PRODUCTION` | 生産。社内生産による商品の増加。 | 増加 |
| `CONSUMPTION` | 消費。生産や社内利用による商品の消費。 | 減少 |
| `SCRAP` | 廃棄。商品の破損や期限切れによる廃棄。 | 減少 |
| `INITIAL_LOAD` | 初期ロード。システム導入時の初期在庫設定。 | 増加 |

## トランザクションログと監査証跡

各トランザクションタイプによる在庫変動は、トランザクションログに記録され、監査証跡として保持されます。これにより、以下のことが可能になります：

- 在庫変動の履歴追跡
- 在庫不一致の原因特定
- 会計監査への対応
- 在庫レポートの生成

## API上での使用例

### トランザクションログの取得（GET /api/v1/transaction_log）

特定のトランザクションタイプでフィルタリングする例：

```
GET /api/v1/transaction_log?transaction_type=ADJUSTMENT_PLUS
```

レスポンス例：

```json
{
  "items": [
    {
      "id": "TL123456",
      "article_code": "GADGET001",
      "article_name": "スマートウォッチ",
      "warehouse_code": "WH001",
      "location_code": "A-01-01",
      "batch_code": "LOT202301",
      "transaction_type": "ADJUSTMENT_PLUS",
      "quantity": 10,
      "unit_of_measure": "EA",
      "reference_document": "ADJ00123",
      "note": "実地棚卸による在庫調整",
      "created_at": "2023-06-15T14:30:00+09:00",
      "created_by": "user123"
    }
  ],
  "total_count": 1,
  "limit": 100,
  "offset": 0
}
```

## Pythonでの使用例（pylogilessライブラリ使用）

```python
from pylogiless import LogilessClient
from datetime import datetime, timedelta

client = LogilessClient(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    redirect_uri="YOUR_REDIRECT_URI"
)
client.set_token(access_token="YOUR_ACCESS_TOKEN", refresh_token="YOUR_REFRESH_TOKEN")

# 昨日からの出荷配送に関するトランザクションログを取得
yesterday = datetime.now() - timedelta(days=1)
yesterday_str = yesterday.strftime("%Y-%m-%d")

outbound_transactions = client.transaction_log.list(
    transaction_type="OUTBOUND_DELIVERY",
    date_from=yesterday_str
)

# 結果の表示
for transaction in outbound_transactions.get("items", []):
    print(f"トランザクションID: {transaction.get('id')}")
    print(f"商品コード: {transaction.get('article_code')}")
    print(f"商品名: {transaction.get('article_name')}")
    print(f"数量: {transaction.get('quantity')} {transaction.get('unit_of_measure')}")
    print(f"参照ドキュメント: {transaction.get('reference_document')}")
    print(f"作成日時: {transaction.get('created_at')}")
    print("---")
```

## 関連リソース

- [トランザクションログ (Transaction Log) API](../api/transaction_log.md)
- [実在庫サマリー (Actual Inventory Summary) API](../api/actual_inventory_summary.md)
- [論理在庫サマリー (Logical Inventory Summary) API](../api/logical_inventory_summary.md)
- [出荷配送 (Outbound Delivery) API](../api/outbound_delivery.md)
- [入荷配送 (Inbound Delivery) API](../api/inbound_delivery.md) 