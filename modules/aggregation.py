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
    # Debug print to console and file
    debug_msg = f"\n=== AGGREGATE_DATA CALLED ===\n"
    debug_msg += f"Number of data_files received: {len(data_files)}\n"
    for i, f in enumerate(data_files):
        debug_msg += f"  File {i+1}: {f.name} (size: {f.size} bytes)\n"
    debug_msg += "=" * 30 + "\n"
    
    print(debug_msg)
    
    # Also write to file for debugging
    with open(r"D:\python\tri-merger\debug_log.txt", "w", encoding="utf-8") as f:
        f.write(debug_msg)
    
    # ファイルが空の場合のエラーチェック
    if not data_files:
        raise ValueError("データファイルがアップロードされていません。少なくとも1つのExcelファイルを選択してください。")
    
    logging.info(f"Received {len(data_files)} data files for aggregation")
    logs = []
    all_data_list = []
    
    logs.append("--- データ読み込みと変換処理を開始 ---")
    logs.append(f"アップロードされたファイル数: {len(data_files)}")
    for i, f in enumerate(data_files):
        logs.append(f"  {i+1}. {f.name} (サイズ: {f.size} bytes)")
    
    # 全ファイルから統合マッピングを作成（90個の質問すべてをカバー）
    global_q_to_text_map = {}
    for col in question_master_df.columns:
        if col != '質問文' and col != '初出ファイル' and col.endswith('.xlsx'):
            temp_mapping = question_master_df[['質問文', col]].dropna()
            for _, row in temp_mapping.iterrows():
                # まだマッピングされていない質問のみ追加
                if row[col] not in global_q_to_text_map:
                    global_q_to_text_map[row[col]] = row['質問文']
    
    logs.append(f"統合マッピングを作成: {len(global_q_to_text_map)}個の質問コードをテキストにマッピング")
    logs.append(f"question_masterから検出された総質問数: {len(question_master_df)}個")
    
    print(f"🔍 DEBUG: Starting to process {len(data_files)} files")

    for uploaded_file in data_files:
        print(f"🔍 DEBUG: Processing file: {uploaded_file.name}")

        # ファイル名の文字化け対策（question_master.pyと同じ処理）
        original_filename = uploaded_file.name
        filename = original_filename

        # デバッグ用ログ
        logging.info(f"Original filename in aggregation: {repr(original_filename)}")
        print(f"🔍 DEBUG: Original filename: {repr(original_filename)}")
        
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
            
            if filename in question_master_df.columns:
                file_column = filename
            elif original_filename in question_master_df.columns:
                file_column = original_filename
            
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
                print(f"🔍 DEBUG: About to read Excel file: {filename}")
                df_data = pd.read_excel(uploaded_file, sheet_name='data')
                print(f"✅ DEBUG: Successfully read Excel: {len(df_data)} rows, {len(df_data.columns)} columns")
                logs.append(f"'{filename}' のdataシートを読み込み。元データ: {len(df_data)}行, {len(df_data.columns)}列")
                
                if df_data.empty:
                    logs.append(f"'{filename}' のdataシートは空です。スキップします。")
                    continue

                # グローバルマッピングを使用してすべての列をrename
                new_columns = {}
                mapped_count = 0
                for col in df_data.columns:
                    if col in global_q_to_text_map:
                        new_columns[col] = global_q_to_text_map[col]
                        mapped_count += 1
                    else:
                        # サフィックス付きの列をチェック（例: Q-001_1, Q-001_2など）
                        for q_num, q_text in global_q_to_text_map.items():
                            if str(col).startswith(q_num + '_'):
                                suffix = str(col).replace(q_num, '')
                                new_columns[col] = f"{q_text}{suffix}"
                                mapped_count += 1
                                break
                
                logs.append(f"'{filename}' で {mapped_count}/{len(df_data.columns)} 列がマッピングされました。")
                df_data.rename(columns=new_columns, inplace=True)
                
                all_data_list.append(df_data)
                logs.append(f"'{filename}' のデータを読み込み完了。({len(df_data)}件) -> all_data_list合計: {len(all_data_list)}ファイル")

            except Exception as e:
                print(f"❌ DEBUG: Error processing {filename}: {e}")
                import traceback
                error_traceback = traceback.format_exc()
                print(f"❌ DEBUG: Full traceback:\n{error_traceback}")
                logs.append(f"'{filename}' のデータシート処理中にエラー: {e}")
                logs.append(f"エラー詳細: {error_traceback}")

    print(f"🔍 DEBUG: Checking data files processing results")
    print(f"   all_data_list length: {len(all_data_list)}")
    print(f"   Original data_files count: {len(data_files)}")

    if not all_data_list:
        print(f"❌ NO DATA FOUND! This is the error, not reindexing!")
        print(f"   Files were processed but no data sheets were successfully read")
        print(f"   Check the logs above for file processing errors")
        raise ValueError("集計対象のデータが見つかりませんでした。")
    
    logs.append("--- 全データの結合処理を開始 ---")
    logs.append(f"結合対象のファイル数: {len(all_data_list)}")
    for i, df in enumerate(all_data_list):
        logs.append(f"  ファイル{i+1}: {len(df)}件のデータ")
    
    # Fix duplicate columns before concat to prevent reindexing errors
    def fix_duplicate_columns_for_concat(dfs_list):
        """Fix duplicate column names across dataframes before concat"""
        if len(dfs_list) <= 1:
            return dfs_list

        print(f"🔍 Checking for duplicate columns across {len(dfs_list)} dataframes")

        # Collect all column names from all dataframes
        all_columns = set()
        df_columns = []

        for i, df in enumerate(dfs_list):
            cols = list(df.columns)
            df_columns.append(cols)
            all_columns.update(cols)
            print(f"   DataFrame {i+1}: {len(cols)} columns")

            # Check for duplicates within the same dataframe
            if df.columns.duplicated().any():
                print(f"   ⚠️ DataFrame {i+1} has internal duplicate columns")

        # Find columns that appear in multiple dataframes
        column_counts = {}
        for i, cols in enumerate(df_columns):
            for col in cols:
                if col not in column_counts:
                    column_counts[col] = []
                column_counts[col].append(i)

        # Identify problematic columns (appear in multiple dataframes)
        problematic_columns = {col: dfs for col, dfs in column_counts.items() if len(dfs) > 1}

        if problematic_columns:
            print(f"   ⚠️ Found {len(problematic_columns)} columns appearing in multiple dataframes")
            for col, df_indices in list(problematic_columns.items())[:5]:  # Show first 5
                print(f"     '{col}' appears in dataframes: {df_indices}")

        # Create union of all columns for consistent structure
        all_columns_list = sorted(list(all_columns))
        print(f"   Total unique columns across all dataframes: {len(all_columns_list)}")

        # Reindex all dataframes to have the same columns
        fixed_dfs = []
        for i, df in enumerate(dfs_list):
            print(f"   Reindexing DataFrame {i+1}...")

            # Fix duplicate column names first - this is the core issue!
            df_copy = df.copy()
            if df_copy.columns.duplicated().any():
                print(f"     ⚠️ Found {df_copy.columns.duplicated().sum()} duplicate column names, fixing...")
                # Make column names unique by adding suffixes using pandas built-in method
                cols = pd.io.common.dedup_names(df_copy.columns, is_potential_multiindex=False)
                df_copy.columns = cols
                print(f"     ✅ Fixed duplicate columns using pandas dedup_names")
            else:
                print(f"     ✅ No duplicate columns found")

            # Reindex to include all columns, filling missing with NaN
            try:
                df_reindexed = df_copy.reindex(columns=all_columns_list, fill_value=None)
                fixed_dfs.append(df_reindexed)
                print(f"     ✅ Reindexed from {len(df_copy.columns)} to {len(df_reindexed.columns)} columns")
            except Exception as e:
                print(f"     ❌ Reindexing failed: {e}")
                # Fallback: keep original dataframe
                fixed_dfs.append(df_copy)

        return fixed_dfs

    # Debug logging for reindex issues
    print(f"🔍 DEBUG: About to concat {len(all_data_list)} dataframes")
    for i, df in enumerate(all_data_list):
        print(f"   DataFrame {i+1}: shape={df.shape}, index_unique={df.index.is_unique}")
        print(f"   Columns: {len(df.columns)} columns")
        if df.columns.duplicated().any():
            print(f"   ⚠️ Duplicate columns detected!")

    # Apply simple duplicate column fix before concat
    print(f"🔧 Applying simple duplicate column resolution...")

    # Step 1: Fix duplicate columns within each dataframe
    simple_fixed_list = []
    for i, df in enumerate(all_data_list):
        print(f"   Processing DataFrame {i+1}: {df.shape}")

        if df.columns.duplicated().any():
            print(f"     ⚠️ Found {df.columns.duplicated().sum()} duplicate columns, fixing...")
            # Simple approach: use make_unique from pandas
            df_copy = df.copy()
            df_copy.columns = pd.io.common.dedup_names(df_copy.columns, is_potential_multiindex=False)
            print(f"     ✅ Fixed duplicate columns")
            simple_fixed_list.append(df_copy)
        else:
            print(f"     ✅ No duplicate columns")
            simple_fixed_list.append(df.copy())

    # Step 2: Try concat with ignore_index and sort=False
    try:
        print(f"🔧 Attempting concat with {len(simple_fixed_list)} dataframes...")
        merged_df = pd.concat(simple_fixed_list, ignore_index=True, sort=False)
        print(f"✅ Concat successful: {merged_df.shape}")
    except Exception as e:
        print(f"❌ CONCAT FAILED: {e}")

        # Fallback: Try with different concat options
        print(f"🔧 Trying fallback concat options...")
        try:
            # Reset index on all dataframes first
            reset_list = []
            for i, df in enumerate(simple_fixed_list):
                df_reset = df.reset_index(drop=True)
                reset_list.append(df_reset)

            merged_df = pd.concat(reset_list, ignore_index=True, sort=False)
            print(f"✅ Fallback concat successful: {merged_df.shape}")
        except Exception as e2:
            print(f"❌ Fallback concat also failed: {e2}")
            import traceback
            traceback.print_exc()
            raise

    logs.append(f"全ファイルのデータを結合しました。合計: {len(merged_df)}件")

    if '回答日時' in merged_df.columns:
        print(f"🔍 DEBUG: Processing datetime column")
        print(f"   merged_df shape before datetime: {merged_df.shape}")
        print(f"   Index unique before datetime: {merged_df.index.is_unique}")

        try:
            merged_df['回答日時'] = pd.to_datetime(merged_df['回答日時'], errors='coerce')
            print(f"✅ Datetime conversion successful")
        except Exception as e:
            print(f"❌ DATETIME CONVERSION FAILED: {e}")
            raise

        try:
            before_drop = len(merged_df)
            merged_df.dropna(subset=['回答日時'], inplace=True)
            after_drop = len(merged_df)
            print(f"✅ dropna successful: {before_drop} -> {after_drop}")
        except Exception as e:
            print(f"❌ DROPNA FAILED: {e}")
            import traceback
            traceback.print_exc()
            raise

        try:
            print(f"🔍 DEBUG: About to sort by 回答日時")
            print(f"   Index before sort: unique={merged_df.index.is_unique}")
            merged_df.sort_values(by='回答日時', inplace=True)
            print(f"✅ Sort successful")
        except Exception as e:
            print(f"❌ SORT_VALUES FAILED: {e}")
            print("🎯 THIS MIGHT BE THE REINDEXING ERROR!")
            import traceback
            traceback.print_exc()
            raise

        logs.append(f"回答日時でソートしました。")

    # クライアント別の集計
    client_results = {}
    logs.append("--- クライアント別集計処理を開始 ---")
    logs.append(f"🔍 デバッグ: {len(data_files)} ファイルアップロード, {len(all_data_list)} ファイル処理済み")
    logs.append(f"🔍 デバッグ: merged_dfは合計 {len(merged_df)} 行")
    
    for client_name, group in client_settings_df.groupby('クライアント名'):
        logs.append(f"'{client_name}' の集計を開始します...")
        
        # クライアント設定から質問を取得
        questions_to_aggregate = group['集計対象の質問文'].tolist()
        
        # 固定質問を追加（重複を除外）
        all_questions = list(dict.fromkeys(FIXED_QUESTIONS + questions_to_aggregate))
        logs.append(f"'{client_name}' には固定質問を含む合計 {len(all_questions)} 個の質問を集計します。")
        logs.append(f"'{client_name}' の内訳: 固定質問{len(FIXED_QUESTIONS)}個 + クライアント質問{len(questions_to_aggregate)}個")
        
        # このクライアントの質問のみを選択
        cols_to_select = ['NO']
        found_questions = []
        not_found_questions = []
        
        # クライアント固有の質問リストを作成
        client_specific_questions = questions_to_aggregate  # クライアント設定からの質問
        
        for q in all_questions:
            found = False
            columns_for_this_question = []
            
            # 完全一致の列を探す
            if q in merged_df.columns:
                columns_for_this_question.append(q)
                found = True
            
            # サフィックス付きの列を探す（例: 質問_1, 質問_2など）
            for col in merged_df.columns:
                if str(col).startswith(q + '_'):
                    columns_for_this_question.append(col)
                    found = True
            
            # このクライアントの質問リストに含まれている場合のみ追加
            if found and q in all_questions:  # all_questionsには固定質問+クライアント質問が含まれる
                cols_to_select.extend(columns_for_this_question)
                found_questions.append(q)
            elif not found:
                not_found_questions.append(q)
        
        cols_to_select = list(dict.fromkeys(cols_to_select))  # 重複を除去
        
        logs.append(f"'{client_name}' - 見つかった質問: {len(found_questions)}/{len(all_questions)}")
        logs.append(f"'{client_name}' - 選択した列数: {len(cols_to_select)}")
        logs.append(f"'{client_name}' - merged_dfの総列数: {len(merged_df.columns)}")
        
        if not_found_questions:
            logs.append(f"'{client_name}' - 見つからなかった質問: {len(not_found_questions)} 個")
            for q in not_found_questions[:3]:
                logs.append(f"  - {q[:50]}...")
            
        # デバッグ: 実際にどの質問が見つかったか
        logs.append(f"'{client_name}' - デバッグ: 見つかった質問の例:")
        for q in found_questions[:3]:
            logs.append(f"  ✓ {q[:50]}...")
            
        # デバッグ: 実際に選択されたcolumnsの例
        logs.append(f"'{client_name}' - デバッグ: 選択された列の例:")
        for col in cols_to_select[1:6]:  # NO以外の最初の5列
            logs.append(f"  → {col[:50]}...")
            
        # デバッグ: このクライアント固有の質問があるか
        client_unique_questions = [q for q in questions_to_aggregate if q not in FIXED_QUESTIONS]
        logs.append(f"'{client_name}' - クライアント固有質問: {len(client_unique_questions)}個")
        for q in client_unique_questions[:2]:
            logs.append(f"  🔹 {q[:50]}...")
        
        if '回答日時' in merged_df.columns:
            cols_to_select.append('回答日時')
        
        if len(cols_to_select) <= 1:
            logs.append(f"'{client_name}' の集計対象の質問がデータ内に見つかりませんでした。")
            continue
            
        # クライアントデータを選択（全762件から必要な列のみ）
        print(f"🔍 DEBUG: Selecting client data for {client_name}")
        print(f"   Columns to select: {len(cols_to_select)}")
        print(f"   merged_df shape: {merged_df.shape}")
        print(f"   merged_df index unique: {merged_df.index.is_unique}")

        try:
            client_data = merged_df[cols_to_select]
            print(f"✅ Client data selection successful: {client_data.shape}")
        except Exception as e:
            print(f"❌ CLIENT DATA SELECTION FAILED: {e}")
            print("🎯 THIS MIGHT BE THE REINDEXING ERROR!")
            import traceback
            traceback.print_exc()
            raise
        
        # このクライアント専用のマッピングを作成
        logs.append(f"'{client_name}' 専用のマッピングを作成中...")
        
        base_mapping_df = pd.DataFrame()
        text_to_q_map = {}
        
        # すべてのファイルから質問マッピングを収集（固定質問を含む全質問を確実にマッピング）
        for file_col in question_master_df.columns:
            if file_col != '質問文' and file_col.endswith('.xlsx'):
                temp_mapping = question_master_df[['質問文', file_col]].dropna()
                for _, row in temp_mapping.iterrows():
                    if row['質問文'] not in text_to_q_map:
                        text_to_q_map[row['質問文']] = row[file_col]
        
        # このクライアント専用のマッピングを作成
        # クライアントの質問リストから、該当するマッピングのみを抽出
        client_mapping_data = []
        
        for question_text in all_questions:
            # question_masterでこの質問を探す
            matching_rows = question_master_df[question_master_df['質問文'] == question_text]
            if not matching_rows.empty:
                row = matching_rows.iloc[0]
                # この質問に対して最初に見つかった非NULLのmappingを使用
                for col in question_master_df.columns:
                    if col.endswith('.xlsx') and pd.notna(row[col]):
                        client_mapping_data.append({
                            '質問文': question_text,
                            '質問番号': row[col]
                        })
                        break
        
        base_mapping_df = pd.DataFrame(client_mapping_data)
        logs.append(f"'{client_name}' のマッピング: {len(base_mapping_df)}個の質問")

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
            'base_file': f"{client_name}専用マッピング",
            'mapping': base_mapping_df
        }
        
        logs.append(f"'{client_name}' の集計が完了しました。")
    
    # サマリー情報をログに追加
    logs.append("=== サマリー ===")
    logs.append(f"アップロードファイル数: {len(data_files)}")
    logs.append(f"処理済みファイル数: {len(all_data_list)}")
    logs.append(f"merged_df総行数: {len(merged_df)}")
    logs.append(f"処理済みクライアント数: {len(client_results)}")
    for i, df in enumerate(all_data_list):
        logs.append(f"  ファイル{i+1}の寄与行数: {len(df)} 行")
    
    return client_results, merged_df, logs