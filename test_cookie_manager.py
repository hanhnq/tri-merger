import streamlit as st
import extra_streamlit_components as stx
import time

st.title("Cookie Manager Test")

# Get cookie manager
cookie_manager = stx.CookieManager()

# Try to get all cookies
st.write("Getting all cookies...")
all_cookies = cookie_manager.get_all()
st.write("All cookies:", all_cookies)

# Try to get specific cookie
tm_auth = cookie_manager.get(cookie="tm_auth")
st.write("tm_auth cookie:", tm_auth)

# Set a test cookie
if st.button("Set Test Cookie"):
    cookie_manager.set("test_cookie", "test_value", key="set_test")
    st.success("Cookie set!")
    
# Delete test cookie
if st.button("Delete Test Cookie"):
    cookie_manager.delete("test_cookie", key="delete_test")
    st.success("Cookie deleted!")

# Show raw cookies from JavaScript
if st.button("Show Browser Cookies"):
    st.code("""
    // This would show in browser console:
    document.cookie
    """)