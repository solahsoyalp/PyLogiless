# 倉庫 API

倉庫APIは、商品を保管・管理する物理的な施設の情報を管理するためのインターフェースを提供します。

## 概要

倉庫は、商品の保管、ピッキング、梱包、出荷などの物流業務を行う施設です。倉庫APIを使用することで、倉庫の登録、更新、取得を行い、在庫管理や物流業務の効率化を図ることができます。

## API エンドポイント

### 倉庫一覧の取得

```
GET /api/v1/warehouse
```

#### 認証

このAPIを使用するには、OAuth2アクセストークンが必要です。

#### リクエストパラメータ

| パラメータ | 型 | 必須 | 説明 |
|------|------|------|------|
| `warehouse_code` | string | いいえ | 倉庫コードでフィルタリング |
| `warehouse_name` | string | いいえ | 倉庫名でフィルタリング（部分一致） |
| `is_active` | boolean | いいえ | アクティブ状態でフィルタリング（`true` または `false`） |
| `limit` | integer | いいえ | 1ページあたりの最大件数（デフォルト: 100） |
| `offset` | integer | いいえ | 取得開始位置（デフォルト: 0） |
| `sort` | string | いいえ | 並び順（例：`warehouse_code`, `-created_at`） |

#### レスポンスフィールド

| フィールド | 型 | 説明 |
|------|------|------|
| `items` | array | 倉庫情報の配列 |
| `total_count` | integer | 検索条件に一致する総件数 |
| `limit` | integer | 1ページあたりの最大件数 |
| `offset` | integer | 取得開始位置 |

`items`配列の各要素には、以下のフィールドが含まれます：

| フィールド | 型 | 説明 |
|------|------|------|
| `id` | string | 倉庫ID |
| `warehouse_code` | string | 倉庫コード |
| `warehouse_name` | string | 倉庫名 |
| `warehouse_type` | string | 倉庫タイプ（`DISTRIBUTION_CENTER`、`STORE`、`MANUFACTURER`など） |
| `address` | object | 住所情報 |
| `contact` | object | 連絡先情報 |
| `capacity` | object | 倉庫容量情報 |
| `operating_hours` | object | 営業時間情報 |
| `features` | array | 倉庫の特徴や機能のリスト |
| `is_active` | boolean | アクティブ状態 |
| `note` | string | 備考 |
| `created_at` | string | 作成日時（ISO 8601形式） |
| `updated_at` | string | 更新日時（ISO 8601形式） |

`address`オブジェクトには、以下のフィールドが含まれます：

| フィールド | 型 | 説明 |
|------|------|------|
| `postal_code` | string | 郵便番号 |
| `prefecture` | string | 都道府県 |
| `city` | string | 市区町村 |
| `street` | string | 番地・建物名 |
| `country` | string | 国名（デフォルト: "Japan"） |

`contact`オブジェクトには、以下のフィールドが含まれます：

| フィールド | 型 | 説明 |
|------|------|------|
| `contact_person` | string | 担当者名 |
| `phone` | string | 電話番号 |
| `email` | string | メールアドレス |
| `fax` | string | FAX番号 |

`capacity`オブジェクトには、以下のフィールドが含まれます：

| フィールド | 型 | 説明 |
|------|------|------|
| `total_area` | number | 総面積（m²） |
| `storage_capacity` | number | 保管容量（m³） |
| `max_weight_capacity` | number | 最大重量容量（kg） |

`operating_hours`オブジェクトには、以下のフィールドが含まれます：

| フィールド | 型 | 説明 |
|------|------|------|
| `weekday_open` | string | 平日の開始時間（HH:MM形式） |
| `weekday_close` | string | 平日の終了時間（HH:MM形式） |
| `weekend_open` | string | 週末の開始時間（HH:MM形式） |
| `weekend_close` | string | 週末の終了時間（HH:MM形式） |
| `time_zone` | string | タイムゾーン（例："Asia/Tokyo"） |

#### レスポンス例

