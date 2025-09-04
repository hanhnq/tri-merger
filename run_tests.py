#!/usr/bin/env python3
"""テスト実行スクリプト"""

import sys
import subprocess
import argparse


def run_unit_tests():
    """ユニットテストを実行"""
    print("=== ユニットテストを実行中 ===")
    cmd = ["pytest", "tests/test_auth.py", "tests/test_question_master.py", "tests/test_aggregation.py", "-v"]
    result = subprocess.run(cmd)
    return result.returncode


def run_e2e_tests():
    """E2Eテストを実行"""
    print("\n=== E2Eテストを実行中 ===")
    print("Streamlitアプリケーションを起動しています...")
    
    # Streamlitアプリを起動
    app_process = subprocess.Popen(
        ["streamlit", "run", "app.py", "--server.port=8501", "--server.headless=true"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    import time
    time.sleep(5)  # アプリの起動を待つ
    
    try:
        # E2Eテストを実行
        cmd = ["pytest", "tests/test_e2e_workflow.py", "-v", "--headed"]  # --headedでブラウザを表示
        result = subprocess.run(cmd)
        return result.returncode
    finally:
        # アプリケーションを終了
        app_process.terminate()
        app_process.wait()


def main():
    parser = argparse.ArgumentParser(description="テストを実行")
    parser.add_argument("--unit", action="store_true", help="ユニットテストのみ実行")
    parser.add_argument("--e2e", action="store_true", help="E2Eテストのみ実行")
    parser.add_argument("--all", action="store_true", help="すべてのテストを実行（デフォルト）")
    
    args = parser.parse_args()
    
    # 引数が指定されていない場合はすべて実行
    if not any([args.unit, args.e2e]):
        args.all = True
    
    exit_code = 0
    
    if args.unit or args.all:
        code = run_unit_tests()
        if code != 0:
            exit_code = code
    
    if args.e2e or args.all:
        code = run_e2e_tests()
        if code != 0:
            exit_code = code
    
    if exit_code == 0:
        print("\n✅ すべてのテストが成功しました！")
    else:
        print("\n❌ 一部のテストが失敗しました。")
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()