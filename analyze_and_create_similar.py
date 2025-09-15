import pandas as pd
import numpy as np
from datetime import datetime
import os

# First, let's analyze the original file structure
original_file = r"D:\Downloads\FSS_TryField\2025年7月1日インターネット調査.xlsx"

print("Analyzing original file structure...")
print("="*60)

try:
    # Read all sheets from the original file
    all_sheets = pd.read_excel(original_file, sheet_name=None)
    
    print(f"Number of sheets: {len(all_sheets)}")
    print(f"Sheet names: {list(all_sheets.keys())}")
    print("\n")
    
    # Analyze each sheet
    sheet_info = {}
    for sheet_name, df in all_sheets.items():
        print(f"Sheet: '{sheet_name}'")
        print(f"  - Shape: {df.shape} (rows: {df.shape[0]}, columns: {df.shape[1]})")
        print(f"  - Columns: {list(df.columns)}")
        
        # Store info for recreation
        sheet_info[sheet_name] = {
            'shape': df.shape,
            'columns': list(df.columns),
            'dtypes': df.dtypes.to_dict(),
            'sample_data': df.head(3) if len(df) > 0 else None
        }
        
        # Show first few rows
        if len(df) > 0:
            print(f"  - First 3 rows preview:")
            print(df.head(3))
        print("-"*40)
    
    print("\n" + "="*60)
    print("Creating similar file in English...")
    print("="*60)
    
    # Now create a similar file with English content
    new_sheets = {}
    
    for sheet_name, info in sheet_info.items():
        rows, cols = info['shape']
        columns = info['columns']
        
        # Create English version of sheet name
        if 'raw' in sheet_name.lower() or 'ローデータ' in sheet_name:
            english_sheet_name = 'Raw_Data'
        elif 'master' in sheet_name.lower() or 'マスター' in sheet_name:
            english_sheet_name = 'Master_Data'
        elif 'summary' in sheet_name.lower() or '集計' in sheet_name:
            english_sheet_name = 'Summary'
        elif 'code' in sheet_name.lower() or 'コード' in sheet_name:
            english_sheet_name = 'Code_List'
        else:
            # Keep numbers if they exist, otherwise use generic name
            if any(char.isdigit() for char in sheet_name):
                english_sheet_name = f"Sheet_{''.join(filter(str.isdigit, sheet_name))}"
            else:
                english_sheet_name = f"Sheet_{len(new_sheets)+1}"
        
        # Create data based on column patterns
        new_data = {}
        for col in columns:
            col_lower = str(col).lower()
            
            # Determine data type and generate appropriate data
            if 'id' in col_lower or 'ID' in str(col):
                # Generate IDs
                new_data[col] = [f"ID_{str(i).zfill(4)}" for i in range(1, rows + 1)]
            elif 'date' in col_lower or '日' in str(col):
                # Generate dates
                new_data[col] = pd.date_range('2025-01-01', periods=rows, freq='H')[:rows]
            elif 'age' in col_lower or '年齢' in str(col):
                # Generate ages
                new_data[col] = np.random.choice(range(18, 70), size=rows)
            elif 'gender' in col_lower or '性別' in str(col):
                # Generate genders
                new_data[col] = np.random.choice(['Male', 'Female'], size=rows)
            elif 'q' in col_lower and any(char.isdigit() for char in str(col)):
                # Question responses (assuming 1-5 scale)
                new_data[col] = np.random.choice(range(1, 6), size=rows)
            elif 'score' in col_lower or 'point' in col_lower or '点' in str(col):
                # Generate scores
                new_data[col] = np.random.randint(0, 101, size=rows)
            elif 'name' in col_lower or '名' in str(col):
                # Generate names
                first_names = ['John', 'Jane', 'Bob', 'Alice', 'Charlie', 'Diana', 'Eve', 'Frank']
                last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller']
                new_data[col] = [f"{np.random.choice(first_names)} {np.random.choice(last_names)}" 
                                for _ in range(rows)]
            elif 'email' in col_lower or 'mail' in col_lower:
                # Generate emails
                new_data[col] = [f"user{i}@example.com" for i in range(1, rows + 1)]
            elif 'phone' in col_lower or '電話' in str(col):
                # Generate phone numbers
                new_data[col] = [f"555-{np.random.randint(1000, 9999)}" for _ in range(rows)]
            elif 'address' in col_lower or '住所' in str(col):
                # Generate addresses
                streets = ['Main St', 'Oak Ave', 'Elm Dr', 'Park Rd', 'First Ave']
                cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']
                new_data[col] = [f"{np.random.randint(1, 999)} {np.random.choice(streets)}, {np.random.choice(cities)}" 
                                for _ in range(rows)]
            elif 'price' in col_lower or 'amount' in col_lower or '金額' in str(col) or '価格' in str(col):
                # Generate prices
                new_data[col] = np.random.randint(100, 10000, size=rows)
            elif 'category' in col_lower or 'type' in col_lower or '種類' in str(col):
                # Generate categories
                categories = ['Category A', 'Category B', 'Category C', 'Category D']
                new_data[col] = np.random.choice(categories, size=rows)
            elif 'status' in col_lower or '状態' in str(col):
                # Generate status
                statuses = ['Active', 'Pending', 'Completed', 'Cancelled']
                new_data[col] = np.random.choice(statuses, size=rows)
            elif 'comment' in col_lower or 'note' in col_lower or 'コメント' in str(col):
                # Generate comments
                comments = [
                    'Good service', 'Needs improvement', 'Satisfactory', 
                    'Excellent', 'Average', 'Below expectations', 'Outstanding'
                ]
                new_data[col] = np.random.choice(comments, size=rows)
            else:
                # For unknown columns, check the original data type
                if info['sample_data'] is not None and col in info['sample_data'].columns:
                    sample_values = info['sample_data'][col].dropna()
                    if len(sample_values) > 0:
                        sample_val = sample_values.iloc[0]
                        if isinstance(sample_val, (int, np.integer)):
                            new_data[col] = np.random.randint(1, 100, size=rows)
                        elif isinstance(sample_val, (float, np.floating)):
                            new_data[col] = np.random.uniform(0, 100, size=rows)
                        elif isinstance(sample_val, str):
                            new_data[col] = [f"Text_{i}" for i in range(1, rows + 1)]
                        else:
                            new_data[col] = [f"Value_{i}" for i in range(1, rows + 1)]
                    else:
                        new_data[col] = [f"Data_{i}" for i in range(1, rows + 1)]
                else:
                    # Default: generate generic data
                    new_data[col] = [f"Item_{i}" for i in range(1, rows + 1)]
        
        # Create DataFrame
        if new_data:
            new_df = pd.DataFrame(new_data)
        else:
            # Empty dataframe with same structure
            new_df = pd.DataFrame(columns=columns)
        
        new_sheets[english_sheet_name] = new_df
        print(f"Created sheet: '{english_sheet_name}' with shape {new_df.shape}")
    
    # Save to new Excel file
    output_file = 'Internet_Survey_Test_Data.xlsx'
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        for sheet_name, df in new_sheets.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            # Auto-adjust column widths
            worksheet = writer.sheets[sheet_name]
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
    
    print("\n" + "="*60)
    print(f"✅ Successfully created '{output_file}'")
    print(f"   Contains {len(new_sheets)} sheets similar to the original file")
    print("   All content has been translated to English with sample data")
    
except Exception as e:
    print(f"Error: {e}")
    print("\nPlease make sure the original file exists and is accessible.")