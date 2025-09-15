import pandas as pd
import sys

# Analyze the client settings file structure
file_path = r"D:\Downloads\FSS_TryField\client_settings.xlsx"

try:
    # Read all sheets
    excel_file = pd.ExcelFile(file_path)
    print(f"Number of sheets: {len(excel_file.sheet_names)}")
    print(f"Sheet names: {excel_file.sheet_names}")
    print("\n" + "="*60 + "\n")
    
    # Analyze each sheet
    for sheet_name in excel_file.sheet_names:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        print(f"Sheet: {sheet_name}")
        print(f"Shape: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")
        print("\nFirst 10 rows:")
        print(df.head(10))
        print("\n" + "-"*60 + "\n")
        
except Exception as e:
    print(f"Error reading file: {e}")
    sys.exit(1)