#!/bin/bash
# ==============================================================================
# RAVEN SHOP AUTOMATION - DEVELOPMENT MODE STARTUP SCRIPT
# ==============================================================================
# Usage: ./start_dev.sh
# Starts both backend and frontend in development mode with hot reload
# ==============================================================================

set -e  # Exit on error

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     RAVEN SHOP AUTOMATION - DEVELOPMENT MODE                   ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .env file not found${NC}"
    echo "   Creating .env from .env.example..."
    cp .env.example .env
    echo -e "${BLUE}✓ .env created${NC}"
    echo -e "${RED}   ⚠️  IMPORTANT: Edit .env with your configuration before proceeding${NC}"
fi

# Set development environment
export APP_ENV=development
export NODE_ENV=development

echo -e "${BLUE}Environment: ${GREEN}DEVELOPMENT${NC}"
echo ""

# Check for required tools
echo -e "${BLUE}Checking prerequisites...${NC}"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python3 not found${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python3${NC}"

if ! command -v npm &> /dev/null; then
    echo -e "${RED}✗ npm not found${NC}"
    exit 1
fi
echo -e "${GREEN}✓ npm${NC}"

echo ""
echo -e "${BLUE}Starting services...${NC}"
echo ""

# Start backend in background
echo -e "${YELLOW}Starting Backend Server (port 8000)...${NC}"
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Start backend with environment variables
python -m uvicorn main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --reload \
    --log-level debug &

BACKEND_PID=$!
echo -e "${GREEN}✓ Backend started (PID: $BACKEND_PID)${NC}"

cd ..
sleep 2

# Start frontend
echo -e "${YELLOW}Starting Frontend Server (port 3000)...${NC}"
cd frontend

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "Installing npm packages..."
    npm install
fi

npm run dev &

FRONTEND_PID=$!
echo -e "${GREEN}✓ Frontend started (PID: $FRONTEND_PID)${NC}"

cd ..
echo ""
echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ Development environment ready!${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
echo ""
echo "📋 Services Running:"
echo "   Frontend:  http://localhost:3000"
echo "   Backend:   http://localhost:8000"
echo "   API Docs:  http://localhost:8000/docs"
echo ""
echo "📝 Process IDs:"
echo "   Frontend: $FRONTEND_PID"
echo "   Backend:  $BACKEND_PID"
echo ""
echo "🛑 To stop: Press Ctrl+C or run: kill $FRONTEND_PID $BACKEND_PID"
echo ""

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; echo 'Services stopped.'" SIGINT SIGTERM
wait
