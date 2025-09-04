# テストガイド

このディレクトリには、アンケート集計システムのテストコードが含まれています。

## テストの種類

### 1. ユニットテスト
- **test_auth.py** - 認証機能のテスト
  - パスワード検証
  - セッションタイムアウト
  - ログアウト機能

- **test_question_master.py** - 質問マスター作成機能のテスト
  - 正常なファイルからの質問マスター作成
  - 文字化けファイル名の処理
  - エラーハンドリング

- **test_aggregation.py** - データ集計機能のテスト
  - クライアント設定に基づくデータフィルタリング
  - 質問文と質問番号の相互変換
  - 複数ファイルの結合

### 2. E2Eテスト (test_e2e_workflow.py)
- 認証フロー
- ページ間ナビゲーション
- 質問マスター作成の完全なワークフロー
- クライアント設定サンプルのダウンロード
- データ集計の実行
- エラーハンドリング

## テストの実行方法

### 必要な準備
```bash
# 依存関係のインストール
pip install -r requirements.txt

# Playwrightのブラウザをインストール
playwright install
```

### すべてのテストを実行
```bash
python run_tests.py --all
# または
python run_tests.py
```

### ユニットテストのみ実行
```bash
python run_tests.py --unit
# または直接pytestを使用
pytest tests/test_auth.py tests/test_question_master.py tests/test_aggregation.py -v
```

### E2Eテストのみ実行
```bash
python run_tests.py --e2e
```

### 特定のテストファイルを実行
```bash
pytest tests/test_auth.py -v
```

### 特定のテストケースを実行
```bash
pytest tests/test_auth.py::TestAuth::test_verify_password_correct -v
```

## E2Eテストの注意事項

1. **アプリケーションの起動**
   - E2Eテストは自動的にStreamlitアプリを起動します
   - ポート8501が使用可能である必要があります

2. **ブラウザの表示**
   - デフォルトではヘッドレスモードで実行されます
   - ブラウザを表示したい場合は `--headed` オプションを使用します
   ```bash
   pytest tests/test_e2e_workflow.py --headed
   ```

3. **パスワード**
   - テストで使用するパスワードは `tri-merger-2024` です

4. **スクリーンショット**
   - テスト失敗時は自動的にスクリーンショットが `tests/screenshots/` に保存されます

## フィクスチャデータ

`fixtures/` ディレクトリには以下のテスト用データが含まれています：

- **sample_survey1.xlsx** - サンプルアンケートファイル1
- **sample_survey2.xlsx** - サンプルアンケートファイル2（異なる質問番号）
- **client_settings.xlsx** - クライアント設定サンプル
- **no_question_sheet.xlsx** - エラーテスト用（質問対応表シートなし）
- **no_data_sheet.xlsx** - エラーテスト用（dataシートなし）

## トラブルシューティング

### ポートが使用中の場合
```bash
# 使用中のプロセスを確認
lsof -i :8501
# プロセスを終了
kill -9 <PID>
```

### Playwrightのインストールエラー
```bash
# Playwrightを再インストール
pip uninstall playwright
pip install playwright
playwright install
```

### テストがタイムアウトする場合
- `conftest.py` のタイムアウト設定を調整
- マシンのスペックに応じて待機時間を延長

## CI/CDへの統合

GitHub Actionsなどで自動テストを実行する場合の例：

```yaml
- name: Install dependencies
  run: |
    pip install -r requirements.txt
    playwright install

- name: Run unit tests
  run: pytest tests/test_*.py -v --tb=short

- name: Run E2E tests
  run: |
    python run_tests.py --e2e
```