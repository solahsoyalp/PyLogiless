# 商品タイプ (Article Type)

商品タイプは、商品の用途や機能を分類するための区分です。

## 概要

商品タイプは、各商品の用途や取り扱い方法を指定します。在庫管理や出荷処理において、商品タイプに応じた適切な処理を行うために使用されます。

## 使用できる値

| 値 | 説明 |
|------|------|
| `SALE` | 販売商品。一般的な販売用の商品。 |
| `SAMPLE` | サンプル商品。展示や試用のための商品。 |
| `GIFT` | ギフト商品。販促や特典として利用される商品。 |
| `RAW_MATERIAL` | 原材料。製造工程で使用される原材料。 |
| `SEMI_FINISHED` | 半製品。製造途中の状態の商品。 |
| `FINISHED` | 完成品。製造が完了し出荷可能な状態の商品。 |
| `RETURNABLE` | 返却可能商品。返却される前提の貸出商品。 |
| `PACKAGING` | 包装材。商品の梱包に使用される資材。 |
| `CONSUMABLE` | 消耗品。倉庫内で使用される消耗品。 |
| `SERVICE` | サービス。物理的な商品ではなくサービスとして提供されるもの。 |

## API上での使用例

### 商品の作成（POST /api/v1/article）

```json
{
  "article_code": "ARTICLE001",
  "article_name": "テスト商品",
  "article_type": "SALE",
  "tax_indicator": "TAXABLE",
  "tax_rate": 10.0,
  "unit_of_measure": "個"
}
```

### 商品一覧の取得（GET /api/v1/article）

商品タイプでフィルタリングする例：

```
GET /api/v1/article?article_type=SALE
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

# 特定の商品タイプの商品一覧を取得
sale_articles = client.article.list(article_type="SALE")

# 新しい商品を作成
new_article = client.article.create({
    "article_code": "ARTICLE001",
    "article_name": "テスト商品",
    "article_type": "FINISHED",
    "tax_indicator": "TAXABLE",
    "tax_rate": 10.0,
    "unit_of_measure": "個"
})
```

## 関連リソース

- [商品 (Article) API](../interface/article.md)
- [税区分 (Tax Indicator)](tax_indicator.md)
- [温度管理 (Temperature Control)](temperature_control.md) 