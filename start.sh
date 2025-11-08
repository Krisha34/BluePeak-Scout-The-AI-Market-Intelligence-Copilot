#!/bin/bash

# BluePeak Compass - Universal Startup Script
# This script handles all setup and runs both backend and frontend

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BACKEND_PORT=8000
FRONTEND_PORT=3000
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/backend"
FRONTEND_DIR="$SCRIPT_DIR/frontend"

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Banner
echo -e "${BLUE}"
echo "╔════════════════════════════════════════╗"
echo "║    BluePeak Compass Startup Script    ║"
echo "║    Competitive Intelligence Platform   ║"
echo "╚════════════════════════════════════════╝"
echo -e "${NC}"

# Check if running on macOS, Linux, or Windows (Git Bash/WSL)
OS_TYPE="$(uname -s)"
log_info "Detected OS: $OS_TYPE"

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if port is in use
port_in_use() {
    local port=$1
    if [[ "$OS_TYPE" == "Darwin" ]]; then
        lsof -i :$port >/dev/null 2>&1
    else
        netstat -tuln | grep ":$port " >/dev/null 2>&1
    fi
}

# Function to get PID using a port
get_pid_using_port() {
    local port=$1
    if [[ "$OS_TYPE" == "Darwin" ]]; then
        lsof -ti :$port
    else
        lsof -ti :$port 2>/dev/null || netstat -tulpn 2>/dev/null | grep ":$port " | awk '{print $7}' | cut -d'/' -f1
    fi
}

# Function to kill process on port
kill_process_on_port() {
    local port=$1
    local pids=$(get_pid_using_port $port)

    if [ ! -z "$pids" ]; then
        log_warning "Port $port is in use by process(es): $pids"
        read -p "Do you want to kill these processes? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "$pids" | xargs kill -9 2>/dev/null || true
            sleep 2
            log_success "Processes killed on port $port"
            return 0
        else
            return 1
        fi
    fi
    return 0
}

# Step 1: Check Prerequisites
log_info "Step 1: Checking prerequisites..."

# Check Python
if ! command_exists python3; then
    log_error "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
log_success "Python $PYTHON_VERSION found"

# Check Node.js
if ! command_exists node; then
    log_error "Node.js is not installed. Please install Node.js 18 or higher."
    exit 1
fi

NODE_VERSION=$(node --version)
log_success "Node.js $NODE_VERSION found"

# Check npm
if ! command_exists npm; then
    log_error "npm is not installed. Please install npm."
    exit 1
fi

NPM_VERSION=$(npm --version)
log_success "npm $NPM_VERSION found"

# Step 2: Check and Handle Port Usage
log_info "Step 2: Checking port availability..."

# Check backend port
if port_in_use $BACKEND_PORT; then
    if ! kill_process_on_port $BACKEND_PORT; then
        log_error "Cannot start backend on port $BACKEND_PORT. Port is in use."
        read -p "Use alternative port 8001? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            BACKEND_PORT=8001
            log_info "Will use port $BACKEND_PORT for backend"
        else
            exit 1
        fi
    fi
else
    log_success "Port $BACKEND_PORT is available for backend"
fi

# Check frontend port
if port_in_use $FRONTEND_PORT; then
    if ! kill_process_on_port $FRONTEND_PORT; then
        log_error "Cannot start frontend on port $FRONTEND_PORT. Port is in use."
        read -p "Use alternative port 3001? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            FRONTEND_PORT=3001
            log_info "Will use port $FRONTEND_PORT for frontend"
        else
            exit 1
        fi
    fi
else
    log_success "Port $FRONTEND_PORT is available for frontend"
fi

# Step 3: Setup Backend
log_info "Step 3: Setting up backend..."

cd "$BACKEND_DIR"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    log_info "Creating Python virtual environment..."
    python3 -m venv venv
    log_success "Virtual environment created"
else
    log_success "Virtual environment found"
fi

# Activate virtual environment
log_info "Activating virtual environment..."
source venv/bin/activate

