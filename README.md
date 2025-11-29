# AI First Aid Assistant

A comprehensive AI-powered medical image analysis and first aid guidance system using Google Gemini's Vision API.

## Features

- 🤖 **AI-Powered Image Analysis**: Upload injury images for instant analysis using Gemini Vision API
- 🏥 **First Aid Guidance**: Get step-by-step first aid instructions based on injury type and severity
- 🚨 **Emergency Mode**: Quick access to emergency procedures and contact information
- 👶 **Age-Appropriate Guidance**: Customized guidance for infants, children, and elderly patients
- 🔊 **Audio Assistance**: Listen to first aid guidance (text-to-speech)
- 📚 **Knowledge Base**: Comprehensive database of first aid information
- ⚠️ **Safety Warnings**: Prominent emergency alerts and professional consultation recommendations

## Project Structure

```
ai-first-aid-assistant/
├── frontend/                 # Streamlit web interface
│   ├── app.py              # Main application
│   ├── components/         # UI components
│   │   ├── upload_box.py
│   │   ├── panic_mode.py
│   │   ├── audio_player.py
│   │   ├── result_cards.py
│   │   ├── warning_box.py
│   │   └── doctor_box.py
│   ├── assets/             # Images and static files
│   └── utils/
│       └── api_client.py   # Backend API client
├── backend/                # FastAPI backend
│   ├── main.py            # Main application
│   ├── routers/           # API endpoints
│   │   ├── analyze_image.py
│   │   └── generate_first_aid.py
│   ├── services/          # Business logic
│   │   ├── gemini_vision.py
│   │   ├── generator.py
│   │   ├── rag_engine.py
│   │   ├── panic_mode.py
│   │   ├── child_elder_detector.py
│   │   └── audio_generator.py
│   ├── data/
│   │   └── first_aid.txt  # Knowledge base
│   └── utils/             # Utility functions
│       ├── chunker.py
│       ├── response_builder.py
│       └── file_utils.py
├── config/                 # Configuration
│   ├── settings.py
│   └── env.example
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager
- Gemini API key from Google

### Setup Steps

1. **Clone the repository**
```bash
git clone <repository-url>
cd ai-first-aid-assistant
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp config/env.example config/.env
```

Edit `.env` file and add your Gemini API key:
```
GEMINI_API_KEY=your_actual_api_key_here
```

## Running the Application

### Start the Backend Server

```bash
python -m backend.main
```

The backend API will be available at `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`

### Start the Frontend Application (in a new terminal)

```bash
streamlit run frontend/app.py
```

The frontend will be available at `http://localhost:8501`

## API Endpoints

### Image Analysis
- **POST** `/analyze/image` - Upload and analyze an injury image

### First Aid Generation
- **GET** `/first-aid/generate` - Get first aid guidance
- **GET** `/first-aid/emergency/{injury_type}` - Get emergency instructions
- **POST** `/first-aid/audio` - Generate audio guidance
- **GET** `/first-aid/prevention/{injury_type}` - Get prevention tips

### Health Check
- **GET** `/health` - Check API availability

## Configuration

Edit `config/settings.py` to customize:
- API endpoints and ports
- File upload limits
- TTS settings
- Backend URL for frontend

## Usage

1. **Upload an Image**: Take a photo of the injury and upload it
2. **Select Age Group**: Specify the patient's age group for appropriate guidance
3. **View Analysis**: See injury type, severity, and first aid steps
4. **Get Guidance**: Read or listen to step-by-step first aid instructions
5. **Seek Professional Help**: Follow recommendations to consult healthcare professionals

## Important Disclaimers

⚠️ **MEDICAL DISCLAIMER**

This application provides **GENERAL EDUCATIONAL INFORMATION ONLY** and is **NOT a substitute for professional medical advice, diagnosis, or treatment**.

- Always consult with qualified healthcare professionals
- In case of emergency, call 911 immediately
- Do not delay seeking professional help
- Results should be verified by medical professionals
- Not suitable for production medical use

## Safety Features

- 🚨 Emergency mode with quick access to emergency numbers
- ⚠️ Prominent disclaimers and warnings
- 👨‍⚕️ Recommendations to consult healthcare professionals
- 📞 Emergency contact information
- 🔒 Privacy protections for uploaded images

## Technologies Used

- **Frontend**: Streamlit (Python UI framework)
- **Backend**: FastAPI (Python web framework)
- **AI/ML**: Google Gemini 1.5 Vision API
- **Database**: File-based knowledge base
- **TTS**: pyttsx3 for text-to-speech
- **API**: RESTful API with async operations

## Development

### Project Setup for Development

```bash
# Install development dependencies
pip install -r requirements.txt
pip install pytest pytest-asyncio

# Run tests
pytest

# Format code
black frontend/ backend/

# Lint code
flake8 frontend/ backend/
```

## Future Enhancements

- [ ] Integration with real medical databases
- [ ] Multi-language support
- [ ] Machine learning model improvements
- [ ] Real-time video analysis
- [ ] Integration with emergency services APIs
- [ ] Mobile app version
- [ ] Advanced symptom checker
- [ ] Patient history tracking

## Contributing

Contributions are welcome! Please ensure:
- Code follows PEP 8 style guidelines
- Changes are tested
- Documentation is updated
- Medical accuracy is maintained

## License

This project is provided as-is for educational purposes.

## Support

For issues and questions:
- Check the documentation
- Review the API documentation at `/docs`
- Consult medical professionals for health concerns

## Acknowledgments

- Google Gemini API for image analysis capabilities
- Streamlit for the frontend framework
- FastAPI for the backend framework
- First aid knowledge from established medical sources

---

**Remember**: This is an educational tool. Always seek professional medical help for actual medical emergencies.

🏥 **In Case of Emergency: CALL 911** 🏥
