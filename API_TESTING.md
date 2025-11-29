# API Testing Guide

## Test the API Endpoints

### Using cURL

#### 1. Health Check
```bash
curl http://localhost:8000/health
```

Expected Response:
```json
{"status": "healthy", "version": "1.0.0"}
```

#### 2. Root Endpoint
```bash
curl http://localhost:8000/
```

#### 3. Get First Aid Guidance
```bash
curl "http://localhost:8000/first-aid/generate?injury_type=cut&severity=moderate&affected_area=hand&age_group=adult"
```

#### 4. Get Emergency Guidance
```bash
curl http://localhost:8000/first-aid/emergency/severe%20bleeding
```

#### 5. Get Prevention Tips
```bash
curl http://localhost:8000/first-aid/prevention/burns
```

### Using Python Requests

```python
import requests

# Health check
response = requests.get("http://localhost:8000/health")
print(response.json())

# Get first aid guidance
params = {
    "injury_type": "burn",
    "severity": "moderate",
    "affected_area": "arm",
    "age_group": "adult"
}
response = requests.get("http://localhost:8000/first-aid/generate", params=params)
print(response.json())

# Upload image
files = {"file": open("path/to/image.jpg", "rb")}
response = requests.post("http://localhost:8000/analyze/image", files=files)
print(response.json())
```

### Using Postman

1. Open Postman
2. Create new request
3. Set method to GET/POST
4. Enter URL: http://localhost:8000/health
5. Click Send

### Interactive API Documentation

Visit: http://localhost:8000/docs

- Try all endpoints directly from the browser
- See request/response schemas
- Test with sample data

## Expected Response Format

```json
{
  "status": "success",
  "timestamp": "2024-01-01T12:00:00.000000",
  "data": {
    "injury_type": "burn",
    "severity": "moderate",
    "affected_area": "arm",
    "age_group": "adult",
    "is_emergency": false,
    "first_aid_steps": [
      {
        "order": 1,
        "title": "Cool the burn",
        "description": "Immerse in cool water for 15-20 minutes",
        "warning": "Do not use ice",
        "duration": "15-20 minutes"
      }
    ],
    "professional_help": "...",
    "emergency_number": "911",
    "confidence_score": 0.85
  }
}
```

## Test Scenarios

### Scenario 1: Minor Cut
```
Endpoint: /first-aid/generate
Parameters:
  - injury_type: cut
  - severity: mild
  - affected_area: finger
  - age_group: adult
```

### Scenario 2: Severe Burn (Emergency)
```
Endpoint: /first-aid/emergency/burn
```

### Scenario 3: Child Fracture
```
Endpoint: /first-aid/generate
Parameters:
  - injury_type: fracture
  - severity: severe
  - affected_area: arm
  - age_group: child
```

### Scenario 4: Elder with Head Injury
```
Endpoint: /first-aid/generate
Parameters:
  - injury_type: head injury
  - severity: moderate
  - age_group: elder
```

## Performance Testing

### Load Testing with Apache Bench
```bash
ab -n 100 -c 10 http://localhost:8000/health
```

### Performance Metrics
- Endpoint response time: < 2 seconds (without image analysis)
- Image analysis time: 3-10 seconds (depends on image size)
- Concurrent requests: minimum 10

## Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| 404 Not Found | Check endpoint URL spelling |
| 500 Server Error | Check backend logs for detailed error |
| Connection refused | Ensure backend is running on port 8000 |
| CORS error | Check CORS middleware in main.py |
| API key error | Verify GEMINI_API_KEY in settings.py |

## Debugging Tips

1. Enable debug logging in backend
2. Check console output for error messages
3. Use print statements in service functions
4. Monitor network requests with browser DevTools
5. Test endpoints one by one

---

For more details, see the main README.md
