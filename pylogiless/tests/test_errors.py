"""
errors.py のテスト

raise_for_error の全分岐、各例外クラスの継承関係、
LogilessError/LogilessValidationError の __str__ 挙動、
body のキー欠落時のデフォルトメッセージ挙動を網羅する。
"""
import pytest

from pylogiless.api.errors import (
    LogilessError,
    LogilessAuthError,
    LogilessValidationError,
    LogilessRateLimitError,
    LogilessResourceLockedError,
    LogilessServerError,
    raise_for_error,
)


# ---------------------------------------------------------------------------
# 継承関係: 全例外が LogilessError のサブクラスであること
# ---------------------------------------------------------------------------
class TestInheritance:
    def test_all_errors_subclass_logiless_error(self):
        """全カスタム例外が LogilessError を継承していることを確認"""
        for cls in (
            LogilessAuthError,
            LogilessValidationError,
            LogilessRateLimitError,
            LogilessResourceLockedError,
            LogilessServerError,
        ):
            assert issubclass(cls, LogilessError)

    def test_logiless_error_is_exception(self):
        """基底 LogilessError が Exception を継承していることを確認"""
        assert issubclass(LogilessError, Exception)

    def test_instances_are_logiless_error(self):
        """各例外のインスタンスが LogilessError として捕捉できることを確認"""
        for cls in (
            LogilessAuthError,
            LogilessRateLimitError,
            LogilessResourceLockedError,
            LogilessServerError,
        ):
            assert isinstance(cls("msg"), LogilessError)
        assert isinstance(LogilessValidationError("msg"), LogilessError)


# ---------------------------------------------------------------------------
# LogilessError.__str__ の status_code 有無による分岐
# ---------------------------------------------------------------------------
class TestLogilessErrorStr:
    def test_str_with_status_code(self):
        """status_code がある場合は '<code> - <message>' 形式になる"""
        err = LogilessError("失敗しました", status_code=418)
        assert str(err) == "418 - 失敗しました"

    def test_str_without_status_code(self):
        """status_code がない場合はメッセージのみを返す"""
        err = LogilessError("失敗しました")
        assert str(err) == "失敗しました"

    def test_str_with_status_code_zero(self):
        """status_code が 0（falsy）の場合はメッセージのみを返す"""
        err = LogilessError("失敗しました", status_code=0)
        assert str(err) == "失敗しました"

    def test_attributes_stored(self):
        """message/status_code/response 属性が正しく保持される"""
        body = {"error": "x"}
        err = LogilessError("msg", status_code=500, response=body)
        assert err.message == "msg"
        assert err.status_code == 500
        assert err.response is body


# ---------------------------------------------------------------------------
# LogilessValidationError: message と validation_errors の保持と __str__
# ---------------------------------------------------------------------------
class TestValidationError:
    def test_holds_message_and_validation_errors(self):
        """message と validation_errors を正しく保持する"""
        ve = {"name": "必須です", "qty": "数値で入力してください"}
        err = LogilessValidationError("検証失敗", status_code=400, validation_errors=ve)
        assert err.message == "検証失敗"
        assert err.validation_errors == ve

    def test_validation_errors_defaults_to_empty_dict(self):
        """validation_errors 未指定時は空 dict になる"""
        err = LogilessValidationError("検証失敗")
        assert err.validation_errors == {}

    def test_validation_errors_none_becomes_empty_dict(self):
        """validation_errors に None を渡すと空 dict になる"""
        err = LogilessValidationError("検証失敗", validation_errors=None)
        assert err.validation_errors == {}

    def test_str_includes_validation_details(self):
        """__str__ にバリデーション詳細が含まれる"""
        err = LogilessValidationError(
            "検証失敗", status_code=400, validation_errors={"name": "必須です"}
        )
        s = str(err)
        assert "400 - 検証失敗" in s
        assert "バリデーションエラー:" in s
        assert "name: 必須です" in s

    def test_str_multiple_validation_details(self):
        """複数のバリデーション詳細がカンマ区切りで含まれる"""
        err = LogilessValidationError(
            "検証失敗",
            status_code=400,
            validation_errors={"a": "A詳細", "b": "B詳細"},
        )
        s = str(err)
        assert "a: A詳細" in s
        assert "b: B詳細" in s

    def test_str_without_validation_errors(self):
        """validation_errors が空なら基底クラスの __str__ と同じになる"""
        err = LogilessValidationError("検証失敗", status_code=400)
        assert str(err) == "400 - 検証失敗"
        assert "バリデーションエラー:" not in str(err)

    def test_str_without_status_code_with_validation(self):
        """status_code 無し + 詳細あり: メッセージとバリデーション詳細のみ"""
        err = LogilessValidationError(
            "検証失敗", validation_errors={"name": "必須です"}
        )
        s = str(err)
        assert s.startswith("検証失敗")
        assert "name: 必須です" in s


