import pandas as pd
import io
from datetime import datetime

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
        filename = uploaded_file.name
        if filename.endswith('.xlsx') and not filename.startswith('~'):
            logs.append(f"'{filename}' の処理を開始...")
            
            file_mapping = question_master_df[['質問文', filename]].dropna()
            q_to_text_map = dict(zip(file_mapping[filename], file_mapping['質問文']))
            
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
        
        questions_to_aggregate = group['集計対象の質問文'].tolist()
        
        cols_to_select = ['NO']
        for q in questions_to_aggregate:
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
        
        # 基準ファイルを特定
        file_list = sorted([f.name for f in data_files if f.name.endswith('.xlsx') and not f.name.startswith('~')])
        base_file = file_list[0] if file_list else None
        
        base_mapping_df = pd.DataFrame()
        text_to_q_map = {}
        if base_file:
            # 基準ファイルの質問マッピングを取得
            base_mapping_df = question_master_df[question_master_df.columns.intersection(['質問文', base_file])].copy()
            base_mapping_df = base_mapping_df.rename(columns={base_file: '質問番号'}).dropna()
            text_to_q_map = dict(zip(base_mapping_df['質問文'], base_mapping_df['質問番号']))

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