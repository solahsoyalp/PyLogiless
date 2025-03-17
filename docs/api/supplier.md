# 仕入先 API

仕入先APIは、商品を供給する業者や製造元の情報を管理するためのインターフェースを提供します。

## 概要

仕入先は、商品の調達先となる業者や製造元の情報を管理します。仕入先APIを使用することで、取引先情報の登録、更新、取得を行い、入荷配送や発注などの業務に活用することができます。

## API エンドポイント

### 仕入先一覧の取得

```
GET /api/v1/supplier
```

#### 認証

このAPIを使用するには、OAuth2アクセストークンが必要です。

#### リクエストパラメータ

| パラメータ | 型 | 必須 | 説明 |
|------|------|------|------|
| `supplier_code` | string | いいえ | 仕入先コードでフィルタリング |
| `supplier_name` | string | いいえ | 仕入先名でフィルタリング（部分一致） |
| `is_active` | boolean | いいえ | アクティブ状態でフィルタリング（`true` または `false`） |
| `limit` | integer | いいえ | 1ページあたりの最大件数（デフォルト: 100） |
| `offset` | integer | いいえ | 取得開始位置（デフォルト: 0） |
| `sort` | string | いいえ | 並び順（例：`supplier_code`, `-created_at`） |

#### レスポンスフィールド

| フィールド | 型 | 説明 |
|------|------|------|
| `items` | array | 仕入先情報の配列 |
| `total_count` | integer | 検索条件に一致する総件数 |
| `limit` | integer | 1ページあたりの最大件数 |
| `offset` | integer | 取得開始位置 |

`items`配列の各要素には、以下のフィールドが含まれます：

| フィールド | 型 | 説明 |
|------|------|------|
| `id` | string | 仕入先ID |
| `supplier_code` | string | 仕入先コード |
| `supplier_name` | string | 仕入先名 |
| `address` | object | 住所情報 |
| `contact` | object | 連絡先情報 |
| `payment_terms` | object | 支払条件 |
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

`payment_terms`オブジェクトには、以下のフィールドが含まれます：

| フィールド | 型 | 説明 |
|------|------|------|
| `payment_method` | string | 支払方法（`BANK_TRANSFER`、`CREDIT_CARD`など） |
| `payment_term_days` | integer | 支払期間（日数） |
| `currency` | string | 通貨（デフォルト: "JPY"） |

#### レスポンス例

```json
{
  "items": [
    {
      "id": "S123456",
      "supplier_code": "SUP001",
      "supplier_name": "株式会社山田商事",
      "address": {
        "postal_code": "100-0001",
        "prefecture": "東京都",
        "city": "千代田区",
        "street": "大手町1-1-1",
        "country": "Japan"
      },
      "contact": {
        "contact_person": "山田太郎",
        "phone": "03-1234-5678",
        "email": "yamada@example.com",
        "fax": "03-1234-5679"
      },
      "payment_terms": {
        "payment_method": "BANK_TRANSFER",
        "payment_term_days": 30,
        "currency": "JPY"
      },
      "is_active": true,
      "note": "電子機器関連の主要仕入先",
      "created_at": "2023-04-01T09:00:00+09:00",
      "updated_at": "2023-04-01T09:00:00+09:00"
    }
  ],
  "total_count": 1,
  "limit": 100,
  "offset": 0
}
```

### 特定の仕入先の取得

```
GET /api/v1/supplier/{supplier_id}
```

#### 認証

このAPIを使用するには、OAuth2アクセストークンが必要です。

#### パスパラメータ

| パラメータ | 型 | 必須 | 説明 |
|------|------|------|------|
| `supplier_id` | string | はい | 仕入先ID |

#### レスポンスフィールド

特定の仕入先の詳細情報が返されます。フィールドは「仕入先一覧の取得」のレスポンスの`items`配列の要素と同じです。

### 仕入先の作成

```
POST /api/v1/supplier
```

#### 認証

このAPIを使用するには、OAuth2アクセストークンが必要です。

#### リクエストボディ

| フィールド | 型 | 必須 | 説明 |
|------|------|------|------|
| `supplier_code` | string | はい | 仕入先コード |
| `supplier_name` | string | はい | 仕入先名 |
| `address` | object | いいえ | 住所情報 |
| `contact` | object | いいえ | 連絡先情報 |
| `payment_terms` | object | いいえ | 支払条件 |
| `is_active` | boolean | いいえ | アクティブ状態（デフォルト: `true`） |
| `note` | string | いいえ | 備考 |