# ---------------------------------------------------------------------------
# raise_for_error: 全分岐が想定の例外型を送出すること
# ---------------------------------------------------------------------------
class TestRaiseForError:
    def test_400_raises_validation_error(self):
        """400 は LogilessValidationError を送出し message/errors を保持する"""
        body = {"message": "不正な入力", "errors": {"name": "必須です"}}
        with pytest.raises(LogilessValidationError) as exc_info:
            raise_for_error(400, body)
        err = exc_info.value
        assert err.status_code == 400
        assert err.message == "不正な入力"
        assert err.validation_errors == {"name": "必須です"}
        assert err.response is body

    def test_401_raises_auth_error(self):
        """401 は LogilessAuthError を送出する"""
        body = {"error": "invalid_token", "error_description": "トークン無効"}
        with pytest.raises(LogilessAuthError) as exc_info:
            raise_for_error(401, body)
        err = exc_info.value
        assert err.status_code == 401
        assert err.message == "invalid_token: トークン無効"

    def test_403_raises_auth_error(self):
        """403 も LogilessAuthError を送出する"""
        body = {"error": "forbidden", "error_description": "権限なし"}
        with pytest.raises(LogilessAuthError) as exc_info:
            raise_for_error(403, body)
        err = exc_info.value
        assert err.status_code == 403
        assert err.message == "forbidden: 権限なし"

    def test_423_raises_resource_locked_error(self):
        """423 は LogilessResourceLockedError を送出する"""
        body = {"error": "locked", "error_description": "ロック中"}
        with pytest.raises(LogilessResourceLockedError) as exc_info:
            raise_for_error(423, body)
        err = exc_info.value
        assert err.status_code == 423
        assert err.message == "locked: ロック中"

    def test_429_raises_rate_limit_error(self):
        """429 は LogilessRateLimitError を送出する"""
        body = {"error": "rate_limited", "error_description": "制限超過"}
        with pytest.raises(LogilessRateLimitError) as exc_info:
            raise_for_error(429, body)
        err = exc_info.value
        assert err.status_code == 429
        assert err.message == "rate_limited: 制限超過"

    def test_500_raises_server_error(self):
        """500 は LogilessServerError を送出する"""
        body = {"error": "server_error", "error_description": "内部エラー"}
        with pytest.raises(LogilessServerError) as exc_info:
            raise_for_error(500, body)
        err = exc_info.value
        assert err.status_code == 500
        assert err.message == "server_error: 内部エラー"

    def test_503_raises_server_error(self):
        """503（500以上）も LogilessServerError を送出する"""
        body = {"error": "unavailable", "error_description": "利用不可"}
        with pytest.raises(LogilessServerError) as exc_info:
            raise_for_error(503, body)
        err = exc_info.value
        assert err.status_code == 503
        assert err.message == "unavailable: 利用不可"

    def test_unknown_code_raises_base_error(self):
        """未知コード（418など）は基底 LogilessError を送出する"""
        body = {"error": "teapot", "error_description": "私はティーポット"}
        with pytest.raises(LogilessError) as exc_info:
            raise_for_error(418, body)
        err = exc_info.value
        # 具体的な派生クラスではなく基底クラスそのものであることを確認
        assert type(err) is LogilessError
        assert err.status_code == 418
        assert err.message == "teapot: 私はティーポット"

    def test_unknown_code_404(self):
        """404 も既知分岐に該当せず基底 LogilessError になる"""
        with pytest.raises(LogilessError) as exc_info:
            raise_for_error(404, {})
        assert type(exc_info.value) is LogilessError
        assert exc_info.value.status_code == 404


# ---------------------------------------------------------------------------
# body にキーが欠けている場合のデフォルトメッセージ挙動
# ---------------------------------------------------------------------------
class TestDefaultMessages:
    def test_400_default_message(self):
        """400 で message/errors 欠落時はデフォルト値を使う"""
        with pytest.raises(LogilessValidationError) as exc_info:
            raise_for_error(400, {})
        err = exc_info.value
        assert err.message == "バリデーションエラー"
        assert err.validation_errors == {}

    def test_401_default_message(self):
        """401 で error/error_description 欠落時はデフォルト値を使う"""
        with pytest.raises(LogilessAuthError) as exc_info:
            raise_for_error(401, {})
        assert exc_info.value.message == "認証エラー: 認証に失敗しました"

    def test_403_default_message(self):
        """403 デフォルトメッセージ"""
        with pytest.raises(LogilessAuthError) as exc_info:
            raise_for_error(403, {})
        assert exc_info.value.message == "アクセス拒否: リクエストへのアクセスが拒否されました"

    def test_423_default_message(self):
        """423 デフォルトメッセージ"""
        with pytest.raises(LogilessResourceLockedError) as exc_info:
            raise_for_error(423, {})
        assert exc_info.value.message == "リソースロック: リソースがロックされています"

    def test_429_default_message(self):
        """429 デフォルトメッセージ"""
        with pytest.raises(LogilessRateLimitError) as exc_info:
            raise_for_error(429, {})
        assert exc_info.value.message == "レート制限超過: APIのリクエストレート制限を超えました"

    def test_500_default_message(self):
        """500 デフォルトメッセージ"""
        with pytest.raises(LogilessServerError) as exc_info:
            raise_for_error(500, {})
        assert exc_info.value.message == "サーバーエラー: 内部サーバーエラーが発生しました"

    def test_unknown_code_default_message(self):
        """未知コードのデフォルトメッセージ"""
        with pytest.raises(LogilessError) as exc_info:
            raise_for_error(418, {})
        assert exc_info.value.message == "未知のエラー: エラーが発生しました"

    def test_400_partial_body_only_message(self):
        """400 で message のみ存在し errors 欠落時の挙動"""
        with pytest.raises(LogilessValidationError) as exc_info:
            raise_for_error(400, {"message": "カスタム"})
        err = exc_info.value
        assert err.message == "カスタム"
        assert err.validation_errors == {}
