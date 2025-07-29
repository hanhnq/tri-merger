import streamlit as st
import os
from datetime import datetime, timedelta

# Streamlit Cloudの場合はst.secrets、ローカルの場合は環境変数を使用
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def check_password():
    """
    パスワード認証を行う関数
    
    Returns:
        bool: 認証成功時True、失敗時False
    """
    # セッション状態の初期化
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "auth_time" not in st.session_state:
        st.session_state.auth_time = None
    
    # 既に認証済みの場合
    if st.session_state.authenticated:
        # タイムアウトチェック
        if check_session_timeout():
            return True
        else:
            st.session_state.authenticated = False
            st.session_state.auth_time = None
            st.error("セッションがタイムアウトしました。再度ログインしてください。")
    
    # ログインフォームの表示
    with st.container():
        st.markdown("## 🔐 ログイン")
        st.markdown("---")
        
        # パスワード入力
        password = st.text_input(
            "パスワードを入力してください",
            type="password",
            key="password_input"
        )
        
        col1, col2, col3 = st.columns([1, 1, 3])
        with col1:
            if st.button("ログイン", type="primary"):
                if verify_password(password):
                    st.session_state.authenticated = True
                    st.session_state.auth_time = datetime.now()
                    st.success("ログインに成功しました！")
                    st.rerun()
                else:
                    st.error("パスワードが正しくありません。")
    
    return False

def verify_password(password):
    """
    入力されたパスワードを検証する
    
    Args:
        password: 入力されたパスワード
    
    Returns:
        bool: パスワードが正しい場合True
    """
    # Streamlit Cloudではst.secretsを使用
    if hasattr(st, 'secrets') and 'APP_PASSWORD' in st.secrets:
        correct_password = st.secrets["APP_PASSWORD"]
    else:
        correct_password = os.getenv("APP_PASSWORD", "tri-merger-2024")
    return password == correct_password

def check_session_timeout():
    """
    セッションのタイムアウトをチェックする
    
    Returns:
        bool: タイムアウトしていない場合True
    """
    if st.session_state.auth_time is None:
        return False
    
    # Streamlit Cloudではst.secretsを使用
    if hasattr(st, 'secrets') and 'SESSION_TIMEOUT' in st.secrets:
        timeout_seconds = int(st.secrets["SESSION_TIMEOUT"])
    else:
        timeout_seconds = int(os.getenv("SESSION_TIMEOUT", "3600"))
    timeout_delta = timedelta(seconds=timeout_seconds)
    
    if datetime.now() - st.session_state.auth_time > timeout_delta:
        return False
    
    # セッション時間を更新
    st.session_state.auth_time = datetime.now()
    return True

def logout():
    """
    ログアウト処理を行う
    """
    st.session_state.authenticated = False
    st.session_state.auth_time = None
    st.rerun()