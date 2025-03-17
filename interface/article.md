# 商品 (Article) API

このAPIでは、商品情報の作成、取得、更新、削除を行うことができます。

## エンドポイント

- `GET /api/v1/article` - 商品一覧の取得
- `GET /api/v1/article/{article_code}` - 特定の商品の取得
- `POST /api/v1/article` - 商品の作成
- `PUT /api/v1/article/{article_code}` - 商品の更新
- `DELETE /api/v1/article/{article_code}` - 商品の削除

## 認証

このAPIを使用するには、適切なアクセス権を持つOAuth2アクセストークンが必要です。認証の詳細については、[認証ガイド](../docs/authentication.md)を参照してください。

## 一覧取得（GET /api/v1/article）

### リクエストパラメータ

| パラメータ名 | 型 | 必須 | 説明 |
|------------|------|------|------|
| article_code | string | いいえ | 商品コードでフィルタリング |
| article_name | string | いいえ | 商品名でフィルタリング（部分一致） |
| article_type | string | いいえ | 商品タイプでフィルタリング。詳細は[商品タイプ](../type/article_type.md)を参照 |
| tax_indicator | string | いいえ | 税区分でフィルタリング。詳細は[税区分](../type/tax_indicator.md)を参照 |
| limit | integer | いいえ | 取得する結果の最大数（デフォルト: 100, 最大: 1000） |
| offset | integer | いいえ | 結果セットの開始オフセット（ページング用、デフォルト: 0） |
| sort | string | いいえ | ソートフィールドとソート順（例: `article_code:asc`, `article_name:desc`） |

### レスポンスフィールド

| フィールド名 | 型 | 説明 |
|------------|------|------|
| items | array | 商品オブジェクトの配列 |
| total_count | integer | 条件に一致する総商品数 |
| limit | integer | 適用されたlimitパラメータ |
| offset | integer | 適用されたoffsetパラメータ |

### 商品オブジェクトのフィールド

| フィールド名 | 型 | 説明 |
|------------|------|------|
| article_code | string | 商品コード（一意） |
| article_name | string | 商品名 |
| article_type | string | 商品タイプ。詳細は[商品タイプ](../type/article_type.md)を参照 |
| tax_indicator | string | 税区分。詳細は[税区分](../type/tax_indicator.md)を参照 |
| tax_rate | number | 税率（%） |
| unit_of_measure | string | 単位（個、ケース、パレットなど） |
| gross_weight | number | 総重量（kg） |
| net_weight | number | 正味重量（kg） |
| volume | number | 体積（㎥） |
| length | number | 長さ（cm） |
| width | number | 幅（cm） |
| height | number | 高さ（cm） |
| note | string | 備考 |
| temperature_control | string | 温度管理区分。詳細は[温度管理](../type/temperature_control.md)を参照 |
| is_active | boolean | アクティブ状態 |
| created_at | string | 作成日時（ISO 8601形式） |
| updated_at | string | 更新日時（ISO 8601形式） |

### レスポンス例

```json
{
  "items": [
    {
      "article_code": "ARTICLE001",
      "article_name": "テスト商品1",
      "article_type": "SALE",
      "tax_indicator": "TAXABLE",
      "tax_rate": 10.0,
      "unit_of_measure": "個",
      "gross_weight": 1.5,
      "net_weight": 1.2,
      "volume": 0.01,
      "length": 10.0,
      "width": 5.0,
      "height": 2.0,
      "note": "テスト用商品",
      "temperature_control": "NORMAL",
      "is_active": true,
      "created_at": "2023-01-15T09:00:00+09:00",
      "updated_at": "2023-06-01T10:30:00+09:00"
    },
    {
      "article_code": "ARTICLE002",
      "article_name": "テスト商品2",
      "article_type": "SALE",
      "tax_indicator": "TAXABLE",
      "tax_rate": 10.0,
      "unit_of_measure": "個",
      "gross_weight": 0.5,
      "net_weight": 0.4,
      "volume": 0.005,
      "length": 5.0,
      "width": 5.0,
      "height": 2.0,
      "note": null,
      "temperature_control": "REFRIGERATED",
      "is_active": true,
      "created_at": "2023-01-16T09:00:00+09:00",
      "updated_at": "2023-06-01T10:30:00+09:00"
    }
  ],
  "total_count": 2,
  "limit": 100,
  "offset": 0
}
```

## 特定の商品の取得（GET /api/v1/article/{article_code}）

### URLパラメータ

| パラメータ名 | 型 | 必須 | 説明 |
|------------|------|------|------|
| article_code | string | はい | 取得する商品の商品コード |

### レスポンス

