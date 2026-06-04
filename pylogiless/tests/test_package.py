"""
パッケージレベルのテスト

pylogiless パッケージの公開API・バージョン・__all__・リソースクラスの
継承関係・LogilessClient のリソース属性などを検証する。
ネットワークアクセスは行わない（リソース生成のみを確認する）。
"""
import inspect

import pytest

import pylogiless
from pylogiless import LogilessClient, LogilessAuth
from pylogiless.api.client import APIResource


# __all__ に列挙されている全シンボル
ALL_SYMBOLS = [
    "LogilessClient",
    "LogilessAuth",
    "LogilessError",
    "LogilessAuthError",
    "LogilessValidationError",
    "LogilessRateLimitError",
    "LogilessResourceLockedError",
    "LogilessServerError",
    "APIResource",
    "ArticleResource",
    "ActualInventorySummaryResource",
    "LogicalInventorySummaryResource",
    "OutboundDeliveryResource",
    "InboundDeliveryResource",
    "SalesOrderResource",
    "WarehouseResource",
    "StoreResource",
    "LocationResource",
    "ReorderPointResource",
    "SupplierResource",
    "ArticleMapResource",
    "DailyInventorySummaryResource",
    "TransactionLogResource",
    "InterWarehouseTransferResource",
    "SalesReturnResource",
]

# 16個のリソースクラス名
RESOURCE_CLASS_NAMES = [
    "ArticleResource",
    "ActualInventorySummaryResource",
    "LogicalInventorySummaryResource",
    "OutboundDeliveryResource",
    "InboundDeliveryResource",
    "SalesOrderResource",
    "SalesReturnResource",
    "WarehouseResource",
    "StoreResource",
    "LocationResource",
    "ReorderPointResource",
    "SupplierResource",
    "ArticleMapResource",
    "DailyInventorySummaryResource",
    "TransactionLogResource",
    "InterWarehouseTransferResource",
]

# LogilessClient が保持する16個のリソース属性とそのクラス名のマッピング
RESOURCE_ATTRIBUTES = {
    "article": "ArticleResource",
    "actual_inventory_summary": "ActualInventorySummaryResource",
    "logical_inventory_summary": "LogicalInventorySummaryResource",
    "outbound_delivery": "OutboundDeliveryResource",
    "inbound_delivery": "InboundDeliveryResource",
    "sales_order": "SalesOrderResource",
    "sales_return": "SalesReturnResource",
    "warehouse": "WarehouseResource",
    "store": "StoreResource",
    "location": "LocationResource",
    "reorder_point": "ReorderPointResource",
    "supplier": "SupplierResource",
    "article_map": "ArticleMapResource",
    "daily_inventory_summary": "DailyInventorySummaryResource",
    "transaction_log": "TransactionLogResource",
    "inter_warehouse_transfer": "InterWarehouseTransferResource",
}


def _make_client(api_base_url=None):
    """テスト用に静的トークン方式の LogilessClient を生成するヘルパー"""
    return LogilessClient(
        access_token="test_access_token",
        merchant_id="test_merchant_id",
        api_base_url=api_base_url,
    )


class TestPackageMetadata:
    """パッケージのメタデータ（バージョン・__all__）を検証する"""

    def test_version_value(self):
        """__version__ が文字列 "0.3.0" であること"""
        assert isinstance(pylogiless.__version__, str)
        assert pylogiless.__version__ == "0.3.0"

    def test_all_is_list(self):
        """__all__ が定義され、期待するシンボル集合と一致すること"""
        assert hasattr(pylogiless, "__all__")
        assert set(pylogiless.__all__) == set(ALL_SYMBOLS)

    @pytest.mark.parametrize("symbol", ALL_SYMBOLS)
    def test_all_symbols_importable(self, symbol):
        """__all__ に列挙された全シンボルが実際に import 可能であること"""
        assert hasattr(pylogiless, symbol), f"{symbol} がパッケージに存在しません"
        assert getattr(pylogiless, symbol) is not None


class TestResourceClasses:
    """16個のリソースクラスが APIResource を継承していることを検証する"""

    @pytest.mark.parametrize("class_name", RESOURCE_CLASS_NAMES)
    def test_is_apiresource_subclass(self, class_name):
        """各リソースクラスが APIResource のサブクラスであること"""
        cls = getattr(pylogiless, class_name)
        assert inspect.isclass(cls)
        assert issubclass(cls, APIResource)

    def test_resource_class_count(self):
        """リソースクラスがちょうど16個であること"""
        assert len(RESOURCE_CLASS_NAMES) == 16

    def test_apiresource_itself_not_counted(self):
        """APIResource 基底クラスはサブクラス集合に含めていないこと（自己参照の確認）"""
        assert "APIResource" not in RESOURCE_CLASS_NAMES


