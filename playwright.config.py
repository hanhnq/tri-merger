"""Playwright configuration for E2E tests"""

import os
from playwright.sync_api import Playwright


# テスト設定
class Config:
    # Streamlitアプリケーションの設定
    APP_URL = os.getenv("APP_URL", "http://localhost:8501")
    
    # ブラウザ設定
    BROWSER = os.getenv("BROWSER", "chromium")  # chromium, firefox, webkit
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    SLOW_MO = int(os.getenv("SLOW_MO", "0"))  # ミリ秒単位での遅延
    
    # タイムアウト設定
    DEFAULT_TIMEOUT = 30000  # 30秒
    NAVIGATION_TIMEOUT = 60000  # 60秒
    
    # スクリーンショット設定
    SCREENSHOT_ON_FAILURE = True
    SCREENSHOT_DIR = "tests/screenshots"
    
    # ビューポート設定
    VIEWPORT_WIDTH = 1280
    VIEWPORT_HEIGHT = 720


def pytest_configure(config):
    """pytest設定のカスタマイズ"""
    os.makedirs(Config.SCREENSHOT_DIR, exist_ok=True)