[商品オブジェクト](#商品オブジェクトのフィールド)を返します。

## 商品の作成（POST /api/v1/article）

### リクエストボディ

| フィールド名 | 型 | 必須 | 説明 |
|------------|------|------|------|
| article_code | string | はい | 商品コード（一意） |
| article_name | string | はい | 商品名 |
| article_type | string | はい | 商品タイプ。詳細は[商品タイプ](../type/article_type.md)を参照 |
| tax_indicator | string | はい | 税区分。詳細は[税区分](../type/tax_indicator.md)を参照 |
| tax_rate | number | はい | 税率（%） |
| unit_of_measure | string | はい | 単位（個、ケース、パレットなど） |
| gross_weight | number | いいえ | 総重量（kg） |
| net_weight | number | いいえ | 正味重量（kg） |
| volume | number | いいえ | 体積（㎥） |
| length | number | いいえ | 長さ（cm） |
| width | number | いいえ | 幅（cm） |
| height | number | いいえ | 高さ（cm） |
| note | string | いいえ | 備考 |
| temperature_control | string | いいえ | 温度管理区分。詳細は[温度管理](../type/temperature_control.md)を参照。デフォルトは`NORMAL` |
| is_active | boolean | いいえ | アクティブ状態。デフォルトは`true` |

### リクエスト例

```json
{
  "article_code": "ARTICLE003",
  "article_name": "新商品",
  "article_type": "SALE",
  "tax_indicator": "TAXABLE",
  "tax_rate": 10.0,
  "unit_of_measure": "個",
  "gross_weight": 2.0,
  "net_weight": 1.8,
  "volume": 0.02,
  "length": 15.0,
  "width": 10.0,
  "height": 5.0,
  "note": "新しいテスト商品",
  "temperature_control": "FROZEN",
  "is_active": true
}
```

### レスポンス

作成された[商品オブジェクト](#商品オブジェクトのフィールド)を返します。

## 商品の更新（PUT /api/v1/article/{article_code}）

### URLパラメータ

| パラメータ名 | 型 | 必須 | 説明 |
|------------|------|------|------|
| article_code | string | はい | 更新する商品の商品コード |

### リクエストボディ

更新したいフィールドのみを含めることができます。

| フィールド名 | 型 | 必須 | 説明 |
|------------|------|------|------|
| article_name | string | いいえ | 商品名 |
| article_type | string | いいえ | 商品タイプ。詳細は[商品タイプ](../type/article_type.md)を参照 |
| tax_indicator | string | いいえ | 税区分。詳細は[税区分](../type/tax_indicator.md)を参照 |
| tax_rate | number | いいえ | 税率（%） |
| unit_of_measure | string | いいえ | 単位（個、ケース、パレットなど） |
| gross_weight | number | いいえ | 総重量（kg） |
| net_weight | number | いいえ | 正味重量（kg） |
| volume | number | いいえ | 体積（㎥） |
| length | number | いいえ | 長さ（cm） |
| width | number | いいえ | 幅（cm） |
| height | number | いいえ | 高さ（cm） |
| note | string | いいえ | 備考 |
| temperature_control | string | いいえ | 温度管理区分。詳細は[温度管理](../type/temperature_control.md)を参照 |
| is_active | boolean | いいえ | アクティブ状態 |

### リクエスト例

```json
{
  "article_name": "更新された商品名",
  "note": "商品情報を更新しました",
  "is_active": false
}
```

### レスポンス

更新された[商品オブジェクト](#商品オブジェクトのフィールド)を返します。

## 商品の削除（DELETE /api/v1/article/{article_code}）

### URLパラメータ

| パラメータ名 | 型 | 必須 | 説明 |
|------------|------|------|------|
| article_code | string | はい | 削除する商品の商品コード |

### レスポンス

削除成功時は、ステータスコード`204 No Content`を返します。

## エラーコード

| ステータスコード | エラーコード | 説明 |
|---------------|-------------|------|
| 400 | validation_error | リクエストパラメータまたはボディが無効です |
| 401 | unauthorized | アクセストークンが無効または期限切れです |
| 403 | forbidden | このリソースへのアクセス権がありません |
| 404 | not_found | 指定された商品が見つかりません |
| 409 | conflict | 商品コードが既に存在します（作成時） |
| 422 | unprocessable_entity | 商品が使用中のため削除できません |
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

# 商品一覧の取得
articles = client.article.list(
    article_type="SALE",
    limit=10
)

# 特定の商品の取得
article = client.article.get("ARTICLE001")

# 商品の作成
new_article = client.article.create({
    "article_code": "ARTICLE003",
    "article_name": "新商品",
    "article_type": "SALE",
    "tax_indicator": "TAXABLE",
    "tax_rate": 10.0,
    "unit_of_measure": "個",
    "gross_weight": 2.0
})

# 商品の更新
updated_article = client.article.update("ARTICLE003", {
    "article_name": "更新された商品名"
})

# 商品の削除
client.article.delete("ARTICLE003")

# 結果の表示
for item in articles.get("items", []):
    print(f"商品コード: {item.get('article_code')}, 商品名: {item.get('article_name')}")
```

## 関連リソース

- [商品タイプ (Article Type)](../type/article_type.md)
- [税区分 (Tax Indicator)](../type/tax_indicator.md)
- [温度管理 (Temperature Control)](../type/temperature_control.md)
- [実際の在庫サマリ (Actual Inventory Summary)](actual_inventory_summary.md)
- [商品マッピング (Article Map)](article_map.md) 