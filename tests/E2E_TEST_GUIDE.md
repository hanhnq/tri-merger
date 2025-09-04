# E2Eテスト実行ガイド

## デプロイ済みアプリケーションのテスト

### 対象URL
https://tri-merger-absurd-plain-advertisement.squadbase.app/

### 必要な認証情報

1. **Squadbase認証**（プラットフォームレベル）
   - ユーザー名またはメールアドレス
   - パスワード

2. **アプリケーション認証**（アプリレベル）
   - パスワード: `tri-merger-2024`

### セットアップ手順

1. **必要なパッケージのインストール**
```bash
pip install playwright pytest-playwright
playwright install chromium
```

2. **環境変数の設定**
```bash
# Squadbase認証情報を環境変数として設定
export SQUADBASE_USERNAME='your-username-or-email'
export SQUADBASE_PASSWORD='your-squadbase-password'
```

3. **テストの実行**
```bash
# ヘッドレスモード（バックグラウンド実行）
pytest tests/test_e2e_deployed.py -v

# ヘッドモード（ブラウザ表示あり）
pytest tests/test_e2e_deployed.py -v --headed

# 特定のテストのみ実行
pytest tests/test_e2e_deployed.py::TestE2EDeployed::test_deployed_app_access -v --headed
```

### テスト内容

1. **test_deployed_app_access**
   - Squadbase認証の通過
   - アプリケーションログイン画面の表示確認

2. **test_full_workflow**
   - Squadbase認証
   - アプリケーション認証（tri-merger-2024）
   - 質問マスター作成画面への遷移

3. **test_without_squadbase_auth**
   - 認証なしでのアクセス（エラー確認）

### トラブルシューティング

#### 認証情報が設定されていない場合
```
SKIPPED [1] tests/test_e2e_deployed.py:65: Squadbase認証情報が設定されていません。
```
→ 環境変数を設定してください

#### Squadbaseのログイン画面が変更されている場合
`handle_squadbase_auth`メソッドのセレクタを調整する必要があります：
- メールフィールド: `input[type="email"]`
- ユーザー名フィールド: `input[name="username"]`
- パスワードフィールド: `input[type="password"]`
- ログインボタン: `button[type="submit"]`

### セキュリティ注意事項

- 認証情報は環境変数で管理し、コードにハードコードしない
- CI/CD環境では、シークレット管理機能を使用する
- テスト実行後は環境変数をクリアする：
  ```bash
  unset SQUADBASE_USERNAME
  unset SQUADBASE_PASSWORD
  ```

### ローカルアプリケーションのテスト

ローカルで起動したアプリケーションをテストする場合：
```bash
# Streamlitアプリを起動
streamlit run app.py &

# ローカル版のE2Eテストを実行
pytest tests/test_e2e_workflow.py -v
```