# 🚀 BluePeak Compass - Quick Start

Get up and running in 10 minutes!

## Prerequisites Checklist

- [ ] Python 3.11+ installed
- [ ] Node.js 18+ installed
- [ ] Docker & Docker Compose installed
- [ ] Anthropic Claude API key
- [ ] Supabase account

## 5-Step Setup

### Step 1: Clone & Configure (2 min)

```bash
# Clone repository
cd bluepeak-compass

# Backend environment
cd backend
cp .env.example .env
# Edit .env: Add ANTHROPIC_API_KEY, SUPABASE_URL, SUPABASE_KEY

# Frontend environment
cd ../frontend
cp .env.local.example .env.local
# Edit .env.local: Add API URLs
```

### Step 2: Database Setup (2 min)

1. Create Supabase project at https://supabase.com
2. Copy URL and keys to `.env`
3. Run `database/schema.sql` in Supabase SQL Editor

### Step 3: Install Dependencies (3 min)

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

### Step 4: Generate Data (1 min)

```bash
cd scripts
python generate_dummy_data.py
```

### Step 5: Launch (2 min)

**Option A - Docker (Easiest):**
```bash
docker-compose up -d
```

**Option B - Manual:**
```bash
# Terminal 1 - Redis
docker run -d -p 6379:6379 redis:7-alpine

# Terminal 2 - Backend
cd backend && source venv/bin/activate
uvicorn app.main:app --reload

# Terminal 3 - Frontend
cd frontend && npm run dev
```

## Access Your App

- 🌐 **Frontend:** http://localhost:3000
- 🔌 **Backend API:** http://localhost:8000
- 📚 **API Docs:** http://localhost:8000/api/v1/docs

## Test Drive

1. **Dashboard** - View metrics and recent activity
2. **Chat** - Ask: "What are the top trends in AI?"
3. **Trends** - Browse emerging market trends
4. **Reports** - Click "Generate New Report"
5. **Competitors** - View competitor intelligence

## Essential Commands

```bash
# Start everything
docker-compose up -d

# View logs
docker-compose logs -f

# Stop everything
docker-compose down

# Restart after changes
docker-compose restart

# Generate more data
python scripts/generate_dummy_data.py
```

## Quick Troubleshooting

**Issue:** Module not found
```bash
cd backend && pip install -r requirements.txt
cd frontend && npm install
```

**Issue:** Database connection failed
- Check Supabase URL and keys in `.env`
- Verify schema was run in Supabase

**Issue:** Port already in use
```bash
# Kill process on port
lsof -i :8000  # or :3000
kill -9 <PID>
```

**Issue:** Redis connection failed
```bash
docker run -d -p 6379:6379 redis:7-alpine
```

## Environment Variables Reference

**Must Have:**
```env
ANTHROPIC_API_KEY=sk-ant-xxxxx
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJxxxxx
```

**Optional:**
```env
SLACK_BOT_TOKEN=xoxb-xxxxx
SENDGRID_API_KEY=SG.xxxxx
```

## Next Steps

1. ✅ Explore all features in the UI
2. ✅ Read `README.md` for detailed info
3. ✅ Check `API_DOCUMENTATION.md` for API reference
4. ✅ Review `SETUP_GUIDE.md` for deployment
5. ✅ Customize with your own data

## Deploy to Production

```bash
cd deployment
chmod +x deploy.sh
export ANTHROPIC_API_KEY="your_key"
export SUPABASE_URL="your_url"
export SUPABASE_KEY="your_key"
./deploy.sh
```

## Need Help?

- 📖 Full docs in `/docs` folder
- 🔧 Troubleshooting in `SETUP_GUIDE.md`
- 💬 API reference at `/api/v1/docs`
- 🐛 Common issues in `README.md`

## Project Structure

```
bluepeak-compass/
├── backend/          # FastAPI + AI Agents
├── frontend/         # Next.js UI
├── database/         # Schema & migrations
├── deployment/       # Docker & GCP configs
├── scripts/          # Utilities
└── docs/            # Documentation
```

## Key Files

- `backend/app/main.py` - API application
- `frontend/src/app/page.tsx` - Dashboard
- `database/schema.sql` - Database schema
- `docker-compose.yml` - Local deployment
- `.env` files - Configuration

## Tips for Success

1. **Start Simple:** Use Docker Compose for first run
2. **Check Logs:** `docker-compose logs -f` is your friend
3. **Test API:** Use interactive docs at `/api/v1/docs`
4. **Generate Data:** Run dummy data script for testing
5. **Monitor Costs:** Track Claude API usage in console

## Hackathon Demo Tips

1. **Show Dashboard:** Metrics and real-time updates
2. **Demo Chat:** Ask intelligent questions
3. **Generate Report:** Live AI report generation
4. **Explain Agents:** Multi-agent architecture
5. **Highlight Scale:** Production-ready deployment

---

**⏱️ Total Setup Time: ~10 minutes**

**🎯 You're Ready to Go!**

Start exploring competitive intelligence with BluePeak Compass! 🚀
