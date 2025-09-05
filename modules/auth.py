import os
import json
import secrets
import logging
import streamlit as st
from datetime import datetime, timedelta

# ロガー（最初に初期化して以降で利用）
logger = logging.getLogger(__name__)
if not logger.handlers:
    logging.basicConfig(level=os.environ.get("AUTH_LOG_LEVEL", "INFO"))

try:
    # クッキー管理（暗号化）
    from streamlit_cookies_manager import EncryptedCookieManager  # type: ignore
    # st.cache の非推奨警告を回避するため、ライブラリ内関数を安全にモンキーパッチ
    try:
        import base64
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC  # type: ignore
        from cryptography.hazmat.primitives import hashes  # type: ignore
        import streamlit_cookies_manager.encrypted_cookie_manager as _encmod  # type: ignore

        @_encmod.st.cache_data if hasattr(_encmod, 'st') else st.cache_data  # fallback
        def _patched_key_from_parameters(salt: bytes, iterations: int, password: str):
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=iterations,
            )
            return base64.urlsafe_b64encode(kdf.derive(password.encode('utf-8')))

        # 置換（元の関数は @st.cache でラップされているため警告が出る）
        _encmod.key_from_parameters = _patched_key_from_parameters  # type: ignore
        logger.info("Patched streamlit_cookies_manager.key_from_parameters -> st.cache_data")
    except Exception as _e:
        # パッチ失敗時はそのまま（警告は出るが機能は維持）
        logger.warning("Patch for key_from_parameters failed: %s", _e)
except Exception as e:  # ライブラリ未導入時も他機能を壊さない
    EncryptedCookieManager = None  # type: ignore
    logger.warning(
        "EncryptedCookieManager not available (install streamlit-cookies-manager). reason=%s",
        e,
    )

# 以降、logger は上部で初期化済み

# クッキー設定
_COOKIE_KEY = "tm_auth"
_COOKIE_SECRET = (
    os.environ.get("COOKIES_PASSWORD")
    or (getattr(st, "secrets", {}) or {}).get("COOKIES_PASSWORD")
    or "dev-cookie-secret"
)
_COOKIE_EXPIRE_DAYS = 7

# この実行サイクル内で使うCookieManager（重複生成回避用）
_RUN_CM = None  # 型: Optional[EncryptedCookieManager]

# CookieManager は毎回インスタンス化（前回のnot ready状態を引きずらない）
def _get_cookie_manager():
    """Cookie Manager を返す（ない場合は None）。毎実行で生成し、ready判定は呼び出し側で行う。"""
    if not EncryptedCookieManager:
        logger.info("CookieManager disabled: import failure (streamlit-cookies-manager not installed)")
        return None
    if os.environ.get("PYTEST_CURRENT_TEST"):
        if os.environ.get("ALLOW_COOKIES_IN_TEST") == "1":
            logger.info("CookieManager enabled during pytest (ALLOW_COOKIES_IN_TEST=1)")
        else:
            logger.info("CookieManager disabled: pytest detected (PYTEST_CURRENT_TEST set)")
            return None
    try:
        cm = EncryptedCookieManager(prefix="tri-merger", password=_COOKIE_SECRET)
        logger.info("CookieManager initialized (prefix=tri-merger)")
        return cm
    except Exception as e:
        logger.warning("CookieManager init failed: %s", e)
        return None

def _write_auth_cookie(expire_days: int = _COOKIE_EXPIRE_DAYS):
    cm = _RUN_CM or _get_cookie_manager()
    if cm is None:
        logger.warning("_write_auth_cookie: CookieManager unavailable (skip)")
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
        logger.info("auth cookie written: exp=%s", exp.isoformat())
    except Exception as e:
        logger.warning("_write_auth_cookie failed: %s", e)

def _read_auth_cookie():
    cm = _RUN_CM or _get_cookie_manager()
    if cm is None:
        logger.info("_read_auth_cookie: CookieManager unavailable")
        return None
    try:
        raw = cm.get(_COOKIE_KEY) if hasattr(cm, "get") else cm[_COOKIE_KEY]
    except Exception as e:
        logger.warning("_read_auth_cookie read error: %s", e)
        raw = None
    if not raw:
        logger.debug("_read_auth_cookie: no cookie found")
        return None
    try:
        data = json.loads(raw)
        logger.debug("_read_auth_cookie: loaded exp_ts=%s, auth=%s", data.get("exp"), data.get("auth"))
        return data
    except Exception as e:
        logger.warning("_read_auth_cookie parse error: %s", e)
        return None

def _clear_auth_cookie():
    cm = _RUN_CM or _get_cookie_manager()
    if cm is None:
        logger.info("_clear_auth_cookie: CookieManager unavailable")
        return
    try:
        if hasattr(cm, "__delitem__"):
            del cm[_COOKIE_KEY]
        else:
            cm[_COOKIE_KEY] = ""
        cm.save()
        logger.info("auth cookie cleared")
    except Exception as e:
        logger.warning("_clear_auth_cookie failed: %s", e)

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
    logger.debug("check_password: init authenticated=%s auth_time=%s", st.session_state.authenticated, st.session_state.auth_time)

    # Cookieコンポーネントの初期化完了を担保
    global _RUN_CM
    _RUN_CM = _get_cookie_manager()
    cm = _RUN_CM
    if cm is not None and hasattr(cm, "ready") and not cm.ready():
        logger.debug("CookieManager not ready yet -> st.stop() to rerun")
        st.stop()
    
    # Cookie による自動ログイン（他タブ/ブラウザ再起動後の継続）
    if not st.session_state.authenticated:
        c = _read_auth_cookie()
        now_ts = int(datetime.now().timestamp())
        if c:
            valid = c.get("auth") and int(c.get("exp", 0)) > now_ts
            logger.info("check_password: cookie found valid=%s", bool(valid))
            if valid:
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
                    logger.info("login success: session established")
                    st.success("ログインに成功しました！")
                    st.rerun()
                else:
                    logger.info("login failure: wrong password")
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
    # 7日 * 24時間 * 60分 * 60秒 = 604800秒
    timeout_seconds = 7 * 24 * 60 * 60
    timeout_delta = timedelta(seconds=timeout_seconds)
    
    if datetime.now() - st.session_state.auth_time > timeout_delta:
        logger.info("check_session_timeout: expired")
        return False
    
    # セッション時間を更新（スライディング延長）
    st.session_state.auth_time = datetime.now()
    _write_auth_cookie()
    logger.debug("check_session_timeout: renewed session and cookie")
    return True

def logout():
    """
    ログアウト処理を行う
    """
    st.session_state.authenticated = False
    st.session_state.auth_time = None
    _clear_auth_cookie()
    st.rerun()
