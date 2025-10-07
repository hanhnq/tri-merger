import pandas as pd

# Đọc một file kết quả để kiểm tra columns
file_path = r'D:\P-SS\AutoMotion Inc_集計結果(8).xlsx'
df = pd.read_excel(file_path, sheet_name='元データ')

print("=== KIỂM TRA CỘT TRONG FILE KẾT QUẢ ===")
print(f"Tổng số cột: {len(df.columns)}")
print("\n20 cột đầu tiên:")
for i, col in enumerate(df.columns[:20], 1):
    print(f"  {i}. {col}")

# Kiểm tra xem có cột nào là câu hỏi thực tế không
print("\n=== TÌM CÁC CỘT CÓ VẺ LÀ CÂU HỎI ===")
question_cols = [col for col in df.columns if not col.startswith('Q-') and col not in ['NO', '回答日時']]
print(f"Số cột câu hỏi (không phải Q-xxx): {len(question_cols)}")
if question_cols:
    print("Một số câu hỏi:")
    for q in question_cols[:5]:
        print(f"  - {q}")

# Đọc client_settings để so sánh
client_settings = pd.read_excel('client_settings.xlsx')
automotion_questions = client_settings[client_settings['クライアント名'] == 'AutoMotion Inc']['集計対象の質問文'].tolist()

print("\n=== CÂU HỎI CỦA AUTOMOTION INC TRONG CLIENT_SETTINGS ===")
print(f"Số câu hỏi: {len(automotion_questions)}")
for i, q in enumerate(automotion_questions[:5], 1):
    print(f"  {i}. {q}")

# Kiểm tra xem câu hỏi có trong columns không
print("\n=== KIỂM TRA KHỚP ===")
found = 0
not_found = 0
for q in automotion_questions[:10]:  # Kiểm tra 10 câu đầu
    if q in df.columns:
        print(f"  ✓ TÌM THẤY: {q}")
        found += 1
    else:
        print(f"  ✗ KHÔNG TÌM: {q}")
        not_found += 1

print(f"\nKết quả: {found} tìm thấy, {not_found} không tìm thấy")