"""
APIリソースパッケージ

APIResource 基底クラスと16個の *Resource クラスを
論理グループ（masters / documents / inventory）から集約して公開します。
"""
from .base import APIResource
from .documents import (
    InboundDeliveryResource,
    OutboundDeliveryResource,
    SalesOrderResource,
    SalesReturnResource,
)
from .inventory import (
    ActualInventorySummaryResource,
    DailyInventorySummaryResource,
    InterWarehouseTransferResource,
    LogicalInventorySummaryResource,
    ReorderPointResource,
    TransactionLogResource,
)
from .masters import (
    ArticleMapResource,
    ArticleResource,
    LocationResource,
    StoreResource,
    SupplierResource,
    WarehouseResource,
)

__all__ = [
    "APIResource",
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
