@echo off
REM AI First Aid Assistant - Windows Setup Script
REM This script sets up the project on Windows

echo.
echo ========================================
echo AI First Aid Assistant Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://www.python.org
    pause
    exit /b 1
)

echo [1/6] Python found!
python --version

REM Create virtual environment
echo.
echo [2/6] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

REM Activate virtual environment
echo.
echo [3/6] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Install dependencies
echo.
echo [4/6] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

REM Configure API key
echo.
echo [5/6] Configuring API key...
python -c "
import os

settings_file = 'config/settings.py'

# Update settings file with provided API key
api_key = input('Enter your Gemini API key: ').strip()

if api_key:
    with open(settings_file, 'r') as f:
        content = f.read()
    
    # Replace the placeholder API key
    new_content = content.replace(
        'GEMINI_API_KEY = os.getenv(\"GEMINI_API_KEY\", \"AIzaSyDum5wQ8PydeGE-rsvIyiWJMSua9rjsDqs\")',
        f'GEMINI_API_KEY = os.getenv(\"GEMINI_API_KEY\", \"{api_key}\")'
    )
    
    with open(settings_file, 'w') as f:
        f.write(new_content)
    
    print(f'API key configured successfully!')
else:
    print('Warning: No API key provided. Update config/settings.py manually.')
"

REM Verify installation
echo.
echo [6/6] Verifying installation...
python -c "import streamlit; import fastapi; import google.generativeai; print('All dependencies installed successfully!')"
if errorlevel 1 (
    echo ERROR: Dependencies verification failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo.
echo Terminal 1 - Run Backend:
echo   venv\Scripts\activate
echo   python -m backend.main
echo.
echo Terminal 2 - Run Frontend:
echo   venv\Scripts\activate
echo   streamlit run frontend/app.py
echo.
echo Then open:
echo   Frontend: http://localhost:8501
echo   API Docs: http://localhost:8000/docs
echo.
pause
