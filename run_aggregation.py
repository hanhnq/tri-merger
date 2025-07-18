import os
import pandas as pd
import logging
from datetime import datetime

def setup_logging():
    """ロギングを設定する"""
    log_filename = os.path.join('result', f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

def aggregate_data(data_dir, question_master_path, client_settings_path, result_dir):
    """
    クライアント設定に基づき、アンケートデータを集計し、
    クライアントごとに個別のExcelファイルとして出力する。
    """
    try:
        df_master = pd.read_excel(question_master_path)
        df_settings = pd.read_excel(client_settings_path)
    except FileNotFoundError as e:
        logging.error(f"エラー: 必要なファイルが見つかりません。 {e}")
        return

    all_data_list = []
    
    logging.info("--- データ読み込みと変換処理を開始 ---")
    for filename in os.listdir(data_dir):
        if filename.endswith('.xlsx') and not filename.startswith('~'):
            filepath = os.path.join(data_dir, filename)
            logging.info(f"'{filename}' の処理を開始...")
            
            file_mapping = df_master[['質問文', filename]].dropna()
            q_to_text_map = dict(zip(file_mapping[filename], file_mapping['質問文']))
            
            try:
                df_data = pd.read_excel(filepath, sheet_name='data')
                if df_data.empty:
                    logging.warning(f"'{filename}' のdataシートは空です。スキップします。")
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
                logging.info(f"'{filename}' のデータを読み込み完了。({len(df_data)}件)")

            except Exception as e:
                logging.error(f"'{filename}' のデータシート処理中にエラー: {e}")

    if not all_data_list:
        logging.error("集計対象のデータが見つかりませんでした。")
        return
    
    logging.info("--- 全データの結合処理を開始 ---")
    merged_df = pd.concat(all_data_list, ignore_index=True, sort=False)
    logging.info(f"全ファイルのデータを結合しました。合計: {len(merged_df)}件")

    if '回答日時' in merged_df.columns:
        merged_df['回答日時'] = pd.to_datetime(merged_df['回答日時'], errors='coerce')
        merged_df.dropna(subset=['回答日時'], inplace=True)
        merged_df.sort_values(by='回答日時', inplace=True)
        logging.info(f"回答日時でソートしました。")
        
        # original_count = len(merged_df)
        # merged_df = merged_df.head(100)
        # logging.info(f"先頭100件を抽出しました。(元の件数: {original_count} -> 抽出後: {len(merged_df)})")

    # 中間ファイルを出力
    intermediate_path = os.path.join(result_dir, '中間データ_全件結合済み.xlsx')
    merged_df.to_excel(intermediate_path, index=False)
    logging.info(f"中間ファイルを '{intermediate_path}' に保存しました。")


    logging.info("--- クライアント別集計処理を開始 ---")
    for client_name, group in df_settings.groupby('クライアント名'):
        logging.info(f"'{client_name}' の集計を開始します...")
        
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
            logging.warning(f"'{client_name}' の集計対象の質問がデータ内に見つかりませんでした。")
            continue
            
        client_data = merged_df[cols_to_select]
        
        output_filename = os.path.join(result_dir, f"{client_name}_集計結果.xlsx")
        
        # --- 出力前に列名を質問文から基準ファイルの質問番号に戻す ---
        # 基準ファイルを特定
        file_list = sorted([f for f in os.listdir(data_dir) if f.endswith('.xlsx') and not f.startswith('~')])
        base_file = file_list[0] if file_list else None
        
        base_mapping_df = pd.DataFrame()
        text_to_q_map = {}
        if base_file:
            # 基準ファイルの質問マッピングを取得
            base_mapping_df = df_master[df_master.columns.intersection(['質問文', base_file])].copy()
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
        
        # 基準ファイル情報をDataFrameにする
        base_info_df = pd.DataFrame([{'基準ファイル名': base_file}])

        with pd.ExcelWriter(output_filename) as writer:
            output_client_data.to_excel(writer, sheet_name='元データ', index=False)
            base_info_df.to_excel(writer, sheet_name='基準ファイル情報', index=False)
            if not base_mapping_df.empty:
                base_mapping_df.to_excel(writer, sheet_name='基準質問マッピング', index=False)
            
        logging.info(f"'{client_name}' の集計結果を '{output_filename}' に保存しました。")


if __name__ == '__main__':
    setup_logging()
    DATA_DIR = 'data'
    RESULT_DIR = 'result'
    QUESTION_MASTER_PATH = os.path.join(RESULT_DIR, '質問マスター.xlsx')
    CLIENT_SETTINGS_PATH = 'client_settings.xlsx'
    
    if not os.path.exists(RESULT_DIR):
        os.makedirs(RESULT_DIR)
        
    aggregate_data(DATA_DIR, QUESTION_MASTER_PATH, CLIENT_SETTINGS_PATH, RESULT_DIR)
