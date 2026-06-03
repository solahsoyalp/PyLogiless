"""
LogilessClient.request の残存エラー分岐のテスト

成功応答のJSONパース失敗と、想定外の例外のフォールバックを網羅する。
"""
from unittest import mock

import pytest

from pylogiless import LogilessClient
from pylogiless.api.errors import LogilessError


def _client():
    return LogilessClient(access_token="t", merchant_id="m")


@mock.patch("requests.request")
def test_json_parse_error_on_success_is_wrapped(mock_request):
    """200/JSON応答だが本文パースに失敗した場合 LogilessError(JSONパースエラー)"""
    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json.side_effect = ValueError("broken json")
    mock_request.return_value = mock_response

    with pytest.raises(LogilessError, match="JSONパースエラー"):
        _client().request("GET", "https://example.com/x")


@mock.patch("requests.request")
def test_unexpected_exception_is_wrapped(mock_request):
    """RequestException/ValueError/LogilessError 以外の例外は『不明なエラー』に包む"""
    mock_request.side_effect = RuntimeError("totally unexpected")

    with pytest.raises(LogilessError, match="不明なエラー"):
        _client().request("GET", "https://example.com/x")
