# 温度管理区分 (Temperature Control)

温度管理区分は、商品の保管および輸送時に適用される温度条件の要件を表します。

## 概要

温度管理区分は、各商品の保管および輸送に必要な温度条件を指定するために使用されます。食品、医薬品、化学製品など、特定の温度範囲で管理する必要がある商品に特に重要です。適切な温度管理は、商品の品質と安全性を確保するために不可欠です。

## 使用できる値

| 値 | 説明 | 推奨温度範囲 |
|------|------|------|
| `AMBIENT` | 常温。特別な温度管理が不要で、通常の室温で保管可能。 | 15°C〜25°C |
| `REFRIGERATED` | 冷蔵。低温での保管が必要。 | 2°C〜8°C |
| `FROZEN` | 冷凍。氷点下での保管が必要。 | -18°C以下 |
| `DEEP_FROZEN` | 超低温冷凍。非常に低温での保管が必要。 | -60°C以下 |
| `CONTROLLED_ROOM_TEMP` | 管理された室温。特定の温度範囲内での保管が必要。 | 20°C〜25°C |
| `COOL` | 涼しい環境。冷蔵ほどではないが、通常の室温より低い温度での保管が必要。 | 8°C〜15°C |
| `WARM` | 温かい環境。通常の室温より高い温度での保管が必要。 | 30°C〜40°C |
| `HEAT_SENSITIVE` | 熱に敏感。高温を避ける必要がある。 | 25°C以下 |
| `COLD_SENSITIVE` | 寒さに敏感。低温を避ける必要がある。 | 10°C以上 |

## 温度ゾーンと保管要件

各温度管理区分に対応する倉庫内の保管エリア：

- `AMBIENT`：常温エリア - 特別な温度制御が不要
- `REFRIGERATED`：冷蔵エリア - 冷蔵設備が必要
- `FROZEN`：冷凍エリア - 冷凍設備が必要
- `DEEP_FROZEN`：超低温エリア - 特殊な超低温設備が必要
- その他の区分：適切な温度制御機能を持つ専用エリア

## API上での使用例

### 商品登録時の温度管理区分指定（POST /api/v1/article）

```json
{
  "article_code": "FOOD001",
  "article_name": "冷凍ピザ",
  "article_type": "SALE",
  "tax_indicator": "STANDARD",
  "unit_of_measure": "EA",
  "temperature_control": "FROZEN",
  "is_active": true
}
```

### 商品情報の取得（GET /api/v1/article/{article_code}）

レスポンス例：

```json
{
  "article_code": "FOOD001",
  "article_name": "冷凍ピザ",
  "article_type": "SALE",
  "tax_indicator": "STANDARD",
  "tax_rate": 10.0,
  "unit_of_measure": "EA",
  "gross_weight": 0.5,
  "net_weight": 0.45,
  "volume": 0.001,
  "dimensions": {
    "length": 30.0,
    "width": 30.0,
    "height": 5.0
  },
  "temperature_control": "FROZEN",
  "is_active": true,
  "created_at": "2023-04-01T09:00:00+09:00",
  "updated_at": "2023-04-01T09:00:00+09:00"
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

# 冷蔵管理が必要な新商品の登録
new_article = {
    "article_code": "DAIRY001",
    "article_name": "牛乳",
    "article_type": "SALE",
    "tax_indicator": "REDUCED",
    "unit_of_measure": "EA",
    "temperature_control": "REFRIGERATED",
    "is_active": True
}

client.article.create(article=new_article)

# 特定の温度管理区分の商品リストを取得
refrigerated_products = client.article.list(
    filters={
        "temperature_control": "REFRIGERATED"
    }
)

# 結果の表示
for product in refrigerated_products.get("items", []):
    print(f"商品コード: {product.get('article_code')}")
    print(f"商品名: {product.get('article_name')}")
    print(f"温度管理区分: {product.get('temperature_control')}")
    print("---")
```

## 関連リソース

- [商品 (Article) API](../interface/article.md)
- [商品タイプ (Article Type)](article_type.md)
- [出荷配送 (Outbound Delivery) API](../interface/outbound_delivery.md)
- [入荷配送 (Inbound Delivery) API](../interface/inbound_delivery.md) 