class TestClientResourceAttributes:
    """LogilessClient が16個のリソース属性を保持することを検証する"""

    def setup_method(self):
        """各テスト前に静的トークン方式のクライアントを生成する"""
        self.client = _make_client()

    def test_attribute_count(self):
        """検証対象のリソース属性がちょうど16個であること"""
        assert len(RESOURCE_ATTRIBUTES) == 16

    @pytest.mark.parametrize("attr_name", list(RESOURCE_ATTRIBUTES.keys()))
    def test_has_resource_attribute(self, attr_name):
        """各リソース属性が存在し None でないこと"""
        assert hasattr(self.client, attr_name)
        assert getattr(self.client, attr_name) is not None

    @pytest.mark.parametrize(
        "attr_name,class_name", list(RESOURCE_ATTRIBUTES.items())
    )
    def test_resource_attribute_type(self, attr_name, class_name):
        """各リソース属性が対応するリソースクラスのインスタンスであること"""
        expected_cls = getattr(pylogiless, class_name)
        resource = getattr(self.client, attr_name)
        assert isinstance(resource, expected_cls)
        assert isinstance(resource, APIResource)

    @pytest.mark.parametrize("attr_name", list(RESOURCE_ATTRIBUTES.keys()))
    def test_resource_back_reference(self, attr_name):
        """各リソースが生成元クライアントを client 属性として保持すること"""
        resource = getattr(self.client, attr_name)
        assert resource.client is self.client

    def test_resource_path_contains_merchant_id(self):
        """リソースパスが merchant/<merchant_id>/ 形式であること"""
        for attr_name in RESOURCE_ATTRIBUTES:
            resource = getattr(self.client, attr_name)
            assert resource.resource_path.startswith("merchant/test_merchant_id/")


class TestClientBaseUrl:
    """api_base_url のデフォルト/カスタム指定の挙動を検証する"""

    def test_default_base_url(self):
        """api_base_url 未指定時はクラス既定値が使われること"""
        client = _make_client()
        assert client.api_base_url == LogilessClient.API_BASE_URL
        assert client.api_base_url == "https://app2.logiless.com/api/v1"

    def test_custom_base_url(self):
        """api_base_url を指定すると上書きされること"""
        custom = "https://example.test/api/v1"
        client = _make_client(api_base_url=custom)
        assert client.api_base_url == custom

    def test_resource_url_uses_base_url(self):
        """リソースが生成するURLが api_base_url を基点とすること"""
        custom = "https://example.test/api/v1"
        client = _make_client(api_base_url=custom)
        url = client.article._make_url()
        assert url == f"{custom}/merchant/test_merchant_id/articles"


class TestOAuth2KeywordArguments:
    """LogilessAuth / LogilessClient が OAuth2 キーワード引数を受け付けることを検証する"""

    def test_auth_accepts_oauth2_kwargs(self):
        """LogilessAuth が OAuth2 用キーワード引数を受け付け保持すること"""
        auth = LogilessAuth(
            client_id="cid",
            client_secret="secret",
            redirect_uri="https://cb.test/callback",
            refresh_token="rtok",
        )
        assert auth.client_id == "cid"
        assert auth.client_secret == "secret"
        assert auth.redirect_uri == "https://cb.test/callback"
        assert auth.refresh_token == "rtok"

    def test_client_accepts_oauth2_kwargs(self):
        """LogilessClient が OAuth2 用キーワード引数を auth へ受け渡すこと"""
        client = LogilessClient(
            client_id="cid",
            client_secret="secret",
            redirect_uri="https://cb.test/callback",
            refresh_token="rtok",
        )
        assert client.auth.client_id == "cid"
        assert client.auth.client_secret == "secret"
        assert client.auth.redirect_uri == "https://cb.test/callback"
        assert client.auth.refresh_token == "rtok"

    def test_client_oauth2_resources_initialized(self):
        """OAuth2方式で生成したクライアントでも16リソースが初期化されること"""
        client = LogilessClient(
            client_id="cid",
            client_secret="secret",
            redirect_uri="https://cb.test/callback",
            refresh_token="rtok",
        )
        for attr_name in RESOURCE_ATTRIBUTES:
            assert getattr(client, attr_name) is not None
