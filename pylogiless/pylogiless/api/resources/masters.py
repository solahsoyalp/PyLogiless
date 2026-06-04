"""
マスタ（商品・倉庫・店舗・ロケーション・サプライヤー・商品マッピング）関連の
APIリソースクラスを提供するモジュール
"""
from typing import TYPE_CHECKING

from .base import APIResource

if TYPE_CHECKING:
    from ..client import LogilessClient


class ArticleResource(APIResource):
    """
    商品情報に関するリソースクラス
    """

    def __init__(self, client: "LogilessClient"):
        """
        ArticleResourceの初期化

        Args:
            client (LogilessClient): LogilessClientインスタンス
        """
        super().__init__(client, f"merchant/{client.auth.merchant_id}/articles")


class WarehouseResource(APIResource):
    """
    倉庫(Warehouse)リソースを扱うクラス
    """

    def __init__(self, client: "LogilessClient"):
        """
        WarehouseResourceクラスの初期化

        Args:
            client (LogilessClient): LogilessClientインスタンス
        """
        super().__init__(client, f"merchant/{client.auth.merchant_id}/warehouses")


class StoreResource(APIResource):
    """
    店舗(Store)リソースを扱うクラス
    """

    def __init__(self, client: "LogilessClient"):
        """
        StoreResourceクラスの初期化

        Args:
            client (LogilessClient): LogilessClientインスタンス
        """
        super().__init__(client, f"merchant/{client.auth.merchant_id}/stores")


class LocationResource(APIResource):
    """
    ロケーション情報に関するリソースクラス
    """

    def __init__(self, client: "LogilessClient"):
        """
        LocationResourceの初期化

        Args:
            client (LogilessClient): LogilessClientインスタンス
        """
        super().__init__(client, f"merchant/{client.auth.merchant_id}/locations")


class SupplierResource(APIResource):
    """
    サプライヤー情報に関するリソースクラス
    """

    def __init__(self, client: "LogilessClient"):
        """
        SupplierResourceの初期化

        Args:
            client (LogilessClient): LogilessClientインスタンス
        """
        super().__init__(client, f"merchant/{client.auth.merchant_id}/suppliers")


class ArticleMapResource(APIResource):
    """
    商品マッピングに関するリソースクラス
    """

    def __init__(self, client: "LogilessClient"):
        """
        ArticleMapResourceの初期化

        Args:
            client (LogilessClient): LogilessClientインスタンス
        """
        super().__init__(client, f"merchant/{client.auth.merchant_id}/article_maps")
