import pandas as pd

# Đọc client_settings
client_df = pd.read_excel('client_settings.xlsx')

FIXED_QUESTIONS = [
    'Please tell us your age and gender',
    'What is your annual household income?',
    'What is your highest level of education?',
    'What is your employment status?',
    'Which region do you live in?'
]

print("=== PHÂN TÍCH CUỐI CÙNG - SAU KHI REMOVE DUPLICATES ===\n")

client_unique_questions = {}
for client in client_df['クライアント名'].unique():
    questions_to_aggregate = client_df[client_df['クライアント名'] == client]['集計対象の質問文'].tolist()
    
    # Logic giống như trong aggregation.py
    all_questions = list(dict.fromkeys(FIXED_QUESTIONS + questions_to_aggregate))
    
    client_unique_questions[client] = set(all_questions)
    
    print(f"{client}:")
    print(f"  Raw questions: {len(questions_to_aggregate)}")
    print(f"  Unique questions (after dedup): {len(all_questions)}")

# Kiểm tra sự khác biệt giữa các clients
print("\n=== SỰ KHÁC BIỆT GIỮA CÁC CLIENTS (SAU DEDUP) ===")

clients = list(client_unique_questions.keys())
for i, client1 in enumerate(clients):
    for j, client2 in enumerate(clients):
        if i < j:  # Tránh so sánh trùng lặp
            common = client_unique_questions[client1].intersection(client_unique_questions[client2])
            diff1 = client_unique_questions[client1] - client_unique_questions[client2]
            diff2 = client_unique_questions[client2] - client_unique_questions[client1]
            
            print(f"\n{client1} vs {client2}:")
            print(f"  Common: {len(common)} câu")
            print(f"  {client1} riêng: {len(diff1)} câu")
            print(f"  {client2} riêng: {len(diff2)} câu")
            
            if diff1:
                print(f"  Ví dụ {client1} riêng:")
                for q in list(diff1)[:2]:
                    print(f"    - {q[:50]}...")
            
            if diff2:
                print(f"  Ví dụ {client2} riêng:")
                for q in list(diff2)[:2]:
                    print(f"    - {q[:50]}...")

# Kết luận
all_clients = list(client_unique_questions.keys())
if len(set([len(client_unique_questions[c]) for c in all_clients])) == 1:
    print(f"\n❌ TẤT CẢ CLIENTS ĐỀU CÓ CÙNG SỐ CÂU HỎI: {len(client_unique_questions[all_clients[0]])}")
else:
    print(f"\n✅ CLIENTS CÓ SỐ CÂU HỎI KHÁC NHAU:")
    for c in all_clients:
        print(f"  {c}: {len(client_unique_questions[c])} câu")