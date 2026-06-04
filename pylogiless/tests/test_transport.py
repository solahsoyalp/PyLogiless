"""
transport 層（Session / retry / timeout）の挙動を検証するテスト

LogilessClient の HTTP は self.session.request 経由で発行され、
通信例外（RequestException）およびリトライ対象ステータスコード
（constants.RETRYABLE_STATUS_CODES）では最大 max_retries 回まで
time.sleep(retry_delay) を挟んで再試行される。
ネットワークアクセスはせず、session.request と time.sleep をモックする。
"""
from unittest import mock

import pytest
import requests
from requests.exceptions import ConnectionError as RequestsConnectionError
from requests.exceptions import RequestException

from pylogiless import LogilessClient
from pylogiless.api import constants
from pylogiless.api.errors import (
    LogilessError,
    LogilessRateLimitError,
    LogilessServerError,
    LogilessValidationError,
)


def _make_response(status_code=200, json_data=None, content_type="application/json", text=""):
    """requests.Response を模した Mock を生成するヘルパー"""
    response = mock.Mock()
    response.status_code = status_code
    response.headers = {"Content-Type": content_type}
    response.text = text
    if json_data is None:
        response.json.side_effect = ValueError("No JSON")
    else:
        response.json.return_value = json_data
    return response


def _client(**kwargs):
    """ダミー資格情報のクライアントを生成"""
    return LogilessClient("t", "m", **kwargs)


class TestTransportConfiguration:
    """timeout / max_retries / retry_delay と session の構成を検証"""

    def test_default_values(self):
        """既定値が constants から取得されること"""
        client = _client()
        assert client.timeout == constants.DEFAULT_TIMEOUT
        assert client.max_retries == constants.DEFAULT_MAX_RETRIES
        assert client.retry_delay == constants.DEFAULT_RETRY_DELAY

    def test_custom_values(self):
        """引数指定が反映されること"""
        client = _client(timeout=5, max_retries=7, retry_delay=0.25)
        assert client.timeout == 5
        assert client.max_retries == 7
        assert client.retry_delay == 0.25

    def test_session_is_requests_session(self):
        """self.session が requests.Session のインスタンスであること"""
        client = _client()
        assert isinstance(client.session, requests.Session)

    def test_timeout_passed_through(self):
        """request 時に self.timeout が session.request の timeout に渡ること"""
        client = _client(timeout=12)
        with mock.patch.object(
            client.session, "request", return_value=_make_response(200, {})
        ) as mocked:
            client.request("GET", "https://example.com/x")
        assert mocked.call_args.kwargs["timeout"] == 12


class TestRetryableStatusCodes:
    """リトライ対象ステータスコードの再試行挙動を検証"""

    @pytest.mark.parametrize(
        "status_code,exc",
        [
            (500, LogilessServerError),
            (503, LogilessServerError),
            (429, LogilessRateLimitError),
        ],
    )
    def test_retryable_status_exhausts_then_raises(self, status_code, exc):
        """リトライ対象ステータスが max_retries 回再試行後に対応例外を送出すること"""
        client = _client(max_retries=3, retry_delay=0.01)
        resp = _make_response(status_code, {"error": "boom"})
        with mock.patch("time.sleep") as sleep_mock:
            with mock.patch.object(
                client.session, "request", return_value=resp
            ) as req_mock:
                with pytest.raises(exc):
                    client.request("GET", "https://example.com/x")
        # 初回 + max_retries 回 = 4 回呼ばれる
        assert req_mock.call_count == client.max_retries + 1
        # リトライ回数ぶん sleep される
        assert sleep_mock.call_count == client.max_retries
        sleep_mock.assert_called_with(client.retry_delay)

    def test_retry_then_success_returns_dict(self):
        """1回失敗(503)→2回目200 でdictを返すこと"""
        client = _client(max_retries=3, retry_delay=0.01)
        expected = {"ok": True}
        responses = [
            _make_response(503, {"error": "temporary"}),
            _make_response(200, expected),
        ]
        with mock.patch("time.sleep") as sleep_mock:
            with mock.patch.object(
                client.session, "request", side_effect=responses
            ) as req_mock:
                result = client.request("GET", "https://example.com/x")
        assert result == expected
        assert req_mock.call_count == 2
        assert sleep_mock.call_count == 1

    def test_no_retries_when_max_retries_zero(self):
        """max_retries=0 のとき再試行されず1回で例外送出"""
        client = _client(max_retries=0)
        resp = _make_response(500, {"error": "boom"})
        with mock.patch("time.sleep") as sleep_mock:
            with mock.patch.object(
                client.session, "request", return_value=resp
            ) as req_mock:
                with pytest.raises(LogilessServerError):
                    client.request("GET", "https://example.com/x")
        assert req_mock.call_count == 1
        sleep_mock.assert_not_called()


