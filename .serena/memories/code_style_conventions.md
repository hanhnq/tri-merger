# Code Style and Conventions

## Python Code Style
- **Python Version**: 3.11
- **Language**: Mixed Japanese and English (Japanese for UI strings, English for code)
- **Comments**: Japanese comments explaining functionality
- **Docstrings**: Japanese docstrings with clear parameter and return type descriptions

## Naming Conventions
- **Functions**: snake_case (e.g., `check_password`, `verify_password`)
- **Variables**: snake_case with descriptive names
- **Constants**: Not explicitly defined, but would follow UPPER_SNAKE_CASE
- **File names**: English names for modules, Japanese names acceptable for Streamlit pages

## Code Organization
- **Modular structure**: Separate modules for auth, aggregation, and question handling
- **Clear separation of concerns**: Each module handles specific functionality
- **Session state management**: Using `st.session_state` for maintaining state

## Type Hints
- Function signatures include docstrings with type information
- Example:
  ```python
  def check_password():
      """
      パスワード認証を行う関数
      
      Returns:
          bool: 認証成功時True、失敗時False
      """
  ```

## Error Handling
- User-friendly error messages in Japanese
- Using Streamlit's `st.error()` and `st.success()` for feedback

## UI/UX Patterns
- Consistent use of emojis in page titles and buttons
- Clear step-by-step workflow
- Container-based layout with columns
- Expandable sections for detailed information