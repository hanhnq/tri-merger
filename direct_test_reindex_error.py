import sys
import os
sys.path.append('.')

from modules.aggregation import aggregate_data
import pandas as pd

def test_reindex_error_directly():
    """Test reindex error trực tiếp với files và mock client settings"""

    print("=== DIRECT REINDEX ERROR TEST ===")

    file_paths = [
        "D:/Downloads/FSS_TryField/jp_test/【2025年8月14日】一般インターネット調査 (2).xlsx",
        "D:/Downloads/FSS_TryField/jp_test/【2025年8月20日】一般インターネット調査 (2).xlsx"
    ]

    # Mock Streamlit uploaded file objects
    class MockUploadedFile:
        def __init__(self, filepath):
            self.name = os.path.basename(filepath)
            self.size = os.path.getsize(filepath)
            self._filepath = filepath

        def read(self):
            with open(self._filepath, 'rb') as f:
                return f.read()

        def seek(self, pos):
            pass

    # Create mock uploaded files
    data_files = [MockUploadedFile(fp) for fp in file_paths]
    print(f"Created {len(data_files)} mock files")

    # Create mock question master
    question_master_data = {
        '質問番号': ['Q-001', 'Q-002', 'Q-003'],
        '質問文': ['あなたの年代性別を教えてください。', 'あなたがお住まいの都道府県をお知らせください。', 'テスト質問']
    }
    question_master_df = pd.DataFrame(question_master_data)
    print(f"Mock question master: {question_master_df.shape}")

    # Create mock client settings
    client_settings_data = {
        'クライアント名': ['テストクライアント'],
        '集計対象の質問文': ['あなたの年代性別を教えてください。']
    }
    client_settings_df = pd.DataFrame(client_settings_data)
    print(f"Mock client settings: {client_settings_df.shape}")

    print(f"\n🚀 CALLING aggregate_data function directly...")
    print("This should trigger all debug output...")

    try:
        client_results, merged_df, logs = aggregate_data(
            data_files,
            question_master_df,
            client_settings_df
        )

        print(f"\n✅ SUCCESS! No reindex error occurred")
        print(f"Client results: {len(client_results)}")
        print(f"Merged data: {merged_df.shape}")
        print(f"Logs: {len(logs)}")

    except Exception as e:
        print(f"\n❌ ERROR CAUGHT: {e}")
        print("🎯 THIS IS THE REINDEXING ERROR!")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_reindex_error_directly()