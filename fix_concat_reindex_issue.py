"""
Fix for pandas concat reindexing error when merging files with duplicate column names
"""

import pandas as pd

def fix_duplicate_columns_for_concat(dfs_list):
    """Fix duplicate column names across dataframes before concat"""

    if len(dfs_list) <= 1:
        return dfs_list

    print(f"🔍 Checking for duplicate columns across {len(dfs_list)} dataframes")

    # Collect all column names from all dataframes
    all_columns = set()
    df_columns = []

    for i, df in enumerate(dfs_list):
        cols = list(df.columns)
        df_columns.append(cols)
        all_columns.update(cols)
        print(f"   DataFrame {i+1}: {len(cols)} columns")

        # Check for duplicates within the same dataframe
        if df.columns.duplicated().any():
            print(f"   ⚠️ DataFrame {i+1} has internal duplicate columns")

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
        print(f"   ⚠️ Found {len(problematic_columns)} columns appearing in multiple dataframes")
        for col, df_indices in list(problematic_columns.items())[:5]:  # Show first 5
            print(f"     '{col}' appears in dataframes: {df_indices}")

    # Create union of all columns for consistent structure
    all_columns_list = sorted(list(all_columns))
    print(f"   Total unique columns across all dataframes: {len(all_columns_list)}")

    # Reindex all dataframes to have the same columns
    fixed_dfs = []
    for i, df in enumerate(dfs_list):
        print(f"   Reindexing DataFrame {i+1}...")

        # Reindex to include all columns, filling missing with NaN
        try:
            df_reindexed = df.reindex(columns=all_columns_list, fill_value=None)
            fixed_dfs.append(df_reindexed)
            print(f"     ✅ Reindexed from {len(df.columns)} to {len(df_reindexed.columns)} columns")
        except Exception as e:
            print(f"     ❌ Reindexing failed: {e}")
            # Fallback: keep original dataframe
            fixed_dfs.append(df)

    return fixed_dfs

# Test with sample data
if __name__ == "__main__":
    # Create sample dataframes with overlapping columns (like our Excel files)
    df1 = pd.DataFrame({
        'NO': [1, 2, 3],
        'Q-001': ['A', 'B', 'C'],
        'Q-002': ['X', 'Y', 'Z'],
        'Q-100': ['Data1', 'Data2', 'Data3']  # Only in df1
    })

    df2 = pd.DataFrame({
        'NO': [4, 5],
        'Q-001': ['D', 'E'],
        'Q-003': ['P', 'Q'],  # Only in df2
        'Q-200': ['Data4', 'Data5']  # Only in df2
    })

    print("=== Testing fix_duplicate_columns_for_concat ===")
    fixed_dfs = fix_duplicate_columns_for_concat([df1, df2])

    print(f"\n=== Testing concat with fixed dataframes ===")
    try:
        result = pd.concat(fixed_dfs, ignore_index=True, sort=False)
        print(f"✅ Concat successful: {result.shape}")
        print(f"Result columns: {len(result.columns)}")
    except Exception as e:
        print(f"❌ Concat still failed: {e}")