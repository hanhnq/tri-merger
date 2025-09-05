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
    logs = []
    all_data_list = []
    
    logs.append("--- データ読み込みと変換処理を開始 ---")
    
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
            if filename in question_master_df.columns:
                file_column = filename
            elif original_filename in question_master_df.columns:
                file_column = original_filename
            else:
                # 列名を確認してログ出力
                logging.warning(f"File column not found for {filename} or {original_filename}")
                logging.info(f"Available columns: {list(question_master_df.columns)}")
                continue
                
            file_mapping = question_master_df[['質問文', file_column]].dropna()
            q_to_text_map = dict(zip(file_mapping[file_column], file_mapping['質問文']))
            
            try:
                df_data = pd.read_excel(uploaded_file, sheet_name='data')
                if df_data.empty:
                    logs.append(f"'{filename}' のdataシートは空です。スキップします。")
                    continue

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
        base_file = file_list[0] if file_list else None
        
        base_mapping_df = pd.DataFrame()
        text_to_q_map = {}
        
        # すべてのファイルから質問マッピングを収集（固定質問を含む全質問を確実にマッピング）
        for file_col in question_master_df.columns:
            if file_col != '質問文' and file_col.endswith('.xlsx'):
                temp_mapping = question_master_df[['質問文', file_col]].dropna()
                for _, row in temp_mapping.iterrows():
                    if row['質問文'] not in text_to_q_map:
                        text_to_q_map[row['質問文']] = row[file_col]
        
        # 基準ファイルの情報を取得（出力用）
        if base_file:
            if base_file in question_master_df.columns:
                base_mapping_df = question_master_df[question_master_df.columns.intersection(['質問文', base_file])].copy()
                base_mapping_df = base_mapping_df.rename(columns={base_file: '質問番号'}).dropna()
            else:
                # 元のファイル名で試す
                for f in data_files:
                    if f.name.endswith('.xlsx') and not f.name.startswith('~'):
                        if f.name in question_master_df.columns:
                            base_mapping_df = question_master_df[question_master_df.columns.intersection(['質問文', f.name])].copy()
                            base_mapping_df = base_mapping_df.rename(columns={f.name: '質問番号'}).dropna()
                            break

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
        
        client_results[client_name] = {
            'data': output_client_data,
            'base_file': base_file,
            'mapping': base_mapping_df
        }
        
        logs.append(f"'{client_name}' の集計が完了しました。")
    
    return client_results, merged_df, logs