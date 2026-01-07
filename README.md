# 🎲 Rubik Speedcube Timer

Rubik-kocka időmérő alkalmazás - Multi-paradigma programozás beadandó

## 📋 Projekt Bemutató

**Funkciók**: Scramble generálás, időmérés mentése, statisztikák, vizualizáció (Plotly), automatizált napi scramble

**Technológiák**: FastAPI, Streamlit, SQLAlchemy, Pydantic, SQLite, Schedule, Pytest

## 🏗️ Architektúra

**Moduláris rétegzett szerkezet:**
- `models.py` - SQLAlchemy ORM + Pydantic sémák (adatbázis réteg)
- `services.py` - Üzleti logika, 3 paradigma demonstrációja
- `main.py` - FastAPI backend, 5 REST végpont
- `app.py` - Streamlit frontend
- `automation.py` - Schedule automatizáció
- `test_app.py` - Pytest unit tesztek

**3 Programozási Paradigma:**
- **Procedurális**: `generate_scramble()` - for ciklus, szekvenciális
- **Funkcionális**: `calculate_average()` - reduce(), lambda, immutable
- **OOP**: `TimerService` osztály - encapsulation, methods, dependency injection

## 🚀 Indítás

### Telepítés
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Backend indítás
```bash
uvicorn main:app --reload --port 8000
```

### Frontend indítás
```bash
streamlit run app.py
```

### Automatikus indítás (mindkettő)
```bash
./start.sh
```

**URL-ek:**
- Frontend: http://localhost:8501
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 📡 API Végpontok

| Method | Endpoint | Leírás |
|--------|----------|--------|
| GET | `/scramble` | Új scramble generálás (procedurális) |
| GET | `/scramble/daily` | Napi scramble (OOP) |
| POST | `/times` | Idő mentése (OOP + Pydantic) |
| GET | `/times` | Összes idő listázása |
| GET | `/stats` | Statisztikák (OOP + funkcionális) |

## 🧪 Tesztelés

```bash
pytest test_app.py -v
```

3 teszt: procedurális, funkcionális (parametrize), OOP

## ☁️ Deployment

### Backend (Render.com)
1. Push kód GitHub-ra
2. https://render.com → New Web Service
3. Connect repository
4. Build: `pip install -r requirements.txt`
5. Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Másold ki a deployed URL-t (pl. `https://rubik-api.onrender.com`)

### Frontend (Streamlit Cloud)
1. https://streamlit.io/cloud → New app
2. Repository, branch, `app.py` kiválasztása
3. **Secrets** (Settings → Secrets):
   ```toml
   API_URL = "https://rubik-api.onrender.com"
   ```
4. Deploy
