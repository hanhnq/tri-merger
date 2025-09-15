import os
import pandas as pd

# Danh sách 5 file kết quả
files = [
    r'D:\P-SS\AutoMotion Inc_集計結果(8).xlsx',
    r'D:\P-SS\EcoGreen Solutions_集計結果(6).xlsx', 
    r'D:\P-SS\FitLife Wellness_集計結果(2).xlsx',
    r'D:\P-SS\LearnForward Academy_集計結果(1).xlsx',
    r'D:\P-SS\StreamVibe Media_集計結果(2).xlsx'
]

print("=== KIỂM TRA 5 FILE KẾT QUẢ TỔNG HỢP ===\n")

for i, file_path in enumerate(files, 1):
    file_name = os.path.basename(file_path)
    client_name = file_name.split('_')[0]
    
    if os.path.exists(file_path):
        print(f"✓ File {i}: {file_name}")
        print(f"  Client: {client_name}")
        print(f"  Path: {file_path}")
        
        # Đọc file để kiểm tra nội dung
        try:
            df = pd.read_excel(file_path)
            print(f"  Số dòng dữ liệu: {len(df)}")
            print(f"  Số cột: {len(df.columns)}")
            if len(df.columns) > 0:
                print(f"  Một số cột đầu: {list(df.columns[:5])}")
        except Exception as e:
            print(f"  Lỗi khi đọc file: {e}")
    else:
        print(f"✗ File {i}: {file_name} - KHÔNG TỒN TẠI")
    
    print()

print("\n=== KẾT LUẬN ===")
existing_files = [f for f in files if os.path.exists(f)]
print(f"Tìm thấy {len(existing_files)}/{len(files)} files")

if len(existing_files) == 5:
    print("✅ TẤT CẢ 5 CLIENTS ĐÃ ĐƯỢC XỬ LÝ THÀNH CÔNG!")
    print("\nVấn đề: Mặc dù đã tạo được 5 file kết quả, nhưng UI chỉ hiển thị 2 clients.")
    print("Nguyên nhân có thể: Logic hiển thị trong UI bị giới hạn hoặc cache.")
else:
    print("⚠️ Chưa đủ 5 files kết quả")