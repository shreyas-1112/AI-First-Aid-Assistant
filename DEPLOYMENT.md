# Deployment Guide

## Production Deployment Options

### Option 1: Local Server (Development)

Already covered in QUICKSTART.md

### Option 2: Docker Containerization

#### Create Dockerfile for Backend

Create `backend/Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Create Dockerfile for Frontend

Create `frontend/Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

RUN pip install --no-cache-dir streamlit

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### Docker Compose

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: backend/Dockerfile
    ports:
      - "8000:8000"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - BACKEND_HOST=0.0.0.0
      - BACKEND_PORT=8000
    volumes:
      - ./backend:/app/backend

  frontend:
    build:
      context: .
      dockerfile: frontend/Dockerfile
    ports:
      - "8501:8501"
    environment:
      - BACKEND_URL=http://backend:8000
    depends_on:
      - backend
    volumes:
      - ./frontend:/app/frontend
```

#### Run with Docker Compose

```bash
docker-compose up
```

### Option 3: Cloud Deployment

#### Google Cloud Platform (GCP)

1. **Create GCP Project**
```bash
gcloud projects create ai-first-aid-assistant
gcloud config set project ai-first-aid-assistant
```

2. **Enable APIs**
```bash
gcloud services enable appengine.googleapis.com
gcloud services enable generativeai.googleapis.com
```

3. **Deploy Backend to Cloud Run**
```bash
cd backend
gcloud run deploy ai-first-aid-backend \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=${GEMINI_API_KEY}
```

4. **Deploy Frontend to App Engine**
```bash
cd frontend

# Create app.yaml
cat > app.yaml << EOF
runtime: python39

env: standard

env_variables:
  BACKEND_URL: "https://ai-first-aid-backend-xxx.a.run.app"
  GEMINI_API_KEY: "${GEMINI_API_KEY}"
EOF

gcloud app deploy
```

#### Heroku Deployment

1. **Install Heroku CLI**
```bash
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

2. **Login to Heroku**
```bash
heroku login
```

3. **Create Procfile**
```
web: python -m uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

4. **Create app.json** for frontend
```json
{
  "name": "AI First Aid Assistant",
  "description": "Medical image analysis and first aid guidance"
}
```

5. **Deploy**
```bash
git init
git add .
git commit -m "Initial commit"
heroku create ai-first-aid-assistant
heroku config:set GEMINI_API_KEY=${GEMINI_API_KEY}
git push heroku main
```

### Option 4: AWS Deployment

#### Using EC2

1. **Launch EC2 Instance**
   - AMI: Ubuntu 20.04 LTS
   - Instance Type: t2.medium (minimum)
   - Security Group: Allow ports 8000, 8501, 80, 443

2. **Setup Server**
```bash
ssh -i key.pem ubuntu@your-instance-ip

# Install Python and dependencies
sudo apt update
sudo apt install python3.9 python3-pip python3-venv

# Clone repository
git clone <repo-url>
cd ai-first-aid-assistant

# Setup virtual environment
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup environment variables
export GEMINI_API_KEY=your_api_key
export BACKEND_HOST=0.0.0.0
export BACKEND_PORT=8000
```

3. **Run with Supervisor**
```bash
sudo apt install supervisor

# Create supervisor config for backend
sudo nano /etc/supervisor/conf.d/backend.conf
```

```ini
[program:ai-first-aid-backend]
directory=/home/ubuntu/ai-first-aid-assistant
command=/home/ubuntu/ai-first-aid-assistant/venv/bin/python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
autostart=true
autorestart=true
stderr_logfile=/var/log/backend.err.log
stdout_logfile=/var/log/backend.out.log
```

4. **Setup Nginx Reverse Proxy**
```bash
sudo apt install nginx

sudo nano /etc/nginx/sites-available/ai-first-aid
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
    }

    location /api {
        proxy_pass http://localhost:8000;
    }
}
```

## Production Checklist

- [ ] Use environment variables for sensitive data (API keys)
- [ ] Enable HTTPS/SSL certificate
- [ ] Configure logging and monitoring
- [ ] Setup database for persistent storage
- [ ] Implement rate limiting
- [ ] Add authentication/authorization
- [ ] Configure backups
- [ ] Setup health checks
- [ ] Document deployment process
- [ ] Test disaster recovery
- [ ] Setup CI/CD pipeline
- [ ] Monitor performance and errors
- [ ] Implement caching layer
- [ ] Setup CDN for static files
- [ ] Document API changes

## Environment Variables

```bash
# API Configuration
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-1.5-flash

# Backend Configuration
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
DEBUG=False

# Frontend Configuration
FRONTEND_HOST=0.0.0.0
FRONTEND_PORT=8501
BACKEND_URL=http://localhost:8000

# Database (if added)
DATABASE_URL=postgresql://user:password@localhost/db

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/ai-first-aid.log
```

## Monitoring and Logging

```bash
# View logs
docker logs container-name

# Health monitoring
curl http://your-app/health

# Performance metrics
# Use tools like Datadog, New Relic, or CloudWatch
```

## Security Best Practices

1. **API Key Management**
   - Never commit API keys
   - Use environment variables
   - Rotate keys regularly
   - Use service accounts

2. **Data Protection**
   - Encrypt data in transit (HTTPS)
   - Encrypt data at rest
   - Implement access controls
   - Regular security audits

3. **Rate Limiting**
```python
# In backend/main.py
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)
```

4. **CORS Configuration**
```python
# Restrict to specific origins in production
allow_origins=["https://yourdomain.com"]
```

## Scaling Considerations

- Load balancing with multiple backend instances
- Caching with Redis
- Database optimization
- CDN for static assets
- Horizontal scaling with Kubernetes

---

For questions about specific platforms, consult their documentation.
