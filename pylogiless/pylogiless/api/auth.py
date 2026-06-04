"""
認証関連の機能を提供するモジュール

本モジュールは2つの認証スタイルをハイブリッドにサポートします。

1. 静的アクセストークン方式（既定・後方互換）
   事前に取得した ``access_token`` と ``merchant_id`` をそのまま利用します。
   有効期限の追跡やリフレッシュは行いません。

2. OAuth2 認可コードフロー方式
   ``client_id`` / ``client_secret`` / ``redirect_uri`` を指定すると、
   認可URLの生成・認可コードからのトークン取得・リフレッシュトークンによる
   自動更新が利用できます（LOGILESS APIドキュメントのOAuth2仕様に準拠）。
"""
import time
from typing import Any, Dict, Optional, Tuple

import requests
from requests.exceptions import RequestException

from . import constants


class LogilessAuth:
    """
    LOGILESS APIの認証を処理するクラス

    静的アクセストークンと OAuth2 認可コードフローの両方に対応します。
    """

    # OAuth2 エンドポイント（LOGILESS APIドキュメント準拠。値は constants 由来）
    AUTH_URL = constants.OAUTH_AUTH_URL
    TOKEN_URL = constants.OAUTH_TOKEN_URL

    def __init__(
        self,
        access_token: Optional[str] = None,
        merchant_id: Optional[str] = None,
        *,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        redirect_uri: Optional[str] = None,
        refresh_token: Optional[str] = None,
        token_expires_at: Optional[float] = None,
    ):
        """
        LogilessAuthクラスの初期化

        Args:
            access_token (Optional[str]): アクセストークン（静的トークン方式で利用）
            merchant_id (Optional[str]): マーチャントID
            client_id (Optional[str]): OAuth2クライアントID
            client_secret (Optional[str]): OAuth2クライアントシークレット
            redirect_uri (Optional[str]): OAuth2リダイレクトURI（登録済みのもの）
            refresh_token (Optional[str]): リフレッシュトークン
            token_expires_at (Optional[float]): アクセストークンの有効期限（UNIX時刻）
        """
        self.access_token = access_token
        self.merchant_id = merchant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.refresh_token = refresh_token
        self.token_expires_at = token_expires_at

    def _can_refresh(self) -> bool:
        """
        リフレッシュトークンによる自動更新が可能かどうかを返す

        Returns:
            bool: refresh_token・client_id・client_secret が揃っていればTrue
        """
        return bool(self.refresh_token and self.client_id and self.client_secret)

    def get_auth_header(self) -> Dict[str, str]:
        """
        APIリクエスト用の認証ヘッダーを取得する

        Returns:
            Dict[str, str]: Authorization ヘッダーを含む辞書
        """
        return {"Authorization": f"Bearer {self.access_token}"}

    def get_authorization_url(self) -> str:
        """
        OAuth2 認可URLを生成する

        ユーザーをこのURLへリダイレクトし、承認後に返却される ``code`` を
        :meth:`fetch_token` に渡してアクセストークンを取得します。

        Returns:
            str: 認可エンドポイントのURL

        Raises:
            ValueError: client_id または redirect_uri が未設定の場合
        """
        if not self.client_id or not self.redirect_uri:
            raise ValueError("認可URLの生成には client_id と redirect_uri が必要です")
        return (
            f"{self.AUTH_URL}?client_id={self.client_id}"
            f"&response_type=code&redirect_uri={self.redirect_uri}"
        )

    def fetch_token(self, code: str) -> Dict[str, Any]:
        """
        認可コードをアクセストークンに交換する

        Args:
            code (str): 認可エンドポイントから返却された認可コード（有効期限約30秒）

        Returns:
            Dict[str, Any]: トークンエンドポイントのレスポンス
                （access_token, refresh_token, expires_in, token_type を含む）

        Raises:
            ValueError: 必要なOAuth2情報が未設定、またはトークン取得に失敗した場合
        """
        if not (self.client_id and self.client_secret and self.redirect_uri):
            raise ValueError(
                "トークン取得には client_id, client_secret, redirect_uri が必要です"
            )
        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri,
        }
        return self._request_token(params)

    def refresh_access_token(self) -> Dict[str, Any]:
        """
        リフレッシュトークンを使ってアクセストークンを更新する

        Returns:
            Dict[str, Any]: トークンエンドポイントのレスポンス

        Raises:
            ValueError: refresh_token・client_id・client_secret のいずれかが未設定、
                またはトークン更新に失敗した場合
        """
        if not self._can_refresh():
            raise ValueError(
                "トークンの更新には refresh_token, client_id, client_secret が必要です"
            )
        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
            "grant_type": "refresh_token",
        }
        return self._request_token(params)

    def _request_token(self, params: Dict[str, str]) -> Dict[str, Any]:
        """
        トークンエンドポイントへGETリクエストを送り、結果を保存する

        Args:
            params (Dict[str, str]): リクエストパラメータ

        Returns:
            Dict[str, Any]: トークンエンドポイントのレスポンス

        Raises:
            ValueError: リクエスト失敗・エラーレスポンス・JSONパース失敗の場合
        """
        try:
            response = requests.get(self.TOKEN_URL, params=params)
        except RequestException as e:
            raise ValueError(f"トークンリクエストに失敗しました: {str(e)}")

        if response.status_code >= 400:
            try:
                error_data = response.json()
            except ValueError:
                error_data = {"error": "解析エラー", "error_description": response.text}
            error = error_data.get("error", "不明なエラー")
            error_description = error_data.get("error_description", "")
            raise ValueError(f"トークン取得エラー: {error}: {error_description}")

        try:
            data = response.json()
        except ValueError as e:
            raise ValueError(f"トークンレスポンスのJSONパースに失敗しました: {str(e)}")

        self.set_token(
            data.get("access_token"),
            data.get("refresh_token", self.refresh_token),
            data.get("expires_in"),
        )
        return data

    def set_token(
        self,
        access_token: Optional[str],
        refresh_token: Optional[str] = None,
        expires_in: Optional[int] = None,
    ) -> None:
        """
        トークン情報を手動で設定する

        Args:
            access_token (Optional[str]): アクセストークン
            refresh_token (Optional[str], optional): リフレッシュトークン
            expires_in (Optional[int], optional): 有効期限までの秒数。
                指定すると ``token_expires_at`` を現在時刻からの相対で設定します。
        """
        self.access_token = access_token
        if refresh_token is not None:
            self.refresh_token = refresh_token
        if expires_in is not None:
            self.token_expires_at = time.time() + float(expires_in)

    def is_token_expired(self) -> bool:
        """
        アクセストークンが期限切れかどうかを確認する

        静的トークン方式（有効期限が未設定）の場合は常に期限切れではないと
        みなします。OAuth2方式で有効期限が判明している場合のみ実際に判定します。

        Returns:
            bool: トークンが期限切れ（または未設定）の場合はTrue
        """
        if not self.access_token:
            return True
        if self.token_expires_at is None:
            return False
        return time.time() >= self.token_expires_at

    def ensure_active_token(self) -> Tuple[bool, Optional[str]]:
        """
        アクセストークンが有効であることを確認する

        期限切れ（または未設定）でも、リフレッシュ可能であれば自動的に
        トークンを更新して有効化を試みます。

        Returns:
            Tuple[bool, Optional[str]]:
                - トークンが有効であればTrue、そうでなければFalse
                - エラーメッセージ（エラーがない場合はNone）
        """
        if not self.access_token:
            if self._can_refresh():
                try:
                    self.refresh_access_token()
                    return True, None
                except ValueError as e:
                    return False, str(e)
            return False, "アクセストークンが設定されていません"

        if self.is_token_expired():
            if self._can_refresh():
                try:
                    self.refresh_access_token()
                    return True, None
                except ValueError as e:
                    return False, str(e)
            return False, "トークンの有効期限が切れています"

        return True, None
