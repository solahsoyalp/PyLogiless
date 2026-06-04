"""
在庫関連のAPIリソースクラスを提供するモジュール
"""
from typing import TYPE_CHECKING

from .base import APIResource

if TYPE_CHECKING:
    from ..client import LogilessClient


class ActualInventorySummaryResource(APIResource):
    """
    実在庫サマリ(ActualInventorySummary)リソースを扱うクラス
    """

    def __init__(self, client: "LogilessClient"):
        """
        ActualInventorySummaryResourceクラスの初期化

        Args:
            client (LogilessClient): LogilessClientインスタンス
        """
        super().__init__(client, f"merchant/{client.auth.merchant_id}/actual_inventory_summaries")


class LogicalInventorySummaryResource(APIResource):
    """
    論理在庫サマリ(LogicalInventorySummary)リソースを扱うクラス
    """

    def __init__(self, client: "LogilessClient"):
        """
        LogicalInventorySummaryResourceクラスの初期化

        Args:
            client (LogilessClient): LogilessClientインスタンス
        """
        super().__init__(client, f"merchant/{client.auth.merchant_id}/logical_inventory_summaries")


class ReorderPointResource(APIResource):
    """
    再注文点に関するリソースクラス
    """

    def __init__(self, client: "LogilessClient"):
        """
        ReorderPointResourceの初期化

        Args:
            client (LogilessClient): LogilessClientインスタンス
        """
        super().__init__(client, f"merchant/{client.auth.merchant_id}/reorder_points")


class DailyInventorySummaryResource(APIResource):
    """
    日次在庫サマリに関するリソースクラス
    """

    def __init__(self, client: "LogilessClient"):
        """
        DailyInventorySummaryResourceの初期化

        Args:
            client (LogilessClient): LogilessClientインスタンス
        """
        super().__init__(client, f"merchant/{client.auth.merchant_id}/daily_inventory_summaries")


class TransactionLogResource(APIResource):
    """
    取引ログに関するリソースクラス
    """

    def __init__(self, client: "LogilessClient"):
        """
        TransactionLogResourceの初期化

        Args:
            client (LogilessClient): LogilessClientインスタンス
        """
        super().__init__(client, f"merchant/{client.auth.merchant_id}/transaction_logs")


class InterWarehouseTransferResource(APIResource):
    """
    倉庫間移動に関するリソースクラス
    """

    def __init__(self, client: "LogilessClient"):
        """
        InterWarehouseTransferResourceの初期化

        Args:
            client (LogilessClient): LogilessClientインスタンス
        """
        super().__init__(client, f"merchant/{client.auth.merchant_id}/inter_warehouse_transfers")
