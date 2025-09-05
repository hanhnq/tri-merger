import os
import json
import secrets
import logging
import streamlit as st
from datetime import datetime, timedelta

# ロガー
logger = logging.getLogger(__name__)
if not logger.handlers:
    logging.basicConfig(level=os.environ.get("AUTH_LOG_LEVEL", "DEBUG"),
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# extra-streamlit-componentsのCookieManager
try:
    import extra_streamlit_components as stx
    COOKIE_MANAGER_AVAILABLE = True
    logger.info("extra-streamlit-components loaded successfully")
except Exception as e:
    COOKIE_MANAGER_AVAILABLE = False
    logger.warning("extra-streamlit-components not available: %s", e)

# クッキー設定
_COOKIE_KEY = "tm_auth"
_COOKIE_EXPIRE_DAYS = 7

def get_cookie_manager():
    """Cookie Managerを取得（extra-streamlit-components版）"""
    if not COOKIE_MANAGER_AVAILABLE:
        logger.warning("Cookie manager not available")
        return None
    
    # CookieManagerをsession_stateで管理（重複初期化を防ぐ）
    if "cookie_manager" not in st.session_state:
        st.session_state.cookie_manager = stx.CookieManager()
        logger.info("CookieManager initialized from extra-streamlit-components")
    
    return st.session_state.cookie_manager

def write_auth_cookie(expire_days: int = _COOKIE_EXPIRE_DAYS):
    """認証Cookieを書き込む"""
    cm = get_cookie_manager()
    if cm is None:
        logger.warning("write_auth_cookie: CookieManager unavailable")
        return
    
    try:
        # Cookieの内容を作成
        exp = datetime.now() + timedelta(days=expire_days)
        payload = {
            "v": 1,
            "auth": True,
            "exp": int(exp.timestamp()),
            "nonce": secrets.token_urlsafe(8),
        }
        
        # Cookieをセット（期限付き）
        cm.set(
            cookie=_COOKIE_KEY,
            val=json.dumps(payload, separators=(",", ":")),
            expires_at=exp,
            key=f"set_{_COOKIE_KEY}"  # Streamlitのキー重複を防ぐ
        )
        logger.info("Auth cookie written: exp=%s", exp.isoformat())
    except Exception as e:
        logger.error("write_auth_cookie failed: %s", e, exc_info=True)

def read_auth_cookie():
    """認証Cookieを読み込む"""
    cm = get_cookie_manager()
    if cm is None:
        logger.info("read_auth_cookie: CookieManager unavailable")
        return None
    
    try:
        # まず全てのCookieを取得してみる（デバッグ用）
        all_cookies = cm.get_all()
        logger.debug("read_auth_cookie: all_cookies=%s", all_cookies)
        
        # 特定のCookieを取得
        logger.debug("read_auth_cookie: Attempting to get cookie with key=%s", _COOKIE_KEY)
        raw = cm.get(cookie=_COOKIE_KEY)
        logger.debug("read_auth_cookie: raw value from cm.get()=%s", raw)
        
        # all_cookiesに含まれているが、getで取得できない場合の処理
        if raw is None and all_cookies and _COOKIE_KEY in all_cookies:
            raw = all_cookies.get(_COOKIE_KEY)
            logger.debug("read_auth_cookie: Using value from all_cookies=%s", raw)
        
        if not raw:
            logger.debug("read_auth_cookie: no cookie found")
            return None
        
        # JSONパース
        if isinstance(raw, dict):
            # すでに辞書の場合はそのまま返す
            data = raw
        else:
            # 文字列の場合はJSONパース
            data = json.loads(raw)
        logger.debug("read_auth_cookie: loaded exp_ts=%s, auth=%s", data.get("exp"), data.get("auth"))
        return data
    except Exception as e:
        logger.error("read_auth_cookie error: %s", e, exc_info=True)
        return None

def clear_auth_cookie():
    """認証Cookieをクリア"""
    cm = get_cookie_manager()
    if cm is None:
        logger.info("clear_auth_cookie: CookieManager unavailable")
        return
    
    try:
        # Cookieを削除（空文字をセット）
        cm.delete(cookie=_COOKIE_KEY, key=f"delete_{_COOKIE_KEY}")
        logger.info("Auth cookie cleared")
    except Exception as e:
        logger.error("clear_auth_cookie failed: %s", e, exc_info=True)

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
    if "cookie_check_count" not in st.session_state:
        st.session_state.cookie_check_count = 0
    
    logger.debug("check_password: authenticated=%s, auth_time=%s, cookie_check_count=%s", 
                 st.session_state.authenticated, st.session_state.auth_time,
                 st.session_state.cookie_check_count)
    
    # Cookieによる自動ログイン（他タブ/ブラウザ再起動後の継続）
    if not st.session_state.authenticated:
        cookie_data = read_auth_cookie()
        
        # CookieManagerが初期化中の可能性があるので、数回リトライする
        if cookie_data is None and st.session_state.cookie_check_count < 3:
            st.session_state.cookie_check_count += 1
            logger.debug("Cookie not found, retry count: %s", st.session_state.cookie_check_count)
            # CookieManagerの初期化を待つためにrerun
            import time
            time.sleep(0.1)  # 少し待つ
            st.rerun()
        
        if cookie_data:
            # リトライカウントをリセット
            st.session_state.cookie_check_count = 0
            
            now_ts = int(datetime.now().timestamp())
            exp_ts = int(cookie_data.get("exp", 0))
            is_auth = cookie_data.get("auth", False)
            
            if is_auth and exp_ts > now_ts:
                logger.info("Auto-login from cookie: valid until %s", 
                            datetime.fromtimestamp(exp_ts).isoformat())
                st.session_state.authenticated = True
                st.session_state.auth_time = datetime.now()
                # スライディング延長
                write_auth_cookie()
                return True
            elif exp_ts <= now_ts:
                logger.info("Cookie expired at %s", datetime.fromtimestamp(exp_ts).isoformat())
                clear_auth_cookie()
    
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
                    write_auth_cookie()
                    logger.info("Login success: session established")
                    st.success("ログインに成功しました！")
                    st.rerun()
                else:
                    logger.info("Login failure: wrong password")
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
        logger.debug("check_session_timeout: no auth_time -> timeout")
        return False
    
    # タイムアウト時間を直接指定（1週間）
    timeout_seconds = 7 * 24 * 60 * 60
    timeout_delta = timedelta(seconds=timeout_seconds)
    
    if datetime.now() - st.session_state.auth_time > timeout_delta:
        logger.info("check_session_timeout: expired")
        return False
    
    # セッション時間を更新（スライディング延長）
    st.session_state.auth_time = datetime.now()
    write_auth_cookie()
    logger.debug("check_session_timeout: renewed session and cookie")
    return True

def logout():
    """
    ログアウト処理を行う
    """
    st.session_state.authenticated = False
    st.session_state.auth_time = None
    clear_auth_cookie()
    st.rerun()