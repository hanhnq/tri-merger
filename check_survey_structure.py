import pandas as pd
import os

def check_survey_structure(filename):
    """Check the structure of a survey file"""
    print(f"\nChecking: {filename}")
    print("="*60)
    
    try:
        # Check what sheets are available
        excel_file = pd.ExcelFile(filename)
        print(f"Available sheets: {excel_file.sheet_names}")
        
        # Try to read the 質問対応表 sheet
        if '質問対応表' in excel_file.sheet_names:
            print("\n✓ Found '質問対応表' sheet")
            
            # Read with no header first to see the structure
            df = pd.read_excel(filename, sheet_name='質問対応表', header=None)
            print(f"Shape: {df.shape}")
            print("\nFirst 10 rows (raw):")
            print(df.head(10))
            
            # Check what's in row 2 (index=2)
            if len(df) > 2:
                print(f"\nRow 2 (potential header): {df.iloc[2].tolist()}")
            
            # Try the logic from question_master.py
            print("\nTrying to apply question_master.py logic...")
            df_q = pd.read_excel(filename, sheet_name='質問対応表', header=None)
            
            # Set row 2 as header
            df_q.columns = df_q.iloc[2]
            print(f"Columns after setting row 2 as header: {df_q.columns.tolist()}")
            
            # Use rows from index 3 onwards
            df_q = df_q.iloc[3:].reset_index(drop=True)
            print(f"Shape after removing header rows: {df_q.shape}")
            
            # Check if required columns exist
            if '番号' in df_q.columns and '内容' in df_q.columns:
                print("✓ Found required columns '番号' and '内容'")
                
                # Try to extract Q- questions
                df_q_filtered = df_q[df_q['番号'].astype(str).str.startswith('Q-')]
                print(f"Questions starting with 'Q-': {len(df_q_filtered)}")
                
                if len(df_q_filtered) > 0:
                    print("\nFirst few questions:")
                    print(df_q_filtered[['番号', '内容']].head())
            else:
                print("✗ Required columns '番号' and '内容' not found")
                print(f"Available columns: {df_q.columns.tolist()}")
                
        else:
            print("✗ Sheet '質問対応表' not found")
            
            # Check if Question_Master sheet exists (our English version)
            if 'Question_Master' in excel_file.sheet_names:
                print("\nFound 'Question_Master' sheet instead - this is the English version")
                df = pd.read_excel(filename, sheet_name='Question_Master')
                print(f"Columns: {df.columns.tolist()}")
                print(f"Shape: {df.shape}")
                
    except Exception as e:
        print(f"Error: {e}")

# Check all survey files
survey_files = [
    "Automotive_Vehicle_Survey_2025.xlsx",
    "Fitness_Health_Survey_2025.xlsx",
    "Entertainment_Media_Survey_2025.xlsx",
    "Education_Learning_Survey_2025.xlsx",
    "Environmental_Awareness_Survey_2025.xlsx"
]

for survey_file in survey_files:
    if os.path.exists(survey_file):
        check_survey_structure(survey_file)
    else:
        print(f"\n✗ File not found: {survey_file}")