# Project Overview

## Project Purpose
This is an **アンケート集計システム (Survey Aggregation System)** - a web application built with Streamlit for aggregating and analyzing survey data from multiple Excel files. The system is designed to handle Japanese questionnaires and provides a 3-step workflow for processing survey data.

## Tech Stack
- **Python 3.11** - Main programming language
- **Streamlit 1.31.0** - Web application framework
- **pandas 2.1.4** - Data manipulation and analysis
- **openpyxl 3.1.5** - Excel file reading/writing
- **xlsxwriter 3.2.5** - Excel file creation
- **python-dotenv 1.0.0** - Environment variable management

## Main Features
1. **質問マスター作成 (Question Master Creation)** - Creates a master mapping of question numbers and texts from survey files
2. **クライアント設定 (Client Settings)** - Configure which questions to aggregate for each client
3. **データ集計実行 (Data Aggregation)** - Execute the aggregation based on settings and generate client-specific reports

## Application Type
This is a Streamlit-based web application with authentication, designed for internal use in processing and aggregating survey data from multiple sources.