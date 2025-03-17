# エラーハンドリングガイド

このドキュメントでは、pylogilessライブラリを使用する際に発生する可能性のあるエラーと、それらを適切に処理する方法について説明します。

## 目次

- [エラータイプ](#エラータイプ)
- [一般的なエラー処理パターン](#一般的なエラー処理パターン)
- [認証関連のエラー](#認証関連のエラー)
- [APIリクエスト関連のエラー](#apiリクエスト関連のエラー)
- [エラーコードリファレンス](#エラーコードリファレンス)

## エラータイプ

pylogilessライブラリは以下の主要なエラータイプを提供します：

- `LogilessError` - 全てのエラーの基底クラス
- `LogilessAuthError` - 認証関連のエラー
- `LogilessAPIError` - API呼び出し時のエラー
- `LogilessValidationError` - リクエストデータの検証エラー
- `LogilessRateLimitError` - APIレート制限に達した場合のエラー
- `LogilessServerError` - サーバー側のエラー

これらのエラークラスはすべて `LogilessError` を継承しており、共通のプロパティとメソッドを持っています。

## 一般的なエラー処理パターン

### 基本的なエラーハンドリング

```python
from pylogiless import LogilessClient, LogilessError

client = LogilessClient(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    redirect_uri="YOUR_REDIRECT_URI"
)

try:
    inventory = client.actual_inventory_summary.list()
except LogilessError as e:
    print(f"エラーが発生しました: {e}")
    print(f"エラーコード: {e.error_code}")
    print(f"エラーメッセージ: {e.message}")
    print(f"ステータスコード: {e.status_code}")
```

### 特定のエラータイプに対応する

```python
from pylogiless import (
    LogilessClient, LogilessError, LogilessAuthError, 
    LogilessAPIError, LogilessValidationError,
    LogilessRateLimitError, LogilessServerError
)

client = LogilessClient(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    redirect_uri="YOUR_REDIRECT_URI"
)

try:
    article = client.article.get("ARTICLE_ID")
except LogilessAuthError as e:
    print(f"認証エラー: {e}")
    # トークンを再取得するなどの処理
except LogilessValidationError as e:
    print(f"バリデーションエラー: {e}")
    # リクエストデータを修正するなどの処理
except LogilessRateLimitError as e:
    print(f"レート制限エラー: {e}")
    # 再試行前に待機するなどの処理
except LogilessServerError as e:
    print(f"サーバーエラー: {e}")
    # 後で再試行するなどの処理
except LogilessAPIError as e:
    print(f"API呼び出しエラー: {e}")
    # その他のAPI関連エラー処理
except LogilessError as e:
    print(f"一般的なエラー: {e}")
    # その他のエラー処理
```

## 認証関連のエラー

認証プロセス中に発生する可能性のある一般的なエラーとその処理方法：

```python
from pylogiless import LogilessClient, LogilessAuthError

client = LogilessClient(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    redirect_uri="YOUR_REDIRECT_URI"
)

try:
    # 認可コードによるトークンの取得
    client.fetch_token("INVALID_CODE")
except LogilessAuthError as e:
    if e.error_code == "invalid_grant":
        print("認可コードが無効または期限切れです。新しい認可コードを取得してください。")
        # 新しい認証URLを取得
        auth_url = client.get_authorization_url()
        print(f"新しい認証URL: {auth_url}")
    elif e.error_code == "invalid_client":
        print("クライアントIDまたはクライアントシークレットが無効です。")
    else:
        print(f"認証エラー: {e}")
```

### アクセストークンの自動更新

pylogilessは、アクセストークンが期限切れになった場合に自動的にリフレッシュトークンを使用して新しいアクセストークンを取得します。ただし、リフレッシュトークンが無効または期限切れになった場合は、再認証が必要になります。

```python
from pylogiless import LogilessClient, LogilessAuthError

client = LogilessClient(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    redirect_uri="YOUR_REDIRECT_URI"
)

# 既存のトークンを設定
client.set_token(access_token="EXPIRED_TOKEN", refresh_token="REFRESH_TOKEN")

try:
    # APIリクエストを実行
    inventory = client.actual_inventory_summary.list()
except LogilessAuthError as e:
    if e.error_code == "invalid_token":
        # リフレッシュトークンが無効または期限切れ
        print("再認証が必要です。")
        auth_url = client.get_authorization_url()
        print(f"認証URL: {auth_url}")
    else:
        print(f"認証エラー: {e}")
```

## APIリクエスト関連のエラー

APIリクエスト時に発生する可能性のある一般的なエラーとその処理方法：

### リソースが見つからない場合

```python
from pylogiless import LogilessClient, LogilessAPIError

client = LogilessClient(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    redirect_uri="YOUR_REDIRECT_URI"
)

try:
    # 存在しない商品を取得
    article = client.article.get("NON_EXISTENT_ID")
except LogilessAPIError as e:
    if e.status_code == 404:
        print("指定されたリソースが見つかりません。")
    else:
        print(f"APIエラー: {e}")
```

### バリデーションエラー

```python
from pylogiless import LogilessClient, LogilessValidationError

client = LogilessClient(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    redirect_uri="YOUR_REDIRECT_URI"
)

try:
    # 不正なデータで商品を作成
    new_article = client.article.create({
        # 必須フィールドが不足している
        "article_name": "新商品"
    })
except LogilessValidationError as e:
    print(f"バリデーションエラー: {e}")
    # バリデーションエラーの詳細を取得
    for field, errors in e.validation_errors.items():
        print(f"フィールド '{field}': {', '.join(errors)}")
```

### レート制限エラー

```python
from pylogiless import LogilessClient, LogilessRateLimitError
import time

client = LogilessClient(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    redirect_uri="YOUR_REDIRECT_URI"
)

def get_inventory_with_retry(max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            return client.actual_inventory_summary.list()
        except LogilessRateLimitError as e:
            retries += 1
            if retries >= max_retries:
                raise
            
            # レート制限ヘッダーから待機時間を取得
            wait_time = e.retry_after if e.retry_after else 60
            print(f"レート制限に達しました。{wait_time}秒待機します...")
            time.sleep(wait_time)
    
    return None
```

## エラーコードリファレンス

以下は、APIから返される可能性のある主要なエラーコードとその説明です。

### 認証関連のエラーコード

| エラーコード | 説明 |
|------------|------|
| `invalid_request` | リクエストに必要なパラメータが不足しています |
| `invalid_client` | クライアント認証に失敗しました |
| `invalid_grant` | 提供された認可コードまたはリフレッシュトークンが無効です |
| `unauthorized_client` | クライアントはこのメソッドを使用した認可コードの取得が認可されていません |
| `unsupported_grant_type` | サポートされていない認可タイプが使用されました |
| `invalid_scope` | リクエストされたスコープが無効です |
| `access_denied` | リソース所有者または認可サーバーがリクエストを拒否しました |

### APIリクエスト関連のエラーコード

| エラーコード | ステータスコード | 説明 |
|------------|---------------|------|
| `not_found` | 404 | リクエストされたリソースが見つかりません |
| `validation_error` | 400 | リクエストデータのバリデーションに失敗しました |
| `rate_limit_exceeded` | 429 | APIレート制限に達しました |
| `internal_server_error` | 500 | サーバー内部エラーが発生しました |
| `service_unavailable` | 503 | サービスが一時的に利用できません |
| `conflict` | 409 | リソースの状態に競合が発生しました |
| `forbidden` | 403 | このリソースへのアクセス権がありません |

詳細なエラーコードと説明については、[errors.md](errors.md)を参照してください。 