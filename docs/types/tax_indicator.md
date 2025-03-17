# 税区分 (Tax Indicator)

税区分は、商品やサービスに適用される消費税の種類や率を決定するために使用される分類です。

## 概要

税区分は、商品やサービスの性質に基づいて、適用される消費税の種類や率を決定します。国や地域の税法に準拠して、標準税率、軽減税率、非課税、免税などの区分が設定されています。適切な税区分の選択により、正確な税金計算と法令遵守が確保されます。

## 使用できる値

| 値 | 説明 | 現在の税率（日本） |
|------|------|------|
| `STANDARD` | 標準税率。通常の商品やサービスに適用される消費税率。 | 10% |
| `REDUCED` | 軽減税率。生活必需品や特定の食料品などに適用される軽減された消費税率。 | 8% |
| `ZERO` | ゼロ税率。輸出品など、消費税が0%となる取引に適用。 | 0% |
| `EXEMPT` | 非課税。消費税が課されない取引（医療サービス、教育など）に適用。 | - |
| `OUTSIDE_SCOPE` | 課税対象外。消費税法の適用範囲外の取引に適用。 | - |

## 税区分と課税方式

税区分とともに、課税方式も指定することができます。課税方式には、以下のようなものがあります：

- **内税方式**：表示価格に消費税が含まれている
- **外税方式**：表示価格に消費税が含まれていない

また、税の丸め処理方法も指定できます：

- **四捨五入**：小数点以下を四捨五入
- **切り捨て**：小数点以下を切り捨て
- **切り上げ**：小数点以下を切り上げ

## API上での使用例

### 商品登録時の税区分指定（POST /api/v1/article）

```json
{
  "article_code": "FOOD002",
  "article_name": "有機野菜セット",
  "article_type": "SALE",
  "tax_indicator": "REDUCED",
  "unit_of_measure": "EA",
  "is_active": true
}
```

### 販売注文登録時の税処理方法指定（POST /api/v1/sales_order）

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
      "unit_price": 1080,
      "tax_indicator": "REDUCED",
      "tax_rate": 8.0
    },
    {
      "line_id": "2",
      "article_code": "GADGET001",
      "quantity": 1,
      "unit_price": 5500,
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

# 軽減税率が適用される新商品の登録
new_article = {
    "article_code": "FOOD003",
    "article_name": "パン",
    "article_type": "SALE",
    "tax_indicator": "REDUCED",
    "unit_of_measure": "EA",
    "is_active": True
}

client.article.create(article=new_article)

# 販売注文の登録（税処理方法と丸め方法を指定）
new_sales_order = {
    "reference_id": "SO67890",
    "store_code": "STORE001",
    "tax_processing_method": "INCLUSIVE",
    "tax_rounding_method": "ROUND",
    "items": [
        {
            "line_id": "1",
            "article_code": "FOOD003",
            "quantity": 5,
            "unit_price": 216,  # 税込価格
            "tax_indicator": "REDUCED",
            "tax_rate": 8.0
        }
    ]
}

client.sales_order.create(sales_order=new_sales_order)
```

## 関連リソース

- [商品 (Article) API](../api/article.md)
- [販売注文 (Sales Order) API](../api/sales_order.md)
- [税処理方法 (Tax Processing Method)](tax_processing_method.md)
- [税丸め方法 (Tax Rounding Method)](tax_rounding_method.md) 