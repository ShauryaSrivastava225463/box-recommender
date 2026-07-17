

GREEN='\033[0;32m'; BLUE='\033[0;34m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
step() { echo -e "\n${BLUE}┌─ Step $1 ──────────────────────────────────────────${NC}\n${BLUE}│${NC}  $2"; }
ok()   { echo -e "${GREEN}└─ ✓  $1${NC}"; }
warn() { echo -e "${YELLOW}   ⚠  $1${NC}"; }
fail() { echo -e "${RED}✗  ERROR: $1${NC}"; exit 1; }

echo ""
echo -e "${BLUE}╔══════════════════════════════════════════════╗"
echo -e "║      Box Recommender — Automated Startup     ║"
echo -e "╚══════════════════════════════════════════════╝${NC}"

if [ ! -f "manage.py" ]; then
    fail "manage.py not found. Please run this script from inside box_recommender_project/\n       e.g.  cd box_recommender_project && bash start.sh"
fi

if ! command -v python3 &>/dev/null; then
    fail "python3 not found. Please install Python 3.8+ from https://www.python.org/downloads/"
fi

PYTHON_VER=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo -e "\n   Python $PYTHON_VER detected"

step 1 "Setting up virtual environment (venv/)"
if [ -d "venv" ]; then
    warn "venv/ already exists — skipping creation"
else
    python3 -m venv venv
fi
source venv/bin/activate
ok "Virtual environment ready"


step 2 "Installing dependencies (django + djangorestframework)"
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
ok "Dependencies installed"

# ── Step 3: migrations ────────────────────────────────────────────────────────
step 3 "Applying database migrations"
python manage.py migrate --run-syncdb
ok "Database ready  (db.sqlite3 created)"

step 4 "Loading sample data (5 boxes, 6 products)"
python manage.py seed_data
ok "Sample data loaded"

step 5 "Opening browser"
URL="http://127.0.0.1:8000/"
if command -v open &>/dev/null; then          # macOS
    (sleep 2 && open "$URL") &
elif command -v xdg-open &>/dev/null; then    # Linux
    (sleep 2 && xdg-open "$URL") &
else
    warn "Could not detect a browser opener — please open $URL manually"
fi
ok "Browser will open at $URL in 2 seconds"

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════╗"
echo -e "║  Server starting…                            ║"
echo -e "║                                              ║"
echo -e "║  Home / Demo:  http://127.0.0.1:8000/        ║"
echo -e "║  Admin panel:  http://127.0.0.1:8000/admin/  ║"
echo -e "║  API base:     http://127.0.0.1:8000/api/    ║"
echo -e "║                                              ║"
echo -e "║  Press Ctrl+C to stop.                       ║"
echo -e "╚══════════════════════════════════════════════╝${NC}"
echo ""

python manage.py runserver