class TestRequestExceptionRetry:
    """通信例外（RequestException）の再試行挙動を検証"""

    def test_request_exception_exhausts_then_logiless_error(self):
        """RequestException が max_retries 回再試行後 LogilessError になること"""
        client = _client(max_retries=2, retry_delay=0.01)
        with mock.patch("time.sleep") as sleep_mock:
            with mock.patch.object(
                client.session,
                "request",
                side_effect=RequestsConnectionError("conn refused"),
            ) as req_mock:
                with pytest.raises(LogilessError) as exc:
                    client.request("GET", "https://example.com/x")
        assert "APIリクエストエラー" in str(exc.value)
        assert req_mock.call_count == client.max_retries + 1
        assert sleep_mock.call_count == client.max_retries

    def test_request_exception_then_success(self):
        """通信例外1回→2回目200 でdictを返すこと"""
        client = _client(max_retries=3, retry_delay=0.01)
        expected = {"recovered": 1}
        with mock.patch("time.sleep"):
            with mock.patch.object(
                client.session,
                "request",
                side_effect=[RequestException("flap"), _make_response(200, expected)],
            ) as req_mock:
                result = client.request("GET", "https://example.com/x")
        assert result == expected
        assert req_mock.call_count == 2


class TestNonRetryableStatusCodes:
    """非リトライ対象ステータスが1回で即例外になることを検証"""

    @pytest.mark.parametrize("status_code", [400, 401, 403, 423])
    def test_non_retryable_called_once(self, status_code):
        """400/401/403/423 は再試行されず session.request が1回だけ呼ばれること"""
        client = _client(max_retries=3, retry_delay=0.01)
        resp = _make_response(status_code, {"error": "no retry"})
        with mock.patch("time.sleep") as sleep_mock:
            with mock.patch.object(
                client.session, "request", return_value=resp
            ) as req_mock:
                with pytest.raises(LogilessError):
                    client.request("GET", "https://example.com/x")
        assert req_mock.call_count == 1
        sleep_mock.assert_not_called()

    def test_400_raises_validation_error_once(self):
        """400 は LogilessValidationError を1回で送出すること"""
        client = _client()
        resp = _make_response(400, {"message": "bad", "errors": {"f": "req"}})
        with mock.patch.object(
            client.session, "request", return_value=resp
        ) as req_mock:
            with pytest.raises(LogilessValidationError):
                client.request("POST", "https://example.com/x", json={"a": 1})
        assert req_mock.call_count == 1


class TestIdempotentRetry:
    """再試行の冪等性（非冪等メソッドの二重実行防止）を検証"""

    def test_post_not_retried_on_request_exception(self):
        """POST は通信例外で再試行されず、1回で LogilessError になること"""
        client = _client(max_retries=3, retry_delay=0.01)
        with mock.patch("time.sleep") as sleep_mock:
            with mock.patch.object(
                client.session,
                "request",
                side_effect=RequestsConnectionError("conn refused"),
            ) as req_mock:
                with pytest.raises(LogilessError, match="APIリクエストエラー"):
                    client.request("POST", "https://example.com/x", json={"a": 1})
        assert req_mock.call_count == 1
        sleep_mock.assert_not_called()

    @pytest.mark.parametrize("method", ["PUT", "DELETE", "GET", "HEAD"])
    def test_idempotent_retried_on_request_exception(self, method):
        """冪等メソッドは通信例外で再試行されること"""
        client = _client(max_retries=2, retry_delay=0.01)
        with mock.patch("time.sleep") as sleep_mock:
            with mock.patch.object(
                client.session,
                "request",
                side_effect=RequestsConnectionError("conn refused"),
            ) as req_mock:
                with pytest.raises(LogilessError):
                    client.request(method, "https://example.com/x")
        assert req_mock.call_count == client.max_retries + 1
        assert sleep_mock.call_count == client.max_retries

    @pytest.mark.parametrize("status_code", [500, 502, 504])
    def test_post_not_retried_on_server_error_status(self, status_code):
        """POST はサーバが処理した可能性のある 5xx(500/502/504) では再試行しないこと"""
        client = _client(max_retries=3, retry_delay=0.01)
        resp = _make_response(status_code, {"error": "boom"})
        with mock.patch("time.sleep") as sleep_mock:
            with mock.patch.object(
                client.session, "request", return_value=resp
            ) as req_mock:
                with pytest.raises(LogilessError):
                    client.request("POST", "https://example.com/x", json={"a": 1})
        assert req_mock.call_count == 1
        sleep_mock.assert_not_called()

    @pytest.mark.parametrize("status_code", [429, 503])
    def test_post_retried_on_safe_status(self, status_code):
        """POST でもサーバ未処理が確実なコード(429/503)では再試行すること"""
        client = _client(max_retries=2, retry_delay=0.01)
        resp = _make_response(status_code, {"error": "later"})
        with mock.patch("time.sleep") as sleep_mock:
            with mock.patch.object(
                client.session, "request", return_value=resp
            ) as req_mock:
                with pytest.raises(LogilessError):
                    client.request("POST", "https://example.com/x", json={"a": 1})
        assert req_mock.call_count == client.max_retries + 1
        assert sleep_mock.call_count == client.max_retries

    def test_delete_retried_on_server_error_status(self):
        """冪等メソッド(DELETE)は 500 でも再試行されること"""
        client = _client(max_retries=2, retry_delay=0.01)
        resp = _make_response(500, {"error": "boom"})
        with mock.patch("time.sleep"):
            with mock.patch.object(
                client.session, "request", return_value=resp
            ) as req_mock:
                with pytest.raises(LogilessServerError):
                    client.request("DELETE", "https://example.com/x")
        assert req_mock.call_count == client.max_retries + 1

    def test_helpers_classify_methods(self):
        """_is_idempotent / _should_retry_status の分類を直接検証"""
        assert LogilessClient._is_idempotent("get") is True
        assert LogilessClient._is_idempotent("PUT") is True
        assert LogilessClient._is_idempotent("post") is False
        # 非冪等メソッド: 429/503 のみ再試行可
        assert LogilessClient._should_retry_status("POST", 429) is True
        assert LogilessClient._should_retry_status("POST", 503) is True
        assert LogilessClient._should_retry_status("POST", 500) is False
        # 冪等メソッド: リトライ対象コードは全て再試行可
        assert LogilessClient._should_retry_status("GET", 500) is True
        # リトライ対象外コードは常に False
        assert LogilessClient._should_retry_status("GET", 400) is False


