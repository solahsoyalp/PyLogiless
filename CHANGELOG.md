# Changelog

## [0.4.0] - 2026-06-04

### 破壊的変更
- `LogilessClient` 生成時に `merchant_id` を必須化。未指定の場合は `ValueError`
  を送出（従来は `merchant/None/...` という不正URLへリクエストしていた）(#6)
- 非冪等メソッド（POST など）の自動再試行を抑制。更新処理の二重実行を防ぐため、
  通信例外での再試行は冪等メソッド（GET/HEAD/PUT/DELETE/OPTIONS/TRACE）に限定し、
  ステータスコードによる再試行は非冪等メソッドでは 429/503 のみとした (#2)

### バグ修正
- `files` 指定時に `Content-Type: application/json` を固定していたため
  multipart 送信が壊れる問題を修正。files 指定時は requests に委譲する (#8)
- OAuth2 認可URLのクエリを URL エンコードするよう修正 (#5)
- OAuth2 トークン取得・更新リクエストにタイムアウトを付与 (#9)
- OAuth2 トークン応答に `access_token` が無い場合に成功扱いせず例外を送出 (#4)
- `set_token` で `expires_in` 省略時に旧有効期限を引き継がないよう修正 (#3)

### ドキュメント
- README のテスト実行コマンドを実在するパスへ修正 (#7)

## [0.3.1] - 2026-06-04

### 変更点
- リリース自動化を整備。PyPI Trusted Publishing (OIDC) による `v*` タグ起点の
  自動公開フローを本リリースで検証（コード/APIの機能変更なし）

## [0.3.0] - 2026-06-04

### 追加
- transport層を追加。`LogilessClient` が内部で `requests.Session` を保持し、
  キーワード専用引数 `timeout` / `max_retries` / `retry_delay` による
  タイムアウト・自動リトライに対応（リトライ対象: 通信例外および
  ステータスコード `429 / 500 / 502 / 503 / 504`）
- `py.typed` を同梱し、mypy / pyright などの型チェッカ向けに型情報を配布
- `SECURITY.md` / `RELEASING.md` を追加し、Trusted Publishing(OIDC) による
  PyPI 公開のリリースCIを整備

### 変更点
- リソースクラスを `resources/` サブパッケージへ分割（公開APIは後方互換を維持し、
  `pylogiless` および `pylogiless.api.client` からの import は従来どおり利用可能）
- 既定値・リトライ対象ステータスコード・各種URLを `constants.py` へ集約
- パッケージ設定を `pyproject.toml` の `[project]` テーブルへモダン化し、
  バージョンを `dynamic` 管理に変更
- `requires-python >= 3.8`

## [0.2.1] - 2026-06-04

### 追加
- 受注返品(SalesReturn)APIの追加
- OAuth2 認可コードフロー対応（ハイブリッド）。`client_id` / `client_secret` / `redirect_uri` /
  `refresh_token` を指定すると、認可URL生成・認可コードからのトークン取得・期限切れ時の
  リフレッシュトークンによる自動更新が利用可能（静的アクセストークン方式は従来どおり後方互換）
- 包括的なテストスイート（320件）とCI(GitHub Actions)・カバレッジ設定を追加（ソース行カバレッジ100%）

### 変更点
- 認証ヘッダからX-Merchant-IDを削除しドキュメント仕様に整合
- ドキュメント/docstringの認証説明を更新

## [0.2.0] - 2024-03-21

### 変更点
- バージョンを0.2.0に更新
- Python 3.11のサポートを追加
- 開発ステータスをAlphaからBetaに更新
- 依存パッケージのバージョンを更新
  - requests >= 2.31.0
  - python-dotenv >= 1.0.0

### 機能改善
- 実在庫サマリAPIの改善
- 論理在庫サマリAPIの改善
- 商品一覧APIの改善

### バグ修正
- 環境変数の読み込み処理の改善
- エラーハンドリングの強化

## [0.1.0] - 2024-03-20

### 初期リリース
- LOGILESS APIの基本的な機能を実装
- 実在庫サマリAPIのサポート
- 論理在庫サマリAPIのサポート
- 商品一覧APIのサポート 