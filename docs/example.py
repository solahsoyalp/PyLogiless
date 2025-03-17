#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
LOGILESS API Python クライアントライブラリのサンプルコード

このスクリプトは、pylogilessライブラリを使用してLOGILESS APIにアクセスする
基本的な使用例を示しています。
"""

import os
import sys
import time
from datetime import datetime, timedelta

# pylogilessライブラリをインポート
from pylogiless import LogilessClient, LogilessError, LogilessAuthError

# 環境変数から認証情報を取得するか、直接指定します
CLIENT_ID = os.environ.get("LOGILESS_CLIENT_ID", "YOUR_CLIENT_ID")
CLIENT_SECRET = os.environ.get("LOGILESS_CLIENT_SECRET", "YOUR_CLIENT_SECRET")
REDIRECT_URI = os.environ.get("LOGILESS_REDIRECT_URI", "YOUR_REDIRECT_URI")

# アクセストークンとリフレッシュトークンの保存先
TOKEN_FILE = "tokens.json"


def save_tokens(access_token, refresh_token):
    """トークンをJSONファイルに保存する関数"""
    import json
    
    with open(TOKEN_FILE, "w") as f:
        json.dump({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "updated_at": datetime.now().isoformat()
        }, f)


def load_tokens():
    """保存されたトークンを読み込む関数"""
    import json
    import os
    
    if not os.path.exists(TOKEN_FILE):
        return None, None
    
    try:
        with open(TOKEN_FILE, "r") as f:
            data = json.load(f)
            return data.get("access_token"), data.get("refresh_token")
    except Exception as e:
        print(f"トークンの読み込みエラー: {e}")
        return None, None


def authenticate():
    """認証プロセスを実行する関数"""
    global client
    
    # 保存されたトークンを読み込む
    access_token, refresh_token = load_tokens()
    
    if access_token and refresh_token:
        print("保存されたトークンを使用します。")
        client.set_token(access_token=access_token, refresh_token=refresh_token)
        
        # トークンの有効性を確認
        try:
            # APIリクエストを試行
            client.actual_inventory_summary.list(limit=1)
            print("保存されたトークンは有効です。")
            return True
        except LogilessAuthError as e:
            print(f"保存されたトークンは無効です: {e}")
            # トークンが無効な場合は再認証
    
    # 認証URLを取得
    auth_url = client.get_authorization_url()
    print(f"\n次のURLにアクセスして認証してください:\n{auth_url}\n")
    
    # ユーザーからの認可コードの入力を待機
    auth_code = input("認証後のリダイレクトURLから認可コードを入力してください: ")
    
    try:
        # トークンを取得
        tokens = client.fetch_token(auth_code)
        print("認証成功！")
        
        # トークンを保存
        save_tokens(tokens["access_token"], tokens["refresh_token"])
        return True
    except LogilessAuthError as e:
        print(f"認証エラー: {e}")
        return False


def display_menu():
    """メインメニューを表示する関数"""
    print("\n===== LOGILESS API サンプルメニュー =====")
    print("1. 在庫情報を取得")
    print("2. 商品一覧を取得")
    print("3. 出荷配送情報を取得")
    print("4. 入荷配送情報を取得")
    print("5. 倉庫情報を取得")
    print("0. 終了")
    print("======================================")
    choice = input("選択してください (0-5): ")
    return choice


def get_inventory_summary():
    """在庫情報を取得する関数"""
    try:
        # リクエストパラメータの設定
        params = {
            "limit": 10,  # 取得件数
        }
        
        # フィルタが必要な場合
        warehouse_code = input("倉庫コードでフィルタする場合は入力してください (スキップする場合は空欄): ")
        if warehouse_code:
            params["warehouse_code"] = warehouse_code
        
        article_code = input("商品コードでフィルタする場合は入力してください (スキップする場合は空欄): ")
        if article_code:
            params["article_code"] = article_code
        
        # 在庫情報を取得
        inventory = client.actual_inventory_summary.list(**params)
        
        # 結果を表示
        print("\n=== 在庫情報 ===")
        for item in inventory.get("items", []):
            print(f"商品コード: {item.get('article_code')}")
            print(f"商品名: {item.get('article_name')}")
            print(f"倉庫コード: {item.get('warehouse_code')}")
            print(f"在庫数量: {item.get('stock_quantity')}")
            print(f"予約在庫数量: {item.get('allocated_quantity')}")
            print("---------------")
        
        print(f"全{inventory.get('total_count')}件中{len(inventory.get('items', []))}件を表示")
    
    except LogilessError as e:
        print(f"在庫情報の取得中にエラーが発生しました: {e}")


def get_articles():
    """商品一覧を取得する関数"""
    try:
        # リクエストパラメータの設定
        params = {
            "limit": 10,  # 取得件数
        }
        
        # 商品一覧を取得
        articles = client.article.list(**params)
        
        # 結果を表示
        print("\n=== 商品一覧 ===")
        for article in articles.get("items", []):
            print(f"商品コード: {article.get('article_code')}")
            print(f"商品名: {article.get('article_name')}")
            print(f"商品タイプ: {article.get('article_type')}")
            print(f"単位: {article.get('unit_of_measure')}")
            print(f"税率: {article.get('tax_rate')}%")
            print("---------------")
        
        print(f"全{articles.get('total_count')}件中{len(articles.get('items', []))}件を表示")
        
        # 特定の商品の詳細を表示
        article_code = input("\n詳細を表示する商品コードを入力してください (スキップする場合は空欄): ")
        if article_code:
            try:
                article_detail = client.article.get(article_code)
                print("\n=== 商品詳細 ===")
                for key, value in article_detail.items():
                    print(f"{key}: {value}")
            except LogilessError as e:
                print(f"商品詳細の取得中にエラーが発生しました: {e}")
    
    except LogilessError as e:
        print(f"商品一覧の取得中にエラーが発生しました: {e}")


def get_outbound_deliveries():
    """出荷配送情報を取得する関数"""
    try:
        # 日付範囲の設定
        today = datetime.now().strftime("%Y-%m-%d")
        one_month_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        
        # リクエストパラメータの設定
        params = {
            "limit": 10,
            "date_from": one_month_ago,
            "date_to": today
        }
        
        # 出荷配送情報を取得
        deliveries = client.outbound_delivery.list(**params)
        
        # 結果を表示
        print("\n=== 出荷配送情報 ===")
        for delivery in deliveries.get("items", []):
            print(f"配送番号: {delivery.get('id')}")
            print(f"参照番号: {delivery.get('reference_id')}")
            print(f"店舗コード: {delivery.get('store_code')}")
            print(f"倉庫コード: {delivery.get('warehouse_code')}")
            print(f"配送予定日: {delivery.get('scheduled_delivery_date')}")
            print(f"ステータス: {delivery.get('document_status')}")
            print(f"配送方法: {delivery.get('delivery_method')}")
            print("---------------")
        
        print(f"全{deliveries.get('total_count')}件中{len(deliveries.get('items', []))}件を表示")
    
    except LogilessError as e:
        print(f"出荷配送情報の取得中にエラーが発生しました: {e}")


def get_inbound_deliveries():
    """入荷配送情報を取得する関数"""
    try:
        # 日付範囲の設定
        today = datetime.now().strftime("%Y-%m-%d")
        one_month_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        
        # リクエストパラメータの設定
        params = {
            "limit": 10,
            "date_from": one_month_ago,
            "date_to": today
        }
        
        # 入荷配送情報を取得
        deliveries = client.inbound_delivery.list(**params)
        
        # 結果を表示
        print("\n=== 入荷配送情報 ===")
        for delivery in deliveries.get("items", []):
            print(f"配送番号: {delivery.get('id')}")
            print(f"参照番号: {delivery.get('reference_id')}")
            print(f"サプライヤーコード: {delivery.get('supplier_code')}")
            print(f"倉庫コード: {delivery.get('warehouse_code')}")
            print(f"配送予定日: {delivery.get('scheduled_delivery_date')}")
            print(f"ステータス: {delivery.get('document_status')}")
            print(f"カテゴリ: {delivery.get('inbound_delivery_category')}")
            print("---------------")
        
        print(f"全{deliveries.get('total_count')}件中{len(deliveries.get('items', []))}件を表示")
    
    except LogilessError as e:
        print(f"入荷配送情報の取得中にエラーが発生しました: {e}")


def get_warehouses():
    """倉庫情報を取得する関数"""
    try:
        # 倉庫一覧を取得
        warehouses = client.warehouse.list()
        
        # 結果を表示
        print("\n=== 倉庫一覧 ===")
        for warehouse in warehouses.get("items", []):
            print(f"倉庫コード: {warehouse.get('warehouse_code')}")
            print(f"倉庫名: {warehouse.get('warehouse_name')}")
            print(f"住所: {warehouse.get('address')}")
            print(f"電話番号: {warehouse.get('phone_number')}")
            print("---------------")
        
        print(f"全{warehouses.get('total_count')}件中{len(warehouses.get('items', []))}件を表示")
        
        # 特定の倉庫のロケーション情報を表示
        warehouse_code = input("\nロケーション情報を表示する倉庫コードを入力してください (スキップする場合は空欄): ")
        if warehouse_code:
            try:
                locations = client.location.list(warehouse_code=warehouse_code, limit=10)
                print(f"\n=== 倉庫 {warehouse_code} のロケーション情報 ===")
                for location in locations.get("items", []):
                    print(f"ロケーションコード: {location.get('location_code')}")
                    print(f"ロケーション名: {location.get('location_name')}")
                    print(f"ロケーションタイプ: {location.get('location_type')}")
                    print("---------------")
                
                print(f"全{locations.get('total_count')}件中{len(locations.get('items', []))}件を表示")
            except LogilessError as e:
                print(f"ロケーション情報の取得中にエラーが発生しました: {e}")
    
    except LogilessError as e:
        print(f"倉庫情報の取得中にエラーが発生しました: {e}")


if __name__ == "__main__":
    # クライアントの初期化
    client = LogilessClient(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI
    )
    
    # 認証
    if not authenticate():
        print("認証に失敗しました。終了します。")
        sys.exit(1)
    
    # メインループ
    while True:
        choice = display_menu()
        
        if choice == "0":
            print("プログラムを終了します。")
            break
        elif choice == "1":
            get_inventory_summary()
        elif choice == "2":
            get_articles()
        elif choice == "3":
            get_outbound_deliveries()
        elif choice == "4":
            get_inbound_deliveries()
        elif choice == "5":
            get_warehouses()
        else:
            print("無効な選択です。0から5の数字を入力してください。")
        
        # 処理間の待機時間
        time.sleep(1) 