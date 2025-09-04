"""pytest configuration and fixtures"""

import pytest
import os
import subprocess
import time
from pathlib import Path


@pytest.fixture(scope="session")
def streamlit_app():
    """Streamlitアプリケーションを起動するフィクスチャ"""
    # Streamlitプロセスを起動
    process = subprocess.Popen(
        ["streamlit", "run", "app.py", "--server.port=8501", "--server.headless=true"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # アプリケーションの起動を待つ
    time.sleep(5)
    
    yield process
    
    # テスト終了後にプロセスを終了
    process.terminate()
    process.wait()


@pytest.fixture(scope="session")
def browser_context_args():
    """ブラウザコンテキストの設定"""
    return {
        "viewport": {"width": 1280, "height": 720},
        "ignore_https_errors": True,
    }


@pytest.fixture(scope="function")
def authenticated_page(page):
    """認証済みのページを提供するフィクスチャ（E2Eテスト用）"""
    from playwright.sync_api import Page
    # アプリケーションにアクセス
    page.goto("http://localhost:8501")
    
    # ログイン処理
    page.fill('input[type="password"]', 'tri-merger-2024')
    page.click('button:has-text("ログイン")')
    
    # ログイン完了を待つ
    page.wait_for_selector('h1:has-text("アンケート集計システム")', timeout=10000)
    
    return page


@pytest.fixture(autouse=True)
def screenshot_on_failure(request):
    """テスト失敗時にスクリーンショットを保存（E2Eテスト用）"""
    yield
    
    # E2Eテストの場合のみ実行
    if hasattr(request, 'node') and hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        if 'page' in request.fixturenames:
            page = request.getfixturevalue('page')
            # スクリーンショットディレクトリを作成
            screenshot_dir = Path("tests/screenshots")
            screenshot_dir.mkdir(exist_ok=True)
            
            # テスト名からファイル名を生成
            test_name = request.node.nodeid.replace("/", "_").replace("::", "_")
            screenshot_path = screenshot_dir / f"{test_name}.png"
            
            # スクリーンショットを保存
            page.screenshot(path=str(screenshot_path))
            print(f"Screenshot saved: {screenshot_path}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """テスト結果をitemに保存"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)