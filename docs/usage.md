# pylogiless 使用ガイド

## はじめに
`pylogiless` は、LOGILESS APIをPythonコードから簡単に呼び出せるライブラリです。
認証から各種リソース取得まで、短いコードで実装可能です。

---

## インストール
```bash
pip install pylogiless
```

---

## 初期化と認証
```python
from pylogiless import LogilessClient

client = LogilessClient(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    redirect_uri="YOUR_REDIRECT_URI"
)

# 認可コードを取得後、トークンを取得
code = "AUTH_CODE"
token = client.fetch_token(code)
print(token)
```

---

## API呼び出し例

### 商品操作
```python
# 商品作成
new_article = client.article.create({
    "article_code": "TEST001",
    "article_name": "サンプル商品"
})
print(new_article)

# 商品取得
article = client.article.get("ARTICLE_ID")
print(article)

# 商品リスト取得
articles = client.article.list()
print(articles)

# 商品更新
updated_article = client.article.update("ARTICLE_ID", {"article_name": "新しい商品名"})
print(updated_article)

# 商品削除
result = client.article.delete("ARTICLE_ID")
print(result)
```

### 在庫取得
```python
inventory = client.actual_inventory_summary.list(filter={"warehouse_id": "YOUR_WAREHOUSE_ID"})
print(inventory)
```

## 入庫(Inbound)操作
```python
# 入庫一覧
inbounds = client.inbound_delivery.list(limit=10)
print(inbounds)

# 特定入庫データの取得
inbound = client.inbound_delivery.get("INBOUND_ID")
print(inbound)

# 入庫作成
new_inbound = client.inbound_delivery.create({
    "warehouse_id": "WAREHOUSE_ID",
    "supplier_id": "SUPPLIER_ID",
    "scheduled_date": "2024-01-01",
    "items": [
        {
            "article_id": "ARTICLE_ID",
            "quantity": 100
        }
    ]
})
print(new_inbound)

# 入庫更新
updated_inbound = client.inbound_delivery.update("INBOUND_ID", {"scheduled_date": "2024-01-15"})
print(updated_inbound)
```

## 出荷(Outbound)操作
```python
# 出荷一覧
outbounds = client.outbound_delivery.list(limit=10)
print(outbounds)

# 特定出荷データの取得
outbound = client.outbound_delivery.get("OUTBOUND_ID")
print(outbound)

# 出荷作成
new_outbound = client.outbound_delivery.create({
    "warehouse_id": "WAREHOUSE_ID",
    "store_id": "STORE_ID",
    "scheduled_date": "2024-01-05",
    "items": [
        {
            "article_id": "ARTICLE_ID",
            "quantity": 5
        }
    ]
})
print(new_outbound)

# 出荷更新
updated_outbound = client.outbound_delivery.update("OUTBOUND_ID", {"scheduled_date": "2024-01-20"})
print(updated_outbound)
```

## 注文(Orders)操作
```python
# 注文一覧の取得
orders = client.sales_order.list(limit=10)
print(orders)

# 注文作成
new_order = client.sales_order.create({
    "order_number": "ORDER002",
    "customer_id": "CUSTOMER_ID",
    "order_date": "2024-01-08",
    "warehouse_id": "WAREHOUSE_ID",
    "items": [
        {
            "article_id": "ARTICLE_ID",
            "quantity": 1
        }
    ]
})
print(new_order)

# 注文更新
updated_order = client.sales_order.update("ORDER_ID", {"order_date": "2024-01-12"})
print(updated_order)
```

## その他の機能
- レポート出力
- ラベル印刷
- 在庫移動
などは `client.<resource>` を経由して同様に操作できます。

---

## レポート出力
```python
# report_csv = client.report.export("REPORT_ID", format="csv") # reportリソースは存在しないためコメントアウト
# print(report_csv)  # CSV内容が取得される
print("report機能は未実装です")
```

## ラベル印刷
```python
# label_data = client.label.print("OUTBOUND_ID", { # labelリソースは存在しないためコメントアウト
#    "template_id": "TEMPLATE001"
# })
# print(label_data)  # ラベルPDFなどのバイナリデータ
print("label機能は未実装です")
```

## 在庫移動(Inventory Transfer)
```python
# inter_warehouse_transferを使用
inventory_transfer = client.inter_warehouse_transfer.create({
    "warehouse_id_from": "WAREHOUSE_A",
    "warehouse_id_to": "WAREHOUSE_B",
    "items": [
        {"article_id": "ARTICLE_CODE", "quantity": 50}
    ]
})
print(inventory_transfer)

# 在庫移動の取得
inventory_transfer_list = client.inter_warehouse_transfer.list()
print(inventory_transfer_list)

# 特定の在庫移動の取得
inventory_transfer_item = client.inter_warehouse_transfer.get("TRANSFER_ID")
print(inventory_transfer_item)
```

---

## エラーハンドリング
```python
from pylogiless import LogilessAuthError, LogilessError

try:
    result = client.article.get("INVALID_ID")
except LogilessAuthError as e:
    print("認証エラー:", e)
except LogilessError as e:
    print("APIエラー:", e)

try:
    # result = client.order.get("INVALID_ORDER") # orderリソースはsales_orderに変更されたためコメントアウト
    result = client.sales_order.get("INVALID_ORDER")
except LogilessAuthError as e:
    print("認証エラー:", e)
except LogilessError as e:
    print("APIエラー:", e)
```

---

## まとめ
- `LogilessClient` で簡単にAPIリクエストを実行可能
- 認証、記事操作、在庫操作など、直感的なメソッド構成
- カスタマイズやエラーハンドリングも柔軟に対応可能
