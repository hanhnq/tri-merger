import streamlit as st
import pandas as pd
import io
# from modules.auth import check_password  # 一時的にコメントアウト
from modules.question_master import create_question_master

# 認証チェック（一時的にコメントアウト - ファイルアップロード問題の調査のため）
# if not check_password():
#     st.stop()

st.title("📝 ステップ1: 質問マスター作成")
st.markdown("---")

# 進捗インジケーター
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("#### 1️⃣ 質問マスター作成 ✅")
with col2:
    st.markdown("#### 2️⃣ クライアント設定")
with col3:
    st.markdown("#### 3️⃣ データ集計")

st.markdown("---")

st.markdown("""
### 質問マスターとは？
アンケートファイル間で質問番号が異なる場合に、質問文をキーとして
各ファイルの質問番号を対応付けるマスターファイルです。
""")

# ファイルアップロード
st.markdown("### アンケートファイルをアップロード")
st.info("📌 ファイルサイズ制限: 各ファイル50MB以内")
uploaded_files = st.file_uploader(
    "Excelファイルを選択（複数可）",
    type=['xlsx'],
    accept_multiple_files=True,
    help="質問対応表シートを含むアンケートファイルを選択してください"
)

# アップロードされたファイルの情報を表示
if uploaded_files:
    st.success(f"✅ {len(uploaded_files)}個のファイルがアップロードされました")
    with st.expander("アップロードファイル詳細"):
        for i, file in enumerate(uploaded_files):
            st.text(f"{i+1}. {file.name} - {file.size:,} bytes")

# 作成ボタン
if st.button("📋 質問マスターを作成", type="primary", disabled=not uploaded_files):
    try:
        # デバッグ情報を表示
        st.info(f"📂 {len(uploaded_files)}個のファイルを処理中...")
        for i, file in enumerate(uploaded_files):
            st.text(f"  - ファイル{i+1}: {file.name} ({file.size:,} bytes)")
        
        with st.spinner("質問マスターを作成中..."):
            # 質問マスター作成
            master_df = create_question_master(uploaded_files)
            
            # セッション状態に保存
            st.session_state.question_master = master_df
            
        st.success("✅ 質問マスターの作成が完了しました！")
        
    except ValueError as e:
        st.error(f"⚠️ 入力エラー: {str(e)}")
    except Exception as e:
        st.error(f"❌ エラーが発生しました: {str(e)}")
        st.error(f"エラータイプ: {type(e).__name__}")
        import traceback
        st.text("詳細なエラー情報:")
        st.code(traceback.format_exc())

# 結果表示
if 'question_master' in st.session_state:
    st.markdown("---")
    st.markdown("## 📊 作成された質問マスター")
    
    # プレビュー
    st.markdown("### プレビュー")
    st.dataframe(st.session_state.question_master)
    
    # 統計情報
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("質問数", len(st.session_state.question_master))
    with col2:
        file_cols = [col for col in st.session_state.question_master.columns if col not in ['質問文', '初出ファイル']]
        st.metric("ファイル数", len(file_cols))
    with col3:
        coverage = st.session_state.question_master[file_cols].notna().sum().sum()
        total = len(st.session_state.question_master) * len(file_cols)
        st.metric("カバー率", f"{coverage/total*100:.1f}%")
    
    # ダウンロード
    st.markdown("### 📥 ダウンロード")
    
    # Excelファイルの作成
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        st.session_state.question_master.to_excel(writer, index=False)
    buffer.seek(0)
    
    st.download_button(
        label="📄 質問マスターをダウンロード",
        data=buffer,
        file_name="質問マスター.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# 使い方の説明
with st.expander("ℹ️ 使い方"):
    st.markdown("""
    ### 質問マスター作成の手順
    
    1. **ファイルアップロード**: 質問対応表を含むアンケートExcelファイルを複数選択
    2. **作成実行**: 「質問マスターを作成」ボタンをクリック
    3. **確認**: 作成された質問マスターをプレビューで確認
    4. **ダウンロード**: 質問マスターファイルをダウンロード
    
    ### 注意事項
    - アップロードするファイルには「質問対応表」シートが必要です
    - 質問対応表の3行目がヘッダー、4行目以降がデータとして処理されます
    - 質問番号は「Q-」で始まる形式である必要があります
    - ファイル名でソートし、最初のファイルを基準として質問の並び順を決定します
    """)

# 次のステップへのナビゲーション
st.markdown("---")
st.markdown("### 🚀 次のステップ")
col1, col2 = st.columns([3, 1])
with col1:
    st.info("質問マスターを作成したら、次はクライアント設定を行います。")
with col2:
    if st.button("次へ: クライアント設定 →", type="primary", use_container_width=True):
        st.switch_page("pages/2_⚙️_設定サンプル作成.py")