#### リクエスト例

```json
{
  "supplier_code": "SUP002",
  "supplier_name": "株式会社鈴木製作所",
  "address": {
    "postal_code": "541-0052",
    "prefecture": "大阪府",
    "city": "大阪市中央区",
    "street": "安土町1-1-1",
    "country": "Japan"
  },
  "contact": {
    "contact_person": "鈴木一郎",
    "phone": "06-1234-5678",
    "email": "suzuki@example.com",
    "fax": "06-1234-5679"
  },
  "payment_terms": {
    "payment_method": "BANK_TRANSFER",
    "payment_term_days": 45,
    "currency": "JPY"
  },
  "is_active": true,
  "note": "機械部品の専門メーカー"
}
```

#### レスポンスフィールド

作成された仕入先の詳細情報が返されます。

### 仕入先の更新

```
PUT /api/v1/supplier/{supplier_id}
```

#### 認証

このAPIを使用するには、OAuth2アクセストークンが必要です。

#### パスパラメータ

| パラメータ | 型 | 必須 | 説明 |
|------|------|------|------|
| `supplier_id` | string | はい | 仕入先ID |

#### リクエストボディ

| フィールド | 型 | 必須 | 説明 |
|------|------|------|------|
| `supplier_code` | string | いいえ | 仕入先コード |
| `supplier_name` | string | いいえ | 仕入先名 |
| `address` | object | いいえ | 住所情報 |
| `contact` | object | いいえ | 連絡先情報 |
| `payment_terms` | object | いいえ | 支払条件 |
| `is_active` | boolean | いいえ | アクティブ状態 |
| `note` | string | いいえ | 備考 |

更新したいフィールドのみを含めることができます。

#### リクエスト例

```json
{
  "contact": {
    "contact_person": "鈴木次郎",
    "phone": "06-1234-5678",
    "email": "suzuki.jiro@example.com",
    "fax": "06-1234-5679"
  },
  "note": "担当者が変更になりました"
}
```

#### レスポンスフィールド

更新された仕入先の詳細情報が返されます。

## エラーコード

| ステータスコード | 説明 |
|------|------|
| `400` | リクエストパラメータが無効 |
| `401` | 認証エラー |
| `403` | アクセス権限がない |
| `404` | 指定されたリソースが存在しない |
| `409` | リソースの競合（例：既に存在する仕入先コード） |
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

# 仕入先一覧を取得
suppliers = client.supplier.list(
    is_active=True,
    limit=10
)

# 結果の表示
for supplier in suppliers.get("items", []):
    print(f"仕入先ID: {supplier.get('id')}")
    print(f"仕入先コード: {supplier.get('supplier_code')}")
    print(f"仕入先名: {supplier.get('supplier_name')}")
    print(f"連絡先: {supplier.get('contact', {}).get('contact_person')}")
    print("---")

# 新しい仕入先を作成
new_supplier = {
    "supplier_code": "SUP003",
    "supplier_name": "株式会社佐藤商店",
    "address": {
        "postal_code": "980-0811",
        "prefecture": "宮城県",
        "city": "仙台市青葉区",
        "street": "一番町1-1-1",
        "country": "Japan"
    },
    "contact": {
        "contact_person": "佐藤健太",
        "phone": "022-123-4567",
        "email": "sato@example.com",
        "fax": "022-123-4568"
    },
    "payment_terms": {
        "payment_method": "BANK_TRANSFER",
        "payment_term_days": 30,
        "currency": "JPY"
    },
    "is_active": True,
    "note": "食品関連の卸売業者"
}

created_supplier = client.supplier.create(supplier=new_supplier)
print(f"作成された仕入先ID: {created_supplier.get('id')}")

# 仕入先を更新
client.supplier.update(
    supplier_id=created_supplier.get('id'),
    is_active=False,
    note="取引一時停止中"
)
```

## 関連リソース

- [入荷配送 (Inbound Delivery) API](inbound_delivery.md)
- [入荷配送カテゴリ (Inbound Delivery Category)](../types/inbound_delivery_category.md)
- [商品 (Article) API](article.md) 