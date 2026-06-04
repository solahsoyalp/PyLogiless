"""
pylogiless 全体で共有する定数

API のベースURL・OAuth2 エンドポイント・transport 層の既定値
（タイムアウト/リトライ回数/リトライ間隔）・リトライ対象ステータスコードを
一元的に定義します。client.py / auth.py はここから参照します。
"""

# LOGILESS API のベースURL
API_BASE_URL = "https://app2.logiless.com/api/v1"

# OAuth2 エンドポイント（LOGILESS APIドキュメント準拠）
OAUTH_AUTH_URL = "https://app2.logiless.com/oauth/v2/auth"
OAUTH_TOKEN_URL = "https://app2.logiless.com/oauth2/token"

# transport 層の既定値
DEFAULT_TIMEOUT = 30
DEFAULT_MAX_RETRIES = 3
DEFAULT_RETRY_DELAY = 1.0

# リトライ対象とするHTTPステータスコード
# 429（レート制限）と代表的な一時的サーバーエラー（5xx）を再試行する。
RETRYABLE_STATUS_CODES = frozenset({429, 500, 502, 503, 504})

# HTTP 上で冪等とみなせるメソッド。
# 通信例外（応答前に切断され、サーバ側で処理済みか不明なケース）での
# 自動再試行は、これらのメソッドに限定する。POST のような非冪等メソッドを
# 無条件に再試行すると、更新処理が二重実行される恐れがあるため。
IDEMPOTENT_METHODS = frozenset({"GET", "HEAD", "PUT", "DELETE", "OPTIONS", "TRACE"})

# 非冪等メソッドでも安全に再試行できるステータスコード。
# サーバが要求を処理せず明示的に拒否したことが分かる（429: レート制限,
# 503: 一時的に利用不可）ため、二重実行の懸念がない。
SAFE_TO_RETRY_STATUS_FOR_NON_IDEMPOTENT = frozenset({429, 503})
