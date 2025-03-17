# ドキュメント行ステータス (Document Line Status)

ドキュメント行ステータスは、出荷配送、入荷配送、倉庫間転送などのドキュメント内の個々の明細行（アイテム）の処理状態を表します。

## 概要

ドキュメント行ステータスは、ドキュメント内の各アイテムの処理状態を個別に追跡するために使用されます。ドキュメント全体のステータスとは別に、各行の状態を追跡することで、部分的な処理や進捗状況の詳細な管理が可能になります。

## 使用できる値

| 値 | 説明 |
|------|------|
| `PLANNED` | 計画済み。処理が計画されている状態。 |
| `CONFIRMED` | 確認済み。記録された内容が確認された状態。 |
| `PICKED` | ピック済み。商品がピックされた状態。 |
| `PACKED` | 梱包済み。商品が梱包された状態。 |
| `SHIPPED` | 出荷済み。商品が出荷された状態。 |
| `DELIVERED` | 配送完了。商品が配送先に到着した状態。 |
| `CANCELED` | キャンセル済み。処理がキャンセルされた状態。 |
| `RECEIVED` | 受領済み。商品が受領された状態。 |
| `RETURNED` | 返品済み。商品が返品された状態。 |
| `ON_HOLD` | 保留中。何らかの理由で処理が保留されている状態。 |
| `PARTIALLY_RECEIVED` | 一部受領。一部の商品のみが受領された状態。 |
| `PARTIALLY_SHIPPED` | 一部出荷。一部の商品のみが出荷された状態。 |

## ドキュメントステータスとの関係

ドキュメント行ステータスは、ドキュメント全体のステータスと連動しますが、より詳細なレベルでの追跡を可能にします。例えば：

- ドキュメント全体が `IN_PROCESS` の状態でも、個々の行は `PICKED`、`PACKED`、`SHIPPED` などの異なるステータスを持つことができます。
- いくつかの行が `DELIVERED` になり、一部がまだ `IN_TRANSIT` の場合、ドキュメント全体のステータスは `PARTIALLY_DELIVERED` になることがあります。

## ステータスの遷移

一般的なステータスの遷移は以下の通りです：

1. `PLANNED` → `CONFIRMED` → `PICKED` → `PACKED` → `SHIPPED` → `DELIVERED`（出荷配送の場合）
2. `PLANNED` → `CONFIRMED` → `RECEIVED`（入荷配送の場合）

ただし、すべてのステータスがすべてのドキュメントタイプで使用されるわけではなく、ビジネスプロセスによって異なる場合があります。

## API上での使用例

### 出荷配送明細の更新（PUT /api/v1/outbound_delivery/{id}/items/{line_id}）

```json
{
  "status": "PICKED",
  "note": "商品のピックが完了しました"
}
```

### 入荷配送明細の更新（PUT /api/v1/inbound_delivery/{id}/items/{line_id}）

```json
{
  "status": "RECEIVED",
  "received_quantity": 10,
  "note": "予定通り受領しました"
}
```

## Pythonでの使用例（pylogilessライブラリ使用）

```python
from pylogiless import LogilessClient

client = LogilessClient(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    redirect_uri="YOUR_REDIRECT_URI"
)
client.set_token(access_token="YOUR_ACCESS_TOKEN", refresh_token="YOUR_REFRESH_TOKEN")

# 出荷配送の特定の明細行のステータスを更新
client.outbound_delivery.update_line_item(
    delivery_id="OD12345",
    line_id="1",
    status="PACKED",
    note="梱包完了"
)

# 入荷配送の特定の明細行のステータスを更新
client.inbound_delivery.update_line_item(
    delivery_id="ID12345",
    line_id="1",
    status="RECEIVED",
    received_quantity=15,
    note="予定より5個多く受領"
)
```

## 関連リソース

- [出荷配送 (Outbound Delivery) API](../api/outbound_delivery.md)
- [入荷配送 (Inbound Delivery) API](../api/inbound_delivery.md)
- [倉庫間転送 (Inter-Warehouse Transfer) API](../api/inter_warehouse_transfer.md)
- [ドキュメントステータス (Document Status)](document_status.md)
- [配送ステータス (Delivery Status)](delivery_status.md) 