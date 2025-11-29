#!/bin/bash
# AI First Aid Assistant - Linux/Mac Setup Script

echo ""
echo "========================================"
echo "AI First Aid Assistant Setup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.9+ from https://www.python.org"
    exit 1
fi

echo "[1/6] Python found!"
python3 --version

# Create virtual environment
echo ""
echo "[2/6] Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi

# Activate virtual environment
echo ""
echo "[3/6] Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi

# Install dependencies
echo ""
echo "[4/6] Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

# Configure API key
echo ""
echo "[5/6] Configuring API key..."
read -p "Enter your Gemini API key: " api_key

if [ -n "$api_key" ]; then
    # Update settings.py with the API key
    sed -i "s/AIzaSyDum5wQ8PydeGE-rsvIyiWJMSua9rjsDqs/$api_key/" config/settings.py
    echo "API key configured successfully!"
else
    echo "Warning: No API key provided. Update config/settings.py manually."
fi

# Verify installation
echo ""
echo "[6/6] Verifying installation..."
python3 -c "import streamlit; import fastapi; import google.generativeai; print('All dependencies installed successfully!')"
if [ $? -ne 0 ]; then
    echo "ERROR: Dependencies verification failed"
    exit 1
fi

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo ""
echo "Terminal 1 - Run Backend:"
echo "  source venv/bin/activate"
echo "  python -m backend.main"
echo ""
echo "Terminal 2 - Run Frontend:"
echo "  source venv/bin/activate"
echo "  streamlit run frontend/app.py"
echo ""
echo "Then open:"
echo "  Frontend: http://localhost:8501"
echo "  API Docs: http://localhost:8000/docs"
echo ""
