import pytest
import pandas as pd
import os
import io
from datetime import datetime, timedelta
from modules.aggregation import aggregate_data
from modules.question_master import create_question_master


class TestAggregation:
    """データ集計機能のテストクラス"""
    
    @pytest.fixture
    def fixtures_dir(self):
        """フィクスチャディレクトリのパスを返す"""
        return os.path.join(os.path.dirname(__file__), 'fixtures')
    
    @pytest.fixture
    def data_files(self, fixtures_dir):
        """データファイルを読み込んでファイルオブジェクトのリストを返す"""
        files = []
        for filename in ['sample_survey1.xlsx', 'sample_survey2.xlsx']:
            filepath = os.path.join(fixtures_dir, filename)
            with open(filepath, 'rb') as f:
                file_content = f.read()
            
            file_obj = io.BytesIO(file_content)
            file_obj.name = filename
            files.append(file_obj)
        
        return files
    
    @pytest.fixture
    def question_master_df(self, data_files):
        """質問マスターDataFrameを作成して返す"""
        # ファイルオブジェクトを再度作成（create_question_masterで消費されるため）
        files_for_master = []
        for file_obj in data_files:
            file_obj.seek(0)
            new_file = io.BytesIO(file_obj.read())
            new_file.name = file_obj.name
            files_for_master.append(new_file)
            file_obj.seek(0)
        
        return create_question_master(files_for_master)
    
    @pytest.fixture
    def client_settings_df(self, fixtures_dir):
        """クライアント設定DataFrameを読み込んで返す"""
        filepath = os.path.join(fixtures_dir, 'client_settings.xlsx')
        return pd.read_excel(filepath)
    
    def test_aggregate_data_normal(self, data_files, question_master_df, client_settings_df):
        """正常なケースでデータ集計が実行されることを確認"""
        results, merged_df, logs = aggregate_data(data_files, question_master_df, client_settings_df)
        
        # 結果の型を確認
        assert isinstance(results, dict)
        assert isinstance(merged_df, pd.DataFrame)
        assert isinstance(logs, list)
        
        # クライアント数を確認
        assert len(results) == 2  # クライアントAとクライアントB
        assert 'クライアントA' in results
        assert 'クライアントB' in results
        
        # ログが記録されていることを確認
        assert len(logs) > 0
        assert any('データ読み込みと変換処理を開始' in log for log in logs)
    
    def test_client_data_filtering(self, data_files, question_master_df, client_settings_df):
        """クライアント設定に基づいて正しくデータがフィルタリングされることを確認"""
        results, merged_df, logs = aggregate_data(data_files, question_master_df, client_settings_df)
        
        # クライアントAのデータを確認
        client_a_data = results['クライアントA']['data']
        client_a_columns = list(client_a_data.columns)
        
        # 必要な列が含まれていることを確認（質問番号形式）
        assert 'NO' in client_a_columns
        # 質問番号で確認（質問文は質問番号に変換されている）
        assert any(col.startswith('Q-') for col in client_a_columns)
        
        # 具体的な質問番号を確認
        # クライアントAの設定: 年代、性別、知っていますか
        expected_questions_a = ['Q-1', 'Q-2', 'Q-3']  # sample_survey1.xlsxの番号
        for q in expected_questions_a:
            assert any(col == q or col.startswith(q + '_') for col in client_a_columns)
        
        # クライアントBのデータを確認
        client_b_data = results['クライアントB']['data']
        client_b_columns = list(client_b_data.columns)
        
        # クライアントBの質問番号を確認
        # クライアントBの設定: 利用したことがありますか、満足度、その他ご意見、どこで知りましたか
        expected_questions_b = ['Q-4', 'Q-5', 'Q-6']  # sample_survey1.xlsxの番号
        for q in expected_questions_b:
            assert any(col == q or col.startswith(q + '_') for col in client_b_columns)
    
    def test_question_text_to_number_conversion(self, data_files, question_master_df, client_settings_df):
        """質問文が質問番号に正しく変換されることを確認"""
        results, merged_df, logs = aggregate_data(data_files, question_master_df, client_settings_df)
        
        # クライアントAのデータで確認
        client_a_data = results['クライアントA']['data']
        
        # 質問番号形式の列名が存在することを確認（Q-で始まる）
        q_columns = [col for col in client_a_data.columns if str(col).startswith('Q-')]
        assert len(q_columns) > 0
    
    def test_fa_column_inclusion(self, data_files, question_master_df, client_settings_df):
        """FA（自由回答）列が自動的に含まれることを確認"""
        results, merged_df, logs = aggregate_data(data_files, question_master_df, client_settings_df)
        
        # クライアントBのデータを確認（「その他ご意見」を含む）
        client_b_data = results['クライアントB']['data']
        client_b_columns = list(client_b_data.columns)
        
        # FA列が含まれていることを確認
        fa_columns = [col for col in client_b_columns if '_FA' in str(col)]
        assert len(fa_columns) > 0
    
    def test_date_sorting(self, data_files, question_master_df, client_settings_df):
        """回答日時でソートされることを確認"""
        results, merged_df, logs = aggregate_data(data_files, question_master_df, client_settings_df)
        
        # merged_dfに回答日時列が存在することを確認
        assert '回答日時' in merged_df.columns
        
        # 日付が昇順にソートされていることを確認
        dates = merged_df['回答日時'].dropna()
        assert dates.equals(dates.sort_values())
    
    def test_multiple_file_merge(self, data_files, question_master_df, client_settings_df):
        """複数ファイルのデータが正しく結合されることを確認"""
        results, merged_df, logs = aggregate_data(data_files, question_master_df, client_settings_df)
        
        # 両方のファイルのデータが含まれていることを確認
        # sample_survey1.xlsx: NO 1-10, sample_survey2.xlsx: NO 11-20
        assert len(merged_df) == 20
        assert merged_df['NO'].min() == 1
        assert merged_df['NO'].max() == 20
    
    def test_empty_data_files(self, question_master_df, client_settings_df):
        """データファイルが空の場合のエラーハンドリング"""
        with pytest.raises(ValueError, match="集計対象のデータが見つかりませんでした"):
            aggregate_data([], question_master_df, client_settings_df)
    
    def test_missing_data_sheet(self, fixtures_dir, question_master_df, client_settings_df):
        """dataシートがないファイルの処理"""
        filepath = os.path.join(fixtures_dir, 'no_data_sheet.xlsx')
        with open(filepath, 'rb') as f:
            file_content = f.read()
        
        file_obj = io.BytesIO(file_content)
        file_obj.name = 'no_data_sheet.xlsx'
        
        # エラーがログに記録されることを確認
        with pytest.raises(ValueError, match="集計対象のデータが見つかりませんでした"):
            results, merged_df, logs = aggregate_data([file_obj], question_master_df, client_settings_df)
    
    def test_malformed_filename_handling(self, data_files, question_master_df, client_settings_df):
        """文字化けしたファイル名の処理を確認"""
        # ファイル名を意図的に文字化けさせる
        malformed_file = data_files[0]
        malformed_file.seek(0)
        malformed_file.name = "テスト\udcffファイル.xlsx"
        
        # エラーなく処理されることを確認（ただし、質問マスターとの対応が取れない可能性）
        results, merged_df, logs = aggregate_data([malformed_file, data_files[1]], 
                                                 question_master_df, client_settings_df)
        
        # 少なくとも1つのファイルのデータは処理されることを確認
        assert len(merged_df) > 0
    
    def test_base_file_determination(self, data_files, question_master_df, client_settings_df):
        """基準ファイルが正しく特定されることを確認"""
        results, merged_df, logs = aggregate_data(data_files, question_master_df, client_settings_df)
        
        # 各クライアントの結果に基準ファイル情報が含まれることを確認
        for client_name, client_info in results.items():
            assert 'base_file' in client_info
            assert client_info['base_file'] is not None
            assert 'sample_survey' in client_info['base_file']
    
    def test_client_without_matching_questions(self, data_files, question_master_df):
        """設定された質問がデータに存在しないクライアントの処理"""
        # 存在しない質問を含む設定を作成
        invalid_settings = pd.DataFrame({
            'クライアント名': ['クライアントC'],
            '集計対象の質問文': ['存在しない質問です。']
        })
        
        results, merged_df, logs = aggregate_data(data_files, question_master_df, invalid_settings)
        
        # クライアントCの結果を確認
        if 'クライアントC' in results:
            # データが存在する場合、NOと回答日時のみのデータになることを確認
            client_c_data = results['クライアントC']['data']
            assert len(client_c_data.columns) <= 2  # NOと回答日時のみ
        
        # ログにメッセージが含まれることを確認
        assert any('クライアントC' in log for log in logs)