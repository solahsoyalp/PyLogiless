"""
16リソースのURL生成およびCRUDメソッドのテスト

各リソースの _make_url() が
".../api/v1/merchant/<merchant_id>/<suffix>" の形になることを
pytest.mark.parametrize で16リソース全件網羅して検証する。
さらに get/list/create/update/delete が client.request を
正しい HTTP メソッド・URL・引数で1回だけ呼ぶことを検証する。
"""
from unittest import mock

import pytest

from pylogiless import LogilessClient


# ダミー認証情報。merchant_id="m" がURLに埋め込まれることを確認できる。
ACCESS_TOKEN = "t"
MERCHANT_ID = "m"
BASE_URL = "https://app2.logiless.com/api/v1"

# (リソース属性名, エンドポイント接尾辞) の16リソース対応表（FACTSに厳密準拠）
RESOURCE_SUFFIXES = [
    ("article", "articles"),
    ("actual_inventory_summary", "actual_inventory_summaries"),
    ("logical_inventory_summary", "logical_inventory_summaries"),
    ("outbound_delivery", "outbound_deliveries"),
    ("inbound_delivery", "inbound_deliveries"),
    ("sales_order", "sales_orders"),
    ("sales_return", "sales_returns"),
    ("warehouse", "warehouses"),
    ("store", "stores"),
    ("location", "locations"),
    ("reorder_point", "reorder_points"),
    ("supplier", "suppliers"),
    ("article_map", "article_maps"),
    ("daily_inventory_summary", "daily_inventory_summaries"),
    ("transaction_log", "transaction_logs"),
    ("inter_warehouse_transfer", "inter_warehouse_transfers"),
]


@pytest.fixture
def client():
    """ダミーのアクセストークン/マーチャントIDでクライアントを生成する。"""
    return LogilessClient(ACCESS_TOKEN, MERCHANT_ID)


class TestResourceMakeUrl:
    """各リソースの _make_url() が期待のフルURLになることを検証する。"""

    @pytest.mark.parametrize("attr_name,suffix", RESOURCE_SUFFIXES)
    def test_make_url_base(self, client, attr_name, suffix):
        """path無しの _make_url() が merchant 配下のベースURLになること。"""
        resource = getattr(client, attr_name)
        expected = f"{BASE_URL}/merchant/{MERCHANT_ID}/{suffix}"
        assert resource._make_url() == expected

    @pytest.mark.parametrize("attr_name,suffix", RESOURCE_SUFFIXES)
    def test_make_url_with_id(self, client, attr_name, suffix):
        """path付きの _make_url() が末尾にIDを連結したURLになること。"""
        resource = getattr(client, attr_name)
        expected = f"{BASE_URL}/merchant/{MERCHANT_ID}/{suffix}/123"
        assert resource._make_url("123") == expected

    @pytest.mark.parametrize("attr_name,suffix", RESOURCE_SUFFIXES)
    def test_resource_path(self, client, attr_name, suffix):
        """resource_path が merchant/<mid>/<suffix> 形式であること。"""
        resource = getattr(client, attr_name)
        assert resource.resource_path == f"merchant/{MERCHANT_ID}/{suffix}"


