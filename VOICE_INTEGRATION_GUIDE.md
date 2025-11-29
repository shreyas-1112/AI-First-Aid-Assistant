# Voice Feature Integration Guide

## ✅ What's Been Added

### 1. **Backend Voice Coach Service** (`backend/services/voice_coach.py`)
- Real-time voice-guided first aid coaching
- Step-by-step guidance with voice announcements
- Automatic timer generation with voice cues
- Emergency voice guides
- Customizable voice settings (speed, volume)

### 2. **Voice Router** (`backend/routers/voice_coach.py`)
New API endpoints:
- `POST /voice/prepare-coaching` - Prepare voice coaching session
- `GET /voice/step-guidance/{step_number}` - Get voice for specific step
- `POST /voice/emergency-guide` - Emergency voice guidance
- `POST /voice/audio-summary` - Generate audio summary
- `POST /voice/settings` - Update voice settings
- `GET /voice/settings` - Get current settings

### 3. **Streamlit Voice Coach Component** (`frontend/components/voice_coach.py`)
- Display voice coaching UI
- Step-by-step instruction with voice buttons
- Countdown timer with visual feedback
- Voice settings adjustments
- Emergency guidance display
- Pause menu controls

### 4. **Updated Frontend** (`frontend/app.py`)
- New "🎤 Voice Coach" page
- Integrated voice coach component
- Direct voice coaching mode access

### 5. **Updated API Client** (`frontend/utils/api_client.py`)
New client methods:
- `prepare_voice_coaching()` - Start voice session
- `get_voice_step_guidance()` - Get step voice
- `create_emergency_voice_guide()` - Emergency guide
- `generate_audio_summary()` - Audio summary
- `update_voice_settings()` - Adjust settings
- `get_voice_settings()` - Get settings

### 6. **Updated Backend Main** (`backend/main.py`)
- Integrated voice_coach router
- Updated API endpoints documentation

---

## 🚀 How to Use Voice Features

### Step 1: Start the Backend
```powershell
python -m backend.main
```

### Step 2: Start the Frontend
```powershell
streamlit run frontend/app.py
```

### Step 3: Use Voice Coach Mode

1. Navigate to **"🎤 Voice Coach"** in the sidebar
2. Select:
   - Injury type (e.g., "Burns", "Cuts", etc.)
   - Severity level (Mild, Moderate, Severe)
   - Patient age group (Child, Adult, Elder)
3. Click **"🎙️ Start Voice Coaching"**
4. Follow the voice-guided steps:
   - 🔊 Listen to step instructions
   - ⏱️ Use countdown timer
   - 📋 Follow written instructions
   - ⏯️ Use pause menu as needed

### Step 4: Adjust Voice Settings
- Use the "🔧 Voice Settings" section to adjust:
  - Speech Rate (50-300 words per minute)
  - Volume (0.0 to 1.0)

---

## 📱 Features Overview

### Voice Guidance Features
✅ **Step Announcements** - Voice reads each step title and description  
✅ **Action Cues** - Voice announces what action to perform  
✅ **Timer Announcements** - Voice announces time intervals during timed steps  
✅ **Emergency Alerts** - Urgent voice guidance for emergencies  
✅ **Completion Messages** - Voice confirms when guidance is complete  

### Interactive Controls
✅ **Read Step Button** - Play voice for current step  
✅ **Read Instructions Button** - Play action instructions only  
✅ **Start Timer Button** - Begin countdown with visual progress  
✅ **Pause Menu** - Resume, Repeat, Skip, or End session  
✅ **Voice Settings** - Adjust speed and volume  

### Timer Features
✅ **Countdown Display** - Visual progress bar with remaining time  
✅ **Color-Coded Urgency** - Green→Yellow→Red as time runs out  
✅ **Automatic Announcements** - Voice cues at key intervals  
✅ **Time Estimation** - Total duration calculation  

---

## 🔧 Technical Details