```json
{
  "items": [
    {
      "id": "W123456",
      "warehouse_code": "WH001",
      "warehouse_name": "東京倉庫",
      "warehouse_type": "DISTRIBUTION_CENTER",
      "address": {
        "postal_code": "140-0002",
        "prefecture": "東京都",
        "city": "品川区",
        "street": "東品川1-1-1",
        "country": "Japan"
      },
      "contact": {
        "contact_person": "田中一郎",
        "phone": "03-1234-5678",
        "email": "tanaka@example.com",
        "fax": "03-1234-5679"
      },
      "capacity": {
        "total_area": 5000.0,
        "storage_capacity": 15000.0,
        "max_weight_capacity": 500000.0
      },
      "operating_hours": {
        "weekday_open": "09:00",
        "weekday_close": "18:00",
        "weekend_open": "10:00",
        "weekend_close": "15:00",
        "time_zone": "Asia/Tokyo"
      },
      "features": [
        "TEMPERATURE_CONTROLLED",
        "HAZARDOUS_GOODS",
        "HIGH_SECURITY"
      ],
      "is_active": true,
      "note": "主要配送センター",
      "created_at": "2023-04-01T09:00:00+09:00",
      "updated_at": "2023-04-01T09:00:00+09:00"
    }
  ],
  "total_count": 1,
  "limit": 100,
  "offset": 0
}
```

### 特定の倉庫の取得

```
GET /api/v1/warehouse/{warehouse_id}
```

#### 認証

このAPIを使用するには、OAuth2アクセストークンが必要です。

#### パスパラメータ

| パラメータ | 型 | 必須 | 説明 |
|------|------|------|------|
| `warehouse_id` | string | はい | 倉庫ID |

#### レスポンスフィールド

特定の倉庫の詳細情報が返されます。フィールドは「倉庫一覧の取得」のレスポンスの`items`配列の要素と同じです。

### 倉庫の作成

```
POST /api/v1/warehouse
```

#### 認証

このAPIを使用するには、OAuth2アクセストークンが必要です。

#### リクエストボディ

| フィールド | 型 | 必須 | 説明 |
|------|------|------|------|
| `warehouse_code` | string | はい | 倉庫コード |
| `warehouse_name` | string | はい | 倉庫名 |
| `warehouse_type` | string | はい | 倉庫タイプ |
| `address` | object | いいえ | 住所情報 |
| `contact` | object | いいえ | 連絡先情報 |
| `capacity` | object | いいえ | 倉庫容量情報 |
| `operating_hours` | object | いいえ | 営業時間情報 |
| `features` | array | いいえ | 倉庫の特徴や機能のリスト |
| `is_active` | boolean | いいえ | アクティブ状態（デフォルト: `true`） |
| `note` | string | いいえ | 備考 |

#### リクエスト例

```json
{
  "warehouse_code": "WH002",
  "warehouse_name": "大阪倉庫",
  "warehouse_type": "DISTRIBUTION_CENTER",
  "address": {
    "postal_code": "550-0001",
    "prefecture": "大阪府",
    "city": "大阪市西区",
    "street": "土佐堀1-1-1",
    "country": "Japan"
  },
  "contact": {
    "contact_person": "山本太郎",
    "phone": "06-1234-5678",
    "email": "yamamoto@example.com",
    "fax": "06-1234-5679"
  },
  "capacity": {
    "total_area": 3000.0,
    "storage_capacity": 9000.0,
    "max_weight_capacity": 300000.0
  },
  "operating_hours": {
    "weekday_open": "09:00",
    "weekday_close": "18:00",
    "weekend_open": null,
    "weekend_close": null,
    "time_zone": "Asia/Tokyo"
  },
  "features": [
    "TEMPERATURE_CONTROLLED"
  ],
  "is_active": true,
  "note": "関西地域の配送拠点"
}
```

#### レスポンスフィールド

作成された倉庫の詳細情報が返されます。

### 倉庫の更新

```
PUT /api/v1/warehouse/{warehouse_id}
```

#### 認証

このAPIを使用するには、OAuth2アクセストークンが必要です。

#### パスパラメータ

| パラメータ | 型 | 必須 | 説明 |
|------|------|------|------|
| `warehouse_id` | string | はい | 倉庫ID |

#### リクエストボディ

