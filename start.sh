#!/bin/bash

# Rubik Speedcube App - Egyszerű indító script

echo "🎲 Rubik Speedcube App - Indítás..."
echo ""

# Projekt könyvtár
cd "$(dirname "$0")"

# Virtual environment aktiválás
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "❌ Virtual environment nem található!"
    echo "Futtasd: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Backend indítása háttérben
echo "🚀 Backend indítása (port 8000)..."
uvicorn main:app --reload --host 0.0.0.0 --port 8000 > /dev/null 2>&1 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

sleep 2

# Frontend indítása háttérben
echo "🎨 Frontend indítása (port 8501)..."
streamlit run app.py --server.port 8501 > /dev/null 2>&1 &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"

sleep 2

echo ""
echo "✅ Alkalmazás elindult!"
echo ""
echo "📡 URL-ek:"
echo "   Frontend: http://localhost:8501"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "🛑 Leállítás: kill $BACKEND_PID $FRONTEND_PID"
echo ""

# PIDs mentése
echo $BACKEND_PID > .backend.pid
echo $FRONTEND_PID > .frontend.pid

# macOS böngésző megnyitás
if [[ "$OSTYPE" == "darwin"* ]]; then
    sleep 1
    open http://localhost:8501
fi

echo "Nyomd meg Enter-t a leállításhoz..."
read

# Cleanup
kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
rm -f .backend.pid .frontend.pid speedcube.db
echo "Leállítva."
