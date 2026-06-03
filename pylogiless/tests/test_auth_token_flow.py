"""
OAuth2 トークンフローの異常系・自動リフレッシュ経路のテスト

test_auth.py の正常系を補完し、_request_token / fetch_token /
ensure_active_token のエラー分岐とリフレッシュ分岐を網羅する。
"""
import time
from unittest import mock

import pytest
from requests.exceptions import ConnectionError as RequestsConnectionError

from pylogiless.api.auth import LogilessAuth


def _oauth_auth():
    """OAuth2情報を備えた LogilessAuth を返すヘルパ"""
    return LogilessAuth(
        client_id="cid",
        client_secret="csecret",
        redirect_uri="https://example.com/cb",
    )


class TestFetchTokenGuard:
    def test_fetch_token_requires_oauth_credentials(self):
        """OAuth2情報が無い状態での fetch_token は ValueError"""
        auth = LogilessAuth(access_token="t", merchant_id="m")
        with pytest.raises(ValueError, match="client_id, client_secret, redirect_uri"):
            auth.fetch_token("code")


class TestRequestTokenErrorBranches:
    @mock.patch("requests.get")
    def test_request_exception_is_wrapped(self, mock_get):
        """通信例外(RequestException)は ValueError に包まれる"""
        mock_get.side_effect = RequestsConnectionError("boom")
        auth = _oauth_auth()
        with pytest.raises(ValueError, match="トークンリクエストに失敗しました"):
            auth.fetch_token("code")

    @mock.patch("requests.get")
    def test_error_response_with_unparsable_body(self, mock_get):
        """エラー応答のbodyがJSONでなくても response.text でフォールバックして例外"""
        mock_response = mock.Mock()
        mock_response.status_code = 400
        mock_response.json.side_effect = ValueError("no json")
        mock_response.text = "Bad Request"
        mock_get.return_value = mock_response

        auth = _oauth_auth()
        with pytest.raises(ValueError, match="トークン取得エラー"):
            auth.fetch_token("code")

    @mock.patch("requests.get")
    def test_success_status_but_invalid_json(self, mock_get):
        """200応答だが本文がJSONとしてパースできない場合は ValueError"""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("no json")
        mock_get.return_value = mock_response

        auth = _oauth_auth()
        with pytest.raises(ValueError, match="JSONパースに失敗"):
            auth.fetch_token("code")


class TestEnsureActiveTokenRefreshBranches:
    @mock.patch.object(LogilessAuth, "refresh_access_token")
    def test_no_token_but_refreshable_succeeds(self, mock_refresh):
        """access_token未設定でもリフレッシュ可能なら自動取得して有効化"""
        auth = LogilessAuth(
            client_id="cid", client_secret="csecret", refresh_token="r"
        )

        def _refresh():
            auth.access_token = "fresh"
            return {}

        mock_refresh.side_effect = _refresh

        ok, error = auth.ensure_active_token()
        assert ok is True
        assert error is None
        mock_refresh.assert_called_once()

    @mock.patch.object(LogilessAuth, "refresh_access_token")
    def test_no_token_refresh_failure_returns_error(self, mock_refresh):
        """access_token未設定・リフレッシュ失敗時は (False, エラー文字列)"""
        auth = LogilessAuth(
            client_id="cid", client_secret="csecret", refresh_token="r"
        )
        mock_refresh.side_effect = ValueError("refresh failed")

        ok, error = auth.ensure_active_token()
        assert ok is False
        assert error == "refresh failed"

    @mock.patch.object(LogilessAuth, "refresh_access_token")
    def test_expired_token_refresh_failure_returns_error(self, mock_refresh):
        """期限切れ・リフレッシュ失敗時は (False, エラー文字列)"""
        auth = LogilessAuth(
            access_token="expired",
            client_id="cid",
            client_secret="csecret",
            refresh_token="r",
        )
        auth.token_expires_at = time.time() - 10
        mock_refresh.side_effect = ValueError("refresh failed")

        ok, error = auth.ensure_active_token()
        assert ok is False
        assert error == "refresh failed"
