# ロケーション API

ロケーションAPIは、倉庫内の保管場所や作業場所を管理するためのインターフェースを提供します。

## 概要

ロケーションは、倉庫内の物理的な保管場所や作業場所を表します。ロケーションAPIを使用することで、倉庫内のすべての場所を適切に管理し、商品の保管、ピッキング、梱包などの作業を効率化することができます。

## API エンドポイント

### ロケーション一覧の取得

```
GET /api/v1/location
```

#### 認証

このAPIを使用するには、OAuth2アクセストークンが必要です。

#### リクエストパラメータ

| パラメータ | 型 | 必須 | 説明 |
|------|------|------|------|
| `warehouse_code` | string | いいえ | 倉庫コードでフィルタリング |
| `location_code` | string | いいえ | ロケーションコードでフィルタリング |
| `location_type` | string | いいえ | ロケーションタイプでフィルタリング（例：`STORAGE`、`RECEIVING`、`SHIPPING`） |
| `is_active` | boolean | いいえ | アクティブ状態でフィルタリング（`true` または `false`） |
| `limit` | integer | いいえ | 1ページあたりの最大件数（デフォルト: 100） |
| `offset` | integer | いいえ | 取得開始位置（デフォルト: 0） |
| `sort` | string | いいえ | 並び順（例：`location_code`, `-created_at`） |

#### レスポンスフィールド

| フィールド | 型 | 説明 |
|------|------|------|
| `items` | array | ロケーション情報の配列 |
| `total_count` | integer | 検索条件に一致する総件数 |
| `limit` | integer | 1ページあたりの最大件数 |
| `offset` | integer | 取得開始位置 |

`items`配列の各要素には、以下のフィールドが含まれます：

| フィールド | 型 | 説明 |
|------|------|------|
| `id` | string | ロケーションID |
| `warehouse_code` | string | 倉庫コード |
| `warehouse_name` | string | 倉庫名 |
| `location_code` | string | ロケーションコード |
| `location_name` | string | ロケーション名 |
| `location_type` | string | ロケーションタイプ（`STORAGE`、`RECEIVING`、`SHIPPING`など） |
| `is_active` | boolean | アクティブ状態 |
| `dimensions` | object | 寸法情報 |
| `capacity` | object | 収容能力情報 |
| `note` | string | 備考 |
| `created_at` | string | 作成日時（ISO 8601形式） |
| `updated_at` | string | 更新日時（ISO 8601形式） |

`dimensions`オブジェクトには、以下のフィールドが含まれます：

| フィールド | 型 | 説明 |
|------|------|------|
| `length` | number | 長さ（cm） |
| `width` | number | 幅（cm） |
| `height` | number | 高さ（cm） |

`capacity`オブジェクトには、以下のフィールドが含まれます：

| フィールド | 型 | 説明 |
|------|------|------|
| `weight_capacity` | number | 重量容量（kg） |
| `volume_capacity` | number | 体積容量（m³） |
| `quantity_capacity` | integer | 数量容量（個数） |

#### レスポンス例

```json
{
  "items": [
    {
      "id": "L123456",
      "warehouse_code": "WH001",
      "warehouse_name": "東京倉庫",
      "location_code": "A-01-01",
      "location_name": "エリアA 棚01 段01",
      "location_type": "STORAGE",
      "is_active": true,
      "dimensions": {
        "length": 100.0,
        "width": 80.0,
        "height": 200.0
      },
      "capacity": {
        "weight_capacity": 500.0,
        "volume_capacity": 1.6,
        "quantity_capacity": 50
      },
      "note": "一般商品用保管エリア",
      "created_at": "2023-04-01T09:00:00+09:00",
      "updated_at": "2023-04-01T09:00:00+09:00"
    }
  ],
  "total_count": 1,
  "limit": 100,
  "offset": 0
}
```

### 特定のロケーションの取得

```
GET /api/v1/location/{location_id}
```

#### 認証

このAPIを使用するには、OAuth2アクセストークンが必要です。

#### パスパラメータ

| パラメータ | 型 | 必須 | 説明 |
|------|------|------|------|
| `location_id` | string | はい | ロケーションID |

#### レスポンスフィールド

特定のロケーションの詳細情報が返されます。フィールドは「ロケーション一覧の取得」のレスポンスの`items`配列の要素と同じです。

