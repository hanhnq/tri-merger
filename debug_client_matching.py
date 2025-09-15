import pandas as pd

# Đọc các files
client_df = pd.read_excel('client_settings.xlsx')
question_master = pd.read_excel('question_master.xlsx')

print("=== KIỂM TRA MATCHING GIỮA CLIENT_SETTINGS VÀ QUESTION_MASTER ===\n")

# Lấy tất cả câu hỏi trong question_master
all_questions_in_master = set(question_master['質問文'].tolist())
print(f"Tổng câu hỏi trong question_master: {len(all_questions_in_master)}")

# Kiểm tra cho từng client
for client in client_df['クライアント名'].unique():
    client_questions = client_df[client_df['クライアント名'] == client]['集計対象の質問文'].tolist()
    print(f"\n{client}:")
    print(f"  Số câu hỏi trong client_settings: {len(client_questions)}")
    
    # Kiểm tra có bao nhiêu câu match với question_master
    matched = [q for q in client_questions if q in all_questions_in_master]
    not_matched = [q for q in client_questions if q not in all_questions_in_master]
    
    print(f"  Câu hỏi MATCH với question_master: {len(matched)}")
    print(f"  Câu hỏi KHÔNG MATCH: {len(not_matched)}")
    
    if not_matched:
        print("  Ví dụ câu không match:")
        for q in not_matched[:3]:
            print(f"    - {q[:50]}...")
            # Tìm câu tương tự trong question_master
            similar = [qm for qm in all_questions_in_master if q[:20].lower() in qm.lower()]
            if similar:
                print(f"      Có thể là: {similar[0][:50]}...")

print("\n=== KẾT LUẬN ===")
print("Nếu nhiều câu không match, có thể do:")
print("1. Khác biệt về dấu câu (? vs không có ?)")
print("2. Khác biệt về viết hoa/thường")
print("3. Khác biệt về khoảng trắng")
print("4. Câu hỏi thực sự khác nhau")