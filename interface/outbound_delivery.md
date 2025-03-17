# 出荷配送 (Outbound Delivery) API

このAPIでは、出荷配送情報の作成、取得、更新を行うことができます。

## エンドポイント

- `GET /api/v1/outbound_delivery` - 出荷配送一覧の取得
- `GET /api/v1/outbound_delivery/{id}` - 特定の出荷配送の取得
- `POST /api/v1/outbound_delivery` - 出荷配送の作成
- `PUT /api/v1/outbound_delivery/{id}` - 出荷配送の更新
- `PUT /api/v1/outbound_delivery/{id}/status` - 出荷配送のステータス更新

## 認証

このAPIを使用するには、適切なアクセス権を持つOAuth2アクセストークンが必要です。認証の詳細については、[認証ガイド](../docs/authentication.md)を参照してください。

## 一覧取得（GET /api/v1/outbound_delivery）

### リクエストパラメータ

| パラメータ名 | 型 | 必須 | 説明 |
|------------|------|------|------|
| reference_id | string | いいえ | 参照IDでフィルタリング |
| store_code | string | いいえ | 店舗コードでフィルタリング |
| warehouse_code | string | いいえ | 倉庫コードでフィルタリング |
| document_status | string | いいえ | ドキュメントステータスでフィルタリング。詳細は[ドキュメントステータス](../type/document_status.md)を参照 |
| delivery_status | string | いいえ | 配送ステータスでフィルタリング。詳細は[配送ステータス](../type/delivery_status.md)を参照 |
| delivery_method | string | いいえ | 配送方法でフィルタリング。詳細は[配送方法](../type/delivery_method.md)を参照 |
| date_from | string | いいえ | この日付以降の配送予定日でフィルタリング（ISO 8601形式：YYYY-MM-DD） |
| date_to | string | いいえ | この日付以前の配送予定日でフィルタリング（ISO 8601形式：YYYY-MM-DD） |
| limit | integer | いいえ | 取得する結果の最大数（デフォルト: 100, 最大: 1000） |
| offset | integer | いいえ | 結果セットの開始オフセット（ページング用、デフォルト: 0） |
| sort | string | いいえ | ソートフィールドとソート順（例: `scheduled_delivery_date:asc`, `created_at:desc`） |

### レスポンスフィールド

| フィールド名 | 型 | 説明 |
|------------|------|------|
| items | array | 出荷配送オブジェクトの配列 |
| total_count | integer | 条件に一致する総出荷配送数 |
| limit | integer | 適用されたlimitパラメータ |
| offset | integer | 適用されたoffsetパラメータ |

### 出荷配送オブジェクトのフィールド

| フィールド名 | 型 | 説明 |
|------------|------|------|
| id | string | 出荷配送ID（一意） |
| reference_id | string | 外部システムの参照ID |
| store_code | string | 店舗コード |
| store_name | string | 店舗名 |
| warehouse_code | string | 倉庫コード |
| warehouse_name | string | 倉庫名 |
| document_status | string | ドキュメントステータス。詳細は[ドキュメントステータス](../type/document_status.md)を参照 |
| delivery_status | string | 配送ステータス。詳細は[配送ステータス](../type/delivery_status.md)を参照 |
| scheduled_delivery_date | string | 配送予定日（ISO 8601形式：YYYY-MM-DD） |
| delivery_method | string | 配送方法。詳細は[配送方法](../type/delivery_method.md)を参照 |
| express_type | string | 配達便区分。詳細は[配達便区分](../type/express_type.md)を参照 |
| tracking_number | string | 追跡番号 |
| note | string | 備考 |
| items | array | 出荷配送明細の配列 |
| created_at | string | 作成日時（ISO 8601形式） |
| updated_at | string | 更新日時（ISO 8601形式） |

### 出荷配送明細オブジェクトのフィールド

| フィールド名 | 型 | 説明 |
|------------|------|------|
| line_id | string | 明細ID |
| article_code | string | 商品コード |
| article_name | string | 商品名 |
| quantity | number | 数量 |
| unit_of_measure | string | 単位 |
| status | string | 明細ステータス。詳細は[ドキュメント明細ステータス](../type/document_line_status.md)を参照 |
| delivered_quantity | number | 出荷済み数量 |
| note | string | 備考 |

### レスポンス例