### Voice Generation Flow
```
User Request
    ↓
Voice Coach Service
    ↓
Audio Generator Service (pyttsx3)
    ↓
Text-to-Speech Audio
    ↓
Frontend Audio Player
    ↓
User Listens
```

### API Request Example
```bash
POST /voice/prepare-coaching
{
    "injury_type": "Burns",
    "severity": "moderate",
    "age_group": "adult"
}

Response:
{
    "status": "success",
    "data": {
        "injury_type": "Burns",
        "total_steps": 5,
        "opening_announcement": {...},
        "steps": [...],
        "closing_announcement": {...},
        "estimated_duration": 180
    }
}
```

---

## 🎯 Usage Scenarios

### 1. **Emergency Situation** 
- User is injured and needs hands-free guidance
- Voice Coach provides step-by-step instructions
- Timer keeps user informed on timing

### 2. **Learning**
- User wants to learn first aid procedures
- Voice guidance reinforces written instructions
- Adjustable speed helps learning pace

### 3. **Accessibility**
- Voice helps visually impaired users
- Audio guidance is clearer than reading
- Timer provides structure

### 4. **Quick Reference**
- User needs fast guidance
- Voice is faster to consume than reading
- Can repeat steps as needed

---

## 📊 Supported Injury Types

- Cuts and Wounds
- Burns
- Fractures
- Head Injury
- Shock
- Allergic Reaction
- Severe Bleeding
- Choking
- Poisoning
- Other

---

## ⚙️ Voice Settings

**Speech Rate:** 50-300 words per minute
- 50-100: Slow (good for understanding)
- 100-200: Normal (standard)
- 200-300: Fast (experienced users)

**Volume:** 0.0-1.0
- 0.0: Silent
- 0.5: Medium
- 0.9: Loud (recommended for emergencies)

---

## 🐛 Troubleshooting

### Issue: No Audio
**Solution:** Check if pyttsx3 is installed
```powershell
pip install pyttsx3
```

### Issue: Audio Playing Slowly
**Solution:** Increase speech rate in settings

### Issue: Can't Hear Audio
**Solution:** 
1. Check system volume
2. Adjust voice volume in settings
3. Check speaker connections

### Issue: Backend Connection Error
**Solution:**
1. Ensure backend is running: `python -m backend.main`
2. Check backend port is 8000
3. Verify no firewall issues

---

## 📝 Integration Checklist

- ✅ Voice Coach Service created
- ✅ Voice Router created
- ✅ Voice Component created
- ✅ Frontend updated with Voice Coach page
- ✅ API Client updated with voice methods
- ✅ Backend main.py updated
- ✅ Audio dependencies installed (pyttsx3)
- ✅ All imports properly configured

---

## 🔗 File References

**Backend:**
- `/backend/services/voice_coach.py` - Voice coaching logic
- `/backend/routers/voice_coach.py` - Voice API endpoints
- `/backend/main.py` - Updated with voice router

**Frontend:**
- `/frontend/components/voice_coach.py` - UI components
- `/frontend/app.py` - Voice Coach page
- `/frontend/utils/api_client.py` - Voice API methods

**Configuration:**
- `/requirements.txt` - pyttsx3 already included

---

## 🎉 Next Steps

1. **Test the Integration**
   - Start backend: `python -m backend.main`
   - Start frontend: `streamlit run frontend/app.py`
   - Try Voice Coach mode

2. **Customize Voice Output**
   - Modify voice settings for your preferences
   - Adjust speech rate and volume

3. **Enhance Features (Optional)**
   - Add more injury types
   - Customize voice messages
   - Add different voice profiles
   - Integrate with external audio services

4. **Gather Feedback**
   - Test with users
   - Refine voice messages based on feedback
   - Improve timer announcements

---

**Version:** 1.0.0  
**Last Updated:** 2025-11-29  
**Status:** ✅ Ready to Use
