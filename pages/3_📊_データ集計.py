import streamlit as st
import pandas as pd
import io
from modules.auth import check_password  # 一時的にコメントアウト
from modules.aggregation import aggregate_data

# 認証チェック（一時的にコメントアウト - ファイルアップロード問題の調査のため）
if not check_password():
    st.stop()

st.title("📊 ステップ3: データ集計")
st.markdown("---")

# 進捗インジケーター
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("#### 1️⃣ 質問マスター作成 ✓")
with col2:
    st.markdown("#### 2️⃣ クライアント設定 ✓")
with col3:
    st.markdown("#### 3️⃣ データ集計 ✅")

st.markdown("---")

# セッション状態の初期化
if 'aggregation_results' not in st.session_state:
    st.session_state.aggregation_results = None
if 'logs' not in st.session_state:
    st.session_state.logs = []

# ファイルアップロードセクション
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 1. アンケートデータファイル")
    st.info("📌 ファイルサイズ制限: 各ファイル50MB以内")
    data_files = st.file_uploader(
        "Excelファイルを選択",
        type=['xlsx'],
        accept_multiple_files=True,
        key="data_files",
        help="dataシートを含むアンケートファイルを複数選択できます"
    )

with col2:
    st.markdown("### 2. 質問マスターファイル")
    question_master_file = st.file_uploader(
        "質問マスターを選択",
        type=['xlsx'],
        key="question_master",
        help="質問マスター作成機能で生成したファイルを選択"
    )

with col3:
    st.markdown("### 3. クライアント設定ファイル")
    client_settings_file = st.file_uploader(
        "クライアント設定を選択",
        type=['xlsx'],
        key="client_settings",
        help="クライアント別の集計設定ファイルを選択"
    )

# 集計実行ボタン
if st.button("🚀 集計を実行", type="primary", disabled=not (data_files and question_master_file and client_settings_file)):
    try:
        # ファイルサイズチェック
        for file in data_files:
            if file.size > 50 * 1024 * 1024:  # 50MB
                st.error(f"❌ ファイル '{file.name}' が50MBを超えています。")
                st.stop()
        
        if question_master_file.size > 50 * 1024 * 1024:
            st.error("❌ 質問マスターファイルが50MBを超えています。")
            st.stop()
            
        if client_settings_file.size > 50 * 1024 * 1024:
            st.error("❌ クライアント設定ファイルが50MBを超えています。")
            st.stop()
        
        with st.spinner("データを処理中..."):
            # ファイルの読み込み
            question_master_df = pd.read_excel(question_master_file)
            client_settings_df = pd.read_excel(client_settings_file)
            
            # 集計処理
            results, merged_df, logs = aggregate_data(data_files, question_master_df, client_settings_df)
            
            # 結果を保存
            st.session_state.aggregation_results = results
            st.session_state.merged_df = merged_df
            st.session_state.logs = logs
            
        st.success("✅ 集計が完了しました！")
        
    except PermissionError:
        st.error("❌ ファイルアクセスエラー: ファイルが開かれている可能性があります。")
    except pd.errors.EmptyDataError:
        st.error("❌ 空のファイルが含まれています。")
    except Exception as e:
        st.error(f"❌ エラーが発生しました: {str(e)}")
        st.error("ファイルが破損しているか、形式が正しくない可能性があります。")

# ログ表示
if st.session_state.logs:
    with st.expander("📝 処理ログを表示"):
        for log in st.session_state.logs:
            st.text(log)

