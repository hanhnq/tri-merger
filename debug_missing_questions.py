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

client = 'AutoMotion Inc'
questions_to_aggregate = client_df[client_df['クライアント名'] == client]['集計対象の質問文'].tolist()

print(f"=== DEBUGGING MISSING QUESTIONS FOR {client} ===")
print(f"FIXED_QUESTIONS: {len(FIXED_QUESTIONS)} câu")
print(f"questions_to_aggregate: {len(questions_to_aggregate)} câu")

# Logic hiện tại
all_questions_before = FIXED_QUESTIONS + questions_to_aggregate
all_questions_after = list(dict.fromkeys(FIXED_QUESTIONS + questions_to_aggregate))

print(f"Trước khi remove duplicates: {len(all_questions_before)} câu")
print(f"Sau khi remove duplicates: {len(all_questions_after)} câu")
print(f"Số câu bị loại bỏ: {len(all_questions_before) - len(all_questions_after)} câu")

# Tìm tất cả duplicates
from collections import Counter
question_counts = Counter(all_questions_before)
duplicates = [(q, count) for q, count in question_counts.items() if count > 1]

print(f"\nTất cả câu hỏi duplicate:")
for q, count in duplicates:
    print(f"  {count}x: {q[:50]}...")

print(f"\nTổng số lần duplicate: {sum([count-1 for q, count in duplicates])}")

# So sánh với expected
expected_total = len(FIXED_QUESTIONS) + len(questions_to_aggregate) - len([q for q in FIXED_QUESTIONS if q in questions_to_aggregate])
print(f"\nExpected (FIXED + CLIENT - OVERLAP): {expected_total}")
print(f"Actual: {len(all_questions_after)}")
print(f"Difference: {expected_total - len(all_questions_after)}")

# Kiểm tra nếu questions_to_aggregate có duplicate nội bộ
internal_duplicates = [(q, count) for q, count in Counter(questions_to_aggregate).items() if count > 1]
if internal_duplicates:
    print(f"\nDuplicates TRONG chính questions_to_aggregate:")
    for q, count in internal_duplicates:
        print(f"  {count}x: {q[:50]}...")
else:
    print(f"\nKhông có duplicates trong questions_to_aggregate")