class TestMultipartContentType:
    """files 指定時に Content-Type を固定しない（multipart送信を壊さない）ことを検証"""

    def test_content_type_json_when_no_files(self):
        """files 未指定時は Content-Type: application/json が付与されること"""
        client = _client()
        with mock.patch.object(
            client.session, "request", return_value=_make_response(200, {})
        ) as mocked:
            client.request("POST", "https://example.com/x", json={"a": 1})
        sent_headers = mocked.call_args.kwargs["headers"]
        assert sent_headers["Content-Type"] == "application/json"

    def test_no_content_type_when_files_present(self):
        """files 指定時は Content-Type を付与せず requests に委ねること"""
        client = _client()
        with mock.patch.object(
            client.session, "request", return_value=_make_response(200, {})
        ) as mocked:
            client.request(
                "POST",
                "https://example.com/x",
                files={"file": ("a.csv", b"data")},
            )
        sent_headers = mocked.call_args.kwargs["headers"]
        assert "Content-Type" not in sent_headers
        # files はそのまま session.request へ渡ること
        assert mocked.call_args.kwargs["files"] == {"file": ("a.csv", b"data")}

    def test_explicit_header_overrides_even_with_files(self):
        """files 指定時でも呼び出し側が明示した Content-Type は尊重されること"""
        client = _client()
        with mock.patch.object(
            client.session, "request", return_value=_make_response(200, {})
        ) as mocked:
            client.request(
                "POST",
                "https://example.com/x",
                files={"file": ("a.csv", b"data")},
                headers={"Content-Type": "multipart/form-data; boundary=xyz"},
            )
        sent_headers = mocked.call_args.kwargs["headers"]
        assert sent_headers["Content-Type"] == "multipart/form-data; boundary=xyz"


class TestResponseParsingErrors:
    """成功応答の解析中に発生する想定外例外のフォールバックを検証"""

    def test_non_json_helper_branch(self):
        """json_data=None のヘルパーが非JSON応答を生成し {"text": ...} を返す"""
        client = _client()
        resp = _make_response(
            200, json_data=None, content_type="text/plain", text="plain body"
        )
        with mock.patch.object(client.session, "request", return_value=resp):
            result = client.request("GET", "https://example.com/x")
        assert result == {"text": "plain body"}

    def test_unexpected_exception_during_parsing_is_wrapped(self):
        """
        成功応答の解析中に ValueError/LogilessError 以外の例外が出た場合、
        『不明なエラー』として LogilessError に包まれること（client.py の最終分岐）
        """
        client = _client()
        resp = mock.Mock()
        resp.status_code = 200
        # headers.get が想定外の例外を投げる状況を作る
        resp.headers = mock.Mock()
        resp.headers.get.side_effect = RuntimeError("header explosion")
        with mock.patch.object(client.session, "request", return_value=resp):
            with pytest.raises(LogilessError, match="不明なエラー"):
                client.request("GET", "https://example.com/x")
