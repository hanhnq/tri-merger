import pandas as pd

# Đọc file client_settings.xlsx
df = pd.read_excel('client_settings.xlsx')

# Hiển thị thông tin
print("=== CLIENT SETTINGS INFO ===")
print(f"Tổng số dòng trong file: {len(df)}")
print(f"\nCác clients có trong file:")
clients = df['クライアント名'].unique()
for i, client in enumerate(clients, 1):
    count = len(df[df['クライアント名'] == client])
    print(f"  {i}. {client} ({count} questions)")

print(f"\nTổng số clients duy nhất: {len(clients)}")

# Kiểm tra xem có đúng 5 clients như mong đợi không
expected_clients = [
    'AutoMotive Plus',
    'LearnForward Academy', 
    'StreamVibe Media',
    'GreenEarth Initiative',
    'FitLife Pro'
]

print("\n=== SO SÁNH VỚI DANH SÁCH MONG ĐỢI ===")
for client in expected_clients:
    if client in clients:
        print(f"✓ {client} - CÓ trong file")
    else:
        print(f"✗ {client} - THIẾU trong file")