```json
{
  "items": [
    {
      "id": "OD00001",
      "reference_id": "REF123",
      "store_code": "STORE001",
      "store_name": "テスト店舗1",
      "warehouse_code": "WH001",
      "warehouse_name": "東京倉庫",
      "document_status": "CONFIRMED",
      "delivery_status": "READY_FOR_DELIVERY",
      "scheduled_delivery_date": "2023-06-15",
      "delivery_method": "NORMAL",
      "express_type": "MORNING",
      "tracking_number": "1234567890",
      "note": "テスト出荷",
      "items": [
        {
          "line_id": "1",
          "article_code": "ARTICLE001",
          "article_name": "テスト商品1",
          "quantity": 10,
          "unit_of_measure": "個",
          "status": "READY",
          "delivered_quantity": 0,
          "note": null
        },
        {
          "line_id": "2",
          "article_code": "ARTICLE002",
          "article_name": "テスト商品2",
          "quantity": 5,
          "unit_of_measure": "個",
          "status": "READY",
          "delivered_quantity": 0,
          "note": null
        }
      ],
      "created_at": "2023-06-01T10:30:00+09:00",
      "updated_at": "2023-06-01T15:45:00+09:00"
    }
  ],
  "total_count": 1,
  "limit": 100,
  "offset": 0
}
```

## 特定の出荷配送の取得（GET /api/v1/outbound_delivery/{id}）

### URLパラメータ

| パラメータ名 | 型 | 必須 | 説明 |
|------------|------|------|------|
| id | string | はい | 取得する出荷配送のID |

### レスポンス

