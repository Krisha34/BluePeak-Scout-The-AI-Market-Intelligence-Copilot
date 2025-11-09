# BluePeak Scout – The AI Market Intelligence Copilot

**Multi-Agent AI Platform for Competitive Intelligence and Market Research**

BluePeak Scout is an AI-powered market intelligence platform built on Claude, LangChain, and Retrieval-Augmented Generation (RAG) that helps BluePeak Marketing reclaim its competitive edge through real-time, data-driven insights.

Traditional manual research limits agencies like BluePeak from staying ahead of fast-moving competitors. BluePeak Scout automates this process — continuously collecting signals from news, competitor websites, job postings, ad libraries, and social media — then uses Claude’s advanced reasoning to generate concise, actionable strategy briefs.

With LangGraph-powered workflows for prompt orchestration, vector-based retrieval for factual grounding, and Claude’s generative reasoning for human-quality recommendations, BluePeak Scout transforms raw web data into clear insights and strategic next steps.

The platform delivers:

📊 Automated competitor & trend tracking with RAG-based insights

🧭 AI-generated weekly briefs summarizing top market movements

💬 Campaign & creative idea generator inspired by real competitor moves

🔔 Smart alerts when competitors launch new products or change pricing

Result: BluePeak’s strategists and account managers save hours of manual research weekly, act faster on market changes, and craft winning campaigns backed by live, explainable intelligence — all powered by Claude’s generative understanding and reasoning capabilities.

