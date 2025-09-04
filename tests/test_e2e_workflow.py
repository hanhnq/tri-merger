import pytest
import os
import time
from playwright.sync_api import Page, expect
from pathlib import Path


class TestE2EWorkflow:
    """End-to-End テストクラス"""
    
    @pytest.fixture
    def fixtures_dir(self):
        """フィクスチャディレクトリのパスを返す"""
        return Path(__file__).parent / 'fixtures'
    
    @pytest.fixture
    def app_url(self):
        """アプリケーションのURLを返す"""
        return "http://localhost:8501"
    
    def wait_for_streamlit(self, page: Page):
        """Streamlitアプリの読み込みを待つ"""
        # Streamlitのロードインジケーターが消えるまで待つ
        page.wait_for_selector('.stSpinner', state='hidden', timeout=30000)
        # 追加の待機時間
        time.sleep(1)
    
    def test_authentication_flow(self, page: Page, app_url):
        """認証フローのテスト"""
        # アプリケーションにアクセス
        page.goto(app_url)
        
        # ログイン画面が表示されることを確認
        expect(page.locator('h2:has-text("🔐 ログイン")')).to_be_visible()
        
        # 間違ったパスワードでログイン試行
        page.fill('input[type="password"]', 'wrong-password')
        page.click('button:has-text("ログイン")')
        
        # エラーメッセージが表示されることを確認
        expect(page.locator('div:has-text("パスワードが正しくありません。")')).to_be_visible(timeout=5000)
        
        # 正しいパスワードでログイン
        page.fill('input[type="password"]', 'tri-merger-2024')
        page.click('button:has-text("ログイン")')
        
        # ログイン成功メッセージを確認
        expect(page.locator('div:has-text("ログインに成功しました！")')).to_be_visible(timeout=5000)
        
        # メインページに遷移することを確認
        self.wait_for_streamlit(page)
        expect(page.locator('h1:has-text("アンケート集計システム")')).to_be_visible(timeout=10000)
    
    def test_navigation_between_pages(self, page: Page, app_url):
        """ページ間のナビゲーションテスト"""
        # ログイン済みの状態を前提とする
        page.goto(app_url)
        
        # ログイン
        page.fill('input[type="password"]', 'tri-merger-2024')
        page.click('button:has-text("ログイン")')
        self.wait_for_streamlit(page)
        
        # サイドバーメニューが表示されることを確認
        expect(page.locator('[data-testid="stSidebar"]')).to_be_visible()
        
        # 質問マスター作成ページへ移動
        page.click('a:has-text("📝 質問マスター作成")')
        self.wait_for_streamlit(page)
        expect(page.locator('h1:has-text("📝 ステップ1: 質問マスター作成")')).to_be_visible()
        
        # 設定サンプル作成ページへ移動
        page.click('a:has-text("⚙️ 設定サンプル作成")')
        self.wait_for_streamlit(page)
        expect(page.locator('h1:has-text("⚙️ ステップ2: クライアント設定")')).to_be_visible()
        
        # データ集計ページへ移動
        page.click('a:has-text("📊 データ集計")')
        self.wait_for_streamlit(page)
        expect(page.locator('h1:has-text("📊 ステップ3: データ集計")')).to_be_visible()
    
    def test_question_master_creation(self, page: Page, app_url, fixtures_dir):
        """質問マスター作成機能のテスト"""
        # ログイン済みの状態から開始
        page.goto(app_url)
        page.fill('input[type="password"]', 'tri-merger-2024')
        page.click('button:has-text("ログイン")')
        self.wait_for_streamlit(page)
        
        # 質問マスター作成ページへ移動
        page.click('a:has-text("📝 質問マスター作成")')
        self.wait_for_streamlit(page)
        
        # ファイルアップロードエリアが表示されることを確認
        expect(page.locator('[data-testid="stFileUploadDropzone"]')).to_be_visible()
        
        # サンプルファイルをアップロード
        sample_file1 = str(fixtures_dir / 'sample_survey1.xlsx')
        sample_file2 = str(fixtures_dir / 'sample_survey2.xlsx')
        
        # ファイルをアップロード
        page.set_input_files('input[type="file"]', [sample_file1, sample_file2])
        
        # 作成ボタンをクリック
        page.click('button:has-text("📋 質問マスターを作成")')
        
        # 成功メッセージを確認
        expect(page.locator('div:has-text("✅ 質問マスターの作成が完了しました！")')).to_be_visible(timeout=10000)
        
        # 結果が表示されることを確認
        expect(page.locator('h2:has-text("📊 作成された質問マスター")')).to_be_visible()
        
        # ダウンロードボタンが表示されることを確認
        expect(page.locator('button:has-text("📄 質問マスターをダウンロード")')).to_be_visible()
    
    def test_client_settings_sample(self, page: Page, app_url):
        """クライアント設定サンプル作成のテスト"""
        # ログイン済みの状態から開始
        page.goto(app_url)
        page.fill('input[type="password"]', 'tri-merger-2024')
        page.click('button:has-text("ログイン")')
        self.wait_for_streamlit(page)
        
        # 設定サンプル作成ページへ移動
        page.click('a:has-text("⚙️ 設定サンプル作成")')
        self.wait_for_streamlit(page)
        
        # サンプルデータが表示されることを確認
        expect(page.locator('h2:has-text("📋 設定ファイルのサンプル")')).to_be_visible()
        
        # ダウンロードボタンが表示されることを確認
        expect(page.locator('button:has-text("📄 設定サンプルをダウンロード")')).to_be_visible()
        
        # 使い方の説明を展開
        page.click('summary:has-text("ℹ️ 設定ファイルの使い方")')
        
        # 説明内容が表示されることを確認
        expect(page.locator('text="サンプルをダウンロード"')).to_be_visible()
    
    def test_data_aggregation(self, page: Page, app_url, fixtures_dir):
        """データ集計機能のテスト"""
        # ログイン済みの状態から開始
        page.goto(app_url)
        page.fill('input[type="password"]', 'tri-merger-2024')
        page.click('button:has-text("ログイン")')
        self.wait_for_streamlit(page)
        
        # データ集計ページへ移動
        page.click('a:has-text("📊 データ集計")')
        self.wait_for_streamlit(page)
        
        # 3つのファイルアップロードエリアが表示されることを確認
        file_uploaders = page.locator('[data-testid="stFileUploadDropzone"]')
        expect(file_uploaders).to_have_count(3)
        
        # 必要なファイルを準備
        data_file1 = str(fixtures_dir / 'sample_survey1.xlsx')
        data_file2 = str(fixtures_dir / 'sample_survey2.xlsx')
        client_settings = str(fixtures_dir / 'client_settings.xlsx')
        
        # まず質問マスターを作成（前のテストで作成されていない場合）
        page.goto(app_url + "/質問マスター作成")
        self.wait_for_streamlit(page)
        page.set_input_files('input[type="file"]', [data_file1, data_file2])
        page.click('button:has-text("📋 質問マスターを作成")')
        expect(page.locator('div:has-text("✅ 質問マスターの作成が完了しました！")')).to_be_visible(timeout=10000)
        
        # 質問マスターをダウンロード（実際のE2Eでは一時ファイルとして保存）
        # ここではテストの簡略化のため、既存のファイルを使用
        
        # データ集計ページに戻る
        page.goto(app_url + "/データ集計")
        self.wait_for_streamlit(page)
        
        # ファイルをアップロード
        # 注：複数のファイルアップローダーがある場合の処理
        uploaders = page.locator('input[type="file"]').all()
        uploaders[0].set_input_files([data_file1, data_file2])  # データファイル
        uploaders[1].set_input_files(data_file1)  # 質問マスター（仮）
        uploaders[2].set_input_files(client_settings)  # クライアント設定
        
        # 集計実行ボタンをクリック
        page.click('button:has-text("🚀 集計を実行")')
        
        # 成功メッセージを確認
        expect(page.locator('div:has-text("✅ 集計が完了しました！")')).to_be_visible(timeout=15000)
        
        # 集計結果が表示されることを確認
        expect(page.locator('h2:has-text("📥 集計結果のダウンロード")')).to_be_visible()
        
        # クライアント別のダウンロードボタンが表示されることを確認
        expect(page.locator('button:has-text("クライアントA")')).to_be_visible()
        expect(page.locator('button:has-text("クライアントB")')).to_be_visible()
    
    def test_file_size_limitation(self, page: Page, app_url):
        """ファイルサイズ制限のテスト"""
        # このテストは実際の大きなファイルが必要なため、
        # ここでは制限の表示を確認するだけにする
        page.goto(app_url)
        page.fill('input[type="password"]', 'tri-merger-2024')
        page.click('button:has-text("ログイン")')
        self.wait_for_streamlit(page)
        
        # 各ページでファイルサイズ制限の表示を確認
        pages = [
            "/質問マスター作成",
            "/データ集計"
        ]
        
        for page_path in pages:
            page.goto(app_url + page_path)
            self.wait_for_streamlit(page)
            expect(page.locator('text="ファイルサイズ制限: 各ファイル50MB以内"')).to_be_visible()
    
    def test_progress_indicators(self, page: Page, app_url):
        """進捗インジケーターのテスト"""
        page.goto(app_url)
        page.fill('input[type="password"]', 'tri-merger-2024')
        page.click('button:has-text("ログイン")')
        self.wait_for_streamlit(page)
        
        # 各ページで進捗インジケーターを確認
        steps = [
            ("/質問マスター作成", "1️⃣ 質問マスター作成 ✅"),
            ("/設定サンプル作成", "2️⃣ クライアント設定 ✅"),
            ("/データ集計", "3️⃣ データ集計 ✅")
        ]
        
        for page_path, active_step in steps:
            page.goto(app_url + page_path)
            self.wait_for_streamlit(page)
            expect(page.locator(f'text="{active_step}"')).to_be_visible()
    
    def test_error_handling(self, page: Page, app_url, fixtures_dir):
        """エラーハンドリングのテスト"""
        page.goto(app_url)
        page.fill('input[type="password"]', 'tri-merger-2024')
        page.click('button:has-text("ログイン")')
        self.wait_for_streamlit(page)
        
        # 質問マスター作成ページで不正なファイルをアップロード
        page.goto(app_url + "/質問マスター作成")
        self.wait_for_streamlit(page)
        
        # 質問対応表シートがないファイルをアップロード
        invalid_file = str(fixtures_dir / 'no_question_sheet.xlsx')
        page.set_input_files('input[type="file"]', invalid_file)
        page.click('button:has-text("📋 質問マスターを作成")')
        
        # エラーメッセージが表示されることを確認
        expect(page.locator('div:has-text("エラーが発生しました")')).to_be_visible(timeout=5000)