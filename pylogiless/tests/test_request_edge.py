"""
LogilessClient.request の残存エラー分岐のテスト

成功応答のJSONパース失敗と、想定外の例外のフォールバックを網羅する。
HTTP は self.session.request 経由で発行されるため、session をモックする。
"""
from unittest import mock

import pytest

from pylogiless import LogilessClient
from pylogiless.api.errors import LogilessError


def _client():
    return LogilessClient(access_token="t", merchant_id="m")


def test_json_parse_error_on_success_is_wrapped():
    """200/JSON応答だが本文パースに失敗した場合 LogilessError(JSONパースエラー)"""
    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json.side_effect = ValueError("broken json")

    client = _client()
    with mock.patch.object(client.session, "request", return_value=mock_response):
        with pytest.raises(LogilessError, match="JSONパースエラー"):
            client.request("GET", "https://example.com/x")


def test_unexpected_exception_is_wrapped():
    """RequestException/ValueError/LogilessError 以外の例外は『不明なエラー』に包む"""
    client = _client()
    with mock.patch.object(
        client.session, "request", side_effect=RuntimeError("totally unexpected")
    ):
        with pytest.raises(LogilessError, match="不明なエラー"):
            client.request("GET", "https://example.com/x")
