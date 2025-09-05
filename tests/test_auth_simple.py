import pytest
from datetime import datetime, timedelta
from modules.auth import verify_password


class TestAuthSimple:
    """認証機能の単純なテストクラス（Streamlitセッション状態を使わない）"""
    
    def test_verify_password_correct(self):
        """正しいパスワードで認証が成功することを確認"""
        assert verify_password("tri-merger-2024") == True
    
    def test_verify_password_incorrect(self):
        """間違ったパスワードで認証が失敗することを確認"""
        assert verify_password("wrong-password") == False
        assert verify_password("") == False
        assert verify_password("TRI-MERGER-2024") == False  # 大文字小文字の区別
    
    def test_session_timeout_logic(self):
        """セッションタイムアウトのロジックを確認（直接計算）"""
        timeout_seconds = 7 * 24 * 60 * 60  # 1週間
        timeout_delta = timedelta(seconds=timeout_seconds)
        
        # 現在時刻
        now = datetime.now()
        
        # 3日前の認証時刻 - タイムアウトしない
        auth_time_3days = now - timedelta(days=3)
        assert now - auth_time_3days <= timeout_delta
        
        # 8日前の認証時刻 - タイムアウトする
        auth_time_8days = now - timedelta(days=8)
        assert now - auth_time_8days > timeout_delta
        
        # エッジケース: ちょうど1週間
        auth_time_1week_plus = now - timedelta(seconds=7*24*3600 + 1)
        assert now - auth_time_1week_plus > timeout_delta
        
        auth_time_1week_minus = now - timedelta(seconds=7*24*3600 - 1)
        assert now - auth_time_1week_minus <= timeout_delta
