"""
pylogiless - LOGILESS API クライアントライブラリ

ロジレス（LOGILESS）APIにPythonからアクセスするためのクライアントライブラリです。
アクセストークンとマーチャントIDによる認証に対応しています。
"""

__version__ = "0.4.0"

from .auth import LogilessAuth
from .client import (
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
from .errors import (
    LogilessError,
    LogilessAuthError,
    LogilessValidationError,
    LogilessRateLimitError,
    LogilessResourceLockedError,
    LogilessServerError,
)

__all__ = [
    "LogilessClient",
    "LogilessAuth",
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
    "LogilessError",
    "LogilessAuthError",
    "LogilessValidationError",
    "LogilessRateLimitError",
    "LogilessResourceLockedError",
    "LogilessServerError",
]
