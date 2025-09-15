import pandas as pd

# Đọc client_settings
client_df = pd.read_excel('client_settings.xlsx')

print("=== PHÂN TÍCH CÂU HỎI CỦA TỪNG CLIENT ===\n")

for client in client_df['クライアント名'].unique():
    client_questions = client_df[client_df['クライアント名'] == client]['集計対象の質問文'].tolist()
    print(f"{client}:")
    print(f"  Số câu hỏi: {len(client_questions)}")
    print(f"  5 câu đầu:")
    for i, q in enumerate(client_questions[:5], 1):
        print(f"    {i}. {q[:50]}...")
    print()

# Kiểm tra xem các client có câu hỏi chung không
print("=== KIỂM TRA CÂU HỎI CHUNG/RIÊNG ===")
all_clients = client_df['クライアント名'].unique()
client_questions_dict = {}
for client in all_clients:
    client_questions_dict[client] = set(client_df[client_df['クライアント名'] == client]['集計対象の質問文'].tolist())

# Tìm câu hỏi chung cho tất cả clients
common_questions = set.intersection(*client_questions_dict.values())
print(f"Câu hỏi chung cho TẤT CẢ clients: {len(common_questions)}")
if common_questions:
    for q in list(common_questions)[:3]:
        print(f"  - {q}")

# Tìm câu hỏi riêng cho từng client
print("\nCâu hỏi RIÊNG cho từng client:")
for client in all_clients:
    other_clients = [c for c in all_clients if c != client]
    other_questions = set.union(*[client_questions_dict[c] for c in other_clients])
    unique_questions = client_questions_dict[client] - other_questions
    print(f"  {client}: {len(unique_questions)} câu riêng")
    if unique_questions:
        for q in list(unique_questions)[:2]:
            print(f"    - {q[:50]}...")