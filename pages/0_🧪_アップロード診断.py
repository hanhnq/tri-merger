import streamlit as st
import sys

st.set_page_config(page_title="🧪 アップロード診断", page_icon="🧪", layout="wide")

st.title("🧪 アップロード診断")
st.info("Squadbase配下でのファイルアップロード挙動を切り分けます。")

with st.expander("🔧 環境情報"):
    st.write({
        "python": sys.version,
        "streamlit": st.__version__,
        "baseUrlPath": st.runtime.get_instance().server.base_url_path if hasattr(st, "runtime") else "N/A",
        "session_state_keys": list(st.session_state.keys()),
    })

st.markdown("---")

st.header("1. 単一ファイルアップロード")
single = st.file_uploader("単一ファイル", key="diag_single", accept_multiple_files=False)
if single is not None:
    st.success(f"受信: {single.name} ({single.size:,} bytes)")
    # 先頭1KBだけ読む（I/O確認）
    head = single.read(1024)
    st.code(head[:64])

st.header("2. 複数ファイルアップロード")
multi = st.file_uploader("複数ファイル", key="diag_multi", accept_multiple_files=True)
if multi:
    st.success(f"受信ファイル数: {len(multi)}")
    for i, f in enumerate(multi, 1):
        st.write(f"{i}. {f.name} ({f.size:,} bytes)")

st.header("3. Excel限定（拡張子制限）")
excel = st.file_uploader("Excelのみ", type=["xlsx", "xls"], key="diag_excel")
if excel is not None:
    st.success(f"受信: {excel.name} ({excel.size:,} bytes)")

st.caption("注: このページは診断専用で、受信ファイルは保存しません。")

