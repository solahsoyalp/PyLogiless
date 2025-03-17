# 認証ガイド

このドキュメントでは、pylogilessライブラリを使用してLOGILESS APIに認証する方法について説明します。

## 目次

- [前提条件](#前提条件)
- [OAuth2認証フロー](#oauth2認証フロー)
- [クライアントの初期化](#クライアントの初期化)
- [認証URLの取得](#認証urlの取得)
- [トークンの取得](#トークンの取得)
- [トークンの更新](#トークンの更新)
- [既存のトークンの使用](#既存のトークンの使用)
- [認証エラーの処理](#認証エラーの処理)
- [ベストプラクティス](#ベストプラクティス)

## 前提条件

LOGILESS APIを使用するには、以下の情報が必要です：

1. クライアントID (`client_id`)
2. クライアントシークレット (`client_secret`)
3. リダイレクトURI (`redirect_uri`)

これらの情報は、LOGILESS管理画面の開発者セクションで取得できます。

## OAuth2認証フロー

pylogilessライブラリは、OAuth2の認可コードフロー（Authorization Code Flow）を使用して認証を行います。このフローは以下のステップで構成されています：

1. ユーザーをLOGILESSの認証ページにリダイレクトします。
2. ユーザーがLOGILESSでログインし、アプリケーションのアクセス権を承認します。
3. ユーザーがリダイレクトURIにリダイレクトされ、認可コードが付与されます。
4. アプリケーションはこの認可コードを使用してアクセストークンとリフレッシュトークンを取得します。
5. アプリケーションはアクセストークンを使用してAPIにアクセスします。
6. アクセストークンの有効期限が切れた場合、リフレッシュトークンを使用して新しいアクセストークンを取得します。

## クライアントの初期化

まず、`LogilessClient`クラスのインスタンスを作成し、認証情報を設定します：

```python
from pylogiless import LogilessClient

client = LogilessClient(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    redirect_uri="YOUR_REDIRECT_URI"
)
```

## 認証URLの取得

認可コードを取得するためのURLを生成します：

```python
auth_url = client.get_authorization_url()
print(f"次のURLにアクセスして認証してください: {auth_url}")
```

このURLをユーザーに提示し、ブラウザでアクセスしてもらいます。ユーザーがLOGILESSにログインして承認すると、指定したリダイレクトURIにリダイレクトされ、URLのクエリパラメータに認可コードが含まれます。

## トークンの取得

認可コードを使用してアクセストークンとリフレッシュトークンを取得します：

```python
# ユーザーが認証後に取得した認可コード
code = "AUTHORIZATION_CODE"

# トークンを取得
tokens = client.fetch_token(code)

# 取得したトークンを表示
print(f"アクセストークン: {tokens['access_token']}")
print(f"リフレッシュトークン: {tokens['refresh_token']}")
print(f"有効期限（秒）: {tokens['expires_in']}")
```

## トークンの更新

アクセストークンの有効期限が切れた場合、pylogilessライブラリは自動的にリフレッシュトークンを使用して新しいアクセストークンを取得します。ただし、必要に応じて手動でトークンを更新することもできます：

```python
# トークンを手動で更新
new_tokens = client.refresh_token()

# 新しいトークンを表示
print(f"新しいアクセストークン: {new_tokens['access_token']}")
print(f"新しいリフレッシュトークン: {new_tokens['refresh_token']}")
print(f"有効期限（秒）: {new_tokens['expires_in']}")
```

## 既存のトークンの使用

既存のアクセストークンとリフレッシュトークンがある場合、それらを設定することができます：

```python
client.set_token(
    access_token="ACCESS_TOKEN",
    refresh_token="REFRESH_TOKEN"
)
```

## 認証エラーの処理

認証プロセス中にエラーが発生する可能性があります。エラーを適切に処理するには、`LogilessAuthError`例外をキャッチします：

```python
from pylogiless import LogilessClient, LogilessAuthError

client = LogilessClient(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    redirect_uri="YOUR_REDIRECT_URI"
)

try:
    # 認可コードによるトークンの取得
    tokens = client.fetch_token("INVALID_CODE")
except LogilessAuthError as e:
    print(f"認証エラーが発生しました: {e}")
    print(f"エラーコード: {e.error_code}")
```

一般的な認証エラーコードとその説明：

- `invalid_request`: リクエストに必要なパラメータが不足しています
- `invalid_client`: クライアント認証に失敗しました
- `invalid_grant`: 提供された認可コードまたはリフレッシュトークンが無効です
- `invalid_token`: アクセストークンが無効または期限切れです

詳細なエラー処理については、[エラーハンドリングガイド](error_handling.md)を参照してください。

## ベストプラクティス

### トークンの保存

アクセストークンとリフレッシュトークンは安全に保存し、再利用することをお勧めします。以下は、トークンをJSONファイルに保存する簡単な例です：

```python
import json
from datetime import datetime

def save_tokens(access_token, refresh_token, token_file="tokens.json"):
    """トークンをJSONファイルに保存する関数"""
    with open(token_file, "w") as f:
        json.dump({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "updated_at": datetime.now().isoformat()
        }, f)

def load_tokens(token_file="tokens.json"):
    """保存されたトークンを読み込む関数"""
    import os
    
    if not os.path.exists(token_file):
        return None, None
    
    try:
        with open(token_file, "r") as f:
            data = json.load(f)
            return data.get("access_token"), data.get("refresh_token")
    except Exception as e:
        print(f"トークンの読み込みエラー: {e}")
        return None, None
```

### トークンの有効性確認

アプリケーションの起動時にトークンの有効性を確認することをお勧めします：

```python
def check_token_validity():
    """トークンの有効性を確認する関数"""
    access_token, refresh_token = load_tokens()
    
    if access_token and refresh_token:
        client.set_token(access_token=access_token, refresh_token=refresh_token)
        
        try:
            # 簡単なAPIリクエストを試行
            client.actual_inventory_summary.list(limit=1)
            return True
        except LogilessAuthError:
            # トークンが無効な場合は再認証
            return False
    
    return False
```

### ユーザー認証フロー

ウェブアプリケーションで完全な認証フローを実装する例：

```python
from flask import Flask, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = "your_secret_key"

@app.route("/login")
def login():
    """ユーザーをLOGILESSの認証ページにリダイレクトする"""
    auth_url = client.get_authorization_url()
    return redirect(auth_url)

@app.route("/callback")
def callback():
    """認可コードを受け取り、トークンを取得する"""
    code = request.args.get("code")
    
    if not code:
        return "認可コードが見つかりません", 400
    
    try:
        tokens = client.fetch_token(code)
        
        # トークンをセッションに保存
        session["access_token"] = tokens["access_token"]
        session["refresh_token"] = tokens["refresh_token"]
        
        return redirect(url_for("dashboard"))
    except LogilessAuthError as e:
        return f"認証エラー: {e}", 400

@app.route("/dashboard")
def dashboard():
    """認証後のダッシュボード"""
    if "access_token" not in session:
        return redirect(url_for("login"))
    
    # セッションからトークンを取得
    client.set_token(
        access_token=session["access_token"],
        refresh_token=session["refresh_token"]
    )
    
    # APIリクエストを実行
    try:
        inventory = client.actual_inventory_summary.list()
        return f"在庫数: {len(inventory.get('items', []))}"
    except LogilessAuthError:
        # トークンが無効になった場合は再ログイン
        return redirect(url_for("login"))
```

### 環境変数の使用

認証情報を環境変数から取得することをお勧めします：

```python
import os

client = LogilessClient(
    client_id=os.environ.get("LOGILESS_CLIENT_ID"),
    client_secret=os.environ.get("LOGILESS_CLIENT_SECRET"),
    redirect_uri=os.environ.get("LOGILESS_REDIRECT_URI")
)
```

より詳細な使用例については、[example.py](example.py)を参照してください。 