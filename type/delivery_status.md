# 配送ステータス (Delivery Status)

配送ステータスは、配送物の現在の状態を表す区分です。

## 概要

配送ステータスは、出荷配送や入荷配送などの配送物の処理状態を詳細に追跡するために使用されます。ドキュメントステータスが配送処理全体の状態を表すのに対し、配送ステータスは配送物自体の状態に焦点を当てています。

## 使用できる値

| 値 | 説明 |
|------|------|
| `NOT_READY` | 準備未完了。配送の準備がまだ完了していない状態。 |
| `READY_FOR_DELIVERY` | 配送準備完了。配送の準備が完了し、出荷可能な状態。 |
| `PICKED_UP` | 集荷済み。配送業者によって集荷された状態。 |
| `IN_TRANSIT` | 輸送中。現在輸送途中の状態。 |
| `DELIVERED` | 配送完了。配送先に到着し、受け取られた状態。 |
| `PARTIALLY_DELIVERED` | 一部配送完了。一部のアイテムのみが配送された状態。 |
| `DELIVERY_FAILED` | 配送失敗。配送が失敗した状態。 |
| `RETURNED` | 返品済み。配送物が返品された状態。 |
| `WAITING_FOR_PICKUP` | 集荷待ち。配送業者による集荷を待っている状態。 |
| `DELAYED` | 遅延。何らかの理由で配送が遅延している状態。 |

## 配送ステータスとドキュメントステータスの関係

配送ステータスとドキュメントステータスは互いに関連していますが、それぞれ異なる側面を追跡します：

- ドキュメントステータス：ドキュメント処理全体の状態（`DRAFT`、`CONFIRMED`など）
- 配送ステータス：配送物自体の物理的な状態（`READY_FOR_DELIVERY`、`IN_TRANSIT`など）

一般的に、ドキュメントステータスが`CONFIRMED`になると、配送ステータスは`NOT_READY`から`READY_FOR_DELIVERY`に変わります。そして、配送ステータスが`DELIVERED`になると、ドキュメントステータスは`DELIVERED`または`COMPLETED`に更新されます。

## API上での使用例

### 出荷配送一覧の取得（GET /api/v1/outbound_delivery）

配送ステータスでフィルタリングする例：

```
GET /api/v1/outbound_delivery?delivery_status=IN_TRANSIT
```

### 配送状況の更新（非公開API）

```json
{
  "delivery_status": "DELIVERED",
  "delivered_at": "2023-06-15T14:30:00+09:00"
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

# 特定の配送ステータスの出荷配送一覧を取得
in_transit_deliveries = client.outbound_delivery.list(delivery_status="IN_TRANSIT")

# 結果の表示
for delivery in in_transit_deliveries.get("items", []):
    print(f"配送ID: {delivery.get('id')}")
    print(f"配送ステータス: {delivery.get('delivery_status')}")
    print(f"追跡番号: {delivery.get('tracking_number')}")
    print("---")
```

## 関連リソース

- [出荷配送 (Outbound Delivery) API](../interface/outbound_delivery.md)
- [入荷配送 (Inbound Delivery) API](../interface/inbound_delivery.md)
- [ドキュメントステータス (Document Status)](document_status.md)
- [配送方法 (Delivery Method)](delivery_method.md) 