import pytest
import os
import time
from playwright.sync_api import Page, expect
from pathlib import Path


class TestE2EDeployed:
    """デプロイ済みアプリケーションのE2Eテスト"""
    
    @pytest.fixture
    def fixtures_dir(self):
        """フィクスチャディレクトリのパスを返す"""
        return Path(__file__).parent / 'fixtures'
    
    @pytest.fixture
    def app_url(self):
        """デプロイ済みアプリケーションのURLを返す"""
        return "https://tri-merger-absurd-plain-advertisement.squadbase.app/"
    
    @pytest.fixture
    def squadbase_credentials(self):
        """Squadbase認証情報を環境変数から取得"""
        return {
            'username': os.getenv('SQUADBASE_USERNAME', ''),
            'password': os.getenv('SQUADBASE_PASSWORD', '')
        }
    
    def handle_squadbase_auth(self, page: Page, credentials: dict):
        """Squadbase認証を処理"""
        # Squadbaseのログインフォームが表示されるか確認
        try:
            # ユーザー名/メールフィールドを探す
            if page.locator('input[type="email"]').is_visible():
                page.fill('input[type="email"]', credentials['username'])
            elif page.locator('input[name="username"]').is_visible():
                page.fill('input[name="username"]', credentials['username'])
            elif page.locator('input[type="text"]').first.is_visible():
                page.fill('input[type="text"]', credentials['username'])
            
            # パスワードフィールド
            page.fill('input[type="password"]', credentials['password'])
            
            # ログインボタンをクリック
            login_button = page.locator('button[type="submit"], button:has-text("ログイン"), button:has-text("Login"), button:has-text("Sign in")')
            if login_button.is_visible():
                login_button.click()
                # 認証完了を待つ
                page.wait_for_load_state('networkidle')
                time.sleep(2)
        except:
            # Squadbase認証が不要な場合はスキップ
            pass
    
    def wait_for_streamlit(self, page: Page):
        """Streamlitアプリの読み込みを待つ"""
        # Streamlitのロードインジケーターが消えるまで待つ
        try:
            page.wait_for_selector('.stSpinner', state='hidden', timeout=30000)
        except:
            pass
        time.sleep(1)
    
    def test_deployed_app_access(self, page: Page, app_url, squadbase_credentials):
        """デプロイ済みアプリへのアクセステスト"""
        # 認証情報が設定されているか確認
        if not squadbase_credentials['username'] or not squadbase_credentials['password']:
            pytest.skip("Squadbase認証情報が設定されていません。環境変数 SQUADBASE_USERNAME と SQUADBASE_PASSWORD を設定してください。")
        
        # アプリケーションにアクセス
        page.goto(app_url)
        
        # Squadbase認証を処理
        self.handle_squadbase_auth(page, squadbase_credentials)
        
        # Streamlitアプリが読み込まれるまで待つ
        self.wait_for_streamlit(page)
        
        # アプリケーションのログイン画面が表示されることを確認
        expect(page.locator('h2:has-text("🔐 ログイン")')).to_be_visible(timeout=10000)
    
    def test_full_workflow(self, page: Page, app_url, squadbase_credentials, fixtures_dir):
        """完全なワークフローテスト"""
        if not squadbase_credentials['username'] or not squadbase_credentials['password']:
            pytest.skip("Squadbase認証情報が設定されていません。")
        
        # アプリケーションにアクセス
        page.goto(app_url)
        
        # Squadbase認証を処理
        self.handle_squadbase_auth(page, squadbase_credentials)
        
        # Streamlitアプリが読み込まれるまで待つ
        self.wait_for_streamlit(page)
        
        # アプリケーション認証（tri-merger-2024）
        page.fill('input[type="password"]', 'tri-merger-2024')
        page.click('button:has-text("ログイン")')
        
        # ログイン成功を確認
        page.wait_for_selector('div:has-text("ログインに成功しました！")', timeout=5000)
        
        # 質問マスター作成ページへ遷移
        page.wait_for_selector('h1:has-text("📊 アンケート集計システム")', timeout=5000)
        
        # ファイルアップロードエリアが表示されることを確認
        expect(page.locator('div:has-text("📁 質問マスター作成")')).to_be_visible()
    
    def test_without_squadbase_auth(self, page: Page, app_url):
        """Squadbase認証なしでのアクセステスト（エラー確認）"""
        # 直接アプリケーションにアクセス
        page.goto(app_url)
        
        # 認証が必要な場合のエラーまたはログイン画面を確認
        # Squadbaseのログイン画面またはStreamlitのログイン画面が表示されることを確認
        page.wait_for_selector('input[type="password"], input[type="email"], input[name="username"]', timeout=10000)


# 実行用のヘルパー関数
def run_deployed_tests():
    """デプロイ済みアプリのテストを実行"""
    import subprocess
    
    print("=" * 60)
    print("デプロイ済みアプリケーションのE2Eテスト")
    print("=" * 60)
    print("\n環境変数を設定してください：")
    print("export SQUADBASE_USERNAME='your-username'")
    print("export SQUADBASE_PASSWORD='your-password'")
    print("\nテスト実行コマンド：")
    print("pytest tests/test_e2e_deployed.py -v --headed")
    print("=" * 60)


if __name__ == "__main__":
    run_deployed_tests()