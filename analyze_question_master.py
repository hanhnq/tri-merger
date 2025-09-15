import pandas as pd

# Đọc question_master
df = pd.read_excel('question_master.xlsx')

print("=== PHÂN TÍCH CHI TIẾT QUESTION_MASTER ===")
print(f"Tổng số câu hỏi: {len(df)}")

# Đếm số câu hỏi có mapping cho mỗi file
for col in df.columns:
    if col.endswith('.xlsx'):
        non_null = df[col].dropna()
        print(f"\n{col}:")
        print(f"  - Số câu có mã: {len(non_null)}")
        print(f"  - Số câu NULL: {df[col].isna().sum()}")
        
        # Xem các mã
        unique_codes = non_null.unique()
        print(f"  - Số mã duy nhất: {len(unique_codes)}")
        print(f"  - Ví dụ mã: {list(unique_codes[:5])}")

# Kiểm tra xem câu hỏi nào có mapping cho TẤT CẢ files
print("\n=== CÂU HỎI CÓ MAPPING CHO TẤT CẢ 5 FILES ===")
file_cols = [col for col in df.columns if col.endswith('.xlsx')]
all_mapped = df[df[file_cols].notna().all(axis=1)]
print(f"Số câu có mapping cho cả 5 files: {len(all_mapped)}")
if len(all_mapped) > 0:
    print("Ví dụ:")
    for i, row in all_mapped.head(3).iterrows():
        print(f"  - {row['質問文']}")
        for col in file_cols:
            print(f"    {col}: {row[col]}")

# Kiểm tra câu hỏi chỉ có trong 1 file
print("\n=== CÂU HỎI CHỈ CÓ TRONG 1 FILE ===")
for col in file_cols:
    other_cols = [c for c in file_cols if c != col]
    unique_to_file = df[df[col].notna() & df[other_cols].isna().all(axis=1)]
    if len(unique_to_file) > 0:
        print(f"\n{col}: {len(unique_to_file)} câu độc quyền")
        for i, row in unique_to_file.head(2).iterrows():
            print(f"  - {row['質問文'][:50]}... -> {row[col]}")