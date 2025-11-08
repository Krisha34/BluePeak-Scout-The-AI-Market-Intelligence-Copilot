#!/bin/bash

# BluePeak Compass - Stop Script
# This script stops both backend and frontend services

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

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

echo -e "${BLUE}"
echo "╔════════════════════════════════════════╗"
echo "║    Stopping BluePeak Compass...       ║"
echo "╚════════════════════════════════════════╝"
echo -e "${NC}"

# Stop backend
if [ -f "$SCRIPT_DIR/.backend.pid" ]; then
    BACKEND_PID=$(cat "$SCRIPT_DIR/.backend.pid")
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        log_info "Stopping backend (PID: $BACKEND_PID)..."
        kill $BACKEND_PID 2>/dev/null || true
        sleep 2
        # Force kill if still running
        if ps -p $BACKEND_PID > /dev/null 2>&1; then
            kill -9 $BACKEND_PID 2>/dev/null || true
        fi
        log_success "Backend stopped"
    else
        log_warning "Backend process not found"
    fi
    rm "$SCRIPT_DIR/.backend.pid"
else
    log_warning "No backend PID file found"
fi

# Stop frontend
if [ -f "$SCRIPT_DIR/.frontend.pid" ]; then
    FRONTEND_PID=$(cat "$SCRIPT_DIR/.frontend.pid")
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        log_info "Stopping frontend (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID 2>/dev/null || true
        sleep 2
        # Force kill if still running
        if ps -p $FRONTEND_PID > /dev/null 2>&1; then
            kill -9 $FRONTEND_PID 2>/dev/null || true
        fi
        log_success "Frontend stopped"
    else
        log_warning "Frontend process not found"
    fi
    rm "$SCRIPT_DIR/.frontend.pid"
else
    log_warning "No frontend PID file found"
fi

# Also kill any processes on ports 8000 and 3000 just to be safe
OS_TYPE="$(uname -s)"
if [[ "$OS_TYPE" == "Darwin" ]]; then
    BACKEND_PIDS=$(lsof -ti :8000 2>/dev/null || true)
    FRONTEND_PIDS=$(lsof -ti :3000 2>/dev/null || true)

    if [ ! -z "$BACKEND_PIDS" ]; then
        log_info "Killing processes on port 8000..."
        echo "$BACKEND_PIDS" | xargs kill -9 2>/dev/null || true
    fi

    if [ ! -z "$FRONTEND_PIDS" ]; then
        log_info "Killing processes on port 3000..."
        echo "$FRONTEND_PIDS" | xargs kill -9 2>/dev/null || true
    fi
fi

echo ""
log_success "BluePeak Compass stopped successfully!"
echo ""
