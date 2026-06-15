@echo off
REM QR Code Event Ticketing System - Startup Script for Windows

echo.
echo ========================================
echo QR Code Event Ticketing System
echo ========================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not installed or not in PATH
    echo Please install Docker from https://www.docker.com/
    pause
    exit /b 1
)

echo [1/5] Docker is installed ✓
echo.

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker Compose is not installed
    echo Please install Docker Desktop which includes Docker Compose
    pause
    exit /b 1
)

echo [2/5] Docker Compose is installed ✓
echo.

REM Create .env file if it doesn't exist
if not exist "backend\.env" (
    echo [3/5] Creating .env file from template...
    copy "backend\.env.example" "backend\.env" >nul
    echo .env file created.
    echo.
    echo ⚠️  IMPORTANT: Update the following in backend\.env:
    echo    - DATABASE_URL: Supabase connection string from https://supabase.com
    echo    - SUPABASE_URL: Your Supabase project URL
    echo    - SUPABASE_ANON_KEY: Your Supabase anon key
    echo    - SUPABASE_SERVICE_ROLE_KEY: Your Supabase service role key
    echo.
) else (
    echo [3/5] .env file already exists ✓
)
echo.

REM Start Docker Compose
echo [4/5] Starting Docker containers...
docker-compose up -d
if errorlevel 1 (
    echo ERROR: Failed to start Docker containers
    pause
    exit /b 1
)

echo [4/5] Docker containers started ✓
echo.

REM Wait for services to be ready
echo [5/5] Waiting for services to be ready...
timeout /t 10 /nobreak

echo.
echo ========================================
echo ✓ Services are now running!
echo ========================================
echo.
echo Frontend:  http://localhost:3000
echo API:       http://localhost:8000
echo API Docs:  http://localhost:8000/docs
echo Database:  localhost:5432
echo.
echo To view logs:
echo   docker-compose logs -f
echo.
echo To stop services:
echo   docker-compose down
echo.
pause