### ロケーションの作成

```
POST /api/v1/location
```

#### 認証

このAPIを使用するには、OAuth2アクセストークンが必要です。

#### リクエストボディ

| フィールド | 型 | 必須 | 説明 |
|------|------|------|------|
| `warehouse_code` | string | はい | 倉庫コード |
| `location_code` | string | はい | ロケーションコード |
| `location_name` | string | いいえ | ロケーション名 |
| `location_type` | string | はい | ロケーションタイプ |
| `is_active` | boolean | いいえ | アクティブ状態（デフォルト: `true`） |
| `dimensions` | object | いいえ | 寸法情報 |
| `capacity` | object | いいえ | 収容能力情報 |
| `note` | string | いいえ | 備考 |

#### リクエスト例

```json
{
  "warehouse_code": "WH001",
  "location_code": "A-02-01",
  "location_name": "エリアA 棚02 段01",
  "location_type": "STORAGE",
  "is_active": true,
  "dimensions": {
    "length": 100.0,
    "width": 80.0,
    "height": 200.0
  },
  "capacity": {
    "weight_capacity": 500.0,
    "volume_capacity": 1.6,
    "quantity_capacity": 50
  },
  "note": "冷蔵品用保管エリア"
}
```

#### レスポンスフィールド

作成されたロケーションの詳細情報が返されます。

### ロケーションの更新

```
PUT /api/v1/location/{location_id}
```

#### 認証

このAPIを使用するには、OAuth2アクセストークンが必要です。

#### パスパラメータ

| パラメータ | 型 | 必須 | 説明 |
|------|------|------|------|
| `location_id` | string | はい | ロケーションID |

#### リクエストボディ

| フィールド | 型 | 必須 | 説明 |
|------|------|------|------|
| `warehouse_code` | string | いいえ | 倉庫コード |
| `location_code` | string | いいえ | ロケーションコード |
| `location_name` | string | いいえ | ロケーション名 |
| `location_type` | string | いいえ | ロケーションタイプ |
| `is_active` | boolean | いいえ | アクティブ状態 |
| `dimensions` | object | いいえ | 寸法情報 |
| `capacity` | object | いいえ | 収容能力情報 |
| `note` | string | いいえ | 備考 |

更新したいフィールドのみを含めることができます。

#### リクエスト例

```json
{
  "is_active": false,
  "note": "メンテナンス中のため一時的に非アクティブ"
}
```

#### レスポンスフィールド

更新されたロケーションの詳細情報が返されます。

## エラーコード

| ステータスコード | 説明 |
|------|------|
| `400` | リクエストパラメータが無効 |
| `401` | 認証エラー |
| `403` | アクセス権限がない |
| `404` | 指定されたリソースが存在しない |
| `409` | リソースの競合（例：既に存在するロケーションコード） |
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

# ロケーション一覧を取得
locations = client.location.list(
    warehouse_code="WH001",
    location_type="STORAGE",
    is_active=True,
    limit=10
)

# 結果の表示
for location in locations.get("items", []):
    print(f"ロケーションID: {location.get('id')}")
    print(f"ロケーションコード: {location.get('location_code')}")
    print(f"ロケーション名: {location.get('location_name')}")
    print(f"タイプ: {location.get('location_type')}")
    print("---")

# 新しいロケーションを作成
new_location = {
    "warehouse_code": "WH001",
    "location_code": "B-01-01",
    "location_name": "エリアB 棚01 段01",
    "location_type": "STORAGE",
    "is_active": True,
    "dimensions": {
        "length": 100.0,
        "width": 80.0,
        "height": 200.0
    },
    "capacity": {
        "weight_capacity": 500.0,
        "volume_capacity": 1.6,
        "quantity_capacity": 50
    },
    "note": "冷凍品用保管エリア"
}

created_location = client.location.create(location=new_location)
print(f"作成されたロケーションID: {created_location.get('id')}")

# ロケーションを更新
client.location.update(
    location_id=created_location.get('id'),
    is_active=False,
    note="メンテナンス中のため一時的に非アクティブ"
)
```

## 関連リソース

- [倉庫 (Warehouse) API](warehouse.md)
- [実在庫サマリー (Actual Inventory Summary) API](actual_inventory_summary.md)
- [トランザクションログ (Transaction Log) API](transaction_log.md) 