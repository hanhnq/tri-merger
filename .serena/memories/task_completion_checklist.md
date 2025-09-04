# Task Completion Checklist

## When a Task is Completed

Since this project doesn't have formal testing or linting tools configured, follow these manual checks:

### 1. Code Quality Checks
- [ ] Ensure all functions have Japanese docstrings explaining purpose and return values
- [ ] Variable and function names follow snake_case convention
- [ ] Japanese UI strings are properly displayed (no mojibake/文字化け)
- [ ] Code is properly indented and formatted

### 2. Functionality Verification
- [ ] Test the feature in Streamlit locally:
  ```bash
  streamlit run app.py
  ```
- [ ] Verify all three workflow steps work correctly:
  - 質問マスター作成 (Question Master Creation)
  - 設定サンプル作成 (Settings Sample Creation)
  - データ集計 (Data Aggregation)
- [ ] Test with sample Excel files containing Japanese text
- [ ] Verify file uploads and downloads work correctly

### 3. Error Handling
- [ ] Test edge cases (empty files, wrong format, etc.)
- [ ] Ensure error messages are user-friendly and in Japanese
- [ ] Verify authentication and session timeout work properly

### 4. Performance
- [ ] Check that large file processing shows appropriate progress indicators
- [ ] Ensure the app doesn't crash with multiple concurrent users

### 5. Git Workflow
- [ ] Review changes: `git diff`
- [ ] Stage changes: `git add .`
- [ ] Commit with descriptive message (can be in Japanese)
- [ ] Push to repository

### 6. Deployment Considerations
- [ ] Ensure all dependencies are in requirements.txt
- [ ] Verify .gitignore excludes sensitive files
- [ ] Check that secrets are properly configured in .streamlit/secrets.toml

### 7. Documentation
- [ ] Update code comments if logic changed significantly
- [ ] Document any new features or breaking changes
- [ ] Update sample files if data format changed

## Suggested Improvements
Consider adding these tools for better quality assurance:
- **pytest** for unit testing
- **black** for code formatting
- **flake8** or **ruff** for linting
- **mypy** for type checking
- **pre-commit** hooks for automated checks