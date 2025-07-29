import pandas as pd
import io
import logging

# ログ設定
logging.basicConfig(level=logging.INFO)

def create_question_master(uploaded_files):
    """
    アップロードされたExcelファイルから「質問対応表」を読み込み、
    質問マスターファイルを作成する。
    
    Args:
        uploaded_files: Streamlitのfile_uploaderから取得したファイルリスト
    
    Returns:
        pandas.DataFrame: 質問マスターデータフレーム
    """
    master_list = []
    
    for uploaded_file in uploaded_files:
        # ファイル名の文字化け対策
        original_filename = uploaded_file.name
        filename = original_filename
        
        # デバッグ用ログ
        logging.info(f"Original filename: {repr(original_filename)}")
        logging.info(f"Filename bytes: {original_filename.encode('utf-8', errors='replace')}")
        
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
                logging.warning(f"Filename contains invalid characters. Using safe name: {filename}")
        except Exception:
            # エラーが発生した場合は、安全なデフォルト名を使用
            import time
            filename = f"file_{int(time.time())}.xlsx"
        
        if filename.endswith('.xlsx') and not filename.startswith('~'):
            try:
                # ヘッダーなしで読み込み、手動で設定する
                df_q = pd.read_excel(uploaded_file, sheet_name='質問対応表', header=None)
                
                # 3行目(index=2)をヘッダーとして設定
                df_q.columns = df_q.iloc[2]
                # 4行目(index=3)以降をデータとして使用
                df_q = df_q.iloc[3:].reset_index(drop=True)

                # 必要な列だけを抽出
                df_q = df_q[['番号', '内容']]
                # 質問文が書かれている行のみを抽出（'番号'列が'Q-'で始まる行）
                df_q = df_q[df_q['番号'].astype(str).str.startswith('Q-')].copy()
                
                # ファイル名を保存（文字化け対策済み）
                df_q['ファイル名'] = filename
                # 元のファイル名も保存（表示用）
                df_q['元ファイル名'] = original_filename
                master_list.append(df_q)

            except Exception as e:
                raise Exception(f"Error processing {filename}: {e}")

    if not master_list:
        raise ValueError("読み込むファイルが見つかりませんでした。")

    master_df = pd.concat(master_list, ignore_index=True)
    master_df.rename(columns={'番号': '質問番号', '内容': '質問文'}, inplace=True)

    # 基準となるファイル（ファイル名でソートして最初のファイル）を特定
    file_list = sorted(list(set([df['ファイル名'].iloc[0] for df in master_list])))
    if not file_list:
        raise ValueError("基準となるファイルが見つかりません。")
    base_file = file_list[0]
    
    # 基準ファイルの質問順序を保持（重複を除外）
    base_order_df = master_df[master_df['ファイル名'] == base_file][['質問文']].drop_duplicates().copy()
    
    # 質問文をキーにしてピボット処理
    pivot_df = master_df.pivot_table(
        index='質問文',
        columns='ファイル名',
        values='質問番号',
        aggfunc='first'
    ).reset_index()

    # 基準ファイルの質問リストを取得
    base_questions_list = base_order_df['質問文'].tolist()

    # pivot_dfを基準ファイルの質問とそれ以外に分割
    df_base = pivot_df[pivot_df['質問文'].isin(base_questions_list)].copy()
    df_other = pivot_df[~pivot_df['質問文'].isin(base_questions_list)].copy()

    # 基準ファイルの質問をその順序通りにソート
    df_base['質問文'] = pd.Categorical(df_base['質問文'], categories=base_questions_list, ordered=True)
    df_base = df_base.sort_values('質問文')

    # その他の質問を質問文でソート
    df_other = df_other.sort_values('質問文')

    # 2つのDataFrameを結合
    final_df = pd.concat([df_base, df_other], ignore_index=True)

    # 各質問が最初に登場したファイルを取得
    master_df_sorted = master_df.sort_values('ファイル名')
    first_appearance = master_df_sorted.groupby('質問文')['ファイル名'].first().reset_index()
    first_appearance.rename(columns={'ファイル名': '初出ファイル'}, inplace=True)

    # 初出ファイル情報をマージ
    final_df = pd.merge(final_df, first_appearance, on='質問文', how='left')

    # 列の順序を調整（初出ファイルを質問文の隣に）
    cols = final_df.columns.tolist()
    cols.insert(1, cols.pop(cols.index('初出ファイル')))
    final_df = final_df[cols]

    # すべてのファイルで質問番号が存在しない行（完全に空の行）を削除
    file_columns = [f for f in final_df.columns if f not in ['質問文', '初出ファイル']]
    cleaned_df = final_df.dropna(subset=file_columns, how='all')

    return cleaned_df