import streamlit as st
from modules.auth import check_password, logout

# Debug patch for reindex errors
try:
    exec(open('debug_reindex_error.py').read())
except:
    pass

# ページ設定
st.set_page_config(
    page_title="アンケート集計システム",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"  # 常に展開状態
)

# 認証チェック
if not check_password():
    st.stop()

# メインページのレイアウト
st.title("📊 アンケート集計システム")
st.markdown("---")

# サイドバーの設定
with st.sidebar:
    st.markdown("## ナビゲーション")
    st.markdown("左側のメニューから機能を選択してください")
    st.markdown("---")
    
    # ログアウトボタン
    if st.button("🚪 ログアウト", use_container_width=True):
        logout()

# メインコンテンツ
st.markdown("""
## 🚀 作業の流れ

このシステムを使用するには、以下の3つのステップを順番に実行してください：
""")

# ステップガイド
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### ステップ 1️⃣
    #### 📝 質問マスター作成
    
    アンケートファイルから質問の対応表を作成します。
    
    - 複数のExcelファイルをアップロード
    - 質問番号と質問文の対応を自動生成
    - マスターファイルをダウンロード
    
    **必要なもの**: アンケートExcelファイル（複数可）
    """)
    if st.button("📝 質問マスター作成へ", use_container_width=True):
        st.switch_page("pages/1_📝_質問マスター作成.py")

with col2:
    st.markdown("""
    ### ステップ 2️⃣
    #### ⚙️ クライアント設定
    
    どのクライアントにどの質問を集計するか設定します。
    
    - サンプルファイルをダウンロード
    - クライアント名と質問を設定
    - 設定ファイルとして保存
    
    **必要なもの**: 質問マスター（参照用）
    """)
    if st.button("⚙️ 設定サンプル作成へ", use_container_width=True):
        st.switch_page("pages/2_⚙️_設定サンプル作成.py")

with col3:
    st.markdown("""
    ### ステップ 3️⃣
    #### 📊 データ集計実行
    
    設定に基づいてデータを集計します。
    
    - 全ファイルをアップロード
    - 自動集計を実行
    - クライアント別にダウンロード
    
    **必要なもの**: 
    - アンケートデータ
    - 質問マスター
    - クライアント設定
    """)
    if st.button("📊 データ集計へ", use_container_width=True):
        st.switch_page("pages/3_📊_データ集計.py")

st.markdown("---")

# システム概要
with st.expander("📖 システムの詳細説明"):
    st.markdown("""
    ### システム概要
    
    このシステムは、複数のアンケートExcelファイルからデータを統合し、
    クライアントごとに必要な質問項目を抽出・集計するためのWebアプリケーションです。
    
    ### 主な特徴
    
    - **自動マッピング**: 異なるファイル間で質問番号が違っても自動で対応
    - **柔軟な設定**: クライアントごとに必要な質問を自由に選択
    - **一括処理**: 複数ファイルを一度に処理可能
    - **Excel出力**: 結果は使い慣れたExcel形式で出力
    
    ### 注意事項
    
    - アップロードするExcelファイルには「質問対応表」と「data」シートが必要です
    - ファイル名は日本語でも問題ありません
    - 大量のデータを処理する場合は時間がかかることがあります
    """)

# フッター
st.markdown("---")
st.markdown("© 2024 アンケート集計システム")