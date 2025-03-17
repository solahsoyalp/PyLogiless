# 税処理方法 (Tax Processing Method)

税処理方法は、商品やサービスの価格表示および消費税の計算方法を指定するために使用される分類です。

## 概要

税処理方法は、取引における価格の表示方法と消費税の計算方法を決定します。価格に消費税が含まれているか（内税）、含まれていないか（外税）を指定することで、システムが適切に税額を計算し、帳票や請求書に反映させることができます。

## 使用できる値

| 値 | 説明 |
|------|------|
| `INCLUSIVE` | 内税方式。価格に消費税が含まれている。表示価格から税額を逆算する。 |
| `EXCLUSIVE` | 外税方式。価格に消費税が含まれていない。表示価格に税率を掛けて税額を計算する。 |

## 税処理方法の適用例

### 内税方式（INCLUSIVE）の例

商品価格が税込み1,080円で、消費税率が8%の場合：
- 表示価格：1,080円（税込み）
- 税抜価格：1,000円（計算：1,080 ÷ 1.08）
- 消費税額：80円（計算：1,080 - 1,000）

### 外税方式（EXCLUSIVE）の例

商品価格が税抜き1,000円で、消費税率が10%の場合：
- 表示価格：1,000円（税抜き）
- 税込価格：1,100円（計算：1,000 × 1.1）
- 消費税額：100円（計算：1,000 × 0.1）

## API上での使用例

### 販売注文登録時の税処理方法指定（POST /api/v1/sales_order）

#### 内税方式の例

```json
{
  "reference_id": "SO12345",
  "store_code": "STORE001",
  "tax_processing_method": "INCLUSIVE",
  "tax_rounding_method": "ROUND",
  "items": [
    {
      "line_id": "1",
      "article_code": "FOOD002",
      "quantity": 2,
      "unit_price": 1080,  // 税込価格
      "tax_indicator": "REDUCED",
      "tax_rate": 8.0
    }
  ]
}
```

#### 外税方式の例

```json
{
  "reference_id": "SO67890",
  "store_code": "STORE001",
  "tax_processing_method": "EXCLUSIVE",
  "tax_rounding_method": "ROUND",
  "items": [
    {
      "line_id": "1",
      "article_code": "GADGET001",
      "quantity": 1,
      "unit_price": 5000,  // 税抜価格
      "tax_indicator": "STANDARD",
      "tax_rate": 10.0
    }
  ]
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

# 内税方式の販売注文の登録
inclusive_sales_order = {
    "reference_id": "SO12345",
    "store_code": "STORE001",
    "tax_processing_method": "INCLUSIVE",
    "tax_rounding_method": "ROUND",
    "items": [
        {
            "line_id": "1",
            "article_code": "FOOD003",
            "quantity": 3,
            "unit_price": 216,  # 税込価格
            "tax_indicator": "REDUCED",
            "tax_rate": 8.0
        }
    ]
}

client.sales_order.create(sales_order=inclusive_sales_order)

# 外税方式の販売注文の登録
exclusive_sales_order = {
    "reference_id": "SO67890",
    "store_code": "STORE001",
    "tax_processing_method": "EXCLUSIVE",
    "tax_rounding_method": "ROUND",
    "items": [
        {
            "line_id": "1",
            "article_code": "GADGET001",
            "quantity": 1,
            "unit_price": 5000,  # 税抜価格
            "tax_indicator": "STANDARD",
            "tax_rate": 10.0
        }
    ]
}

client.sales_order.create(sales_order=exclusive_sales_order)
```

## 会計システムとの連携

税処理方法は、会計システムと連携する際に重要な情報です。適切な税処理方法を設定することで、以下のようなメリットがあります：

- 会計システムへの正確なデータ連携
- 税務報告の自動化と簡素化
- 税計算の一貫性の確保

## 関連リソース

- [税区分 (Tax Indicator)](tax_indicator.md)
- [税丸め方法 (Tax Rounding Method)](tax_rounding_method.md)
- [販売注文 (Sales Order) API](../interface/sales_order.md) 