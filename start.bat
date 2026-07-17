@echo off
REM =============================================================================
REM  start.bat  —  One-command setup & launch  (Windows)
REM
REM  USAGE:
REM      Open Command Prompt (cmd.exe), then run:
REM          cd path\to\box_recommender_project
REM          start.bat
REM
REM  REQUIREMENTS:
REM      Python 3.8 or higher must be installed and on your PATH.
REM      Download from: https://www.python.org/downloads/
REM      During install, tick "Add Python to PATH".
REM      Check with:  python --version
REM
REM  WHAT THIS SCRIPT DOES (automatically, in order):
REM      1. Creates a Python virtual environment  (venv\)
REM      2. Installs django + djangorestframework from requirements.txt
REM      3. Applies database migrations           (creates db.sqlite3)
REM      4. Loads 5 sample boxes + 6 products     (seed_data command)
REM      5. Opens http://127.0.0.1:8000/ in your browser
REM      6. Starts the Django development server
REM
REM  Press Ctrl+C to stop the server.
REM =============================================================================

setlocal

echo.
echo ╔══════════════════════════════════════════════╗
echo ║      Box Recommender — Automated Startup     ║
echo ╚══════════════════════════════════════════════╝

REM ── Guard: must be run from inside box_recommender_project\ ──────────────────
if not exist manage.py (
    echo.
    echo ERROR: manage.py not found.
    echo Please run this script from inside box_recommender_project\
    echo     e.g.  cd box_recommender_project
    echo           start.bat
    pause
    exit /b 1
)

REM ── Guard: python must be available ──────────────────────────────────────────
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Python not found on PATH.
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    echo During installation, make sure to tick "Add Python to PATH".
    pause
    exit /b 1
)

echo.
for /f "tokens=*" %%i in ('python --version 2^>^&1') do echo    %%i detected

REM ── Step 1: Virtual environment ───────────────────────────────────────────────
echo.
echo +-- Step 1: Setting up virtual environment (venv\) --
if exist venv (
    echo    venv\ already exists -- skipping creation
) else (
    python -m venv venv
)
call venv\Scripts\activate.bat
echo    OK  Virtual environment ready

REM ── Step 2: Install dependencies ─────────────────────────────────────────────
echo.
echo +-- Step 2: Installing dependencies --------------------------------
python -m pip install --quiet --upgrade pip
python -m pip install --quiet -r requirements.txt
echo    OK  django and djangorestframework installed

REM ── Step 3: Database migrations ──────────────────────────────────────────────
echo.
echo +-- Step 3: Applying database migrations ---------------------------
python manage.py migrate --run-syncdb
echo    OK  Database ready  (db.sqlite3 created)

REM ── Step 4: Seed sample data ──────────────────────────────────────────────────
echo.
echo +-- Step 4: Loading sample data (5 boxes, 6 products) --------------
python manage.py seed_data
echo    OK  Sample data loaded

REM ── Step 5: Open browser ─────────────────────────────────────────────────────
echo.
echo +-- Step 5: Opening browser ----------------------------------------
start "" http://127.0.0.1:8000/
echo    OK  Browser opening at http://127.0.0.1:8000/

REM ── Step 6: Start server ──────────────────────────────────────────────────────
echo.
echo ╔══════════════════════════════════════════════╗
echo ║  Server starting...                          ║
echo ║                                              ║
echo ║  Home / Demo:  http://127.0.0.1:8000/        ║
echo ║  Admin panel:  http://127.0.0.1:8000/admin/  ║
echo ║  API base:     http://127.0.0.1:8000/api/    ║
echo ║                                              ║
echo ║  Press Ctrl+C to stop.                       ║
echo ╚══════════════════════════════════════════════╝
echo.
python manage.py runserver
