"""
LogilessClient.request メソッドのテスト

self.session.request を unittest.mock でモックし、ネットワークアクセスをせずに
リクエスト送出・レスポンス解析・エラー変換・ヘッダ・パラメータ受け渡しを検証する。

transport 層導入後、HTTP は self.session.request 経由で発行され、
リトライ対象ステータス（429/5xx）や通信例外では複数回呼ばれ得る。
リトライを伴うケースでは time.sleep をモックして待ち時間を消す。
"""
from unittest import mock

import pytest
import requests
from requests.exceptions import RequestException

from pylogiless import LogilessClient
from pylogiless.api.errors import (
    LogilessAuthError,
    LogilessError,
    LogilessRateLimitError,
    LogilessResourceLockedError,
    LogilessServerError,
    LogilessValidationError,
)


def _make_response(status_code=200, json_data=None, content_type="application/json", text=""):
    """
    requests.Response を模した Mock を生成するヘルパー

    Args:
        status_code (int): HTTPステータスコード
        json_data: response.json() が返す値（None なら ValueError を送出）
        content_type (str): Content-Type ヘッダ値
        text (str): response.text の値

    Returns:
        mock.Mock: モックレスポンス
    """
    response = mock.Mock()
    response.status_code = status_code
    response.headers = {"Content-Type": content_type}
    response.text = text
    if json_data is None:
        response.json.side_effect = ValueError("No JSON")
    else:
        response.json.return_value = json_data
    return response


