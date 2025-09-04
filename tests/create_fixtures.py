import pandas as pd
import os
from datetime import datetime, timedelta

def create_sample_survey_files():
    """テスト用のサンプルアンケートファイルを作成"""
    
    fixtures_dir = os.path.dirname(os.path.abspath(__file__)) + '/fixtures'
    os.makedirs(fixtures_dir, exist_ok=True)
    
    # サンプルアンケート1の作成
    # 質問対応表シート
    questions1 = pd.DataFrame([
        ['', '', ''],
        ['', '', ''],
        ['番号', '内容', '備考'],  # 3行目がヘッダー
        ['Q-1', 'あなたの年代を教えてください。', ''],
        ['Q-2', 'あなたの性別を教えてください。', ''],
        ['Q-3', '〇〇というサービスを知っていますか？', ''],
        ['Q-4', '〇〇というサービスを利用したことがありますか？', ''],
        ['Q-5', '〇〇の満足度を教えてください。', ''],
        ['Q-6', 'その他ご意見をお聞かせください。', 'FA']
    ])
    
    # dataシート
    base_date = datetime.now() - timedelta(days=30)
    data1 = pd.DataFrame({
        'NO': range(1, 11),
        '回答日時': [base_date + timedelta(days=i) for i in range(10)],
        'Q-1': ['20代', '30代', '40代', '20代', '30代', '40代', '50代', '20代', '30代', '40代'],
        'Q-2': ['男性', '女性', '男性', '女性', '男性', '女性', '男性', '女性', '男性', '女性'],
        'Q-3': ['知っている', '知らない', '知っている', '知っている', '知らない', '知っている', '知らない', '知っている', '知っている', '知らない'],
        'Q-4': ['利用したことがある', '利用したことがない', '利用したことがある', '利用したことがない', '利用したことがない', '利用したことがある', '利用したことがない', '利用したことがある', '利用したことがない', '利用したことがない'],
        'Q-5': ['満足', '普通', '満足', '不満', '普通', '満足', '普通', '非常に満足', '普通', '不満'],
        'Q-6_FA': ['良いサービスです', '', '便利でした', '', '', '改善希望', '', '素晴らしい', '', 'もっと良くしてほしい']
    })
    
    # Excelファイルとして保存
    with pd.ExcelWriter(f'{fixtures_dir}/sample_survey1.xlsx', engine='xlsxwriter') as writer:
        questions1.to_excel(writer, sheet_name='質問対応表', index=False, header=False)
        data1.to_excel(writer, sheet_name='data', index=False)
    
    # サンプルアンケート2の作成（質問番号が異なる）
    questions2 = pd.DataFrame([
        ['', '', ''],
        ['', '', ''],
        ['番号', '内容', '備考'],
        ['Q-A1', 'あなたの年代を教えてください。', ''],
        ['Q-A2', 'あなたの性別を教えてください。', ''],
        ['Q-B1', '〇〇というサービスを知っていますか？', ''],
        ['Q-B2', '〇〇というサービスを利用したことがありますか？', ''],
        ['Q-B3', '〇〇の満足度を教えてください。', ''],
        ['Q-C1', 'その他ご意見をお聞かせください。', 'FA'],
        ['Q-C2', 'どこで知りましたか？', '']  # survey1にない質問
    ])
    
    data2 = pd.DataFrame({
        'NO': range(11, 21),
        '回答日時': [base_date + timedelta(days=i+10) for i in range(10)],
        'Q-A1': ['20代', '30代', '40代', '50代', '20代', '30代', '40代', '50代', '60代', '20代'],
        'Q-A2': ['男性', '女性', '男性', '女性', '男性', '女性', '男性', '女性', '男性', '女性'],
        'Q-B1': ['知っている', '知っている', '知らない', '知っている', '知らない', '知っている', '知っている', '知らない', '知っている', '知っている'],
        'Q-B2': ['利用したことがある', '利用したことがない', '利用したことがない', '利用したことがある', '利用したことがない', '利用したことがある', '利用したことがない', '利用したことがない', '利用したことがある', '利用したことがない'],
        'Q-B3': ['満足', '普通', '不満', '満足', '普通', '非常に満足', '普通', '不満', '満足', '普通'],
        'Q-C1_FA': ['とても良い', '', '', '改善点あり', '', '最高です', '', '', '便利でした', ''],
        'Q-C2': ['インターネット', 'SNS', '', 'インターネット', '', 'SNS', 'チラシ', '', 'インターネット', 'SNS']
    })
    
    with pd.ExcelWriter(f'{fixtures_dir}/sample_survey2.xlsx', engine='xlsxwriter') as writer:
        questions2.to_excel(writer, sheet_name='質問対応表', index=False, header=False)
        data2.to_excel(writer, sheet_name='data', index=False)
    
    print("サンプルアンケートファイルを作成しました。")

def create_client_settings():
    """クライアント設定ファイルを作成"""
    
    fixtures_dir = os.path.dirname(os.path.abspath(__file__)) + '/fixtures'
    
    settings_data = pd.DataFrame({
        'クライアント名': [
            'クライアントA', 
            'クライアントA', 
            'クライアントA',
            'クライアントB',
            'クライアントB',
            'クライアントB',
            'クライアントB'
        ],
        '集計対象の質問文': [
            'あなたの年代を教えてください。',
            'あなたの性別を教えてください。',
            '〇〇というサービスを知っていますか？',
            '〇〇というサービスを利用したことがありますか？',
            '〇〇の満足度を教えてください。',
            'その他ご意見をお聞かせください。',
            'どこで知りましたか？'
        ]
    })
    
    with pd.ExcelWriter(f'{fixtures_dir}/client_settings.xlsx', engine='xlsxwriter') as writer:
        settings_data.to_excel(writer, sheet_name='設定', index=False)
    
    print("クライアント設定ファイルを作成しました。")

def create_malformed_files():
    """エラーテスト用の不正なファイルを作成"""
    
    fixtures_dir = os.path.dirname(os.path.abspath(__file__)) + '/fixtures'
    
    # 質問対応表シートがないファイル
    data_only = pd.DataFrame({
        'NO': [1, 2, 3],
        'Q-1': ['A', 'B', 'C']
    })
    
    with pd.ExcelWriter(f'{fixtures_dir}/no_question_sheet.xlsx', engine='xlsxwriter') as writer:
        data_only.to_excel(writer, sheet_name='data', index=False)
    
    # dataシートがないファイル
    questions_only = pd.DataFrame([
        ['', '', ''],
        ['', '', ''],
        ['番号', '内容', '備考'],
        ['Q-1', '質問1', '']
    ])
    
    with pd.ExcelWriter(f'{fixtures_dir}/no_data_sheet.xlsx', engine='xlsxwriter') as writer:
        questions_only.to_excel(writer, sheet_name='質問対応表', index=False, header=False)
    
    print("エラーテスト用ファイルを作成しました。")

if __name__ == "__main__":
    create_sample_survey_files()
    create_client_settings()
    create_malformed_files()
    print("\nすべてのフィクスチャファイルの作成が完了しました。")