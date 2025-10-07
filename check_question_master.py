import pandas as pd

# Đọc question_master
df = pd.read_excel('question_master.xlsx')

print("=== CẤU TRÚC FILE QUESTION_MASTER ===")
print(f"Columns: {df.columns.tolist()}")
print(f"Số dòng: {len(df)}")

print("\n=== 10 DÒNG ĐẦU TIÊN ===")
print(df.head(10))

# Kiểm tra xem có column '質問文' không
if '質問文' in df.columns:
    print("\n=== MỘT SỐ CÂU HỎI (質問文) ===")
    for i, q in enumerate(df['質問文'].head(5), 1):
        print(f"{i}. {q}")

# Kiểm tra các columns có vẻ là file mapping
file_cols = [col for col in df.columns if col.endswith('.xlsx') or 'file' in col.lower()]
if file_cols:
    print(f"\n=== CÁC CỘT FILE MAPPING: {file_cols} ===")
    for col in file_cols[:3]:  # Xem 3 columns đầu
        print(f"\n{col}:")
        non_null = df[col].dropna()
        if len(non_null) > 0:
            print(f"  Ví dụ: {non_null.iloc[0]}")

# Kiểm tra mapping cho survey files
survey_files = ['Automotive_Vehicle_Survey_2025.xlsx', 
                'Education_Learning_Survey_2025.xlsx',
                'Entertainment_Media_Survey_2025.xlsx',
                'Environmental_Awareness_Survey_2025.xlsx',
                'Fitness_Health_Survey_2025.xlsx']

print("\n=== KIỂM TRA MAPPING CHO 5 SURVEY FILES ===")
for file in survey_files:
    if file in df.columns:
        non_null = df[file].dropna()
        print(f"✓ {file}: {len(non_null)} mappings")
    else:
        print(f"✗ {file}: KHÔNG CÓ trong columns")