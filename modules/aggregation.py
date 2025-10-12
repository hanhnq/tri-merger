import pandas as pd
import io
from datetime import datetime
import logging

# ログ設定
logging.basicConfig(level=logging.INFO)

# 全クライアントに共通で含まれる固定質問
FIXED_QUESTIONS = [
    'あなたの年代性別を教えてください。',
    'あなたがお住まいの都道府県をお知らせください。',
    '家族構成を教えてください。',
    'あなたの年収を教えてください。',
    '社会人経験は何年間ですか？',
    '最終学歴を教えてください。',
    'あなたのお住いの家賃を教えてください。',
    'あなたに当てはまる選択肢をお知らせください。'
]

def extract_question_mapping_from_survey(uploaded_file):
    """
    アンケートファイルの質問対応表シートから質問とその選択肢を抽出する

    Args:
        uploaded_file: アップロードされたExcelファイル

    Returns:
        list: 質問対応表と同じ形式の辞書のリスト
              [{'番号': 'Q-001', '条件': '必須回答', '内容': '質問文', '区分': 'S/A'},
               {'番号': '1', '条件': '', '内容': '選択肢1', '区分': ''}, ...]
    """
    try:
        # 質問対応表シートが存在するかチェック
        xl_file = pd.ExcelFile(uploaded_file)
        if '質問対応表' not in xl_file.sheet_names:
            return []

        # 質問対応表シートを読み込み
        question_df = pd.read_excel(uploaded_file, sheet_name='質問対応表', header=1)

        # データをクリーンアップ
        mapping_data = []
        for _, row in question_df.iterrows():
            # 空行をスキップ
            if pd.isna(row.iloc[0]) and pd.isna(row.iloc[2]):
                continue

            # 4列の構造に変換
            entry = {
                '番号': str(row.iloc[0]) if pd.notna(row.iloc[0]) else '',
                '条件': str(row.iloc[1]) if pd.notna(row.iloc[1]) else '',
                '内容': str(row.iloc[2]) if pd.notna(row.iloc[2]) else '',
                '区分': str(row.iloc[3]) if pd.notna(row.iloc[3]) else ''
            }
            mapping_data.append(entry)

        return mapping_data

    except Exception as e:
        logging.warning(f"質問対応表の読み込みに失敗: {e}")
        return []