| フィールド | 型 | 必須 | 説明 |
|------|------|------|------|
| `warehouse_code` | string | いいえ | 倉庫コード |
| `warehouse_name` | string | いいえ | 倉庫名 |
| `warehouse_type` | string | いいえ | 倉庫タイプ |
| `address` | object | いいえ | 住所情報 |
| `contact` | object | いいえ | 連絡先情報 |
| `capacity` | object | いいえ | 倉庫容量情報 |
| `operating_hours` | object | いいえ | 営業時間情報 |
| `features` | array | いいえ | 倉庫の特徴や機能のリスト |
| `is_active` | boolean | いいえ | アクティブ状態 |
| `note` | string | いいえ | 備考 |

更新したいフィールドのみを含めることができます。

#### リクエスト例

```json
{
  "contact": {
    "contact_person": "山本次郎",
    "phone": "06-1234-5678",
    "email": "yamamoto.jiro@example.com",
    "fax": "06-1234-5679"
  },
  "operating_hours": {
    "weekday_open": "08:30",
    "weekday_close": "19:00",
    "weekend_open": "10:00",
    "weekend_close": "15:00",
    "time_zone": "Asia/Tokyo"
  },
  "note": "営業時間と担当者が変更になりました"
}
```

#### レスポンスフィールド

更新された倉庫の詳細情報が返されます。

## エラーコード

| ステータスコード | 説明 |
|------|------|
| `400` | リクエストパラメータが無効 |
| `401` | 認証エラー |
| `403` | アクセス権限がない |
| `404` | 指定されたリソースが存在しない |
| `409` | リソースの競合（例：既に存在する倉庫コード） |
| `500` | サーバーエラー |

## 使用例（Python pylogilessライブラリ使用）

```python
from pylogiless import LogilessClient

client = LogilessClient(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    redirect_uri="YOUR_REDIRECT_URI"
)
client.set_token(access_token="YOUR_ACCESS_TOKEN", refresh_token="YOUR_REFRESH_TOKEN")

# 倉庫一覧を取得
warehouses = client.warehouse.list(
    is_active=True,
    limit=10
)

# 結果の表示
for warehouse in warehouses.get("items", []):
    print(f"倉庫ID: {warehouse.get('id')}")
    print(f"倉庫コード: {warehouse.get('warehouse_code')}")
    print(f"倉庫名: {warehouse.get('warehouse_name')}")
    print(f"倉庫タイプ: {warehouse.get('warehouse_type')}")
    print(f"所在地: {warehouse.get('address', {}).get('prefecture')} {warehouse.get('address', {}).get('city')}")
    print("---")

# 新しい倉庫を作成
new_warehouse = {
    "warehouse_code": "WH003",
    "warehouse_name": "福岡倉庫",
    "warehouse_type": "DISTRIBUTION_CENTER",
    "address": {
        "postal_code": "812-0012",
        "prefecture": "福岡県",
        "city": "福岡市博多区",
        "street": "博多駅中央街1-1-1",
        "country": "Japan"
    },
    "contact": {
        "contact_person": "佐藤健太",
        "phone": "092-123-4567",
        "email": "sato@example.com",
        "fax": "092-123-4568"
    },
    "capacity": {
        "total_area": 2000.0,
        "storage_capacity": 6000.0,
        "max_weight_capacity": 200000.0
    },
    "operating_hours": {
        "weekday_open": "09:00",
        "weekday_close": "18:00",
        "weekend_open": null,
        "weekend_close": null,
        "time_zone": "Asia/Tokyo"
    },
    "features": [],
    "is_active": True,
    "note": "九州地域の配送拠点"
}

created_warehouse = client.warehouse.create(warehouse=new_warehouse)
print(f"作成された倉庫ID: {created_warehouse.get('id')}")

# 倉庫を更新
client.warehouse.update(
    warehouse_id=created_warehouse.get('id'),
    features=["TEMPERATURE_CONTROLLED"],
    note="温度管理機能を追加しました"
)
```

## 関連リソース

- [ロケーション (Location) API](location.md)
- [実在庫サマリー (Actual Inventory Summary) API](actual_inventory_summary.md)
- [入荷配送 (Inbound Delivery) API](inbound_delivery.md)
- [出荷配送 (Outbound Delivery) API](outbound_delivery.md)
- [倉庫間転送 (Inter-Warehouse Transfer) API](inter_warehouse_transfer.md) 