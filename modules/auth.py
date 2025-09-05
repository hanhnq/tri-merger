import os
import json
import secrets
import streamlit as st
from datetime import datetime, timedelta

try:
    # クッキー管理（暗号化）
    from streamlit_cookies_manager import EncryptedCookieManager  # type: ignore
except Exception:  # ライブラリ未導入時も他機能を壊さない
    EncryptedCookieManager = None  # type: ignore

# クッキー設定
_COOKIE_KEY = "tm_auth"
_COOKIE_SECRET = (
    os.environ.get("COOKIES_PASSWORD")
    or (getattr(st, "secrets", {}) or {}).get("COOKIES_PASSWORD")
    or "dev-cookie-secret"
)
_COOKIE_EXPIRE_DAYS = 7

def _get_cookie_manager():
    """Streamlit 実行時のみ Cookie Manager を初期化。pytest 等では無効化。"""
    if EncryptedCookieManager is None:
        return None
    # pytest 等（非 Streamlit 実行）ではクッキー機能を無効化
    if os.environ.get("PYTEST_CURRENT_TEST"):
        return None
    try:
        cm = EncryptedCookieManager(prefix="tri-merger", password=_COOKIE_SECRET)
        # 初回アクセス時は Cookie コンポーネントの初期化完了まで待つ
        if hasattr(cm, "ready") and not cm.ready():
            # ここで停止して再実行されると ready() が True になり、以降読書き可能
            st.stop()
        return cm
    except Exception:
        return None

def _write_auth_cookie(expire_days: int = _COOKIE_EXPIRE_DAYS):
    cm = _get_cookie_manager()
    if not cm:
        return
    exp = datetime.now() + timedelta(days=expire_days)
    payload = {
        "v": 1,
        "auth": True,
        "exp": int(exp.timestamp()),
        "nonce": secrets.token_urlsafe(8),
    }
    try:
        cm[_COOKIE_KEY] = json.dumps(payload, separators=(",", ":"))
        cm.save()
    except Exception:
        pass

def _read_auth_cookie():
    cm = _get_cookie_manager()
    if not cm:
        return None
    try:
        raw = cm.get(_COOKIE_KEY) if hasattr(cm, "get") else cm[_COOKIE_KEY]
    except Exception:
        raw = None
    if not raw:
        return None
    try:
        return json.loads(raw)
    except Exception:
        return None

def _clear_auth_cookie():
    cm = _get_cookie_manager()
    if not cm:
        return
    try:
        if hasattr(cm, "__delitem__"):
            del cm[_COOKIE_KEY]
        else:
            cm[_COOKIE_KEY] = ""
        cm.save()
    except Exception:
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
    
    # Cookie による自動ログイン（他タブ/ブラウザ再起動後の継続）
    if not st.session_state.authenticated:
        c = _read_auth_cookie()
        now_ts = int(datetime.now().timestamp())
        if c and c.get("auth") and int(c.get("exp", 0)) > now_ts:
            st.session_state.authenticated = True
            st.session_state.auth_time = datetime.now()
            # スライディング延長
            _write_auth_cookie()
            return True

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
                    # クッキーにも保存（別タブ/再起動でも保持）
                    _write_auth_cookie()
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
    # auth_time が未設定または None の場合はタイムアウト扱い
    if st.session_state.get("auth_time") is None:
        return False
    
    # タイムアウト時間を直接指定（1週間）
    # 7日 * 24時間 * 60分 * 60秒 = 604800秒
    timeout_seconds = 7 * 24 * 60 * 60
    timeout_delta = timedelta(seconds=timeout_seconds)
    
    if datetime.now() - st.session_state.auth_time > timeout_delta:
        return False
    
    # セッション時間を更新（スライディング延長）
    st.session_state.auth_time = datetime.now()
    _write_auth_cookie()
    return True

def logout():
    """
    ログアウト処理を行う
    """
    st.session_state.authenticated = False
    st.session_state.auth_time = None
    _clear_auth_cookie()
    st.rerun()
