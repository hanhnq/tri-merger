import streamlit as st
from datetime import datetime, timedelta

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
    # パスワードを直接指定
    correct_password = "tri-merger-2024"
    return password == correct_password

def check_session_timeout():
    """
    セッションのタイムアウトをチェックする
    
    Returns:
        bool: タイムアウトしていない場合True
    """
    if st.session_state.auth_time is None:
        return False
    
    # タイムアウト時間を直接指定（1時間）
    timeout_seconds = 3600
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