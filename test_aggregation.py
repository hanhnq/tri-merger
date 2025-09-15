import os
import pandas as pd
from datetime import datetime

# Tạo dữ liệu test
def create_test_data():
    # Tạo thư mục nếu chưa có
    os.makedirs('data', exist_ok=True)
    os.makedirs('result', exist_ok=True)
    
    # Tạo 3 file test với sheet 'data'
    for i in range(1, 4):
        data = {
            'NO': range(1, 6),
            'Q1': [f'Answer {i}-{j}' for j in range(1, 6)],
            'Q2': [f'Response {i}-{j}' for j in range(1, 6)],
            '回答日時': [datetime.now() for _ in range(5)]
        }
        df = pd.DataFrame(data)
        
        filename = f'data/test_file_{i}.xlsx'
        with pd.ExcelWriter(filename) as writer:
            df.to_excel(writer, sheet_name='data', index=False)
        print(f"Created: {filename}")
    
    # Tạo 質問マスター.xlsx
    master_data = {
        '質問文': ['質問1', '質問2'],
        'test_file_1.xlsx': ['Q1', 'Q2'],
        'test_file_2.xlsx': ['Q1', 'Q2'],
        'test_file_3.xlsx': ['Q1', 'Q2']
    }
    df_master = pd.DataFrame(master_data)
    df_master.to_excel('result/質問マスター.xlsx', index=False)
    print("Created: result/質問マスター.xlsx")
    
    # Tạo client_settings.xlsx
    settings_data = {
        'クライアント名': ['Client A', 'Client A'],
        '集計対象の質問文': ['質問1', '質問2']
    }
    df_settings = pd.DataFrame(settings_data)
    df_settings.to_excel('client_settings.xlsx', index=False)
    print("Created: client_settings.xlsx")

if __name__ == '__main__':
    create_test_data()
    print("\n--- Running aggregation ---")
    
    # Import và chạy aggregation
    from run_aggregation import aggregate_data, setup_logging
    
    setup_logging()
    aggregate_data('data', 'result/質問マスター.xlsx', 'client_settings.xlsx', 'result')
    
    print("\n--- Checking output ---")
    # Kiểm tra file output
    output_file = 'result/Client A_集計結果.xlsx'
    if os.path.exists(output_file):
        xl = pd.ExcelFile(output_file)
        print(f"Sheets in {output_file}: {xl.sheet_names}")
        
        # Đọc sheet 基準ファイル情報
        df_base = pd.read_excel(output_file, sheet_name='基準ファイル情報')
        print("\n基準ファイル情報 sheet:")
        print(df_base)
        print(f"Number of files shown: {len(df_base)}")