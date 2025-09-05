import pandas as pd
import os

def create_sample_file(output_path):
    """
    サンプル用のクライアント設定ファイルを作成する。
    
    注意: 以下の8つの質問は固定質問として全クライアントに自動的に含まれます：
    - あなたの年代性別を教えてください。
    - あなたがお住まいの都道府県をお知らせください。
    - 家族構成を教えてください。
    - あなたの年収を教えてください。
    - 社会人経験は何年間ですか？
    - 最終学歴を教えてください。
    - あなたのお住いの家賃を教えてください。
    - あなたに当てはまる選択肢をお知らせください。
    """
    data = {
        'クライアント名': ['A社', 'A社', 'B社'],
        '集計対象の質問文': [
            '（ここにA社が集計したい1つ目の質問文を記入）',
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
    print("\n注意: 固定質問（年代性別、都道府県、家族構成、年収、社会人経験、最終学歴、家賃、該当選択肢）は")
    print("自動的に全クライアントに含まれるため、設定ファイルに記載する必要はありません。")

if __name__ == '__main__':
    OUTPUT_FILE = 'client_settings_sample.xlsx'
    create_sample_file(OUTPUT_FILE)
