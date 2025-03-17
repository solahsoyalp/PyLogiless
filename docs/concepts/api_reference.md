# API リファレンス

このドキュメントでは、pylogilessクライアントライブラリで利用可能な主要なAPIエンドポイントの詳細な使用方法を説明します。

## 目次

- [認証](#認証)
- [在庫管理](#在庫管理)
- [配送管理](#配送管理)
- [商品管理](#商品管理)
- [倉庫管理](#倉庫管理)
- [取引ログ](#取引ログ)

## 認証

認証に関する詳細は[認証ガイド](authentication.md)を参照してください。

```python
from pylogiless import LogilessClient

# クライアントの初期化
client = LogilessClient(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    redirect_uri="YOUR_REDIRECT_URI"
)

# 認証URLの取得
auth_url = client.get_authorization_url()

# 認可コードを使用してトークンを取得
code = "AUTHORIZATION_CODE"  # ユーザーが認証後に取得した認可コード
client.fetch_token(code)

# トークンの手動設定
client.set_token(access_token="ACCESS_TOKEN", refresh_token="REFRESH_TOKEN")
```

## 在庫管理

### 実際の在庫サマリー

```python
# 在庫一覧の取得
inventory_list = client.actual_inventory_summary.list()

# 特定の在庫の取得
inventory = client.actual_inventory_summary.get("INVENTORY_ID")

# 在庫の検索（フィルタリング）
filtered_inventory = client.actual_inventory_summary.list(
    article_code="ARTICLE_CODE",
    warehouse_code="WAREHOUSE_CODE"
)
```

### 論理的な在庫サマリー

```python
# 論理的な在庫一覧の取得
logical_inventory = client.logical_inventory_summary.list()

# 特定の論理的な在庫の取得
specific_logical_inventory = client.logical_inventory_summary.get("INVENTORY_ID")

# 論理的な在庫の検索
filtered_logical_inventory = client.logical_inventory_summary.list(
    article_code="ARTICLE_CODE"
)
```

### 日次在庫サマリー

```python
# 日次在庫一覧の取得
daily_inventory = client.daily_inventory_summary.list()

# 日次在庫の検索
filtered_daily_inventory = client.daily_inventory_summary.list(
    date_from="2023-01-01",
    date_to="2023-01-31"
)
```

## 配送管理

### 出荷配送

```python
# 出荷配送一覧の取得
outbound_deliveries = client.outbound_delivery.list()

# 特定の出荷配送の取得
outbound_delivery = client.outbound_delivery.get("DELIVERY_ID")

# 出荷配送の作成
new_outbound_delivery = client.outbound_delivery.create({
    "reference_id": "REF123",
    "store_code": "STORE001",
    "warehouse_code": "WH001",
    "scheduled_delivery_date": "2023-06-01",
    "delivery_method": "NORMAL",
    "items": [
        {
            "line_id": "1",
            "article_code": "ART001",
            "quantity": 10
        }
    ]
})

# 出荷配送の更新
updated_outbound_delivery = client.outbound_delivery.update("DELIVERY_ID", {
    "scheduled_delivery_date": "2023-06-02"
})
```

### 入荷配送

```python
# 入荷配送一覧の取得
inbound_deliveries = client.inbound_delivery.list()

# 特定の入荷配送の取得
inbound_delivery = client.inbound_delivery.get("DELIVERY_ID")

# 入荷配送の作成
new_inbound_delivery = client.inbound_delivery.create({
    "reference_id": "REF456",
    "warehouse_code": "WH001",
    "supplier_code": "SUP001",
    "scheduled_delivery_date": "2023-06-01",
    "inbound_delivery_category": "PURCHASE_ORDER",
    "items": [
        {
            "line_id": "1",
            "article_code": "ART001",
            "quantity": 20
        }
    ]
})
```

### 倉庫間移動

```python
# 倉庫間移動一覧の取得
transfers = client.inter_warehouse_transfer.list()

# 特定の倉庫間移動の取得
transfer = client.inter_warehouse_transfer.get("TRANSFER_ID")

# 倉庫間移動の作成
new_transfer = client.inter_warehouse_transfer.create({
    "reference_id": "TR001",
    "source_warehouse_code": "WH001",
    "target_warehouse_code": "WH002",
    "scheduled_transfer_date": "2023-06-01",
    "items": [
        {
            "line_id": "1",
            "article_code": "ART001",
            "quantity": 5
        }
    ]
})
```

## 商品管理

```python
# 商品一覧の取得
articles = client.article.list()

# 特定の商品の取得
article = client.article.get("ARTICLE_ID")

# 商品の作成
new_article = client.article.create({
    "article_code": "NEW001",
    "article_name": "新商品",
    "article_type": "SALE",
    "tax_indicator": "TAXABLE",
    "tax_rate": 10.0,
    "unit_of_measure": "個",
    "gross_weight": 1.5
})

# 商品の更新
updated_article = client.article.update("ARTICLE_ID", {
    "article_name": "更新された商品名"
})

# 商品の削除
client.article.delete("ARTICLE_ID")
```

## 倉庫管理

```python
# 倉庫一覧の取得
warehouses = client.warehouse.list()

# 特定の倉庫の取得
warehouse = client.warehouse.get("WAREHOUSE_ID")

# ロケーション一覧の取得
locations = client.location.list(warehouse_code="WH001")

# 特定のロケーションの取得
location = client.location.get("LOCATION_ID")
```

## 取引ログ

```python
# 取引ログ一覧の取得
transaction_logs = client.transaction_log.list()

# 特定の日付範囲の取引ログの取得
filtered_logs = client.transaction_log.list(
    date_from="2023-01-01",
    date_to="2023-01-31"
)

# 特定の取引タイプの取引ログの取得
typed_logs = client.transaction_log.list(transaction_type="INBOUND")
```

## その他のエンドポイント

その他のエンドポイントについては、[インターフェース仕様](../interface/)フォルダ内の各ドキュメントを参照してください。

## エラーハンドリング

APIからのエラー応答の処理については、[エラーハンドリングガイド](error_handling.md)を参照してください。 