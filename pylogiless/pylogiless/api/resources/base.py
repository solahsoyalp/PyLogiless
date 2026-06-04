"""
APIリソースの基底クラスを提供するモジュール
"""
from typing import TYPE_CHECKING, Any, Dict, Optional

if TYPE_CHECKING:
    from ..client import LogilessClient


class APIResource:
    """
    APIリソースの基底クラス
    個別のAPIエンドポイントに対応するリソースクラスの基底となるクラスです。
    """

    def __init__(self, client: "LogilessClient", resource_path: str):
        """
        APIResourceクラスの初期化

        Args:
            client (LogilessClient): LogilessClientインスタンス
            resource_path (str): APIリソースのパス
        """
        self.client = client
        self.resource_path = resource_path

    def _make_url(self, path: Optional[str] = None) -> str:
        """
        APIリソースのURLを生成する

        Args:
            path (Optional[str], optional): 追加のパス

        Returns:
            str: 完全なAPIエンドポイントURL
        """
        url = f"{self.client.api_base_url}/{self.resource_path}"
        if path:
            url = f"{url}/{path}"
        return url

    def get(self, resource_id: str, **params) -> Dict[str, Any]:
        """
        リソースを取得する

        Args:
            resource_id (str): 取得するリソースのID
            **params: 追加のクエリパラメータ

        Returns:
            Dict[str, Any]: APIレスポンス
        """
        return self.client.request("GET", self._make_url(resource_id), params=params)

    def list(self, **params) -> Dict[str, Any]:
        """
        リソースのリストを取得する

        Args:
            **params: クエリパラメータ

        Returns:
            Dict[str, Any]: APIレスポンス
        """
        return self.client.request("GET", self._make_url(), params=params)

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        リソースを作成する

        Args:
            data (Dict[str, Any]): 作成するリソースのデータ

        Returns:
            Dict[str, Any]: APIレスポンス
        """
        return self.client.request("POST", self._make_url(), json=data)

    def update(self, resource_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        リソースを更新する

        Args:
            resource_id (str): 更新するリソースのID
            data (Dict[str, Any]): 更新データ

        Returns:
            Dict[str, Any]: APIレスポンス
        """
        return self.client.request("PUT", self._make_url(resource_id), json=data)

    def delete(self, resource_id: str) -> Dict[str, Any]:
        """
        リソースを削除する

        Args:
            resource_id (str): 削除するリソースのID

        Returns:
            Dict[str, Any]: APIレスポンス
        """
        return self.client.request("DELETE", self._make_url(resource_id))
