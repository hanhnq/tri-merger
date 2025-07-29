import streamlit as st
import pandas as pd
import io
from modules.auth import check_password

# 認証チェック
if not check_password():
    # ログイン前はサイドバーを非表示
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {
                display: none;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.stop()

# 認証後はサイドバーを表示
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            display: block;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("⚙️ ステップ2: クライアント設定")
st.markdown("---")

# 進捗インジケーター
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("#### 1️⃣ 質問マスター作成 ✓")
with col2:
    st.markdown("#### 2️⃣ クライアント設定 ✅")
with col3:
    st.markdown("#### 3️⃣ データ集計")

st.markdown("---")

st.markdown("""
### クライアント設定ファイルとは？
どのクライアントにどの質問を集計するかを定義するファイルです。
このファイルに基づいて、データ集計機能が各クライアント向けの
Excelファイルを自動生成します。
""")

# サンプルデータの作成
def create_sample_settings():
    """サンプル用のクライアント設定データを作成"""
    data = {
        'クライアント名': [
            'A社', 
            'A社', 
            'A社',
            'B社',
            'B社',
            'C社'
        ],
        '集計対象の質問文': [
            'あなたの年代を教えてください。',
            'あなたの性別を教えてください。',
            '〇〇というサービスを知っていますか？',
            '〇〇というサービスを利用したことがありますか？',
            '〇〇の満足度を教えてください。',
            'あなたの年代を教えてください。'
        ]
    }
    return pd.DataFrame(data)

# サンプルの表示
st.markdown("## 📋 設定ファイルのサンプル")
sample_df = create_sample_settings()
st.dataframe(sample_df)

# 説明
st.markdown("""
### 📝 設定方法

1. **クライアント名**: 集計結果を分けたいクライアントの名前を入力
2. **集計対象の質問文**: そのクライアントに必要な質問文を正確に入力

### ⚠️ 注意事項

- 質問文は**質問マスター**に記載されているものと完全に一致する必要があります
- 同じクライアントに複数の質問を集計したい場合は、行を追加してください
- 質問文に関連するFA（自由回答）列も自動的に含まれます
""")

# ダウンロードボタン
st.markdown("---")
st.markdown("## 📥 サンプルファイルのダウンロード")

# Excelファイルの作成
buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    sample_df.to_excel(writer, sheet_name='設定', index=False)
    
    # 説明シートの追加
    explanation_data = {
        '項目': ['クライアント名', '集計対象の質問文'],
        '説明': [
            '集計結果を分けたいクライアントの名前を入力してください',
            '質問マスターに記載されている質問文を正確に入力してください'
        ],
        '例': [
            'A社、B社、C社など',
            'あなたの年代を教えてください。'
        ]
    }
    explanation_df = pd.DataFrame(explanation_data)
    explanation_df.to_excel(writer, sheet_name='説明', index=False)
    
buffer.seek(0)

st.download_button(
    label="📄 設定サンプルをダウンロード",
    data=buffer,
    file_name="client_settings_sample.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# 使い方のガイド
with st.expander("ℹ️ 設定ファイルの使い方"):
    st.markdown("""
    ### 手順
    
    1. **サンプルをダウンロード**: 上のボタンからサンプルファイルをダウンロード
    2. **内容を編集**: 
        - クライアント名を実際のクライアント名に変更
        - 集計対象の質問文を質問マスターから正確にコピー
    3. **ファイル名を変更**: `client_settings.xlsx` として保存
    4. **データ集計で使用**: データ集計ページでこのファイルをアップロード
    
    ### よくある質問
    
    **Q: 質問文はどこから取得すればいいですか？**
    A: 「質問マスター作成」機能で生成したファイルの「質問文」列からコピーしてください。
    
    **Q: 一つのクライアントに複数の質問を設定できますか？**
    A: はい、同じクライアント名で複数行作成することで、複数の質問を集計できます。
    
    **Q: FA（自由回答）も含まれますか？**
    A: はい、指定した質問に関連するFA列（例：Q-1_FA）も自動的に含まれます。
    """)

# 次のステップへのナビゲーション
st.markdown("---")
st.markdown("### 🚀 次のステップ")
st.info("設定ファイルを作成したら、左のメニューから「3️⃣ 📊 データ集計」を選択してください。")