# AI First Aid Assistant - Complete Usage Guide

## 🎯 Table of Contents
1. [Initial Setup](#initial-setup)
2. [Running the Application](#running-the-application)
3. [Using the Frontend](#using-the-frontend)
4. [API Usage](#api-usage)
5. [Troubleshooting](#troubleshooting)
6. [Advanced Features](#advanced-features)

---

## 🔧 Initial Setup

### Prerequisites
- Windows/Linux/Mac operating system
- Python 3.9 or higher
- At least 2GB free disk space
- Internet connection
- Your Gemini API key

### Step 1: Extract Project Files
Extract the project to your desired location:
```
c:\Users\sharm\ai-first-aid-assistant
```

### Step 2: Run Setup Script

#### Windows:
1. Open File Explorer
2. Navigate to the project folder
3. Double-click `setup.bat`
4. Enter your Gemini API key when prompted
5. Wait for setup to complete

#### Linux/Mac:
1. Open Terminal
2. Navigate to project folder
3. Run: `chmod +x setup.sh && ./setup.sh`
4. Enter your Gemini API key when prompted
5. Wait for setup to complete

### Step 3: Verify Installation
```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Test imports
python -c "import streamlit; import fastapi; import google.generativeai; print('✓ All dependencies installed')"
```

---

## 🚀 Running the Application

### Method 1: Automated (Recommended)

#### Windows:
Create a file `run.bat`:
```batch
@echo off
start cmd /k "venv\Scripts\activate && python -m backend.main"
start cmd /k "venv\Scripts\activate && streamlit run frontend/app.py"
pause
```
Double-click to run both services.

#### Linux/Mac:
Create a file `run.sh`:
```bash
#!/bin/bash
source venv/bin/activate
python -m backend.main &
streamlit run frontend/app.py
```
Run: `chmod +x run.sh && ./run.sh`

### Method 2: Manual (Two Terminals)

#### Terminal 1 - Start Backend:
```bash
# Activate environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Run backend server
python -m backend.main

# Expected output:
# 🏥 AI First Aid Assistant Backend Starting...
# Uvicorn running on http://0.0.0.0:8000
```

#### Terminal 2 - Start Frontend:
```bash
# Activate environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Run frontend app
streamlit run frontend/app.py

# Expected output:
# You can now view your Streamlit app in your browser.
# Local URL: http://localhost:8501
```

### Verify Services Are Running
- Backend: http://localhost:8000 → Should show welcome message
- Frontend: http://localhost:8501 → Should show the web interface
- API Docs: http://localhost:8000/docs → Swagger UI

---

## 📱 Using the Frontend

### Page 1: Analyze Image

#### Step 1: Upload Image
1. Click "Browse Files" button
2. Select an injury image (JPG, PNG, GIF, WebP)
3. Image will be displayed for preview

#### Step 2: Fill Patient Information
- **Age Group**: Select patient's age group (Infant/Child/Adolescent/Adult/Elder)
- **Allergies**: Enter any known allergies (optional)
- **Medications**: List current medications (optional)
- **Conditions**: Select pre-existing conditions (optional)

#### Step 3: Analyze
1. Click "🔍 Analyze Image" button
2. Wait for analysis (may take 5-10 seconds)
3. View results once complete

#### Results Display:
- **Injury Analysis**: Type, severity, affected area, confidence score
- **Emergency Alert**: If detected as emergency
- **First Aid Steps**: Step-by-step instructions
- **Audio Guidance**: Listen to instructions
- **Professional Help**: When to seek help
- **Age-Specific Guidance**: Tailored recommendations
- **Prevention Tips**: How to prevent similar injuries
- **Doctor Recommendations**: Specialist suggestions

### Page 2: Emergency Mode

#### Activate Emergency Mode
1. Click "🚨 Emergency Mode" in sidebar
2. Review emergency procedures
3. Select injury type from dropdown
4. Click "Get Help"
5. Follow emergency instructions
6. **CALL 911** - Do not delay!

#### Emergency Information Provided:
- Immediate actions to take
- Step-by-step emergency procedures
- Do's and don'ts
- Vital signs to monitor
- Emergency contact numbers

### Page 3: Education

Learn first aid from:
- CPR & First Aid Training resources
- Common injury types overview
- Educational resources
- External links to professional training

### Page 4: About

- Application information
- Disclaimer and legal notice
- Emergency numbers
- Privacy and security information

---

## 🔌 API Usage

### Direct API Calls

#### Using Python Requests:
```python
import requests

# Initialize API client
BASE_URL = "http://localhost:8000"

# Health check
response = requests.get(f"{BASE_URL}/health")
print(response.json())

# Get first aid guidance
params = {
    "injury_type": "burn",
    "severity": "moderate",
    "affected_area": "arm",
    "age_group": "adult"
}
response = requests.get(f"{BASE_URL}/first-aid/generate", params=params)
print(response.json())
```

#### Using cURL:
```bash
# Health check
curl http://localhost:8000/health

# Get guidance
curl "http://localhost:8000/first-aid/generate?injury_type=cut&severity=mild&age_group=adult"

# Upload image
curl -F "file=@image.jpg" http://localhost:8000/analyze/image
```

#### Using Postman:
1. Open Postman
2. Create new request
3. Set method and URL
4. Click Send
5. View response

#### Interactive API Docs:
Visit: **http://localhost:8000/docs**
- See all endpoints
- View request/response formats
- Try endpoints directly
- Generate sample requests

### Common API Requests

#### Request 1: Analyze Cut
```
GET /first-aid/generate?injury_type=cut&severity=mild&affected_area=finger&age_group=adult
```

#### Request 2: Emergency - Severe Bleeding
```
GET /first-aid/emergency/severe%20bleeding
```

#### Request 3: Prevention Tips - Burns
```
GET /first-aid/prevention/burns
```

#### Request 4: Upload and Analyze Image
```
POST /analyze/image
Content-Type: multipart/form-data
file: [binary image data]
age_group: adult
```

---

## 🐛 Troubleshooting

### Problem: Backend Won't Start

**Symptoms**: `Error: Port 8000 already in use`

**Solutions**:
```bash
# Check what's using port 8000
netstat -ano | findstr :8000  # Windows
lsof -i :8000  # Linux/Mac

# Kill the process
taskkill /PID <PID> /F  # Windows
kill -9 <PID>  # Linux/Mac

# Or change port in config/settings.py
BACKEND_PORT = 8001
```

### Problem: Frontend Can't Connect

**Symptoms**: Error message "Backend Connection Error"

**Solutions**:
1. Ensure backend is running first
2. Check BACKEND_URL in `config/settings.py`
3. Verify firewall allows connections
4. Check if services are on same network
5. Restart both services

### Problem: API Key Error

**Symptoms**: `Authentication error` or `Invalid API key`

**Solutions**:
1. Open `config/settings.py`
2. Verify API key is correct:
   ```
   GEMINI_API_KEY = "AIzaSyDum5wQ8PydeGE-rsvIyiWJMSua9rjsDqs"
   ```
3. Check API key has proper permissions
4. Regenerate key from Google Cloud Console
5. Restart backend after updating

### Problem: Import Errors

**Symptoms**: `ModuleNotFoundError: No module named 'streamlit'`

**Solutions**:
```bash
# Reinstall all dependencies
pip install -r requirements.txt

# Or specific package
pip install streamlit==1.28.1
```

### Problem: Image Won't Upload

**Symptoms**: File upload fails or shows format error

**Solutions**:
- Use supported formats: JPG, PNG, GIF, WebP
- Ensure file size < 10MB
- Check file permissions
- Try a different image
- Clear browser cache

### Problem: Slow Response

**Symptoms**: Image analysis takes too long (> 30 seconds)

**Solutions**:
1. Check internet connection speed
2. Try smaller image
3. Check API rate limits
4. Restart services
5. Check system resources

---

## 🎯 Advanced Features

### Custom Knowledge Base

Edit `backend/data/first_aid.txt`:
```
1. Add new injury types
2. Update procedures
3. Add region-specific information
4. Include new medical guidelines
5. Add local emergency numbers
```

### Extending Services

#### Add New Injury Type:
1. Update first_aid.txt
2. Add detection in gemini_vision.py
3. Add guidance in generator.py
4. Test with API

#### Add New Component:
1. Create file in frontend/components/
2. Add functions to render UI
3. Import in app.py
4. Add to appropriate page

### Custom API Endpoints

#### Add Endpoint in routers/:
```python
@router.get("/custom")
async def custom_endpoint(param: str):
    # Your logic here
    return {"result": "value"}
```

### Database Integration

Add to services for persistent storage:
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# Setup database
DATABASE_URL = "sqlite:///./first_aid.db"
engine = create_engine(DATABASE_URL)
```

### Authentication

Add to backend/main.py:
```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def verify_token(credentials = Depends(security)):
    # Verify token logic
    return credentials
```

---

## 📊 Performance Optimization

### Frontend Optimization
- Cache results for repeated searches
- Lazy load images
- Minimize state updates

### Backend Optimization
- Implement Redis caching
- Use async operations
- Optimize database queries
- Add pagination

### API Rate Limiting
```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@app.get("/first-aid/generate")
@limiter.limit("30/minute")
async def generate_first_aid(...):
    # Implementation
```

---

## 📈 Monitoring and Logging

### View Logs
```bash
# Check console output
# Look for errors and warnings

# Save logs to file
python -m backend.main > backend.log 2>&1

# View live logs
tail -f backend.log  # Linux/Mac
Get-Content backend.log -Wait  # Windows
```

### Key Metrics to Monitor
- API response time
- Image analysis success rate
- Error frequency
- User activity

---

## 🔐 Security Best Practices

### API Key Security
- Never share API keys
- Use environment variables
- Rotate keys regularly
- Monitor usage

### Data Protection
- Enable HTTPS in production
- Validate all inputs
- Sanitize outputs
- Implement rate limiting

### Access Control
- Use authentication tokens
- Implement role-based access
- Log access attempts
- Regular security audits

---

## 📚 Resources

### Documentation Files
- `README.md` - Full documentation
- `QUICKSTART.md` - Quick start guide
- `INSTALLATION.md` - Installation details
- `API_TESTING.md` - API testing guide
- `DEPLOYMENT.md` - Production deployment
- `PROJECT_SUMMARY.md` - Project overview

### External Resources
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [Google Generative AI](https://ai.google.dev/)
- [Medical Knowledge](https://www.mayoclinic.org/)

### Support
- Check API documentation: http://localhost:8000/docs
- Review error messages in console
- Check logs for detailed errors
- Consult medical professionals for accuracy

---

## 🎓 Example Workflows

### Workflow 1: Analyze a Cut
1. Go to "Analyze Image" page
2. Upload photo of cut
3. Set age group to "Adult"
4. Click "Analyze Image"
5. Review first aid steps
6. Share audio guidance if available
7. Get professional help recommendation

### Workflow 2: Emergency Response
1. Click "Emergency Mode" in sidebar
2. Select "Severe bleeding" from dropdown
3. Click "Get Help"
4. Read emergency instructions
5. **CALL 911 IMMEDIATELY**
6. Follow on-screen guidance while waiting

### Workflow 3: Learning Prevention
1. Go to "Education" page
2. Browse common injuries
3. Read prevention information
4. Learn proper first aid techniques
5. Get certified through recommended courses

---

## ✅ Quality Assurance

### Before Deployment
- [ ] Test all API endpoints
- [ ] Verify image analysis accuracy
- [ ] Check emergency mode functionality
- [ ] Test with different age groups
- [ ] Verify all components render correctly
- [ ] Check error handling
- [ ] Test with poor internet
- [ ] Verify API key functionality

### After Deployment
- [ ] Monitor error logs
- [ ] Track API response times
- [ ] Check user feedback
- [ ] Update knowledge base
- [ ] Apply security patches
- [ ] Regular backups
- [ ] Capacity planning

---

## 🎉 Success Indicators

Your setup is successful when:
- ✅ Backend starts without errors
- ✅ Frontend loads in browser
- ✅ Can upload and analyze image
- ✅ Receive first aid guidance
- ✅ Emergency mode works
- ✅ API documentation accessible
- ✅ All components render properly
- ✅ No error messages in console

---

## 📞 Getting Help

1. **Check Logs**: Look for error messages in console
2. **Read Docs**: Review relevant documentation file
3. **Try API Docs**: Test endpoints at http://localhost:8000/docs
4. **Restart Services**: Kill and restart backend/frontend
5. **Clear Cache**: Browser cache might have old data
6. **Professional Help**: Consult medical professionals for accuracy

---

## ⚠️ Important Reminders

🚨 **MEDICAL DISCLAIMER**
- This is an educational tool only
- NOT a substitute for professional medical advice
- Always consult healthcare professionals
- In emergency: **CALL 911 IMMEDIATELY**
- Results must be verified by medical professionals

---

**Happy First Aid Assisting! 🏥**

For more details, refer to PROJECT_SUMMARY.md or the main documentation.

Last Updated: November 29, 2025