[出荷配送オブジェクト](#出荷配送オブジェクトのフィールド)を返します。

## 出荷配送の作成（POST /api/v1/outbound_delivery）

### リクエストボディ

| フィールド名 | 型 | 必須 | 説明 |
|------------|------|------|------|
| reference_id | string | いいえ | 外部システムの参照ID |
| store_code | string | はい | 店舗コード |
| warehouse_code | string | はい | 倉庫コード |
| scheduled_delivery_date | string | はい | 配送予定日（ISO 8601形式：YYYY-MM-DD） |
| delivery_method | string | はい | 配送方法。詳細は[配送方法](../type/delivery_method.md)を参照 |
| express_type | string | いいえ | 配達便区分。詳細は[配達便区分](../type/express_type.md)を参照 |
| tracking_number | string | いいえ | 追跡番号 |
| note | string | いいえ | 備考 |
| items | array | はい | 出荷配送明細の配列 |

### 出荷配送明細リクエストのフィールド

| フィールド名 | 型 | 必須 | 説明 |
|------------|------|------|------|
| line_id | string | はい | 明細ID（リクエスト内で一意） |
| article_code | string | はい | 商品コード |
| quantity | number | はい | 数量 |
| note | string | いいえ | 備考 |

### リクエスト例

```json
{
  "reference_id": "REF123",
  "store_code": "STORE001",
  "warehouse_code": "WH001",
  "scheduled_delivery_date": "2023-06-15",
  "delivery_method": "NORMAL",
  "express_type": "MORNING",
  "tracking_number": "1234567890",
  "note": "テスト出荷",
  "items": [
    {
      "line_id": "1",
      "article_code": "ARTICLE001",
      "quantity": 10,
      "note": null
    },
    {
      "line_id": "2",
      "article_code": "ARTICLE002",
      "quantity": 5,
      "note": null
    }
  ]
}
```

### レスポンス

作成された[出荷配送オブジェクト](#出荷配送オブジェクトのフィールド)を返します。
新しく作成された出荷配送のドキュメントステータスは`DRAFT`になります。

## 出荷配送の更新（PUT /api/v1/outbound_delivery/{id}）

### URLパラメータ

| パラメータ名 | 型 | 必須 | 説明 |
|------------|------|------|------|
| id | string | はい | 更新する出荷配送のID |

### リクエストボディ

更新したいフィールドのみを含めることができます。
注意：出荷配送のステータスが`CONFIRMED`以降の場合、一部のフィールドは更新できません。

| フィールド名 | 型 | 必須 | 説明 |
|------------|------|------|------|
| reference_id | string | いいえ | 外部システムの参照ID |
| store_code | string | いいえ | 店舗コード |
| warehouse_code | string | いいえ | 倉庫コード |
| scheduled_delivery_date | string | いいえ | 配送予定日（ISO 8601形式：YYYY-MM-DD） |
| delivery_method | string | いいえ | 配送方法。詳細は[配送方法](../type/delivery_method.md)を参照 |
| express_type | string | いいえ | 配達便区分。詳細は[配達便区分](../type/express_type.md)を参照 |
| tracking_number | string | いいえ | 追跡番号 |
| note | string | いいえ | 備考 |
| items | array | いいえ | 出荷配送明細の配列 |

### リクエスト例

```json
{
  "scheduled_delivery_date": "2023-06-20",
  "note": "配送日を変更しました",
  "tracking_number": "9876543210"
}
```

### レスポンス

更新された[出荷配送オブジェクト](#出荷配送オブジェクトのフィールド)を返します。

## 出荷配送のステータス更新（PUT /api/v1/outbound_delivery/{id}/status）

### URLパラメータ

| パラメータ名 | 型 | 必須 | 説明 |
|------------|------|------|------|
| id | string | はい | 更新する出荷配送のID |

### リクエストボディ

| フィールド名 | 型 | 必須 | 説明 |
|------------|------|------|------|
| document_status | string | はい | 新しいドキュメントステータス。詳細は[ドキュメントステータス](../type/document_status.md)を参照 |

### リクエスト例

```json
{
  "document_status": "CONFIRMED"
}
```

### レスポンス

更新された[出荷配送オブジェクト](#出荷配送オブジェクトのフィールド)を返します。

## ステータスの遷移

出荷配送のドキュメントステータスは以下の順序で遷移します：

1. `DRAFT` - 下書き（初期状態）
2. `CONFIRMED` - 確定済み
3. `IN_PROCESS` - 処理中
4. `DELIVERED` - 配送済み
5. `COMPLETED` - 完了
6. `CANCELED` - キャンセル

`CANCELED`ステータスへは、`DRAFT`または`CONFIRMED`ステータスからのみ遷移可能です。

## エラーコード

| ステータスコード | エラーコード | 説明 |
|---------------|-------------|------|
| 400 | validation_error | リクエストパラメータまたはボディが無効です |
| 401 | unauthorized | アクセストークンが無効または期限切れです |
| 403 | forbidden | このリソースへのアクセス権がありません |
| 404 | not_found | 指定された出荷配送が見つかりません |
| 409 | status_transition_invalid | 現在のステータスから指定されたステータスへの遷移は許可されていません |
| 422 | insufficient_stock | 在庫不足のため処理できません |
| 500 | internal_server_error | サーバー内部エラーが発生しました |

詳細なエラーコードについては、[エラーコードリファレンス](../docs/errors.md)を参照してください。

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

# 出荷配送一覧の取得
deliveries = client.outbound_delivery.list(
    warehouse_code="WH001",
    date_from="2023-06-01",
    date_to="2023-06-30",
    limit=10
)

# 特定の出荷配送の取得
delivery = client.outbound_delivery.get("OD00001")

# 出荷配送の作成
new_delivery = client.outbound_delivery.create({
    "reference_id": "REF123",
    "store_code": "STORE001",
    "warehouse_code": "WH001",
    "scheduled_delivery_date": "2023-06-15",
    "delivery_method": "NORMAL",
    "items": [
        {
            "line_id": "1",
            "article_code": "ARTICLE001",
            "quantity": 10
        }
    ]
})

# 出荷配送の更新
updated_delivery = client.outbound_delivery.update("OD00001", {
    "scheduled_delivery_date": "2023-06-20"
})

# 出荷配送のステータス更新
confirmed_delivery = client.outbound_delivery.update_status("OD00001", {
    "document_status": "CONFIRMED"
})

# 結果の表示
for item in deliveries.get("items", []):
    print(f"配送ID: {item.get('id')}, 店舗: {item.get('store_name')}, 配送予定日: {item.get('scheduled_delivery_date')}")
```

## 関連リソース

- [店舗 (Store)](store.md)
- [倉庫 (Warehouse)](warehouse.md)
- [商品 (Article)](article.md)
- [ドキュメントステータス (Document Status)](../type/document_status.md)
- [配送ステータス (Delivery Status)](../type/delivery_status.md)
- [配送方法 (Delivery Method)](../type/delivery_method.md)
- [配達便区分 (Express Type)](../type/express_type.md)
- [ドキュメント明細ステータス (Document Line Status)](../type/document_line_status.md) 