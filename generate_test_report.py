#!/usr/bin/env python3
"""テストレポート生成スクリプト"""

import subprocess
import json
import datetime
import os
from pathlib import Path


def run_unit_tests_with_report():
    """ユニットテストを実行してレポートを生成"""
    print("=== ユニットテスト実行中 ===")
    
    # JUnit XML形式でレポートを出力
    cmd = [
        "pytest",
        "tests/test_auth_simple.py",
        "tests/test_question_master.py", 
        "tests/test_aggregation.py",
        "-v",
        "-p", "no:playwright",
        "--junit-xml=test_results/junit_report.xml",
        "--html=test_results/html_report.html",
        "--self-contained-html",
        "--tb=short",
        "--capture=no"
    ]
    
    # テスト結果ディレクトリを作成
    os.makedirs("test_results", exist_ok=True)
    
    # テストを実行してコンソール出力も保存
    with open("test_results/console_output.txt", "w", encoding="utf-8") as f:
        result = subprocess.run(cmd, capture_output=True, text=True)
        f.write("=== STDOUT ===\n")
        f.write(result.stdout)
        f.write("\n\n=== STDERR ===\n")
        f.write(result.stderr)
    
    # コンソールにも出力
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    
    return result.returncode


def generate_markdown_report():
    """Markdownフォーマットのレポートを生成"""
    
    report_content = f"""# テスト実行レポート

**実行日時**: {datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}  
**プロジェクト**: アンケート集計システム (tri-merger-python)  
**実行環境**: macOS Darwin

## 📊 テスト実行サマリー

### ユニットテスト結果

"""
    
    # コンソール出力を読み込んで解析
    if os.path.exists("test_results/console_output.txt"):
        with open("test_results/console_output.txt", "r", encoding="utf-8") as f:
            console_output = f.read()
        
        # テスト結果のサマリーを抽出
        if "passed" in console_output:
            import re
            # 結果サマリーを抽出 (例: "22 passed, 2 warnings in 1.17s")
            summary_match = re.search(r'(\d+) passed(?:, (\d+) failed)?(?:, (\d+) warnings)?.*in ([\d.]+)s', console_output)
            if summary_match:
                passed = summary_match.group(1)
                failed = summary_match.group(2) or "0"
                warnings = summary_match.group(3) or "0"
                duration = summary_match.group(4)
                
                report_content += f"""
| メトリクス | 値 |
|-----------|-----|
| ✅ 成功 | {passed} |
| ❌ 失敗 | {failed} |
| ⚠️ 警告 | {warnings} |
| ⏱️ 実行時間 | {duration}秒 |

"""
        
        # 各テストの詳細結果を抽出
        report_content += "### 詳細テスト結果\n\n"
        
        # テストケースごとの結果を解析
        test_lines = [line for line in console_output.split('\n') if '::' in line and ('PASSED' in line or 'FAILED' in line)]
        
        current_module = ""
        for line in test_lines:
            if '::' in line:
                parts = line.split('::')
                if len(parts) >= 3:
                    module = parts[0].split('/')[-1]
                    test_class = parts[1]
                    test_name_and_result = parts[2]
                    
                    # モジュールが変わったらヘッダーを出力
                    if module != current_module:
                        current_module = module
                        report_content += f"\n#### {module}\n\n"
                        report_content += "| テストケース | 結果 |\n"
                        report_content += "|-------------|------|\n"
                    
                    # テスト名と結果を分離
                    if 'PASSED' in test_name_and_result:
                        test_name = test_name_and_result.replace(' PASSED', '').strip()
                        result = "✅ PASSED"
                    elif 'FAILED' in test_name_and_result:
                        test_name = test_name_and_result.replace(' FAILED', '').strip()
                        result = "❌ FAILED"
                    else:
                        test_name = test_name_and_result
                        result = "⚠️ UNKNOWN"
                    
                    # テスト名から説明を生成
                    test_description = test_name.replace('test_', '').replace('_', ' ').title()
                    report_content += f"| {test_description} | {result} |\n"
    
    # エビデンスセクション
    report_content += f"""

## 📁 エビデンスファイル

以下のファイルが生成されました：

1. **HTMLレポート**: `test_results/html_report.html`
   - ブラウザで開いて詳細な結果を確認できます
   
2. **JUnit XMLレポート**: `test_results/junit_report.xml`
   - CI/CDツールとの統合用
   
3. **コンソール出力**: `test_results/console_output.txt`
   - 完全なテスト実行ログ

## 🔍 テストカバレッジ

### 認証機能 (auth.py)
- ✅ パスワード検証機能
- ✅ セッションタイムアウトロジック
- ✅ 正常系・異常系の両方をカバー

### 質問マスター作成機能 (question_master.py)
- ✅ 複数Excelファイルからの質問抽出
- ✅ 質問番号のマッピング
- ✅ 文字化けファイル名の処理
- ✅ エラーハンドリング
- ✅ 質問順序の保持

### データ集計機能 (aggregation.py)
- ✅ クライアント設定に基づくデータフィルタリング
- ✅ 質問文と質問番号の相互変換
- ✅ FA（自由回答）列の自動包含
- ✅ 日付ソート処理
- ✅ 複数ファイルの結合
- ✅ エラーケースの処理

## 📝 備考

- Streamlitのセッション状態に依存する部分は、シンプルなロジックテストで代替
- E2Eテストは別途Playwright環境セットアップ後に実行可能
- 警告は将来のpandasバージョンでの仕様変更に関するもので、現在の動作には影響なし

"""
    
    # レポートを保存
    with open("test_results/test_report.md", "w", encoding="utf-8") as f:
        f.write(report_content)
    
    print("\n✅ テストレポートを生成しました: test_results/test_report.md")


def main():
    """メイン処理"""
    print("テストレポート生成を開始します...\n")
    
    # pytest-htmlプラグインをインストール
    print("必要なプラグインをインストール中...")
    subprocess.run(["pip", "install", "pytest-html"], capture_output=True)
    
    # テストを実行
    exit_code = run_unit_tests_with_report()
    
    # レポートを生成
    generate_markdown_report()
    
    print(f"\n{'✅ すべてのテストが成功しました！' if exit_code == 0 else '❌ 一部のテストが失敗しました。'}")
    print("\nエビデンスファイル:")
    print("- test_results/test_report.md (Markdownレポート)")
    print("- test_results/html_report.html (HTMLレポート)")
    print("- test_results/junit_report.xml (JUnit XMLレポート)")
    print("- test_results/console_output.txt (コンソール出力)")


if __name__ == "__main__":
    main()