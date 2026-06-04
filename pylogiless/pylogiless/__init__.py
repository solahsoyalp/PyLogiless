"""
pylogiless - LOGILESS API クライアントライブラリ

ロジレス（LOGILESS）APIにPythonからアクセスするためのクライアントライブラリです。
アクセストークンとマーチャントIDによる認証に対応しています。
"""

from .api.auth import LogilessAuth
from .api.client import (
    LogilessClient,
    APIResource,
    ArticleResource,
    ActualInventorySummaryResource,
    LogicalInventorySummaryResource,
    OutboundDeliveryResource,
    InboundDeliveryResource,
    SalesOrderResource,
    WarehouseResource,
    StoreResource,
    LocationResource,
    ReorderPointResource,
    SupplierResource,
    ArticleMapResource,
    DailyInventorySummaryResource,
    TransactionLogResource,
    InterWarehouseTransferResource,
    SalesReturnResource,
)
from .api.errors import (
    LogilessError,
    LogilessAuthError,
    LogilessValidationError,
    LogilessRateLimitError,
    LogilessResourceLockedError,
    LogilessServerError,
)

__version__ = "0.3.0"

__all__ = [
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