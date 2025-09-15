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

print(f"FIXED_QUESTIONS: {len(FIXED_QUESTIONS)} câu")

for client in client_df['クライアント名'].unique()[:2]:  # Chỉ test 2 clients
    questions_to_aggregate = client_df[client_df['クライアント名'] == client]['集計対象の質問文'].tolist()
    
    print(f"\n=== {client} ===")
    print(f"questions_to_aggregate: {len(questions_to_aggregate)} câu")
    
    # Logic hiện tại
    all_questions = list(dict.fromkeys(FIXED_QUESTIONS + questions_to_aggregate))
    print(f"all_questions (sau khi remove duplicate): {len(all_questions)} câu")
    
    # Kiểm tra overlap
    overlap = []
    for q in FIXED_QUESTIONS:
        if q in questions_to_aggregate:
            overlap.append(q)
    
    print(f"Overlap giữa FIXED và client questions: {len(overlap)} câu")
    if overlap:
        for q in overlap:
            print(f"  - {q}")
    
    # Tính toán lý thuyết
    expected_total = len(FIXED_QUESTIONS) + len(questions_to_aggregate) - len(overlap)
    print(f"Expected total: {len(FIXED_QUESTIONS)} + {len(questions_to_aggregate)} - {len(overlap)} = {expected_total}")