def aggregate_data(data_files, question_master_df, client_settings_df):
    """
    クライアント設定に基づき、アンケートデータを集計し、
    クライアントごとに個別のデータフレームとして返す。
    
    Args:
        data_files: アップロードされたデータファイルのリスト
        question_master_df: 質問マスターデータフレーム
        client_settings_df: クライアント設定データフレーム
    
    Returns:
        dict: クライアント名をキー、データフレームを値とする辞書
        pandas.DataFrame: 中間データ（全結合データ）
        list: ログメッセージのリスト
    """
    # ファイルが空の場合のエラーチェック
    if not data_files:
        raise ValueError("データファイルがアップロードされていません。少なくとも1つのExcelファイルを選択してください。")

    logging.info(f"Received {len(data_files)} data files for aggregation")
    logs = []
    all_data_list = []

    logs.append("--- データ読み込みと変換処理を開始 ---")
    logs.append(f"アップロードされたファイル数: {len(data_files)}")
    for i, f in enumerate(data_files):
        file_size = getattr(f, 'size', 'unknown')
        logs.append(f"  {i+1}. {f.name} (サイズ: {file_size} bytes)")

    # 🆕 質問対応表の包括的データを収集
    comprehensive_question_mapping = []

    for uploaded_file in data_files:
        # ファイル名の文字化け対策（question_master.pyと同じ処理）
        original_filename = uploaded_file.name
        filename = original_filename
        
        # デバッグ用ログ
        logging.info(f"Original filename in aggregation: {repr(original_filename)}")
        
        # 文字化けの検出と修正
        try:
            # 一般的な文字化けパターンをチェック
            if any(ord(c) > 127 and ord(c) < 256 for c in filename):
                # Latin-1でエンコードされた可能性がある場合
                try:
                    filename = filename.encode('latin-1').decode('utf-8')
                except:
                    pass
            
            # それでも文字化けしている場合は、安全なファイル名を生成
            if '�' in filename or any(ord(c) > 0xFFFF for c in filename):
                import hashlib
                # ファイル名のハッシュ値を使用
                file_hash = hashlib.md5(uploaded_file.name.encode('utf-8', errors='ignore')).hexdigest()[:8]
                filename = f"file_{file_hash}.xlsx"
                logging.warning(f"Filename contains invalid characters in aggregation. Using safe name: {filename}")
        except Exception:
            # エラーが発生した場合は、安全なデフォルト名を使用
            import time
            filename = f"file_{int(time.time())}.xlsx"
            
        if filename.endswith('.xlsx') and not filename.startswith('~'):
            logs.append(f"'{filename}' の処理を開始...")
            
            # question_master_dfの列から対応するファイル名の列を探す
            # 文字化けしたファイル名と修正後のファイル名の両方をチェック
            file_column = None
            q_to_text_map = {}

            # 1. 完全一致をチェック
            if filename in question_master_df.columns:
                file_column = filename
            elif original_filename in question_master_df.columns:
                file_column = original_filename
            # 2. Plus_マージ完成データ.xlsx の特別なケース
            elif "Plus_マージ完成データ" in filename:
                for col in question_master_df.columns:
                    if "Plus2" in col and not col.startswith("[コピー]"):
                        file_column = col
                        break
            # 3. 部分一致での検索（fallback）
            else:
                # ファイル名の主要部分を抽出して検索
                clean_filename = filename.replace(".xlsx", "")
                for col in question_master_df.columns:
                    if col.endswith('.xlsx') and clean_filename in col:
                        file_column = col
                        break

            if file_column:
                file_mapping = question_master_df[['質問文', file_column]].dropna()
                q_to_text_map = dict(zip(file_mapping[file_column], file_mapping['質問文']))
                logs.append(f"'{filename}' の質問マッピングを取得しました。({len(q_to_text_map)}個の質問)")
            else:
                # 具体的なファイルマッピングが見つからない場合でも、ファイルを処理する
                # すべてのファイルから利用可能なマッピングを収集
                logs.append(f"'{filename}' (元: '{original_filename}') に対応する列が見つかりません。")
                logs.append(f"利用可能な列: {[col for col in question_master_df.columns if col.endswith('.xlsx')]}")

                # 汎用マッピングとして最初に見つかったファイルのマッピングを使用
                first_file_col = None
                for col in question_master_df.columns:
                    if col != '質問文' and col.endswith('.xlsx'):
                        first_file_col = col
                        break

                if first_file_col:
                    temp_mapping = question_master_df[['質問文', first_file_col]].dropna()
                    q_to_text_map = dict(zip(temp_mapping[first_file_col], temp_mapping['質問文']))
                    logs.append(f"'{filename}' では '{first_file_col}' のマッピングを代替使用します。({len(q_to_text_map)}個の質問)")
                else:
                    logs.append(f"'{filename}' では利用可能なマッピングがありません。元の列名を使用します。")

                logging.warning(f"File column not found for {filename} or {original_filename}. Using generic mapping from {first_file_col}.")
                logging.info(f"Available columns: {list(question_master_df.columns)}")
            
            try:
                df_data = pd.read_excel(uploaded_file, sheet_name='data')
                if df_data.empty:
                    logs.append(f"'{filename}' のdataシートは空です。スキップします。")
                    continue

                # 🆕 このファイルの質問対応表データを抽出して追加
                file_question_mapping = extract_question_mapping_from_survey(uploaded_file)
                if file_question_mapping:
                    comprehensive_question_mapping.extend(file_question_mapping)
                    logs.append(f"'{filename}' から {len(file_question_mapping)} 行の質問対応表データを抽出")

                new_columns = {}
                for col in df_data.columns:
                    if col in q_to_text_map:
                        new_columns[col] = q_to_text_map[col]
                    else:
                        for q_num, q_text in q_to_text_map.items():
                            if str(col).startswith(q_num + '_'):
                                suffix = str(col).replace(q_num, '')
                                new_columns[col] = f"{q_text}{suffix}"
                                break
                df_data.rename(columns=new_columns, inplace=True)
                
                all_data_list.append(df_data)
                logs.append(f"'{filename}' のデータを読み込み完了。({len(df_data)}件)")

            except Exception as e:
                logs.append(f"'{filename}' のデータシート処理中にエラー: {e}")

    if not all_data_list:
        raise ValueError("集計対象のデータが見つかりませんでした。")
    
    logs.append("--- 全データの結合処理を開始 ---")
    merged_df = pd.concat(all_data_list, ignore_index=True, sort=False)
    logs.append(f"全ファイルのデータを結合しました。合計: {len(merged_df)}件")

    if '回答日時' in merged_df.columns:
        merged_df['回答日時'] = pd.to_datetime(merged_df['回答日時'], errors='coerce')
        merged_df.dropna(subset=['回答日時'], inplace=True)
        merged_df.sort_values(by='回答日時', inplace=True)
        logs.append(f"回答日時でソートしました。")

    # クライアント別の集計
    client_results = {}
    logs.append("--- クライアント別集計処理を開始 ---")
    
    for client_name, group in client_settings_df.groupby('クライアント名'):
        logs.append(f"'{client_name}' の集計を開始します...")
        
        # クライアント設定から質問を取得
        questions_to_aggregate = group['集計対象の質問文'].tolist()
        
        # 固定質問を追加（重複を除外）
        all_questions = list(dict.fromkeys(FIXED_QUESTIONS + questions_to_aggregate))
        logs.append(f"'{client_name}' には固定質問を含む合計 {len(all_questions)} 個の質問を集計します。")
        
        cols_to_select = ['NO']
        for q in all_questions:
            if q in merged_df.columns:
                cols_to_select.append(q)
            for col in merged_df.columns:
                if str(col).startswith(q + '_'):
                    cols_to_select.append(col)
        
        cols_to_select = list(dict.fromkeys(cols_to_select))
        
        if '回答日時' in merged_df.columns:
            cols_to_select.append('回答日時')
        
        if len(cols_to_select) <= 1:
            logs.append(f"'{client_name}' の集計対象の質問がデータ内に見つかりませんでした。")
            continue
            
        client_data = merged_df[cols_to_select]
        
        base_mapping_df = pd.DataFrame()
        text_to_q_map = {}
        
        # すべてのファイルから質問マッピングを収集（固定質問を含む全質問を確実にマッピング）
        for file_col in question_master_df.columns:
            if file_col != '質問文' and file_col.endswith('.xlsx'):
                temp_mapping = question_master_df[['質問文', file_col]].dropna()
                for _, row in temp_mapping.iterrows():
                    if row['質問文'] not in text_to_q_map:
                        text_to_q_map[row['質問文']] = row[file_col]
        
        # 🆕 質問対応表形式のマッピングを作成（質問 + 選択肢を含む）
        # クライアントの質問リストに該当する質問対応表データを抽出
        client_mapping_data = []

        for question_text in all_questions:
            # comprehensive_question_mapping から該当する質問とその選択肢を探す
            question_found = False
            for mapping_entry in comprehensive_question_mapping:
                # 質問のメイン行を探す（番号がQ-で始まり、内容が質問文と一致）
                if (mapping_entry['番号'].startswith('Q-') and
                    mapping_entry['内容'] == question_text):

                    # 質問のメイン行を追加
                    client_mapping_data.append(mapping_entry)
                    question_found = True

                    # この質問の選択肢も探して追加
                    question_index = comprehensive_question_mapping.index(mapping_entry)

                    # 質問の直後から次の質問までの選択肢を収集
                    for i in range(question_index + 1, len(comprehensive_question_mapping)):
                        choice_entry = comprehensive_question_mapping[i]

                        # 次の質問（Q-で始まる）が見つかったら停止
                        if choice_entry['番号'].startswith('Q-'):
                            break

                        # 選択肢（数字の番号で内容がある）を追加
                        if (choice_entry['番号'].isdigit() and
                            choice_entry['内容'].strip()):
                            client_mapping_data.append(choice_entry)

                    break

            # もし質問対応表に見つからない場合は、従来の方法でフォールバック
            if not question_found:
                matching_rows = question_master_df[question_master_df['質問文'] == question_text]
                if not matching_rows.empty:
                    row = matching_rows.iloc[0]
                    for col in question_master_df.columns:
                        if col.endswith('.xlsx') and pd.notna(row[col]):
                            client_mapping_data.append({
                                '番号': row[col],
                                '条件': '',
                                '内容': question_text,
                                '区分': ''
                            })
                            break

        # DataFrameを作成
        if client_mapping_data:
            base_mapping_df = pd.DataFrame(client_mapping_data)
            # 列の順序を調整
            base_mapping_df = base_mapping_df[['番号', '条件', '内容', '区分']]
        else:
            # フォールバック：空のDataFrame
            base_mapping_df = pd.DataFrame(columns=['番号', '条件', '内容', '区分'])

        logs.append(f"'{client_name}' のマッピング: {len(base_mapping_df)}行（質問+選択肢を含む）")

        # client_dataの列名を質問文から質問番号へ再変換（FA列も考慮）
        final_rename_map = {}
        for col_name in client_data.columns:
            # FA列などのサフィックスが付いているかチェック
            is_suffixed = False
            for q_text, q_num in text_to_q_map.items():
                if str(col_name).startswith(q_text + '_'):
                    suffix = str(col_name).replace(q_text, '')
                    final_rename_map[col_name] = q_num + suffix
                    is_suffixed = True
                    break
            # サフィックスがなく、完全一致する場合
            if not is_suffixed and col_name in text_to_q_map:
                final_rename_map[col_name] = text_to_q_map[col_name]

        output_client_data = client_data.rename(columns=final_rename_map)

        # 基準ファイルを特定（文字化け対策済みのファイル名を使用）
        file_list = []
        for f in data_files:
            if f.name.endswith('.xlsx') and not f.name.startswith('~'):
                # 同じ文字化け対策処理を適用
                fname = f.name
                try:
                    if any(ord(c) > 127 and ord(c) < 256 for c in fname):
                        try:
                            fname = fname.encode('latin-1').decode('utf-8')
                        except:
                            pass
                    if '�' in fname or any(ord(c) > 0xFFFF for c in fname):
                        import hashlib
                        file_hash = hashlib.md5(f.name.encode('utf-8', errors='ignore')).hexdigest()[:8]
                        fname = f"file_{file_hash}.xlsx"
                except:
                    import time
                    fname = f"file_{int(time.time())}.xlsx"
                file_list.append(fname)

        file_list = sorted(file_list)
        base_file = file_list[0] if file_list else f"{client_name}専用マッピング"

        client_results[client_name] = {
            'data': output_client_data,
            'base_file': base_file,
            'mapping': base_mapping_df
        }
        
        logs.append(f"'{client_name}' の集計が完了しました。")
    
    return client_results, merged_df, logs