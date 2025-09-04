import pytest
import pandas as pd
import os
import io
from modules.question_master import create_question_master


class TestQuestionMaster:
    """質問マスター作成機能のテストクラス"""
    
    @pytest.fixture
    def fixtures_dir(self):
        """フィクスチャディレクトリのパスを返す"""
        return os.path.join(os.path.dirname(__file__), 'fixtures')
    
    @pytest.fixture
    def sample_files(self, fixtures_dir):
        """サンプルファイルを読み込んでファイルオブジェクトのリストを返す"""
        files = []
        for filename in ['sample_survey1.xlsx', 'sample_survey2.xlsx']:
            filepath = os.path.join(fixtures_dir, filename)
            with open(filepath, 'rb') as f:
                file_content = f.read()
            
            # StreamlitのUploadedFileオブジェクトを模擬
            file_obj = io.BytesIO(file_content)
            file_obj.name = filename
            files.append(file_obj)
        
        return files
    
    def test_create_question_master_normal(self, sample_files):
        """正常なケースで質問マスターが作成されることを確認"""
        result = create_question_master(sample_files)
        
        # 結果がDataFrameであることを確認
        assert isinstance(result, pd.DataFrame)
        
        # 必要な列が存在することを確認
        assert '質問文' in result.columns
        assert '初出ファイル' in result.columns
        
        # 質問文が正しく抽出されていることを確認
        expected_questions = [
            'あなたの年代を教えてください。',
            'あなたの性別を教えてください。',
            '〇〇というサービスを知っていますか？',
            '〇〇というサービスを利用したことがありますか？',
            '〇〇の満足度を教えてください。',
            'その他ご意見をお聞かせください。',
            'どこで知りましたか？'  # survey2にのみ存在
        ]
        
        for question in expected_questions:
            assert question in result['質問文'].values
    
    def test_question_number_mapping(self, sample_files):
        """質問番号のマッピングが正しく行われることを確認"""
        result = create_question_master(sample_files)
        
        # ファイル名の列が存在することを確認
        file_columns = [col for col in result.columns if col not in ['質問文', '初出ファイル']]
        assert len(file_columns) == 2  # 2つのサンプルファイル
        
        # 同じ質問に対して異なる質問番号がマッピングされていることを確認
        age_question = result[result['質問文'] == 'あなたの年代を教えてください。']
        assert len(age_question) == 1
        
        # sample_survey1.xlsxとsample_survey2.xlsxの列を探す
        survey1_col = None
        survey2_col = None
        for col in file_columns:
            if 'sample_survey1' in col:
                survey1_col = col
            elif 'sample_survey2' in col:
                survey2_col = col
        
        assert survey1_col is not None
        assert survey2_col is not None
        
        # 質問番号が異なることを確認
        assert age_question[survey1_col].values[0] == 'Q-1'
        assert age_question[survey2_col].values[0] == 'Q-A1'
    
    def test_empty_file_list(self):
        """空のファイルリストでエラーが発生することを確認"""
        with pytest.raises(ValueError, match="読み込むファイルが見つかりませんでした"):
            create_question_master([])
    
    def test_file_without_question_sheet(self, fixtures_dir):
        """質問対応表シートがないファイルでエラーが発生することを確認"""
        filepath = os.path.join(fixtures_dir, 'no_question_sheet.xlsx')
        with open(filepath, 'rb') as f:
            file_content = f.read()
        
        file_obj = io.BytesIO(file_content)
        file_obj.name = 'no_question_sheet.xlsx'
        
        with pytest.raises(Exception, match="Error processing"):
            create_question_master([file_obj])
    
    def test_malformed_filename_handling(self, sample_files):
        """文字化けしたファイル名の処理を確認"""
        # ファイル名を意図的に文字化けさせる
        malformed_file = sample_files[0]
        malformed_file.name = "テスト\udcffファイル.xlsx"  # 不正なUnicode文字を含む
        
        # エラーなく処理されることを確認
        result = create_question_master([malformed_file, sample_files[1]])
        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0
    
    def test_question_order_preservation(self, sample_files):
        """基準ファイルの質問順序が保持されることを確認"""
        result = create_question_master(sample_files)
        
        # 最初のファイル（sample_survey1.xlsx）の質問順序を確認
        questions = result['質問文'].tolist()
        
        # 基準ファイルの質問が先に来ることを確認
        base_questions = [
            'あなたの年代を教えてください。',
            'あなたの性別を教えてください。',
            '〇〇というサービスを知っていますか？',
            '〇〇というサービスを利用したことがありますか？',
            '〇〇の満足度を教えてください。',
            'その他ご意見をお聞かせください。'
        ]
        
        # 基準ファイルの質問が順序通りに含まれていることを確認
        base_indices = []
        for q in base_questions:
            if q in questions:
                base_indices.append(questions.index(q))
        
        # インデックスが昇順になっていることを確認
        assert base_indices == sorted(base_indices)
    
    def test_duplicate_question_handling(self, sample_files):
        """重複する質問が正しく処理されることを確認"""
        result = create_question_master(sample_files)
        
        # 各質問が1回だけ出現することを確認
        assert len(result['質問文']) == len(result['質問文'].unique())
    
    def test_non_q_prefix_exclusion(self, fixtures_dir):
        """Q-で始まらない番号の行が除外されることを確認"""
        # テスト用のデータを作成
        questions_df = pd.DataFrame([
            ['', '', ''],
            ['', '', ''],
            ['番号', '内容', '備考'],
            ['Q-1', '質問1', ''],
            ['A-1', '回答1', ''],  # Q-で始まらない
            ['Q-2', '質問2', ''],
            ['備考', 'メモ', '']  # Q-で始まらない
        ])
        
        # 一時的なExcelファイルを作成
        temp_file = io.BytesIO()
        with pd.ExcelWriter(temp_file, engine='xlsxwriter') as writer:
            questions_df.to_excel(writer, sheet_name='質問対応表', index=False, header=False)
            pd.DataFrame({'NO': [1]}).to_excel(writer, sheet_name='data', index=False)
        
        temp_file.seek(0)
        temp_file.name = 'test_non_q.xlsx'
        
        result = create_question_master([temp_file])
        
        # Q-で始まる質問のみが含まれることを確認
        assert len(result) == 2  # Q-1とQ-2のみ
        assert all(result[result.columns[-1]].str.startswith('Q-'))