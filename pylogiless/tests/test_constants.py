"""
pylogiless.api.constants の定数の存在・値・型を検証するテスト

constants は client.py / auth.py から参照される transport 層の既定値や
リトライ対象ステータスコードなどを一元定義する。
"""
from pylogiless.api import constants


def test_api_base_url():
    """API_BASE_URL の値を検証"""
    assert constants.API_BASE_URL == "https://app2.logiless.com/api/v1"


def test_oauth_urls():
    """OAuth2 エンドポイントの値を検証"""
    assert constants.OAUTH_AUTH_URL == "https://app2.logiless.com/oauth/v2/auth"
    assert constants.OAUTH_TOKEN_URL == "https://app2.logiless.com/oauth2/token"


def test_default_timeout():
    """DEFAULT_TIMEOUT の値を検証"""
    assert constants.DEFAULT_TIMEOUT == 30


def test_default_max_retries():
    """DEFAULT_MAX_RETRIES の値を検証"""
    assert constants.DEFAULT_MAX_RETRIES == 3


def test_default_retry_delay():
    """DEFAULT_RETRY_DELAY の値と型を検証"""
    assert constants.DEFAULT_RETRY_DELAY == 1.0
    assert isinstance(constants.DEFAULT_RETRY_DELAY, float)


def test_retryable_status_codes_membership():
    """RETRYABLE_STATUS_CODES の中身を検証"""
    assert constants.RETRYABLE_STATUS_CODES == frozenset({429, 500, 502, 503, 504})


def test_retryable_status_codes_is_frozenset():
    """RETRYABLE_STATUS_CODES が frozenset であること"""
    assert isinstance(constants.RETRYABLE_STATUS_CODES, frozenset)


def test_non_retryable_codes_absent():
    """非リトライ対象のステータス(400/401/403/423/501)が含まれないこと"""
    for code in (400, 401, 403, 404, 423, 501):
        assert code not in constants.RETRYABLE_STATUS_CODES