![BluePeak Compass](https://img.shields.io/badge/version-0.1.0-blue)
![Python](https://img.shields.io/badge/python-3.11-green)
![Next.js](https://img.shields.io/badge/next.js-14.0-black)
![FastAPI](https://img.shields.io/badge/fastapi-0.104-teal)

## 🚀 Quick Start (One-Command Setup)

The easiest way to run BluePeak Compass is using our automated startup script:

```bash
# Clone the repository
git clone <repository-url>
cd hackethon

# Make scripts executable
chmod +x start.sh stop.sh

# Run the application
./start.sh
```

**To stop the application:**
```bash
./stop.sh
```

### Prerequisites for Quick Start
- Python 3.8+ ([Download](https://www.python.org/downloads/))
- Node.js 18+ ([Download](https://nodejs.org/))
- Anthropic API Key ([Get Key](https://console.anthropic.com/))
- Supabase Account ([Sign Up](https://supabase.com/))

## 🚀 Features

### Core Capabilities
- **Multi-Agent AI System**: 7 specialized AI agents powered by Claude API
  - Supervisor Agent (orchestration)
  - Competitive Intelligence Agent
  - Market Trend Analyst Agent
  - Social Listening Agent
  - Content Analyzer Agent
  - Synthesis & Reporting Agent
  - RAG Query Assistant Agent

- **Competitive Intelligence**: Real-time competitor monitoring and analysis
- **Market Trends**: AI-powered trend discovery and tracking
- **Research Chat**: RAG-powered conversational interface for queries
- **Automated Reports**: AI-generated intelligence reports
- **Real-time Updates**: WebSocket support for live notifications
- **Integrations**: Slack and email notification support

### Technical Stack
- **Backend**: FastAPI (Python 3.11) + LangGraph
- **Frontend**: Next.js 14 + React + TypeScript + Tailwind CSS
- **Database**: Supabase (PostgreSQL)
- **Vector Store**: ChromaDB for RAG
- **Cache**: Redis
- **AI**: Claude API (Anthropic)
- **Deployment**: Docker + Google Cloud Platform

### See BluePeak Compass In Action


## 📋 Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Supabase account
- Claude API key (Anthropic)
- (Optional) Slack Bot Token
- (Optional) SendGrid API Key

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd bluepeak-compass
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your API keys and configuration
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment variables
cp .env.local.example .env.local
# Edit .env.local with your configuration
```

### 4. Database Setup

1. Create a Supabase project at https://supabase.com
2. Copy your Supabase URL and keys to `.env`
3. Run the database schema:
   - Go to Supabase SQL Editor
   - Run the contents of `database/schema.sql`

### 5. Generate Dummy Data

```bash
cd scripts
python generate_dummy_data.py
```

This will populate your database with:
- 10 competitor companies
- 8 market trends
- ~40 research findings
- 4 sample reports
- 2 sample conversations

## 🚢 Running the Application

### Option 1: Automated Scripts (Easiest) ⭐

Use the provided startup scripts for a hassle-free experience:

```bash
# Start everything
./start.sh

# Stop everything
./stop.sh
```

The startup script automatically:
- Checks system requirements
- Installs dependencies if needed
- Handles port conflicts (offers to kill processes or use alternative ports)
- Validates environment variables
- Creates missing .env files
- Starts both backend and frontend
- Monitors services and shows logs

**Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/api/v1/docs

**View logs:**
```bash
# Follow all logs
tail -f logs/backend.log logs/frontend.log

# Backend only
tail -f logs/backend.log

# Frontend only
tail -f logs/frontend.log
```

### Option 2: Docker Compose

```bash
# From project root
docker-compose up -d
```

### Option 3: Manual Setup

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Terminal 3 - Redis (if not using Docker):**
```bash
redis-server
```

## 🛠️ Script Features & Edge Cases

The `start.sh` script handles various edge cases:

## 📁 Project Structure

```
bluepeak-compass/
├── backend/
│   ├── agents/                 # LangGraph AI agents
│   │   ├── base_agent.py
│   │   ├── supervisor.py
│   │   ├── competitive_intelligence.py
│   │   ├── market_trend_analyst.py
│   │   ├── social_listening.py
│   │   ├── content_analyzer.py
│   │   ├── synthesis_reporting.py
│   │   └── rag_assistant.py
│   ├── app/
│   │   ├── api/
│   │   │   ├── endpoints/      # API route handlers
│   │   │   └── websocket/      # WebSocket handlers
│   │   ├── core/               # Configuration & logging
│   │   ├── models/             # Pydantic schemas
│   │   └── services/           # Business logic
│   ├── database/               # Database client
│   ├── integrations/           # Slack & Email
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/                # Next.js pages
│   │   │   ├── page.tsx        # Dashboard
│   │   │   ├── chat/           # Chat interface
│   │   │   ├── trends/         # Trends explorer
│   │   │   ├── reports/        # Reports section
│   │   │   └── competitors/    # Competitors view
│   │   ├── components/         # React components
│   │   ├── lib/                # API client & utilities
│   │   └── types/              # TypeScript types
│   └── package.json
├── database/
│   └── schema.sql              # Supabase schema
├── deployment/
│   ├── gcp-deploy.yaml         # GCP Cloud Run config
│   └── deploy.sh               # Deployment script
├── scripts/
│   └── generate_dummy_data.py  # Data generator
├── docker-compose.yml
└── README.md
```

## 🔌 API Endpoints

### Competitors
- `GET /api/v1/competitors` - List all competitors
- `GET /api/v1/competitors/{id}` - Get competitor details
- `POST /api/v1/competitors` - Create new competitor
- `PUT /api/v1/competitors/{id}` - Update competitor
- `POST /api/v1/competitors/{id}/analyze` - Trigger AI analysis

### Trends
- `GET /api/v1/trends` - List all trends
- `POST /api/v1/trends` - Create new trend
- `POST /api/v1/trends/discover` - Discover trends with AI
- `GET /api/v1/trends/{id}/trajectory` - Predict trend trajectory

### Chat
- `POST /api/v1/chat` - Send message and get AI response
- `GET /api/v1/chat/conversations` - List conversations
- `GET /api/v1/chat/conversations/{id}` - Get conversation details

### Reports
- `GET /api/v1/reports` - List all reports
- `GET /api/v1/reports/{id}` - Get report details
- `POST /api/v1/reports/generate` - Generate new report
- `POST /api/v1/reports/{id}/export` - Export report

### Analytics
- `GET /api/v1/analytics/metrics` - Get analytics metrics
- `GET /api/v1/analytics/dashboard` - Get dashboard data

Full API documentation available at: http://localhost:8000/api/v1/docs

## 🤖 Multi-Agent System

The platform uses a sophisticated multi-agent architecture:

1. **Supervisor Agent**: Coordinates operations and delegates tasks
2. **Competitive Intelligence Agent**: Analyzes competitors and strategies
3. **Market Trend Analyst Agent**: Identifies and predicts market trends
4. **Social Listening Agent**: Monitors social media and sentiment
5. **Content Analyzer Agent**: Processes and extracts insights from content
6. **Synthesis & Reporting Agent**: Generates comprehensive reports
7. **RAG Query Assistant Agent**: Handles conversational research queries

Each agent is specialized and works autonomously while the Supervisor coordinates their activities.

## 🔐 Environment Variables

### Backend (.env)
```env
# Claude API
ANTHROPIC_API_KEY=your_api_key

# Supabase
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
SUPABASE_SERVICE_KEY=your_service_key

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# Security
SECRET_KEY=your_secret_key

# Optional: Integrations
SLACK_BOT_TOKEN=xoxb-your-token
SENDGRID_API_KEY=your_sendgrid_key
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws
```
Executive Summary

The AI competitive landscape has experienced significant shifts over the past 30 days, characterized by aggressive feature rollouts and strategic pricing adjustments across major players.
AI Features: OpenAI launched GPT-4 Turbo with enhanced multimodal capabilities and reduced latency, while Google responded with Gemini Pro’s expanded context window (2M tokens) and improved code generation. Microsoft integrated advanced AI copilots across Office 365 suite, and Anthropic released Claude 3 with superior reasoning capabilities. Notable trend: 73% of major AI providers now offer real-time API streaming and voice synthesis integration.

Pricing Strategies: A clear race-to-the-bottom emerged with OpenAI reducing GPT-4 API costs by 50%, forcing competitors to follow suit. Google introduced usage-based tiering starting at $0.0005/1K tokens, while Microsoft launched competitive enterprise bundles at $30/user/month. Anthropic maintained premium positioning but added a freemium tier.
Key insight: Enterprise customers are driving demand for transparent, predictable pricing models over pay-per-use structures. The market is consolidating around three pricing archetypes: freemium consumer models, usage-based developer tiers, and flat-rate enterprise packages.

## 📊 Monitoring

- Backend logs: `backend/logs/`
- Application metrics: Available in GCP Console
- Real-time monitoring: WebSocket connection status

## 🤝 Contributing

This is a hackathon project. Contributions welcome!

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

MIT License - see LICENSE file for details

## 🆘 Support

For issues and questions:
- Check API documentation at `/api/v1/docs`
- Review logs in `backend/logs/`
- Verify environment variables are set correctly

## 🎯 Roadmap

- [ ] Advanced filtering and search
- [ ] Custom agent workflows
- [ ] Multi-language support
- [ ] Mobile app
- [ ] Advanced visualization dashboards
- [ ] Export to multiple formats (PDF, Excel, etc.)
- [ ] Team collaboration features
- [ ] API webhooks

## 👏 Acknowledgments

- Built with Claude API (Anthropic)
- Powered by LangGraph and LangChain
- UI components from Tailwind CSS
- Database by Supabase

---

**Built for hackathon - production-ready with room for enhancements**

For questions or support, please open an issue on GitHub.

<img width="1470" height="794" alt="image (7)" src="https://github.com/user-attachments/assets/abd02774-de22-46e4-8c2a-e829808f5ff7" />


