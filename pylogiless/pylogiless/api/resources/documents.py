"""
伝票（配送・受注・返品）関連のAPIリソースクラスを提供するモジュール
"""
from typing import TYPE_CHECKING

from .base import APIResource

if TYPE_CHECKING:
    from ..client import LogilessClient


class OutboundDeliveryResource(APIResource):
    """
    出荷配送(OutboundDelivery)リソースを扱うクラス
    """

    def __init__(self, client: "LogilessClient"):
        """
        OutboundDeliveryResourceクラスの初期化

        Args:
            client (LogilessClient): LogilessClientインスタンス
        """
        super().__init__(client, f"merchant/{client.auth.merchant_id}/outbound_deliveries")


class InboundDeliveryResource(APIResource):
    """
    入荷配送(InboundDelivery)リソースを扱うクラス
    """

    def __init__(self, client: "LogilessClient"):
        """
        InboundDeliveryResourceクラスの初期化

        Args:
            client (LogilessClient): LogilessClientインスタンス
        """
        super().__init__(client, f"merchant/{client.auth.merchant_id}/inbound_deliveries")


class SalesOrderResource(APIResource):
    """
    受注(SalesOrder)リソースを扱うクラス
    """

    def __init__(self, client: "LogilessClient"):
        """
        SalesOrderResourceクラスの初期化

        Args:
            client (LogilessClient): LogilessClientインスタンス
        """
        super().__init__(client, f"merchant/{client.auth.merchant_id}/sales_orders")


class SalesReturnResource(APIResource):
    """
    受注返品(SalesReturn)リソースを扱うクラス
    """

    def __init__(self, client: "LogilessClient"):
        """
        SalesReturnResourceクラスの初期化

        Args:
            client (LogilessClient): LogilessClientインスタンス
        """
        super().__init__(client, f"merchant/{client.auth.merchant_id}/sales_returns")
