#!/usr/bin/env python3
"""
Compare files 75 and 76 to see differences before and after fix
"""

import pandas as pd
import os

def compare_files_75_76():
    """Compare Q-011 structure between files 75 and 76"""

    print("🔍 COMPARING FILES 75 vs 76 (Before vs After Fix)")
    print("=" * 60)

    downloads_dir = "/Users/member/Downloads"

    files_to_check = [
        ("A社_集計結果 (75).xlsx", "File 75 (Before Fix)"),
        ("A社_集計結果 (76).xlsx", "File 76 (After Fix)")
    ]

    results = {}

    for filename, label in files_to_check:
        file_path = os.path.join(downloads_dir, filename)

        if not os.path.exists(file_path):
            print(f"❌ {filename} not found")
            continue

        try:
            df = pd.read_excel(file_path, sheet_name='元データ')

            # Find Q-011 related columns
            q011_columns = [col for col in df.columns if str(col).startswith('Q-011')]
            main_q011 = [col for col in q011_columns if col == 'Q-011']
            sub_q011 = [col for col in q011_columns if col != 'Q-011']

            # Check user 628 data
            user_628 = df[df['NO'] == 628]

            main_data_count = 0
            sub_data_count = 0

            if main_q011:
                main_data_count = user_628['Q-011'].notna().sum()

            if sub_q011:
                sub_data_count = sum(user_628[col].notna().sum() for col in sub_q011)

            results[label] = {
                'total_shape': df.shape,
                'q011_columns_total': len(q011_columns),
                'main_columns': len(main_q011),
                'sub_columns': len(sub_q011),
                'user_628_rows': len(user_628),
                'main_data_count': main_data_count,
                'sub_data_count': sub_data_count,
                'total_columns': len(df.columns)
            }

            print(f"\n📊 {label}")
            print(f"   File shape: {df.shape}")
            print(f"   Total columns: {len(df.columns)}")
            print(f"   Q-011 columns: {len(q011_columns)} total")
            print(f"     - Main Q-011: {len(main_q011)}")
            print(f"     - Sub Q-011_X: {len(sub_q011)}")
            print(f"   User 628: {len(user_628)} rows")
            print(f"     - Main Q-011 data: {main_data_count} rows")
            print(f"     - Sub Q-011_X data: {sub_data_count} total")

        except Exception as e:
            print(f"❌ Error reading {filename}: {e}")

    # Compare results
    if len(results) == 2:
        labels = list(results.keys())
        before = results[labels[0]]
        after = results[labels[1]]

        print(f"\n📊 COMPARISON SUMMARY:")
        print(f"Total columns: {before['total_columns']} → {after['total_columns']} ({after['total_columns'] - before['total_columns']:+d})")
        print(f"Q-011 columns: {before['q011_columns_total']} → {after['q011_columns_total']} ({after['q011_columns_total'] - before['q011_columns_total']:+d})")
        print(f"User 628 main data: {before['main_data_count']} → {after['main_data_count']} ({after['main_data_count'] - before['main_data_count']:+d})")
        print(f"User 628 sub data: {before['sub_data_count']} → {after['sub_data_count']} ({after['sub_data_count'] - before['sub_data_count']:+d})")

        # Analysis
        print(f"\n💡 ANALYSIS:")
        if after['total_columns'] < before['total_columns']:
            print("✅ Column count reduced - good sign of consolidation")
        elif after['total_columns'] > before['total_columns']:
            print("❌ Column count increased - might indicate problems")
        else:
            print("⚪ Column count same - no structural change")

        if after['main_data_count'] == 0 and after['sub_data_count'] > 0:
            print("✅ Pure M/A structure - only sub columns have data")
        elif after['main_data_count'] > 0 and after['sub_data_count'] == 0:
            print("✅ Pure S/A structure - only main column has data")
        elif after['main_data_count'] > 0 and after['sub_data_count'] > 0:
            print("❌ Mixed structure - both main and sub have data (PROBLEM)")
        else:
            print("⚠️ No data found in Q-011 columns")

    return True

if __name__ == '__main__':
    compare_files_75_76()