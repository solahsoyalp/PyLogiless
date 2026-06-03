"""
認証モジュールのテスト
"""
import time
from unittest import mock

import pytest

from pylogiless.api.auth import LogilessAuth


class TestLogilessAuth:
    """
    LogilessAuthクラスのテストケース
    """

    def setup_method(self):
        """
        テスト前の準備
        """
        self.access_token = "test_access_token"
        self.merchant_id = "test_merchant_id"
        self.auth = LogilessAuth(self.access_token, self.merchant_id)

    def test_initialization(self):
        """
        アクセストークンとマーチャントIDで初期化できることをテスト
        """
        assert self.auth.access_token == self.access_token
        assert self.auth.merchant_id == self.merchant_id

    def test_get_auth_header(self):
        """
        認証ヘッダーが Authorization のみを返すことをテスト
        """
        header = self.auth.get_auth_header()

        # Bearer トークンのみを含むことを検証
        assert header == {"Authorization": f"Bearer {self.access_token}"}

        # X-Merchant-ID ヘッダーを含まないことを検証
        assert "X-Merchant-ID" not in header

    def test_is_token_expired_without_token(self):
        """
        アクセストークンが未設定の場合は期限切れ(True)を返すことをテスト
        """
        self.auth.access_token = None
        assert self.auth.is_token_expired() is True

    def test_is_token_expired_with_token(self):
        """
        アクセストークンが設定済みの場合は期限切れでない(False)ことをテスト
        """
        self.auth.access_token = "test_access_token"
        assert self.auth.is_token_expired() is False

    def test_ensure_active_token_without_token(self):
        """
        アクセストークンが未設定の場合は (False, メッセージ) を返すことをテスト
        """
        self.auth.access_token = None
        result, error = self.auth.ensure_active_token()

        assert result is False
        assert error == "アクセストークンが設定されていません"

    def test_ensure_active_token_with_token(self):
        """
        アクセストークンが設定済みの場合は (True, None) を返すことをテスト
        """
        self.auth.access_token = "test_access_token"
        result, error = self.auth.ensure_active_token()

        assert result is True
        assert error is None


class TestLogilessAuthOAuth2:
    """
    OAuth2 認可コードフロー（ハイブリッド対応）のテストケース
    """

    def setup_method(self):
        """
        テスト前の準備
        """
        self.client_id = "test_client_id"
        self.client_secret = "test_client_secret"
        self.redirect_uri = "https://example.com/callback"
        self.auth = LogilessAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
        )

    def test_get_authorization_url(self):
        """
        認可URLが正しく生成されることをテスト
        """
        expected = (
            f"{LogilessAuth.AUTH_URL}?client_id={self.client_id}"
            f"&response_type=code&redirect_uri={self.redirect_uri}"
        )
        assert self.auth.get_authorization_url() == expected

    def test_get_authorization_url_missing_params(self):
        """
        client_id / redirect_uri が無いと例外になることをテスト
        """
        auth = LogilessAuth()
        with pytest.raises(ValueError):
            auth.get_authorization_url()

    @mock.patch("requests.get")
    def test_fetch_token_success(self, mock_get):
        """
        認可コードからトークンを取得し、状態が更新されることをテスト
        """
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "new_access_token",
            "refresh_token": "new_refresh_token",
            "expires_in": 2592000,
            "token_type": "bearer",
        }
        mock_get.return_value = mock_response

        result = self.auth.fetch_token("auth_code")

        assert result == mock_response.json.return_value
        assert self.auth.access_token == "new_access_token"
        assert self.auth.refresh_token == "new_refresh_token"
        assert self.auth.token_expires_at is not None
        mock_get.assert_called_once_with(
            LogilessAuth.TOKEN_URL,
            params={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "code": "auth_code",
                "grant_type": "authorization_code",
                "redirect_uri": self.redirect_uri,
            },
        )

    @mock.patch("requests.get")
    def test_fetch_token_error(self, mock_get):
        """
        トークンエンドポイントがエラーを返した場合に例外になることをテスト
        """
        mock_response = mock.Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "error": "invalid_grant",
            "error_description": "Invalid code",
        }
        mock_get.return_value = mock_response

        with pytest.raises(ValueError, match="トークン取得エラー"):
            self.auth.fetch_token("bad_code")

    @mock.patch("requests.get")
    def test_refresh_access_token_success(self, mock_get):
        """
        リフレッシュトークンでトークンが更新されることをテスト
        """
        self.auth.refresh_token = "existing_refresh_token"

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "refreshed_access_token",
            "refresh_token": "refreshed_refresh_token",
            "expires_in": 2592000,
            "token_type": "bearer",
        }
        mock_get.return_value = mock_response

        result = self.auth.refresh_access_token()

        assert result == mock_response.json.return_value
        assert self.auth.access_token == "refreshed_access_token"
        assert self.auth.refresh_token == "refreshed_refresh_token"
        mock_get.assert_called_once_with(
            LogilessAuth.TOKEN_URL,
            params={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": "existing_refresh_token",
                "grant_type": "refresh_token",
            },
        )

    def test_refresh_access_token_without_credentials(self):
        """
        リフレッシュに必要な情報が揃っていないと例外になることをテスト
        """
        auth = LogilessAuth(access_token="t", merchant_id="m")
        with pytest.raises(ValueError):
            auth.refresh_access_token()

    def test_set_token_sets_expiry(self):
        """
        set_token で expires_in から有効期限が設定されることをテスト
        """
        self.auth.set_token("a_token", "r_token", 3600)
        assert self.auth.access_token == "a_token"
        assert self.auth.refresh_token == "r_token"
        assert self.auth.token_expires_at is not None
        assert self.auth.token_expires_at - time.time() > 3590

    def test_is_token_expired_with_expiry(self):
        """
        有効期限を過ぎたトークンが期限切れ判定されることをテスト
        """
        self.auth.access_token = "a_token"
        self.auth.token_expires_at = time.time() - 10
        assert self.auth.is_token_expired() is True

        self.auth.token_expires_at = time.time() + 3600
        assert self.auth.is_token_expired() is False

    @mock.patch.object(LogilessAuth, "refresh_access_token")
    def test_ensure_active_token_auto_refresh(self, mock_refresh):
        """
        期限切れかつリフレッシュ可能な場合に自動更新されることをテスト
        """
        self.auth.access_token = "expired_token"
        self.auth.refresh_token = "a_refresh_token"
        self.auth.token_expires_at = time.time() - 10

        def _do_refresh():
            self.auth.access_token = "fresh_token"
            self.auth.token_expires_at = time.time() + 3600
            return {}

        mock_refresh.side_effect = _do_refresh

        result, error = self.auth.ensure_active_token()

        assert result is True
        assert error is None
        mock_refresh.assert_called_once()

    def test_ensure_active_token_expired_no_refresh(self):
        """
        期限切れでリフレッシュ不可なら (False, メッセージ) を返すことをテスト
        """
        auth = LogilessAuth(access_token="expired_token", merchant_id="m")
        auth.token_expires_at = time.time() - 10

        result, error = auth.ensure_active_token()

        assert result is False
        assert error == "トークンの有効期限が切れています"