class TestLogilessClientRequest:
    """
    LogilessClient.request の挙動を検証するテストケース
    """

    def setup_method(self):
        """
        ダミーの access_token / merchant_id でクライアントを生成する
        """
        self.client = LogilessClient("dummy_token", "dummy_merchant")
        self.url = "https://app2.logiless.com/api/v1/merchant/dummy_merchant/articles"

    def _patch_request(self, **kwargs):
        """self.client.session.request をモックする"""
        return mock.patch.object(self.client.session, "request", **kwargs)

    def test_returns_dict_on_json_response(self):
        """
        200 かつ Content-Type が application/json の場合に dict を返すことを検証
        """
        expected = {"id": 1, "name": "test"}
        with self._patch_request(return_value=_make_response(200, expected)):
            result = self.client.request("GET", self.url)
        assert result == expected

    def test_returns_text_on_non_json_response(self):
        """
        200 かつ JSON 以外の Content-Type の場合に {"text": ...} を返すことを検証
        """
        resp = _make_response(200, json_data=None, content_type="text/plain", text="hello")
        with self._patch_request(return_value=resp):
            result = self.client.request("GET", self.url)
        assert result == {"text": "hello"}

    def test_400_raises_validation_error(self):
        """
        400 で LogilessValidationError が送出されることを検証
        """
        body = {"message": "不正な入力", "errors": {"name": "必須です"}}
        with self._patch_request(return_value=_make_response(400, body)):
            with pytest.raises(LogilessValidationError) as exc:
                self.client.request("POST", self.url, json={"x": 1})
        assert exc.value.status_code == 400
        assert exc.value.validation_errors == {"name": "必須です"}

    def test_401_raises_auth_error(self):
        """
        401 で LogilessAuthError が送出されることを検証
        """
        with self._patch_request(return_value=_make_response(401, {"error": "unauthorized"})):
            with pytest.raises(LogilessAuthError):
                self.client.request("GET", self.url)

    def test_403_raises_auth_error(self):
        """
        403 で LogilessAuthError が送出されることを検証
        """
        with self._patch_request(return_value=_make_response(403, {"error": "forbidden"})):
            with pytest.raises(LogilessAuthError):
                self.client.request("GET", self.url)

    def test_423_raises_resource_locked_error(self):
        """
        423 で LogilessResourceLockedError が送出されることを検証
        """
        with self._patch_request(return_value=_make_response(423, {"error": "locked"})):
            with pytest.raises(LogilessResourceLockedError):
                self.client.request("GET", self.url)

    def test_429_raises_rate_limit_error(self):
        """
        429 で LogilessRateLimitError が送出されることを検証（リトライ後に最終的に送出）
        """
        with mock.patch("time.sleep"):
            with self._patch_request(return_value=_make_response(429, {"error": "too many"})):
                with pytest.raises(LogilessRateLimitError):
                    self.client.request("GET", self.url)

    def test_500_raises_server_error(self):
        """
        500 で LogilessServerError が送出されることを検証（リトライ後に最終的に送出）
        """
        with mock.patch("time.sleep"):
            with self._patch_request(return_value=_make_response(500, {"error": "server"})):
                with pytest.raises(LogilessServerError):
                    self.client.request("GET", self.url)

    def test_error_body_not_json_still_raises(self):
        """
        エラー応答が response.json() で取得できない場合でも例外になることを検証
        （json() が ValueError を送出 → フォールバックボディで raise_for_error が呼ばれる）
        500 はリトライ対象のため time.sleep をモックする
        """
        resp = _make_response(500, json_data=None, content_type="text/html", text="<html>error</html>")
        with mock.patch("time.sleep"):
            with self._patch_request(return_value=resp):
                with pytest.raises(LogilessServerError):
                    self.client.request("GET", self.url)

    def test_request_exception_wrapped_in_logiless_error(self):
        """
        requests が RequestException を投げた場合に LogilessError に包まれることを検証
        （リトライを使い切って包む）
        """
        with mock.patch("time.sleep"):
            with self._patch_request(side_effect=RequestException("接続失敗")):
                with pytest.raises(LogilessError) as exc:
                    self.client.request("GET", self.url)
        assert "APIリクエストエラー" in str(exc.value)

    def test_invalid_token_raises_without_http_call(self):
        """
        ensure_active_token が無効を返す場合に LogilessError が送出され、
        HTTP 呼び出しが行われないことを検証（auth をモック）
        """
        self.client.auth.ensure_active_token = mock.Mock(return_value=(False, "トークン無効"))
        with self._patch_request() as mocked:
            with pytest.raises(LogilessError) as exc:
                self.client.request("GET", self.url)
        mocked.assert_not_called()
        assert "トークン無効" in str(exc.value)

    def test_default_headers_contain_auth_and_content_type(self):
        """
        リクエストヘッダに Authorization と Content-Type が含まれることを検証
        """
        with self._patch_request(return_value=_make_response(200, {})) as mocked:
            self.client.request("GET", self.url)
        sent_headers = mocked.call_args.kwargs["headers"]
        assert sent_headers["Content-Type"] == "application/json"
        assert sent_headers["Authorization"] == "Bearer dummy_token"

    def test_headers_argument_overrides_defaults(self):
        """
        引数 headers でデフォルトヘッダを上書きできることを検証
        """
        override = {"Content-Type": "text/csv", "X-Custom": "v"}
        with self._patch_request(return_value=_make_response(200, {})) as mocked:
            self.client.request("GET", self.url, headers=override)
        sent_headers = mocked.call_args.kwargs["headers"]
        assert sent_headers["Content-Type"] == "text/csv"
        assert sent_headers["X-Custom"] == "v"
        # Authorization はマージされ残る
        assert sent_headers["Authorization"] == "Bearer dummy_token"

    def test_params_and_json_passed_to_requests(self):
        """
        params / json が session.request にそのまま渡されることを検証
        """
        params = {"page": 2, "limit": 10}
        payload = {"name": "新商品"}
        with self._patch_request(return_value=_make_response(200, {})) as mocked:
            self.client.request("POST", self.url, params=params, json=payload)
        kwargs = mocked.call_args.kwargs
        assert kwargs["params"] == params
        assert kwargs["json"] == payload
        # メソッドと URL は位置引数で渡される
        args = mocked.call_args.args
        assert args[0] == "POST"
        assert args[1] == self.url

    def test_timeout_passed_to_session_request(self):
        """
        self.timeout が session.request の timeout 引数として渡されることを検証
        """
        with self._patch_request(return_value=_make_response(200, {})) as mocked:
            self.client.request("GET", self.url)
        assert mocked.call_args.kwargs["timeout"] == self.client.timeout
