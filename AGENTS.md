# Repository Guidelines

本リポジトリは、Streamlitベースのアンケート集計アプリ（tri‑merger‑python）です。以下の指針に従い、短く正確な変更をお願いします。

## プロジェクト構成
- コア: `modules/`（`aggregation.py`, `question_master.py`, `auth.py`）
- UI: `app.py`, `pages/`（Streamlit マルチページ）
- テスト: `tests/`（pytest/Playwright）, 設定:`pytest.ini`
- データ入出力: `data/`（入力Excel）, `result/`（出力/ログ）, `test_results/`（レポート）
- ユーティリティ: `run_tests.py`, `generate_test_report.py`, `create_*`, `run_aggregation.py`
- 設定: `.env`, `.streamlit/`（テーマ等）

## ビルド・実行・テスト
- セットアップ: `python -m venv venv && source venv/bin/activate`（Windows: `venv\Scripts\activate`）
- 依存インストール: `pip install -r requirements.txt`；E2E用ブラウザ: `playwright install`
- ローカル実行: `streamlit run app.py`
- ユニット: `pytest -v -p no:playwright` または `python run_tests.py --unit`
- E2E: `python run_tests.py --e2e`（ポート`8501`が空いていること）
- すべて/レポート: `python run_tests.py`／`python generate_test_report.py`

## コーディング規約
- 準拠: PEP 8／インデント4スペース。
- 命名: 関数/モジュール`snake_case`、クラス`CamelCase`、定数`UPPER_SNAKE`。
- Docstring: `"""..."""`（日本語可）、型ヒント歓迎。
- ログ: `logging`を使用。`print`はスクリプトや一時デバッグのみに限定。

## テスト指針
- 配置/命名: `tests/`、`test_*.py`、`Test*`、`test_*`（`pytest.ini`準拠）。
- 変更点にはユニットテストを追加。主要ユーザーフローはPlaywrightでE2Eを最小限維持。
- レポート: `generate_test_report.py`で`test_results/`にJUnit/XML/HTML出力。

## コミットとPR
- 形式: Conventional Commits 推奨（例: `fix: 日本語ファイル名の文字化け対策`。絵文字任意）。
- PR要件: 目的/変更点/再現手順、スクリーンショット（UI）、関連Issue、テスト結果を記載。
- チェック: `pytest -v`がグリーンであること。`result/` `data/` `venv/` `test_results/`等の生成物はコミットしない。

## セキュリティ・設定
- 機密値は`.env`に保存しGit管理外。個人情報を含むExcelは共有前にマスキング。
- 開発用パスワードは`modules/auth.py`で固定。本番運用では環境変数化を推奨。

## Squadbaseデプロイ
- 前提: ルートの`squadbase.yml`で設定済み（`framework: streamlit`、`runtime: python3.12`、`entrypoint: app.py`、`package_manager: pip`）。
- Git連携デプロイ: Squadbaseダッシュボード → New App → 対象GitHubリポジトリを選択 → `squadbase.yml`を自動検出 → Deploy。自動デプロイを有効にしていれば`main`へのPushで再デプロイ。
- 環境変数（認証用）: プラットフォーム認証を使う場合は環境に設定。
  ```bash
  export SQUADBASE_USERNAME="<your-username-or-email>"
  export SQUADBASE_PASSWORD="<your-squadbase-password>"
  ```
- 稼働確認: デプロイURLにアクセス（例）`https://tri-merger-absurd-plain-advertisement.squadbase.app/` → Squadbase認証後、アプリ内パスワード`tri-merger-2024`でログイン。
- デプロイ後E2E検証: `pytest tests/test_e2e_deployed.py -v`（ブラウザ表示は`--headed`）。ログインUIが変わった場合は`tests/test_e2e_deployed.py`の`handle_squadbase_auth`を調整。