# Check if requirements need to be installed
if [ ! -f "venv/.requirements_installed" ] || [ requirements.txt -nt venv/.requirements_installed ]; then
    log_info "Installing/updating Python dependencies..."
    pip install --upgrade pip >/dev/null 2>&1
    pip install -r requirements.txt --upgrade
    touch venv/.requirements_installed
    log_success "Python dependencies installed"
else
    log_success "Python dependencies already installed"
fi

# Check .env file
if [ ! -f ".env" ]; then
    log_error ".env file not found in backend directory"
    log_info "Creating .env file from template..."

    cat > .env << 'EOF'
# Application Settings
APP_NAME="BluePeak Compass"
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=INFO

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_PREFIX=/api/v1

# Claude API - Replace with your actual key from https://console.anthropic.com/
ANTHROPIC_API_KEY=your_anthropic_api_key_here
CLAUDE_MODEL=claude-sonnet-4-20250514
MAX_TOKENS=4096

# Supabase Configuration - Replace with your actual credentials from https://supabase.com
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key_here
SUPABASE_SERVICE_KEY=your_supabase_service_key_here

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=

# Vector Database (Chroma)
CHROMA_HOST=localhost
CHROMA_PORT=8001
CHROMA_PERSIST_DIR=./data/chroma

# Authentication
SECRET_KEY=dev-secret-key-change-in-production-12345678901234567890
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Integrations (Optional)
SLACK_BOT_TOKEN=
SLACK_SIGNING_SECRET=
SENDGRID_API_KEY=
FROM_EMAIL="noreply@bluepeak.ai"

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_PERIOD=60

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# Websocket
WS_HEARTBEAT_INTERVAL=30
EOF

    log_warning "Please edit backend/.env and add your API keys:"
    log_warning "  - ANTHROPIC_API_KEY (required)"
    log_warning "  - SUPABASE_URL (required)"
    log_warning "  - SUPABASE_KEY (required)"
    log_warning "  - SUPABASE_SERVICE_KEY (required)"
    echo ""
    read -p "Press Enter after you've configured the .env file..."
fi

# Validate required environment variables
log_info "Validating environment variables..."

