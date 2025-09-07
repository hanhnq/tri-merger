import streamlit as st
import sys

st.title("ファイルアップロードテスト")

# デバッグ情報
st.write("## システム情報")
st.write(f"Streamlit Version: {st.__version__}")
st.write(f"Python Version: {sys.version}")

# シンプルなファイルアップロード
st.write("## 単一ファイルアップロード")
single_file = st.file_uploader(
    "ファイルを選択してください（単一）",
    key="single"
)

if single_file is not None:
    st.success("ファイルがアップロードされました！")
    st.write(f"ファイル名: {single_file.name}")
    st.write(f"ファイルサイズ: {single_file.size} bytes")
    st.write(f"ファイルタイプ: {single_file.type}")

# 複数ファイルアップロード
st.write("## 複数ファイルアップロード")
multiple_files = st.file_uploader(
    "ファイルを選択してください（複数）",
    accept_multiple_files=True,
    key="multiple"
)

if multiple_files:
    st.success(f"{len(multiple_files)}個のファイルがアップロードされました！")
    for file in multiple_files:
        st.write(f"- {file.name} ({file.size} bytes)")

# タイプ制限付きアップロード
st.write("## Excelファイルのみ")
excel_file = st.file_uploader(
    "Excelファイルを選択してください",
    type=['xlsx', 'xls'],
    key="excel"
)

if excel_file is not None:
    st.success("Excelファイルがアップロードされました！")
    st.write(f"ファイル名: {excel_file.name}")
    st.write(f"ファイルサイズ: {excel_file.size} bytes")