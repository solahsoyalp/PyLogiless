# エラーコードリファレンス

このドキュメントでは、LOGILESS APIから返される可能性のあるエラーコードとその説明を提供します。

## 目次

- [認証関連のエラー](#認証関連のエラー)
- [一般的なAPIエラー](#一般的なapiエラー)
- [バリデーションエラー](#バリデーションエラー)
- [リソース固有のエラー](#リソース固有のエラー)
- [エラーレスポンスの形式](#エラーレスポンスの形式)

## 認証関連のエラー

OAuth2認証フローに関連するエラーコードです。

| エラーコード | HTTP ステータス | 説明 |
|------------|---------------|------|
| `invalid_request` | 400 | リクエストに必要なパラメータが不足しているか、サポートされていないパラメータが含まれています。 |
| `invalid_client` | 401 | クライアント認証に失敗しました。クライアントIDまたはクライアントシークレットが無効です。 |
| `invalid_grant` | 400 | 提供された認可コードまたはリフレッシュトークンが無効、期限切れ、または取り消されています。 |
| `unauthorized_client` | 401 | クライアントはこのメソッドを使用した認可コードの取得が認可されていません。 |
| `unsupported_grant_type` | 400 | サポートされていない認可タイプが使用されました。 |
| `invalid_scope` | 400 | リクエストされたスコープが無効、不明、または不正な形式です。 |
| `access_denied` | 403 | リソース所有者または認可サーバーがリクエストを拒否しました。 |
| `invalid_token` | 401 | アクセストークンが無効または期限切れです。 |
| `insufficient_scope` | 403 | 要求されたリソースにアクセスするための十分なスコープがトークンにありません。 |

## 一般的なAPIエラー

APIリクエスト処理中に発生する可能性のある一般的なエラーコードです。

| エラーコード | HTTP ステータス | 説明 |
|------------|---------------|------|
| `not_found` | 404 | リクエストされたリソースが見つかりません。 |
| `method_not_allowed` | 405 | このエンドポイントではサポートされていないHTTPメソッドが使用されました。 |
| `rate_limit_exceeded` | 429 | APIレート制限に達しました。しばらく待ってから再試行してください。 |
| `internal_server_error` | 500 | サーバー内部エラーが発生しました。 |
| `service_unavailable` | 503 | サービスが一時的に利用できません。メンテナンス中または過負荷の可能性があります。 |
| `gateway_timeout` | 504 | サービスが応答しませんでした。後で再試行してください。 |
| `bad_gateway` | 502 | サーバーが無効な応答を受信しました。 |
| `conflict` | 409 | リソースの状態に競合が発生しました。現在の状態を確認してからもう一度お試しください。 |
| `forbidden` | 403 | このリソースへのアクセス権がありません。 |
| `too_many_requests` | 429 | 短時間に多すぎるリクエストが送信されました。 |

## バリデーションエラー

リクエストデータのバリデーション時に発生する可能性のあるエラーコードです。

| エラーコード | HTTP ステータス | 説明 |
|------------|---------------|------|
| `validation_error` | 400 | リクエストデータのバリデーションに失敗しました。詳細はレスポンスの`validation_errors`フィールドを参照してください。 |
| `required_field_missing` | 400 | 必須フィールドが不足しています。 |
| `invalid_field_format` | 400 | フィールドの形式が無効です。 |
| `invalid_field_value` | 400 | フィールドの値が無効です。 |
| `field_length_exceeded` | 400 | フィールドの長さが最大許容値を超えています。 |
| `invalid_date_format` | 400 | 日付フィールドの形式が無効です。ISO 8601形式（YYYY-MM-DD）を使用してください。 |
| `invalid_time_format` | 400 | 時刻フィールドの形式が無効です。ISO 8601形式を使用してください。 |
| `invalid_json` | 400 | リクエストボディが有効なJSONではありません。 |
| `invalid_enum_value` | 400 | 列挙型フィールドの値が許可されたオプションのいずれとも一致しません。 |

## リソース固有のエラー

特定のリソースに関連するエラーコードです。

### 商品（Article）関連のエラー

| エラーコード | HTTP ステータス | 説明 |
|------------|---------------|------|
| `article_not_found` | 404 | 指定された商品が見つかりません。 |
| `article_code_already_exists` | 409 | この商品コードはすでに使用されています。 |
| `article_in_use` | 400 | この商品は現在使用中のため削除できません。 |

### 在庫（Inventory）関連のエラー

| エラーコード | HTTP ステータス | 説明 |
|------------|---------------|------|
| `inventory_not_found` | 404 | 指定された在庫が見つかりません。 |
| `insufficient_stock` | 400 | 操作を完了するのに十分な在庫がありません。 |
| `inventory_locked` | 409 | 在庫は現在別の操作によってロックされています。 |

### 配送（Delivery）関連のエラー

| エラーコード | HTTP ステータス | 説明 |
|------------|---------------|------|
| `delivery_not_found` | 404 | 指定された配送が見つかりません。 |
| `delivery_already_processed` | 400 | この配送はすでに処理されています。 |
| `delivery_status_transition_invalid` | 400 | 現在のステータスからリクエストされたステータスへの移行は許可されていません。 |
| `delivery_items_required` | 400 | 配送には少なくとも1つのアイテムが必要です。 |
| `delivery_date_invalid` | 400 | 指定された配送日が無効です。 |

### 倉庫（Warehouse）関連のエラー

| エラーコード | HTTP ステータス | 説明 |
|------------|---------------|------|
| `warehouse_not_found` | 404 | 指定された倉庫が見つかりません。 |
| `warehouse_code_already_exists` | 409 | この倉庫コードはすでに使用されています。 |
| `warehouse_in_use` | 400 | この倉庫は現在使用中のため削除できません。 |

### ロケーション（Location）関連のエラー

| エラーコード | HTTP ステータス | 説明 |
|------------|---------------|------|
| `location_not_found` | 404 | 指定されたロケーションが見つかりません。 |
| `location_code_already_exists` | 409 | このロケーションコードはすでに使用されています。 |
| `location_in_use` | 400 | このロケーションは現在使用中のため削除できません。 |

### 店舗（Store）関連のエラー

| エラーコード | HTTP ステータス | 説明 |
|------------|---------------|------|
| `store_not_found` | 404 | 指定された店舗が見つかりません。 |
| `store_code_already_exists` | 409 | この店舗コードはすでに使用されています。 |
| `store_in_use` | 400 | この店舗は現在使用中のため削除できません。 |

### サプライヤー（Supplier）関連のエラー

| エラーコード | HTTP ステータス | 説明 |
|------------|---------------|------|
| `supplier_not_found` | 404 | 指定されたサプライヤーが見つかりません。 |
| `supplier_code_already_exists` | 409 | このサプライヤーコードはすでに使用されています。 |
| `supplier_in_use` | 400 | このサプライヤーは現在使用中のため削除できません。 |

## エラーレスポンスの形式

エラーが発生した場合、APIは以下の形式のJSONレスポンスを返します：

```json
{
  "error": {
    "code": "error_code",
    "message": "エラーの説明メッセージ",
    "details": "エラーに関する追加の詳細情報（オプション）",
    "request_id": "リクエストの一意の識別子"
  }
}
```

バリデーションエラーの場合、追加のフィールドが含まれることがあります：

```json
{
  "error": {
    "code": "validation_error",
    "message": "リクエストデータのバリデーションに失敗しました",
    "request_id": "リクエストの一意の識別子",
    "validation_errors": {
      "field_name": [
        "エラーメッセージ1",
        "エラーメッセージ2"
      ],
      "another_field": [
        "エラーメッセージ"
      ]
    }
  }
}
```

### エラー処理の例

pylogilessライブラリを使用したエラー処理の例：

```python
from pylogiless import LogilessClient, LogilessError, LogilessValidationError

client = LogilessClient(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    redirect_uri="YOUR_REDIRECT_URI"
)

try:
    # 存在しない商品を取得
    article = client.article.get("NON_EXISTENT_ID")
except LogilessError as e:
    print(f"エラーコード: {e.error_code}")
    print(f"エラーメッセージ: {e.message}")
    print(f"HTTPステータスコード: {e.status_code}")
    
    if e.error_code == "not_found":
        print("商品が見つかりませんでした。")
    elif isinstance(e, LogilessValidationError):
        print("バリデーションエラー:")
        for field, errors in e.validation_errors.items():
            print(f"  {field}: {', '.join(errors)}")
```

エラーハンドリングの詳細については、[エラーハンドリングガイド](error_handling.md)を参照してください。 