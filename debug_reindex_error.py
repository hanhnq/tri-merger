import pandas as pd
import traceback

# Monkey patch để bắt reindex errors
original_reindex = pd.DataFrame.reindex
original_set_index = pd.DataFrame.set_index
original_pivot_table = pd.DataFrame.pivot_table

def debug_reindex(self, *args, **kwargs):
    try:
        print(f"🔍 REINDEX CALLED: shape={self.shape}, index_unique={self.index.is_unique}")
        print(f"   Index type: {type(self.index)}")
        if hasattr(self.index, 'duplicated'):
            dup_count = self.index.duplicated().sum()
            if dup_count > 0:
                print(f"   ⚠️ DUPLICATE INDEX VALUES: {dup_count}")
                print(f"   Duplicate indices: {self.index[self.index.duplicated()].tolist()[:5]}")

        result = original_reindex(self, *args, **kwargs)
        print(f"   ✅ REINDEX SUCCESS")
        return result
    except Exception as e:
        print(f"   ❌ REINDEX FAILED: {e}")
        print(f"   🎯 THIS IS THE REINDEXING ERROR!")
        traceback.print_exc()
        raise

def debug_set_index(self, *args, **kwargs):
    try:
        print(f"🔍 SET_INDEX CALLED: shape={self.shape}")
        if args:
            col_name = args[0]
            print(f"   Setting index to column: {col_name}")
            if col_name in self.columns:
                col_values = self[col_name]
                unique_count = col_values.nunique()
                total_count = len(col_values)
                print(f"   Column unique values: {unique_count}/{total_count}")
                if unique_count != total_count:
                    dup_count = col_values.duplicated().sum()
                    print(f"   ⚠️ DUPLICATE VALUES IN INDEX COLUMN: {dup_count}")
                    print(f"   Sample duplicates: {col_values[col_values.duplicated()].head(3).tolist()}")

        result = original_set_index(self, *args, **kwargs)
        print(f"   ✅ SET_INDEX SUCCESS")
        return result
    except Exception as e:
        print(f"   ❌ SET_INDEX FAILED: {e}")
        print(f"   🎯 THIS IS THE REINDEXING ERROR!")
        traceback.print_exc()
        raise

def debug_pivot_table(self, *args, **kwargs):
    try:
        print(f"🔍 PIVOT_TABLE CALLED: shape={self.shape}")
        if 'index' in kwargs:
            index_col = kwargs['index']
            print(f"   Pivot index column: {index_col}")
            if index_col in self.columns:
                col_values = self[index_col]
                unique_count = col_values.nunique()
                total_count = len(col_values)
                print(f"   Index column unique values: {unique_count}/{total_count}")

        result = original_pivot_table(self, *args, **kwargs)
        print(f"   ✅ PIVOT_TABLE SUCCESS")
        return result
    except Exception as e:
        print(f"   ❌ PIVOT_TABLE FAILED: {e}")
        print(f"   🎯 THIS IS THE REINDEXING ERROR!")
        traceback.print_exc()
        raise

# Apply monkey patches
pd.DataFrame.reindex = debug_reindex
pd.DataFrame.set_index = debug_set_index
pd.DataFrame.pivot_table = debug_pivot_table

print("🔧 DEBUG PATCHES APPLIED FOR REINDEX ERROR DETECTION")
print("Now any reindex/set_index/pivot_table operations will be logged")