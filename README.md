# pylogiless

LOGILESS APIのPythonクライアントライブラリ。在庫管理や物流管理のためのAPIを簡単に利用できるようにします。

## 認証

本ライブラリは2通りの認証方式をサポートします。いずれの場合も認証ヘッダには
`Authorization: Bearer <access_token>` のみが付与され、マーチャントIDはURLパスに含まれます。

**1. 静的アクセストークン方式（既定）**

事前に発行したアクセストークン (`access_token`) とマーチャントID (`merchant_id`) を
`LogilessClient` に渡します。

```python
client = LogilessClient(access_token="YOUR_TOKEN", merchant_id="YOUR_MERCHANT_ID")
```

**2. OAuth2 認可コードフロー方式**

`client_id` / `client_secret` / `redirect_uri` を渡すと、認可URLの生成・認可コードからの
トークン取得・期限切れ時のリフレッシュトークンによる自動更新が利用できます。

```python
client = LogilessClient(
    merchant_id="YOUR_MERCHANT_ID",
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    redirect_uri="https://example.com/callback",
)
# 1) 認可URLへユーザーを誘導
url = client.auth.get_authorization_url()
# 2) 返ってきた認可コードをトークンに交換
client.auth.fetch_token("AUTHORIZATION_CODE")
# 以降のAPI呼び出しでは、期限切れ時に refresh_token で自動更新されます
```

## 機能

以下のリソースを `client.<resource>` 経由で操作できます。

- 受注 (sales_order)
- 受注返品 (sales_return)
- 出荷 (outbound_delivery)
- 入荷 (inbound_delivery)
- 倉庫間移動 (inter_warehouse_transfer)
- 商品 (article)
- 商品マップ (article_map)
- サプライヤ (supplier)
- 店舗 (store)
- 倉庫 (warehouse)
- ロケーション (location)
- 再注文点 (reorder_point)
- 実在庫サマリ (actual_inventory_summary)
- 論理在庫サマリ (logical_inventory_summary)
- 日次在庫サマリ (daily_inventory_summary)
- 取引ログ (transaction_log)

## インストール

```bash
pip install pylogiless
```

## 必要条件

- Python 3.8以上
- requests >= 2.31.0
- python-dotenv >= 1.0.0

## リトライ・タイムアウト設定

`LogilessClient` はHTTP通信に `requests.Session` を内部で保持し、一時的な通信障害や
サーバー側の過負荷に対して自動リトライを行います。初期化時に以下のキーワード専用引数で
挙動を調整できます。

| 引数 | 既定値 | 説明 |
| --- | --- | --- |
| `timeout` | `30` | 1リクエストあたりのタイムアウト（秒） |
| `max_retries` | `3` | リトライ上限回数 |
| `retry_delay` | `1.0` | リトライ間の待機時間（秒） |

```python
from pylogiless import LogilessClient

client = LogilessClient(
    access_token="YOUR_TOKEN",
    merchant_id="YOUR_MERCHANT_ID",
    timeout=30,
    max_retries=3,
    retry_delay=1.0,
)
```

リトライ対象は `requests` の通信例外（`RequestException`）と、ステータスコード
`429 / 500 / 502 / 503 / 504` のレスポンスです。`max_retries` を使い切った場合は
従来どおり例外を送出します。`423`（locked）や `429` 以外の `4xx` はリトライせず
即座にエラーとなります。

## 型サポート

本ライブラリは `py.typed` マーカーを同梱しており、mypy / pyright などの型チェッカに
型情報を配布します。インポート名はトップレベルの `pylogiless` で、サブモジュールは
`pylogiless.api.{auth,client,errors}` から利用できます。

## レスポンスとページネーション

各リソースメソッドの返り値は、APIレスポンスをパースした生の `dict`（JSON）です。
ページネーションは `list(**params)` に任意のクエリパラメータを渡して制御できます。

```python
# page / per_page を渡してページングする例
articles = client.article.list(page=2, per_page=50)
```

> 注: LOGILESS APIのページング仕様は確定していないため、自動ページネーションは
> 提供していません。受け取った `dict` のページ情報を参照して呼び出し側で制御してください。

## Roadmap

- レスポンスを `dict` から型付き dataclass モデルへ変換する仕組みの検討（将来課題）

## 使用方法

### 環境変数の設定

1. `.env.example`ファイルを`.env`にコピーします：
```bash
cp .env.example .env
```

2. `.env`ファイルを編集し、実際の認証情報を設定します：
```
LOGILESS_ACCESS_TOKEN=your_access_token_here
LOGILESS_MERCHANT_ID=your_merchant_id_here
```

### サンプルコード

```python
from pylogiless import LogilessClient
import os
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# クライアントの初期化
client = LogilessClient(
    access_token=os.getenv("LOGILESS_ACCESS_TOKEN"),
    merchant_id=os.getenv("LOGILESS_MERCHANT_ID")
)

# 実在庫サマリの取得
actual_inventory = client.actual_inventory_summary.list()
print(f"実在庫サマリ: {actual_inventory}")

# 論理在庫サマリの取得
logical_inventory = client.logical_inventory_summary.list()
print(f"論理在庫サマリ: {logical_inventory}")

# 商品一覧の取得
articles = client.article.list()
print(f"商品一覧: {articles}")
```

### エラーハンドリング

```python
try:
    # APIリクエスト
    inventory = client.actual_inventory_summary.list()
except Exception as e:
    print(f"エラーが発生しました: {str(e)}")
```

## 開発環境のセットアップ

1. リポジトリのクローン：
```bash
git clone https://github.com/logiless/pylogiless.git
cd pylogiless
```

2. 仮想環境の作成と有効化：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# または
.\venv\Scripts\activate  # Windows
```

3. 依存パッケージのインストール：
```bash
pip install -e .
```

## テスト

```bash
python -m pytest tests/
```

## 貢献

1. このリポジトリをフォーク
2. 新しいブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add some amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## ライセンス

MIT License

## サポート

- バグ報告や機能要望は[GitHub Issues](https://github.com/logiless/pylogiless/issues)にお願いします
- ドキュメントは[GitHub Wiki](https://github.com/logiless/pylogiless/wiki)で確認できます

## 作者

LOGILESS API Python Client Contributors 