class TestResourceCrudMethods:
    """代表リソース article で各CRUDメソッドの request 呼び出しを検証する。"""

    def test_get_calls_request(self, client):
        """get() が GET と ID付きURL・params で request を1回呼ぶこと。"""
        with mock.patch.object(client, "request") as m:
            m.return_value = {"ok": True}
            result = client.article.get("42", status="active")
            m.assert_called_once_with(
                "GET",
                f"{BASE_URL}/merchant/{MERCHANT_ID}/articles/42",
                params={"status": "active"},
            )
            assert result == {"ok": True}

    def test_get_without_params(self, client):
        """get() を追加paramsなしで呼ぶと params={} で request されること。"""
        with mock.patch.object(client, "request") as m:
            client.article.get("42")
            m.assert_called_once_with(
                "GET",
                f"{BASE_URL}/merchant/{MERCHANT_ID}/articles/42",
                params={},
            )

    def test_list_calls_request(self, client):
        """list() が GET とベースURL・params で request を1回呼ぶこと。"""
        with mock.patch.object(client, "request") as m:
            client.article.list(limit=10, page=2)
            m.assert_called_once_with(
                "GET",
                f"{BASE_URL}/merchant/{MERCHANT_ID}/articles",
                params={"limit": 10, "page": 2},
            )

    def test_create_calls_request(self, client):
        """create() が POST とベースURL・json で request を1回呼ぶこと。"""
        data = {"code": "ABC", "name": "テスト商品"}
        with mock.patch.object(client, "request") as m:
            client.article.create(data)
            m.assert_called_once_with(
                "POST",
                f"{BASE_URL}/merchant/{MERCHANT_ID}/articles",
                json=data,
            )

    def test_update_calls_request(self, client):
        """update() が PUT とID付きURL・json で request を1回呼ぶこと。"""
        data = {"name": "更新後"}
        with mock.patch.object(client, "request") as m:
            client.article.update("42", data)
            m.assert_called_once_with(
                "PUT",
                f"{BASE_URL}/merchant/{MERCHANT_ID}/articles/42",
                json=data,
            )

    def test_delete_calls_request(self, client):
        """delete() が DELETE とID付きURLで request を1回呼ぶこと。"""
        with mock.patch.object(client, "request") as m:
            client.article.delete("42")
            m.assert_called_once_with(
                "DELETE",
                f"{BASE_URL}/merchant/{MERCHANT_ID}/articles/42",
            )


class TestAllResourcesCrudUrls:
    """16リソース全件で各CRUDメソッドが正しいURL・メソッドで request を呼ぶこと。"""

    @pytest.mark.parametrize("attr_name,suffix", RESOURCE_SUFFIXES)
    def test_get_all(self, client, attr_name, suffix):
        """全リソースの get() が GET と ID付きURL で request を呼ぶこと。"""
        resource = getattr(client, attr_name)
        with mock.patch.object(client, "request") as m:
            resource.get("7")
            m.assert_called_once_with(
                "GET",
                f"{BASE_URL}/merchant/{MERCHANT_ID}/{suffix}/7",
                params={},
            )

    @pytest.mark.parametrize("attr_name,suffix", RESOURCE_SUFFIXES)
    def test_list_all(self, client, attr_name, suffix):
        """全リソースの list() が GET とベースURL で request を呼ぶこと。"""
        resource = getattr(client, attr_name)
        with mock.patch.object(client, "request") as m:
            resource.list()
            m.assert_called_once_with(
                "GET",
                f"{BASE_URL}/merchant/{MERCHANT_ID}/{suffix}",
                params={},
            )

    @pytest.mark.parametrize("attr_name,suffix", RESOURCE_SUFFIXES)
    def test_create_all(self, client, attr_name, suffix):
        """全リソースの create() が POST とベースURL・json で request を呼ぶこと。"""
        resource = getattr(client, attr_name)
        data = {"k": "v"}
        with mock.patch.object(client, "request") as m:
            resource.create(data)
            m.assert_called_once_with(
                "POST",
                f"{BASE_URL}/merchant/{MERCHANT_ID}/{suffix}",
                json=data,
            )

    @pytest.mark.parametrize("attr_name,suffix", RESOURCE_SUFFIXES)
    def test_update_all(self, client, attr_name, suffix):
        """全リソースの update() が PUT とID付きURL・json で request を呼ぶこと。"""
        resource = getattr(client, attr_name)
        data = {"k": "v"}
        with mock.patch.object(client, "request") as m:
            resource.update("7", data)
            m.assert_called_once_with(
                "PUT",
                f"{BASE_URL}/merchant/{MERCHANT_ID}/{suffix}/7",
                json=data,
            )

    @pytest.mark.parametrize("attr_name,suffix", RESOURCE_SUFFIXES)
    def test_delete_all(self, client, attr_name, suffix):
        """全リソースの delete() が DELETE とID付きURL で request を呼ぶこと。"""
        resource = getattr(client, attr_name)
        with mock.patch.object(client, "request") as m:
            resource.delete("7")
            m.assert_called_once_with(
                "DELETE",
                f"{BASE_URL}/merchant/{MERCHANT_ID}/{suffix}/7",
            )