# 結果表示とダウンロード
if st.session_state.aggregation_results:
    st.markdown("---")
    st.markdown("## 📥 集計結果のダウンロード")
    
    # 中間データのダウンロード
    if 'merged_df' in st.session_state:
        st.markdown("### 中間データ（全結合データ）")
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            st.session_state.merged_df.to_excel(writer, sheet_name='全結合データ', index=False)

            # Set Calibri font for all cells
            workbook = writer.book
            worksheet = writer.sheets['全結合データ']

            # Create format with Calibri font - force Western charset to prevent Japanese override
            calibri_format = workbook.add_format({
                'font_name': 'Calibri',
                'font_charset': 0  # ANSI_CHARSET - force Western font rendering
            })

            # Apply font to all rows
            for row in range(len(st.session_state.merged_df) + 1):  # +1 for header
                worksheet.set_row(row, None, calibri_format)
        buffer.seek(0)
        
        st.download_button(
            label="📄 中間データをダウンロード",
            data=buffer,
            file_name="中間データ_全件結合済み.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    # クライアント別データのダウンロード
    st.markdown("### クライアント別集計結果")
    
    for client_name, client_info in st.session_state.aggregation_results.items():
        st.markdown(f"#### {client_name}")
        
        # データのプレビュー
        with st.expander(f"{client_name}のデータをプレビュー"):
            st.dataframe(client_info['data'].head(10))
        
        # Excelファイルの作成
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            # データシート
            client_info['data'].to_excel(writer, sheet_name='元データ', index=False)

            # 基準ファイル情報
            base_info_df = pd.DataFrame([{'基準ファイル名': client_info['base_file']}])
            base_info_df.to_excel(writer, sheet_name='基準ファイル情報', index=False)

            # マッピング情報 (新フォーマット: 質問対応表形式)
            mapping_df = None
            formatted_df = None

            if not client_info['mapping'].empty:
                mapping_df = client_info['mapping'].copy()

                # 質問対応表形式の場合 (4列: 番号, 条件, 内容, 区分)
                if '番号' in mapping_df.columns and '内容' in mapping_df.columns:
                    # 質問別にセパレータ行を追加してフォーマット
                    formatted_mapping = []
                    current_question = None

                    for _, row in mapping_df.iterrows():
                        # 質問の開始 (Q-で始まる番号)
                        if str(row['番号']).startswith('Q-'):
                            # 前の質問の後に空行を追加 (最初の質問以外)
                            if current_question is not None:
                                formatted_mapping.append({
                                    '番号': '', '条件': '', '内容': '', '区分': ''
                                })
                            current_question = row['番号']

                        formatted_mapping.append(row.to_dict())

                    # フォーマット済みデータフレームを作成
                    formatted_df = pd.DataFrame(formatted_mapping)
                    formatted_df.to_excel(writer, sheet_name='基準質問マッピング', index=False)
                else:
                    # 古いフォーマットのフォールバック
                    if '質問番号' in mapping_df.columns and '質問文' in mapping_df.columns:
                        mapping_df = mapping_df[['質問番号', '質問文']]
                    mapping_df.to_excel(writer, sheet_name='基準質問マッピング', index=False)

            # Set Calibri font for all sheets - force Western charset
            workbook = writer.book
            calibri_format = workbook.add_format({
                'font_name': 'Calibri',
                'font_charset': 0  # ANSI_CHARSET - force Western font rendering
            })

            # Apply font to all sheets
            for sheet_name, worksheet in writer.sheets.items():
                if sheet_name == '元データ':
                    for row in range(len(client_info['data']) + 1):
                        worksheet.set_row(row, None, calibri_format)
                elif sheet_name == '基準ファイル情報':
                    for row in range(len(base_info_df) + 1):
                        worksheet.set_row(row, None, calibri_format)
                elif sheet_name == '基準質問マッピング':
                    if not client_info['mapping'].empty:
                        # 基準質問マッピング専用のフォーマット設定
                        header_format = workbook.add_format({
                            'font_name': 'Calibri',
                            'font_charset': 0,
                            'bold': True,
                            'border': 1,
                            'bg_color': '#F2F2F2'
                        })

                        question_format = workbook.add_format({
                            'font_name': 'Calibri',
                            'font_charset': 0,
                            'bold': True,
                            'border': 1,
                            'bg_color': '#E6F3FF'
                        })

                        choice_format = workbook.add_format({
                            'font_name': 'Calibri',
                            'font_charset': 0,
                            'border': 1
                        })

                        empty_format = workbook.add_format({
                            'font_name': 'Calibri',
                            'font_charset': 0
                        })

                        # ヘッダー行にフォーマット適用
                        for col in range(4):  # 4列: 番号, 条件, 内容, 区分
                            worksheet.write(0, col, ['番号', '条件', '内容', '区分'][col], header_format)

                        # データ行にフォーマット適用
                        if formatted_df is not None and '番号' in client_info['mapping'].columns:
                            # 新フォーマットの場合: 質問対応表形式
                            for row_idx, (_, row) in enumerate(formatted_df.iterrows(), start=1):
                                row_format = choice_format  # デフォルト

                                # 質問行 (Q-で始まる)
                                if str(row['番号']).startswith('Q-'):
                                    row_format = question_format
                                # 空行
                                elif str(row['番号']).strip() == '':
                                    row_format = empty_format

                                for col_idx, col_name in enumerate(['番号', '条件', '内容', '区分']):
                                    cell_value = row[col_name] if col_name in row else ''
                                    worksheet.write(row_idx, col_idx, cell_value, row_format)

                            # 列幅を自動調整
                            worksheet.set_column('A:A', 10)  # 番号
                            worksheet.set_column('B:B', 12)  # 条件
                            worksheet.set_column('C:C', 50)  # 内容
                            worksheet.set_column('D:D', 8)   # 区分
                        else:
                            # 古いフォーマットのフォールバック
                            if mapping_df is not None:
                                for row in range(len(mapping_df) + 1):
                                    worksheet.set_row(row, None, calibri_format)
        
        buffer.seek(0)
        
        # ダウンロードボタン
        st.download_button(
            label=f"📥 {client_name}の集計結果をダウンロード",
            data=buffer,
            file_name=f"{client_name}_集計結果.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key=f"download_{client_name}"
        )

# 使い方の説明
with st.expander("ℹ️ 使い方"):
    st.markdown("""
    ### データ集計の手順
    
    1. **アンケートデータファイル**: 集計したい複数のアンケートExcelファイルを選択
    2. **質問マスターファイル**: 「質問マスター作成」機能で生成したファイルを選択
    3. **クライアント設定ファイル**: クライアントごとの集計設定を記載したファイルを選択
    4. **集計を実行**: すべてのファイルを選択後、ボタンをクリック
    
    ### 注意事項
    - アンケートファイルには「data」シートが必要です
    - 質問マスターは事前に作成しておく必要があります
    - クライアント設定ファイルの形式は「設定サンプル作成」を参照してください
    
    ### 🔔 固定質問について
    以下の8つの質問は**全クライアントに自動的に含まれます**：
    - あなたの年代性別を教えてください。
    - あなたがお住まいの都道府県をお知らせください。
    - 家族構成を教えてください。
    - あなたの年収を教えてください。
    - 社会人経験は何年間ですか？
    - 最終学歴を教えてください。
    - あなたのお住いの家賃を教えてください。
    - あなたに当てはまる選択肢をお知らせください。
    
    これらの質問は設定ファイルに記載する必要はありません。
    """)

# ナビゲーション
st.markdown("---")
st.markdown("### 🎯 作業完了")
col1, col2 = st.columns([1, 3])
with col1:
    if st.button("← 前へ: クライアント設定", use_container_width=True):
        st.switch_page("pages/2_⚙️_設定サンプル作成.py")
with col2:
    st.success("すべての集計が完了したら、各クライアントのExcelファイルをダウンロードしてください。")