# Safely load environment variables from .env
# This approach handles quoted values, spaces, and special characters correctly
set +e  # Temporarily disable exit on error for pattern matching
while IFS='=' read -r key value; do
    # Skip comments and empty lines
    if [[ $key =~ ^#.* ]] || [[ -z $key ]]; then
        continue
    fi

    # Remove leading/trailing whitespace
    key=$(echo "$key" | xargs)
    value=$(echo "$value" | xargs)

    # Remove quotes if present
    value="${value%\"}"
    value="${value#\"}"
    value="${value%\'}"
    value="${value#\'}"

    # Export the variable
    export "$key=$value"
done < .env
set -e  # Re-enable exit on error

MISSING_VARS=()
if [ -z "$ANTHROPIC_API_KEY" ] || [ "$ANTHROPIC_API_KEY" = "your_anthropic_api_key_here" ]; then
    MISSING_VARS+=("ANTHROPIC_API_KEY")
fi
if [ -z "$SUPABASE_URL" ] || [ "$SUPABASE_URL" = "https://your-project.supabase.co" ]; then
    MISSING_VARS+=("SUPABASE_URL")
fi
if [ -z "$SUPABASE_KEY" ] || [ "$SUPABASE_KEY" = "your_supabase_anon_key_here" ]; then
    MISSING_VARS+=("SUPABASE_KEY")
fi

if [ ${#MISSING_VARS[@]} -gt 0 ]; then
    log_error "Missing or invalid required environment variables: ${MISSING_VARS[*]}"
    log_info "Please configure these in backend/.env file"
    exit 1
fi

log_success "Environment variables validated"

# Update API_PORT if changed
if [ "$BACKEND_PORT" != "8000" ]; then
    log_info "Updating API_PORT in .env to $BACKEND_PORT"
    sed -i.bak "s/API_PORT=8000/API_PORT=$BACKEND_PORT/" .env
fi

# Step 4: Setup Frontend
log_info "Step 4: Setting up frontend..."

cd "$FRONTEND_DIR"

# Check if node_modules exists
if [ ! -d "node_modules" ] || [ package.json -nt node_modules ]; then
    log_info "Installing/updating Node.js dependencies..."
    npm install
    log_success "Node.js dependencies installed"
else
    log_success "Node.js dependencies already installed"
fi

# Update frontend .env if needed
if [ "$BACKEND_PORT" != "8000" ]; then
    log_info "Updating frontend API URL to use port $BACKEND_PORT"
    echo "NEXT_PUBLIC_API_URL=http://localhost:$BACKEND_PORT/api/v1" > .env.local
fi

# Step 5: Start Services
log_info "Step 5: Starting services..."

cd "$SCRIPT_DIR"

# Create logs directory
mkdir -p logs

# Start backend
log_info "Starting backend on port $BACKEND_PORT..."
cd "$BACKEND_DIR"
source venv/bin/activate
nohup uvicorn app.main:app --host 0.0.0.0 --port $BACKEND_PORT --reload > "$SCRIPT_DIR/logs/backend.log" 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > "$SCRIPT_DIR/.backend.pid"
log_success "Backend started (PID: $BACKEND_PID)"

# Wait for backend to be ready
log_info "Waiting for backend to be ready..."
for i in {1..30}; do
    if curl -s "http://localhost:$BACKEND_PORT/api/v1/health" >/dev/null 2>&1; then
        log_success "Backend is ready!"
        break
    fi
    if [ $i -eq 30 ]; then
        log_error "Backend failed to start. Check logs/backend.log for details"
        kill $BACKEND_PID 2>/dev/null || true
        exit 1
    fi
    sleep 1
done

# Start frontend
log_info "Starting frontend on port $FRONTEND_PORT..."
cd "$FRONTEND_DIR"
if [ "$FRONTEND_PORT" != "3000" ]; then
    nohup npm run dev -- -p $FRONTEND_PORT > "$SCRIPT_DIR/logs/frontend.log" 2>&1 &
else
    nohup npm run dev > "$SCRIPT_DIR/logs/frontend.log" 2>&1 &
fi
FRONTEND_PID=$!
echo $FRONTEND_PID > "$SCRIPT_DIR/.frontend.pid"
log_success "Frontend started (PID: $FRONTEND_PID)"

# Wait for frontend to be ready
log_info "Waiting for frontend to be ready..."
sleep 5

# Step 6: Success Message
echo ""
echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║          🚀 SUCCESS! 🚀                ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""
log_success "BluePeak Compass is now running!"
echo ""
echo -e "${BLUE}📊 Frontend:${NC}  http://localhost:$FRONTEND_PORT"
echo -e "${BLUE}🔧 Backend:${NC}   http://localhost:$BACKEND_PORT"
echo -e "${BLUE}📖 API Docs:${NC}  http://localhost:$BACKEND_PORT/docs"
echo ""
echo -e "${YELLOW}Logs:${NC}"
echo -e "  Backend:  tail -f $SCRIPT_DIR/logs/backend.log"
echo -e "  Frontend: tail -f $SCRIPT_DIR/logs/frontend.log"
echo ""
echo -e "${YELLOW}To stop the application:${NC}"
echo -e "  Run: ./stop.sh"
echo -e "  Or:  kill $BACKEND_PID $FRONTEND_PID"
echo ""

# Open browser (optional)
read -p "Open application in browser? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if command_exists open; then
        open "http://localhost:$FRONTEND_PORT"
    elif command_exists xdg-open; then
        xdg-open "http://localhost:$FRONTEND_PORT"
    elif command_exists start; then
        start "http://localhost:$FRONTEND_PORT"
    else
        log_info "Please open http://localhost:$FRONTEND_PORT in your browser"
    fi
fi

# Keep script running to show logs
log_info "Press Ctrl+C to stop watching logs (services will continue running)"
tail -f "$SCRIPT_DIR/logs/backend.log" "$SCRIPT_DIR/logs/frontend.log"
