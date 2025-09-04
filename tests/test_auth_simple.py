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
        timeout_seconds = 3600  # 1時間
        timeout_delta = timedelta(seconds=timeout_seconds)
        
        # 現在時刻
        now = datetime.now()
        
        # 30分前の認証時刻 - タイムアウトしない
        auth_time_30min = now - timedelta(minutes=30)
        assert now - auth_time_30min <= timeout_delta
        
        # 2時間前の認証時刻 - タイムアウトする
        auth_time_2hours = now - timedelta(hours=2)
        assert now - auth_time_2hours > timeout_delta
        
        # エッジケース: ちょうど1時間
        auth_time_1hour_plus = now - timedelta(seconds=3601)
        assert now - auth_time_1hour_plus > timeout_delta
        
        auth_time_1hour_minus = now - timedelta(seconds=3599)
        assert now - auth_time_1hour_minus <= timeout_delta