"""
LOGILESS APIのクライアントモジュール
"""
import time
from typing import Any, Dict, List, Optional, Union

import requests
from requests.exceptions import RequestException

from . import constants
from .auth import LogilessAuth
from .errors import LogilessError, raise_for_error
from .resources import *  # noqa: F401,F403  (後方互換: *Resource を client から再エクスポート)
from .resources import (
    APIResource,
    ActualInventorySummaryResource,
    ArticleMapResource,
    ArticleResource,
    DailyInventorySummaryResource,
    InboundDeliveryResource,
    InterWarehouseTransferResource,
    LocationResource,
    LogicalInventorySummaryResource,
    OutboundDeliveryResource,
    ReorderPointResource,
    SalesOrderResource,
    SalesReturnResource,
    StoreResource,
    SupplierResource,
    TransactionLogResource,
    WarehouseResource,
)


class LogilessClient:
    """
    LOGILESS APIのクライアントクラス
    """

    API_BASE_URL = constants.API_BASE_URL

    def __init__(
        self,
        access_token: Optional[str] = None,
        merchant_id: Optional[str] = None,
        api_base_url: Optional[str] = None,
        *,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        redirect_uri: Optional[str] = None,
        refresh_token: Optional[str] = None,
        timeout: Union[int, float] = constants.DEFAULT_TIMEOUT,
        max_retries: int = constants.DEFAULT_MAX_RETRIES,
        retry_delay: float = constants.DEFAULT_RETRY_DELAY,
    ):
        """
        LogilessClientクラスの初期化

        静的アクセストークン方式（access_token + merchant_id）と、
        OAuth2 認可コードフロー方式（client_id / client_secret / redirect_uri /
        refresh_token）の両方に対応します。OAuth2情報を渡した場合、トークンの
        期限切れ時にリフレッシュトークンで自動更新されます。

        Args:
            access_token (Optional[str]): アクセストークン
            merchant_id (Optional[str]): マーチャントID
            api_base_url (Optional[str], optional): APIベースURL（テスト用など）
            client_id (Optional[str], optional): OAuth2クライアントID
            client_secret (Optional[str], optional): OAuth2クライアントシークレット
            redirect_uri (Optional[str], optional): OAuth2リダイレクトURI
            refresh_token (Optional[str], optional): リフレッシュトークン
            timeout (Union[int, float], optional): HTTPリクエストのタイムアウト秒数
            max_retries (int, optional): リトライ対象エラー時の最大再試行回数
            retry_delay (float, optional): 再試行間の待機秒数
        """
        self.api_base_url = api_base_url or self.API_BASE_URL
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.session = requests.Session()
        self.auth = LogilessAuth(
            access_token,
            merchant_id,
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            refresh_token=refresh_token,
        )

        # APIリソースを初期化
        self.article = ArticleResource(self)
        self.actual_inventory_summary = ActualInventorySummaryResource(self)
        self.logical_inventory_summary = LogicalInventorySummaryResource(self)
        self.outbound_delivery = OutboundDeliveryResource(self)
        self.inbound_delivery = InboundDeliveryResource(self)
        self.sales_order = SalesOrderResource(self)
        self.sales_return = SalesReturnResource(self)
        self.warehouse = WarehouseResource(self)
        self.store = StoreResource(self)
        self.location = LocationResource(self)
        # 追加のAPIリソース
        self.reorder_point = ReorderPointResource(self)
        self.supplier = SupplierResource(self)
        self.article_map = ArticleMapResource(self)
        self.daily_inventory_summary = DailyInventorySummaryResource(self)
        self.transaction_log = TransactionLogResource(self)
        self.inter_warehouse_transfer = InterWarehouseTransferResource(self)

    @staticmethod
    def _is_idempotent(method: str) -> bool:
        """
        HTTPメソッドが冪等かどうかを返す

        Args:
            method (str): HTTPメソッド

        Returns:
            bool: 冪等メソッドであればTrue
        """
        return method.upper() in constants.IDEMPOTENT_METHODS

    @classmethod
    def _should_retry_status(cls, method: str, status_code: int) -> bool:
        """
        ステータスコードに基づき再試行すべきかを判定する

        冪等メソッドはリトライ対象コードすべてで再試行する。非冪等メソッドは
        サーバが処理していないと確実に分かるコード（429 / 503）のみ再試行する。

        Args:
            method (str): HTTPメソッド
            status_code (int): レスポンスのステータスコード

        Returns:
            bool: 再試行すべきであればTrue
        """
        if status_code not in constants.RETRYABLE_STATUS_CODES:
            return False
        if cls._is_idempotent(method):
            return True
        return status_code in constants.SAFE_TO_RETRY_STATUS_FOR_NON_IDEMPOTENT

    def request(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        files: Optional[Dict[str, Any]] = None,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        APIリクエストを実行する

        通信例外（RequestException）および一時的エラーとみなせるステータスコード
        （constants.RETRYABLE_STATUS_CODES）の場合は、最大 ``max_retries`` 回まで
        ``retry_delay`` 秒の待機を挟んで自動的に再試行します。再試行を使い切った
        場合は従来通り例外を送出します。

        ただし更新処理の二重実行を避けるため、再試行は冪等性を考慮します。
        - 通信例外（応答前に切断され処理済みか不明）での再試行は、冪等メソッド
          （GET/HEAD/PUT/DELETE/OPTIONS/TRACE）に限定します。POST のような
          非冪等メソッドは再試行せず即座に例外を送出します。
        - ステータスコードによる再試行は、冪等メソッドでは従来どおり行い、
          非冪等メソッドではサーバが処理していないと確実に分かるコード
          （429 / 503）のみ再試行します。

        Args:
            method (str): HTTPメソッド
            url (str): リクエストURL
            params (Optional[Dict[str, Any]], optional): URLクエリパラメータ
            json (Optional[Dict[str, Any]], optional): JSONリクエストボディ
            headers (Optional[Dict[str, str]], optional): HTTPヘッダー
            files (Optional[Dict[str, Any]], optional): マルチパートファイル

        Returns:
            Union[Dict[str, Any], List[Dict[str, Any]]]: APIレスポンス

        Raises:
            LogilessError: APIエラーが発生した場合
        """
        # トークンが有効かチェック
        token_valid, error_message = self.auth.ensure_active_token()
        if not token_valid:
            raise LogilessError(error_message)

        # ヘッダーの準備
        request_headers = {
            "Content-Type": "application/json",
            **self.auth.get_auth_header(),
        }
        if headers:
            request_headers.update(headers)

        attempt = 0
        while True:
            try:
                # リクエスト実行
                response = self.session.request(
                    method,
                    url,
                    params=params,
                    json=json,
                    headers=request_headers,
                    files=files,
                    timeout=self.timeout,
                )
            except RequestException as e:
                # 通信例外: 冪等メソッドかつリトライ余地があれば待機して再試行。
                # 非冪等メソッドは処理済みの可能性があるため再試行しない。
                if attempt < self.max_retries and self._is_idempotent(method):
                    attempt += 1
                    time.sleep(self.retry_delay)
                    continue
                raise LogilessError(f"APIリクエストエラー: {str(e)}")
            except Exception as e:
                raise LogilessError(f"不明なエラー: {str(e)}")

            # リトライ対象ステータスコード: リトライ余地があり、かつ
            # 冪等性の観点から安全に再試行できる場合のみ再試行する。
            if attempt < self.max_retries and self._should_retry_status(
                method, response.status_code
            ):
                attempt += 1
                time.sleep(self.retry_delay)
                continue

            try:
                # 成功以外のステータスコードの場合、例外をスロー
                if response.status_code >= 400:
                    try:
                        error_data = response.json()
                    except ValueError:
                        error_data = {"error": "解析エラー", "error_description": response.text}
                    raise_for_error(response.status_code, error_data)

                # レスポンスがJSONの場合はパース、そうでなければテキスト
                if response.headers.get("Content-Type", "").startswith("application/json"):
                    return response.json()
                return {"text": response.text}

            except ValueError as e:
                raise LogilessError(f"JSONパースエラー: {str(e)}")
            except LogilessError:
                raise
            except Exception as e:
                raise LogilessError(f"不明なエラー: {str(e)}")
