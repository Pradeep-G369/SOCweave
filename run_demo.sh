#!/bin/bash
# SOCweave Demo Runner
# Usage: bash run_demo.sh --scenario=a   OR   bash run_demo.sh --scenario=b

SCENARIO="a"
for arg in "$@"; do
  case $arg in
    --scenario=*) SCENARIO="${arg#*=}" ;;
  esac
done

echo "============================================"
echo "  SOCweave Demo Runner"
echo "  Scenario: $SCENARIO"
echo "============================================"

# Start backend
cd backend
if [ ! -d "../.venv" ]; then
  echo "[1/3] Creating virtual environment..."
  python -m venv ../.venv
fi

echo "[1/3] Activating virtual environment..."
source ../.venv/Scripts/activate 2>/dev/null || source ../.venv/bin/activate

echo "[2/3] Installing dependencies (if needed)..."
pip install -q -r requirements.txt

echo "[3/3] Starting backend server..."
uvicorn main:app --port 8000 &
BACKEND_PID=$!

sleep 4

echo ""
echo "Backend running at http://127.0.0.1:8000"
echo "Fetching verdict for scenario $SCENARIO ..."
echo ""

curl -s "http://127.0.0.1:8000/scenario/$SCENARIO" | python -m json.tool

echo ""
echo "To view the full UI, run in a separate terminal:"
echo "  cd frontend && npm install && npm run dev"
echo ""
echo "Press Ctrl+C to stop the backend server."
wait $BACKEND_PID