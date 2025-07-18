import pandas as pd
import os

def create_sample_file(output_path):
    """
    サンプル用のクライアント設定ファイルを作成する。
    """
    data = {
        'クライアント名': ['A社', 'A社', 'B社'],
        '集計対象の質問文': [
            'あなたの年代性別を教えてください。',
            '（ここにA社が集計したい2つ目の質問文を記入）',
            '（ここにB社が集計したい質問文を記入）'
        ]
    }
    df = pd.DataFrame(data)
    
    # resultディレクトリがなければ作成
    if not os.path.exists('result'):
        os.makedirs('result')
        
    df.to_excel(output_path, index=False)
    print(f"サンプルファイル '{output_path}' を作成しました。")
    print("このファイルをコピーして 'client_settings.xlsx' を作成し、内容を実際のクライアント名と質問文に書き換えてください。")

if __name__ == '__main__':
    OUTPUT_FILE = 'client_settings_sample.xlsx'
    create_sample_file(OUTPUT_FILE)
