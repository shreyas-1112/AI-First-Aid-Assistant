# AI First Aid Assistant - Installation Guide

## Quick Start (Windows)

### Option 1: Automated Setup
1. Double-click `setup.bat`
2. Enter your Gemini API key when prompted
3. Follow the on-screen instructions

### Option 2: Manual Setup

```powershell
# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run Backend (Terminal 1)
python -m backend.main

# Run Frontend (Terminal 2)
venv\Scripts\activate
streamlit run frontend/app.py
```

## Quick Start (Linux/Mac)

```bash
# Run automated setup
chmod +x setup.sh
./setup.sh

# Or manual setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Terminal 1: Backend
python -m backend.main

# Terminal 2: Frontend
streamlit run frontend/app.py
```

## Access the Application

- **Frontend UI**: http://localhost:8501
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Configuration

1. **API Key**: 
   - Edit `config/settings.py`
   - Update `GEMINI_API_KEY` with your actual key
   - Or set environment variable: `GEMINI_API_KEY=your_key`

2. **Ports** (if default are in use):
   - Backend: `config/settings.py` -> `BACKEND_PORT`
   - Frontend: `config/settings.py` -> `FRONTEND_PORT`

3. **Backend URL** (for frontend):
   - Update `BACKEND_URL` in `config/settings.py`

## Project Files

```
config/
├── settings.py          # Configuration
├── env.example          # Environment template
└── __init__.py

frontend/
├── app.py              # Main Streamlit app
├── components/         # UI components
├── assets/             # Images (placeholder)
├── utils/
│   └── api_client.py   # Backend API client
└── __init__.py

backend/
├── main.py             # FastAPI app
├── routers/            # API endpoints
├── services/           # Business logic
├── data/
│   └── first_aid.txt   # Knowledge base
├── utils/              # Utilities
└── __init__.py

docs/
├── README.md           # Full documentation
├── QUICKSTART.md       # Quick start guide
├── API_TESTING.md      # API testing guide
└── DEPLOYMENT.md       # Deployment options
```

## Troubleshooting

### Python not found
- Install Python 3.9+ from python.org
- Add to PATH during installation

### Module not found errors
```bash
pip install -r requirements.txt
```

### Backend won't start
- Check if port 8000 is available
- Check firewall settings
- Verify Python 3.9+

### Frontend can't connect to backend
- Ensure backend is running first
- Check BACKEND_URL in config/settings.py
- Verify firewall allows connections

### API Key errors
- Verify key is correctly set in config/settings.py
- Check key has proper permissions
- Get new key from Google Cloud Console

## Next Steps

1. Test with sample images
2. Customize first_aid.txt with your knowledge base
3. Add more injury types
4. Deploy to production (see DEPLOYMENT.md)
5. Integrate with medical databases

## Support

- API Docs: http://localhost:8000/docs (Swagger UI)
- Code: Check main README.md
- Tests: Run API_TESTING.md examples
- Issues: Check console output

## Security Notes

- Never commit API keys
- Use environment variables for sensitive data
- Enable HTTPS for production
- Implement authentication if needed
- Regular security audits recommended

---

For more details, see the comprehensive documentation in README.md
