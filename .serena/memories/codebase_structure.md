# Codebase Structure

## Directory Layout
```
tri-merger-python/
├── app.py                    # Main application entry point
├── requirements.txt          # Python dependencies
├── .python-version          # Python version (3.11)
├── .gitignore               # Git ignore file
├── client_settings.xlsx     # Client configuration file
├── client_settings_sample.xlsx  # Sample configuration
├── modules/                 # Core application modules
│   ├── __init__.py
│   ├── auth.py             # Authentication logic
│   ├── aggregation.py      # Data aggregation logic
│   └── question_master.py  # Question master creation
├── pages/                   # Streamlit pages (multi-page app)
│   ├── 1_📝_質問マスター作成.py
│   ├── 2_⚙️_設定サンプル作成.py
│   └── 3_📊_データ集計.py
├── .streamlit/              # Streamlit configuration
│   └── config.toml
└── .devcontainer/           # Dev container configuration

## Key Files
- **app.py**: Main entry point with navigation and authentication check
- **modules/auth.py**: Password authentication with session timeout
- **modules/aggregation.py**: Core data processing and aggregation logic
- **modules/question_master.py**: Question extraction and mapping logic
- **pages/**: Individual pages for the 3-step workflow

## Data Flow
1. Upload survey Excel files → Extract questions → Create master file
2. Configure client settings → Define which questions per client
3. Upload all data → Process based on settings → Generate output files