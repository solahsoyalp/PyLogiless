# ドキュメントステータス (Document Status)

ドキュメントステータスは、配送や注文などの処理状態を表す区分です。

## 概要

ドキュメントステータスは、入荷配送、出荷配送、倉庫間移動などのドキュメントの処理状態を管理するために使用されます。各ドキュメントは作成から完了までのライフサイクルを持ち、そのステータスは順次更新されていきます。

## 使用できる値

| 値 | 説明 |
|------|------|
| `DRAFT` | 下書き。初期作成状態でまだ確定していない状態。 |
| `CONFIRMED` | 確定済み。内容が確認・承認され、処理可能な状態。 |
| `IN_PROCESS` | 処理中。現在処理が進行している状態。 |
| `DELIVERED` | 配送済み。配送が完了した状態。 |
| `COMPLETED` | 完了。全ての処理が完了した状態。 |
| `CANCELED` | キャンセル。処理がキャンセルされた状態。 |
| `ON_HOLD` | 保留中。何らかの理由で処理が保留されている状態。 |
| `REJECTED` | 拒否。処理が拒否された状態。 |
| `PARTIALLY_DELIVERED` | 一部配送済み。一部のアイテムのみが配送完了した状態。 |
| `PARTIALLY_COMPLETED` | 一部完了。一部のアイテムのみが処理完了した状態。 |

## ステータスの遷移

各ドキュメントタイプによってステータスの遷移ルールは異なりますが、一般的な遷移の流れは以下の通りです：

1. `DRAFT` - 下書き（初期状態）
2. `CONFIRMED` - 確定済み
3. `IN_PROCESS` - 処理中
4. `DELIVERED` / `PARTIALLY_DELIVERED` - 配送済み / 一部配送済み
5. `COMPLETED` / `PARTIALLY_COMPLETED` - 完了 / 一部完了

`CANCELED`ステータスへは、通常`DRAFT`または`CONFIRMED`ステータスからのみ遷移可能です。
`ON_HOLD`や`REJECTED`ステータスは、特定の条件下でのみ使用されます。

## API上での使用例

### 出荷配送のステータス更新（PUT /api/v1/outbound_delivery/{id}/status）

```json
{
  "document_status": "CONFIRMED"
}
```

### 出荷配送一覧の取得（GET /api/v1/outbound_delivery）

ドキュメントステータスでフィルタリングする例：

```
GET /api/v1/outbound_delivery?document_status=IN_PROCESS
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

# 特定のステータスの出荷配送一覧を取得
in_process_deliveries = client.outbound_delivery.list(document_status="IN_PROCESS")

# 出荷配送のステータスを更新
confirmed_delivery = client.outbound_delivery.update_status("OD00001", {
    "document_status": "CONFIRMED"
})
```

## 関連リソース

- [出荷配送 (Outbound Delivery) API](../interface/outbound_delivery.md)
- [入荷配送 (Inbound Delivery) API](../interface/inbound_delivery.md)
- [倉庫間移動 (Inter Warehouse Transfer) API](../interface/inter_warehouse_transfer.md)
- [配送ステータス (Delivery Status)](delivery_status.md)
- [ドキュメント明細ステータス (Document Line Status)](document_line_status.md) 