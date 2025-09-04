# Suggested Commands

## Development Commands

### Running the Application
```bash
# Start the Streamlit application
streamlit run app.py

# Run with specific port
streamlit run app.py --server.port 8501
```

### Python Environment
```bash
# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Freeze dependencies
pip freeze > requirements.txt
```

### Testing and Quality Checks
**Note**: No formal testing framework or linting tools are configured in this project. Consider adding:
```bash
# Install development tools (suggested)
pip install pytest black flake8 mypy

# Run tests (if added)
pytest

# Format code (if black is installed)
black .

# Lint code (if flake8 is installed)
flake8 .
```

### Git Commands
```bash
# Check status
git status

# Add changes
git add .

# Commit with Japanese message
git commit -m "🐛 fix: 日本語ファイル名の文字化け対策を実装"

# Push changes
git push origin main
```

### System Commands (Darwin/macOS)
```bash
# List files (including hidden)
ls -la

# Find files
find . -name "*.py"

# Search in files
grep -r "pattern" .

# Check Python version
python3 --version

# Check disk usage
du -sh *

# Monitor processes
top

# Kill Streamlit process if stuck
pkill -f streamlit
```

### Streamlit-specific Commands
```bash
# Clear cache
streamlit cache clear

# Show config
streamlit config show

# Run with debug mode
streamlit run app.py --logger.level debug
```

## Environment Setup
- Ensure Python 3.11 is installed
- Create `.env` file for environment variables (if needed)
- Configure `.streamlit/secrets.toml` for secrets (ignored by git)