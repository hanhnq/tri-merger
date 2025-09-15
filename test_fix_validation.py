#!/usr/bin/env python3
"""
Test script to validate the reindex fix with actual Excel files
"""
import pandas as pd
import sys
import os

def test_concat_fix():
    """Test the concat fix with actual Excel files"""

    file_paths = [
        "D:/Downloads/FSS_TryField/jp_test/【2025年8月14日】一般インターネット調査 (2).xlsx",
        "D:/Downloads/FSS_TryField/jp_test/【2025年8月20日】一般インターネット調査 (2).xlsx"
    ]

    # Verify files exist
    for fp in file_paths:
        if not os.path.exists(fp):
            print(f"❌ File not found: {fp}")
            return False

    print("=== TESTING CONCAT FIX WITH ACTUAL EXCEL FILES ===")

    # Read Excel files and extract data sheets (similar to aggregation logic)
    dataframes = []

    for i, file_path in enumerate(file_paths):
        print(f"\n📁 Processing file {i+1}: {os.path.basename(file_path)}")

        try:
            # Read Excel file
            xls = pd.ExcelFile(file_path, engine='openpyxl')
            print(f"   Available sheets: {xls.sheet_names}")

            # Look for data sheet (excluding 質問対応表)
            data_sheets = [name for name in xls.sheet_names if name != '質問対応表']

            if data_sheets:
                sheet_name = data_sheets[0]  # Use first data sheet
                print(f"   Reading sheet: {sheet_name}")

                df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')
                print(f"   Shape: {df.shape}")
                print(f"   Columns: {len(df.columns)} ({list(df.columns[:5])}...)")

                dataframes.append(df)
            else:
                print(f"   ⚠️ No data sheets found")

        except Exception as e:
            print(f"   ❌ Error reading file: {e}")

    if len(dataframes) < 2:
        print(f"\n❌ Need at least 2 dataframes to test concat, got {len(dataframes)}")
        return False

    print(f"\n🔧 Testing concat with {len(dataframes)} dataframes...")

    # Test original concat (should fail)
    print("\n1️⃣ Testing original concat (should fail):")
    try:
        result_original = pd.concat(dataframes, ignore_index=True, sort=False)
        print(f"   ✅ Original concat succeeded: {result_original.shape}")
        print("   ⚠️ Unexpected! Original concat should have failed")
    except Exception as e:
        print(f"   ❌ Original concat failed (as expected): {e}")

    # Test with our fix
    print("\n2️⃣ Testing with column conflict fix:")

    def fix_duplicate_columns_for_concat(dfs_list):
        """Fix duplicate column names across dataframes before concat"""
        if len(dfs_list) <= 1:
            return dfs_list

        print(f"   🔍 Checking for duplicate columns across {len(dfs_list)} dataframes")

        # Collect all column names from all dataframes
        all_columns = set()
        df_columns = []

        for i, df in enumerate(dfs_list):
            cols = list(df.columns)
            df_columns.append(cols)
            all_columns.update(cols)
            print(f"      DataFrame {i+1}: {len(cols)} columns")

            # Check for duplicates within the same dataframe
            if df.columns.duplicated().any():
                print(f"      ⚠️ DataFrame {i+1} has internal duplicate columns")

        # Find columns that appear in multiple dataframes
        column_counts = {}
        for i, cols in enumerate(df_columns):
            for col in cols:
                if col not in column_counts:
                    column_counts[col] = []
                column_counts[col].append(i)

        # Identify problematic columns (appear in multiple dataframes)
        problematic_columns = {col: dfs for col, dfs in column_counts.items() if len(dfs) > 1}

        if problematic_columns:
            print(f"      ⚠️ Found {len(problematic_columns)} columns appearing in multiple dataframes")
            for col, df_indices in list(problematic_columns.items())[:3]:  # Show first 3
                print(f"         '{col}' appears in dataframes: {df_indices}")

        # Create union of all columns for consistent structure
        all_columns_list = sorted(list(all_columns))
        print(f"      Total unique columns across all dataframes: {len(all_columns_list)}")

        # Reindex all dataframes to have the same columns
        fixed_dfs = []
        for i, df in enumerate(dfs_list):
            print(f"      Reindexing DataFrame {i+1}...")

            # Reindex to include all columns, filling missing with NaN
            try:
                df_reindexed = df.reindex(columns=all_columns_list, fill_value=None)
                fixed_dfs.append(df_reindexed)
                print(f"         ✅ Reindexed from {len(df.columns)} to {len(df_reindexed.columns)} columns")
            except Exception as e:
                print(f"         ❌ Reindexing failed: {e}")
                # Fallback: keep original dataframe
                fixed_dfs.append(df)

        return fixed_dfs

    try:
        # Apply fix
        fixed_dataframes = fix_duplicate_columns_for_concat(dataframes)

        # Test concat with fixed dataframes
        result_fixed = pd.concat(fixed_dataframes, ignore_index=True, sort=False)
        print(f"   ✅ Fixed concat succeeded: {result_fixed.shape}")
        print(f"   📊 Final result: {result_fixed.shape[0]} rows, {result_fixed.shape[1]} columns")

        return True

    except Exception as e:
        print(f"   ❌ Fixed concat failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_concat_fix()
    print(f"\n{'='*60}")
    if success:
        print("🎉 CONCAT FIX VALIDATION: SUCCESS")
        print("   The column conflict resolution fix is working!")
    else:
        print("💥 CONCAT FIX VALIDATION: FAILED")
        print("   The fix needs further adjustment")
    print("="*60)