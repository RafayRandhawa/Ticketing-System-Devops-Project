#!/bin/bash
# QR Code Event Ticketing System - Startup Script for Linux/Mac

set -e

echo ""
echo "========================================"
echo "QR Code Event Ticketing System"
echo "========================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker is not installed"
    echo "Please install Docker from https://www.docker.com/"
    exit 1
fi

echo "[1/5] Docker is installed ✓"
echo ""

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "ERROR: Docker Compose is not installed"
    echo "Please install Docker Compose"
    exit 1
fi

echo "[2/5] Docker Compose is installed ✓"
echo ""

# Create .env file if it doesn't exist
if [ ! -f "backend/.env" ]; then
    echo "[3/5] Creating .env file from template..."
    cp backend/.env.example backend/.env
    echo ".env file created."
    echo ""
    echo "⚠️  IMPORTANT: Update the following in backend/.env:"
    echo "   - DATABASE_URL: Supabase connection string from https://supabase.com"
    echo "   - SUPABASE_URL: Your Supabase project URL"
    echo "   - SUPABASE_ANON_KEY: Your Supabase anon key"
    echo "   - SUPABASE_SERVICE_ROLE_KEY: Your Supabase service role key"
    echo ""
else
    echo "[3/5] .env file already exists ✓"
fi
echo ""

# Start Docker Compose
echo "[4/5] Starting Docker containers..."
docker-compose up -d
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to start Docker containers"
    exit 1
fi

echo "[4/5] Docker containers started ✓"
echo ""

# Wait for services to be ready
echo "[5/5] Waiting for services to be ready..."
sleep 10

echo ""
echo "========================================"
echo "✓ Services are now running!"
echo "========================================"
echo ""
echo "Frontend:  http://localhost:3000"
echo "API:       http://localhost:8000"
echo "API Docs:  http://localhost:8000/docs"
echo "Database:  localhost:5432"
echo ""
echo "To view logs:"
echo "  docker-compose logs -f"
echo ""
echo "To stop services:"
echo "  docker-compose down"
echo ""
