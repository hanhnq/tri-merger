import pandas as pd

# Kiểm tra merged_df sẽ có những columns nào
client_settings = pd.read_excel('client_settings.xlsx')
question_master = pd.read_excel('question_master.xlsx')

print("=== PHÂN TÍCH TẠI SAO CÁC CLIENTS GIỐNG NHAU ===\n")

# Fixed questions
FIXED_QUESTIONS = [
    'Please tell us your age and gender',
    'What is your annual household income?',
    'What is your highest level of education?',
    'What is your employment status?',
    'Which region do you live in?'
]

# Xem từng client có những câu hỏi gì
for client in ['AutoMotion Inc', 'EcoGreen Solutions'][:2]:  # Chỉ xem 2 clients
    client_questions = client_settings[client_settings['クライアント名'] == client]['集計対象の質問文'].tolist()
    all_questions = list(dict.fromkeys(FIXED_QUESTIONS + client_questions))
    
    print(f"\n{client}:")
    print(f"  - Câu hỏi riêng: {len(client_questions)}")
    print(f"  - Tổng cộng (với fixed): {len(all_questions)}")
    
    # Xem những câu hỏi đầu tiên
    print(f"  - 5 câu đầu:")
    for i, q in enumerate(all_questions[:5], 1):
        print(f"    {i}. {q[:40]}...")
    
    # Kiểm tra xem có mapping không
    questions_with_mapping = []
    for q in all_questions:
        if q in question_master['質問文'].values:
            questions_with_mapping.append(q)
    
    print(f"  - Có mapping trong question_master: {len(questions_with_mapping)}/{len(all_questions)}")

print("\n=== VẤN ĐỀ CHÍNH ===")
print("1. Tất cả clients có cùng số câu hỏi (50) thay vì số khác nhau")
print("2. Logic chỉ lấy những câu có trong global_q_to_text_map (50 câu)")
print("3. Cần lọc theo từng client TRƯỚC KHI tạo client_data")
print("\n=== GIẢI PHÁP ===")
print("Thay vì lọc từ merged_df chung, cần:")
print("1. Xác định câu hỏi cụ thể của từng client")
print("2. Chỉ lấy những columns tương ứng với câu hỏi đó")
print("3. Đảm bảo mỗi client có data khác nhau")