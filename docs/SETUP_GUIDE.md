# BluePeak Compass - Complete Setup Guide

Step-by-step guide to set up BluePeak Compass from scratch.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Database Configuration](#database-configuration)
4. [Environment Configuration](#environment-configuration)
5. [Running the Application](#running-the-application)
6. [Generating Dummy Data](#generating-dummy-data)
7. [Testing](#testing)
8. [Production Deployment](#production-deployment)
9. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

1. **Python 3.11+**
   ```bash
   python --version  # Should show 3.11 or higher
   ```
   Download: https://www.python.org/downloads/

2. **Node.js 18+**
   ```bash
   node --version  # Should show 18.0 or higher
   npm --version
   ```
   Download: https://nodejs.org/

3. **Docker & Docker Compose**
   ```bash
   docker --version
   docker-compose --version
   ```
   Download: https://www.docker.com/get-started

4. **Git**
   ```bash
   git --version
   ```

### Required Accounts

1. **Anthropic Claude API**
   - Sign up at: https://console.anthropic.com/
   - Generate API key from dashboard
   - Cost: ~$0.50-$2.00 per 1000 requests

2. **Supabase**
   - Sign up at: https://supabase.com
   - Create new project
   - Free tier available

3. **Optional: Slack**
   - Create Slack app: https://api.slack.com/apps
   - Install to workspace
   - Get Bot Token

4. **Optional: SendGrid**
   - Sign up at: https://sendgrid.com
   - Generate API key
   - Verify sender email

---

## Local Development Setup

### 1. Clone Repository

```bash
git clone <repository-url>
cd bluepeak-compass
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import fastapi; import langchain; print('Backend dependencies OK')"
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Verify installation
npm run build  # Should complete without errors
```

---

## Database Configuration

### 1. Create Supabase Project

1. Go to https://supabase.com/dashboard
2. Click "New Project"
3. Fill in project details:
   - Name: bluepeak-compass
   - Database Password: (save this securely)
   - Region: Choose closest to you
4. Wait for project to initialize (~2 minutes)

### 2. Get Supabase Credentials

From your Supabase project dashboard:

1. Go to Settings > API
2. Copy these values:
   - **Project URL** (e.g., https://xxxxx.supabase.co)
   - **Anon/Public Key** (starts with eyJ...)
   - **Service Role Key** (starts with eyJ... - keep secret!)

### 3. Run Database Schema

1. Go to SQL Editor in Supabase dashboard
2. Create new query
3. Copy entire contents of `database/schema.sql`
4. Run the query
5. Verify tables created:
   - competitors
   - trends
   - research_findings
   - reports
   - conversations
   - integration_settings
   - social_mentions
   - products

---

## Environment Configuration

### 1. Backend Environment

```bash
cd backend
cp .env.example .env
```

Edit `.env` with your actual values:

```env
# Application
APP_NAME=BluePeak Compass
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=INFO

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_PREFIX=/api/v1

# Claude API (REQUIRED)
ANTHROPIC_API_KEY=sk-ant-xxxxx  # Your Claude API key
CLAUDE_MODEL=claude-3-5-sonnet-20241022
MAX_TOKENS=4096

# Supabase (REQUIRED)
SUPABASE_URL=https://xxxxx.supabase.co  # Your Supabase URL
SUPABASE_KEY=eyJ...  # Your anon key
SUPABASE_SERVICE_KEY=eyJ...  # Your service key

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=

# Vector Database
CHROMA_HOST=localhost
CHROMA_PORT=8001
CHROMA_PERSIST_DIR=./data/chroma

# Authentication
SECRET_KEY=your-secret-key-change-in-production  # Generate with: openssl rand -hex 32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Integrations (OPTIONAL)
SLACK_BOT_TOKEN=xoxb-xxxxx  # If using Slack
SLACK_SIGNING_SECRET=xxxxx
SENDGRID_API_KEY=SG.xxxxx  # If using SendGrid
FROM_EMAIL=noreply@bluepeak.ai

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_PERIOD=60

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# WebSocket
WS_HEARTBEAT_INTERVAL=30
```

### 2. Frontend Environment

```bash
cd frontend
cp .env.local.example .env.local
```

Edit `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...
```

---

## Running the Application

### Option 1: Docker Compose (Recommended for Quick Start)

```bash
# From project root
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

Access:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/v1/docs

### Option 2: Manual (Better for Development)

**Terminal 1 - Redis:**
```bash
docker run -d -p 6379:6379 redis:7-alpine
# Or if Redis installed locally:
redis-server
```

**Terminal 2 - Backend:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 3 - Frontend:**
```bash
cd frontend
npm run dev
```

### Verify Installation

1. **Backend Health Check:**
   ```bash
   curl http://localhost:8000/health
   # Should return: {"status":"healthy","environment":"development"}
   ```

2. **Frontend:**
   - Open http://localhost:3000
   - Should see BluePeak Compass dashboard

3. **API Documentation:**
   - Open http://localhost:8000/api/v1/docs
   - Interactive Swagger UI should load

---

## Generating Dummy Data

### Run Data Generator

```bash
cd scripts

# Make sure backend is running first!

# Activate backend virtual environment
source ../backend/venv/bin/activate

# Run generator
python generate_dummy_data.py
```

This will create:
- ✓ 10 competitor companies with realistic data
- ✓ 8 market trends with confidence scores
- ✓ ~40 research findings across competitors
- ✓ 4 sample reports
- ✓ 2 sample conversations

### Verify Data

1. Check Supabase:
   - Go to Table Editor
   - Should see data in all tables

2. Check Application:
   - Reload frontend (http://localhost:3000)
   - Dashboard should show metrics
   - Navigate to each section to verify data

---

## Testing

### Backend Tests

```bash
cd backend
source venv/bin/activate

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test
pytest tests/test_competitors.py
```

### Frontend Tests

```bash
cd frontend

# Run tests
npm test

# Run with coverage
npm test -- --coverage

# Run in watch mode
npm test -- --watch
```

### Manual API Testing

Use the interactive API docs at http://localhost:8000/api/v1/docs

Or with curl:

```bash
# Get competitors
curl http://localhost:8000/api/v1/competitors

# Generate report
curl -X POST http://localhost:8000/api/v1/reports/generate?report_type=comprehensive

# Send chat message
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"What are the latest trends?"}'
```

---

## Production Deployment

### Google Cloud Platform

See detailed guide in `deployment/deploy.sh`

**Quick Steps:**

1. **Prerequisites:**
   ```bash
   # Install gcloud CLI
   # https://cloud.google.com/sdk/docs/install

   # Authenticate
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

2. **Set Environment Variables:**
   ```bash
   export ANTHROPIC_API_KEY="your_key"
   export SUPABASE_URL="your_url"
   export SUPABASE_KEY="your_key"
   ```

3. **Deploy:**
   ```bash
   cd deployment
   chmod +x deploy.sh
   ./deploy.sh
   ```

### Other Platforms

**AWS:**
- Use ECS or App Runner
- Deploy Redis using ElastiCache
- Store secrets in AWS Secrets Manager

**Azure:**
- Use Azure Container Apps
- Deploy Redis using Azure Cache for Redis
- Store secrets in Azure Key Vault

**Heroku:**
- Use Heroku Containers
- Add Redis addon
- Set environment variables in dashboard

---

## Troubleshooting

### Common Issues

#### 1. Module Import Errors

**Problem:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
cd backend
source venv/bin/activate  # Make sure venv is activated!
pip install -r requirements.txt
```

#### 2. Database Connection Errors

**Problem:** `Error connecting to Supabase`

**Solution:**
- Verify SUPABASE_URL and SUPABASE_KEY in .env
- Check Supabase project is active
- Verify schema was run successfully
- Test connection:
  ```bash
  python -c "from database.supabase_client import supabase_client; print('OK')"
  ```

#### 3. Claude API Errors

**Problem:** `AuthenticationError: Invalid API key`

**Solution:**
- Verify ANTHROPIC_API_KEY in .env
- Check API key is active in Anthropic console
- Verify sufficient credits/quota

#### 4. Frontend Won't Start

**Problem:** `Error: Cannot find module`

**Solution:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

#### 5. Redis Connection Failed

**Problem:** `Error connecting to Redis`

**Solution:**
```bash
# Check Redis is running
docker ps | grep redis

# Start Redis if not running
docker run -d -p 6379:6379 redis:7-alpine

# Verify connection
redis-cli ping  # Should return PONG
```

#### 6. Port Already in Use

**Problem:** `Address already in use`

**Solution:**
```bash
# Find process using port
lsof -i :8000  # or :3000

# Kill process
kill -9 <PID>

# Or use different port
uvicorn app.main:app --port 8001
```

### Getting Help

1. **Check Logs:**
   ```bash
   # Backend logs
   tail -f backend/logs/*.log

   # Docker logs
   docker-compose logs -f backend
   ```

2. **Enable Debug Mode:**
   ```env
   # In .env
   DEBUG=True
   LOG_LEVEL=DEBUG
   ```

3. **Test Individual Components:**
   ```bash
   # Test database
   python scripts/test_db_connection.py

   # Test Claude API
   python scripts/test_claude_api.py

   # Test frontend API connection
   npm run test:api
   ```

---

## Next Steps

After successful setup:

1. **Explore the Application:**
   - Dashboard overview
   - Chat with research assistant
   - Browse trends
   - Generate reports

2. **Configure Integrations:**
   - Set up Slack notifications
   - Configure email digests
   - Test webhooks

3. **Customize:**
   - Add your own competitors
   - Define custom trends
   - Adjust AI agent parameters

4. **Monitor Usage:**
   - Track Claude API costs
   - Monitor database usage
   - Review application logs

---

## Support

For additional help:

- **Documentation:** Check `/docs` folder
- **API Reference:** http://localhost:8000/api/v1/docs
- **Issues:** Create GitHub issue
- **Community:** Join Discord/Slack channel

---

**Setup complete! 🎉 Start exploring competitive intelligence with BluePeak Compass.**
