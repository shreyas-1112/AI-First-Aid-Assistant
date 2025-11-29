# AI First Aid Assistant - Quick Start Guide

## Setup Instructions

### 1. Install Python 3.9+

Download from https://www.python.org/downloads/

### 2. Clone/Extract Project

```bash
cd c:\Users\sharm\ai-first-aid-assistant
```

### 3. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure API Key

Edit `config/settings.py` and update:
```python
GEMINI_API_KEY = "AIzaSyDum5wQ8PydeGE-rsvIyiWJMSua9rjsDqs"
```

### 6. Run Backend Server

Open Terminal 1:
```bash
python -m backend.main
```

Wait for message: `Uvicorn running on http://0.0.0.0:8000`

### 7. Run Frontend (New Terminal)

Open Terminal 2:
```bash
venv\Scripts\activate
streamlit run frontend/app.py
```

### 8. Access Application

- Frontend: http://localhost:8501
- API Docs: http://localhost:8000/docs

## Quick Test

1. Go to http://localhost:8501
2. Click "Analyze Image"
3. Upload a sample image or use sample_cut.jpg / sample_burn.jpg from frontend/assets/
4. Fill in patient age group
5. Click "Analyze Image"
6. View results

## Troubleshooting

### Backend won't start
- Check if port 8000 is available: `netstat -an | find "8000"`
- Ensure Python 3.9+ is installed

### Frontend can't connect to backend
- Make sure backend is running first
- Check firewall settings
- Verify BACKEND_URL in config/settings.py

### API Key errors
- Verify API key is correctly set in config/settings.py
- Check API key has proper permissions
- Regenerate API key from Google Cloud Console

### Import errors
- Run `pip install -r requirements.txt` again
- Delete `__pycache__` folders and `.pyc` files
- Recreate virtual environment

## Directory Structure

```
c:\Users\sharm\ai-first-aid-assistant\
├── frontend\
│   ├── app.py
│   ├── components\
│   ├── assets\
│   └── utils\
├── backend\
│   ├── main.py
│   ├── routers\
│   ├── services\
│   ├── data\
│   └── utils\
├── config\
├── requirements.txt
└── README.md
```

## Features

✅ Image analysis using Gemini Vision API
✅ First aid guidance generation
✅ Emergency mode with quick help
✅ Age-appropriate recommendations
✅ Text-to-speech audio guidance
✅ Prevention tips
✅ Safety warnings and disclaimers

## Next Steps

1. Customize first_aid.txt with your medical database
2. Add more injury types and guidance
3. Implement user authentication if needed
4. Deploy to production
5. Add additional safety features

## Support

For issues, check:
- console output for error messages
- API documentation at http://localhost:8000/docs
- requirements.txt for dependency versions

---

⚠️ Remember: This is an educational tool. Always consult healthcare professionals.
