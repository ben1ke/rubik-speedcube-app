# 🎲 Rubik Speedcube Timer

**Egyszerű Rubik-kocka időmérő alkalmazás** - Multi-paradigma programozási beadandó

FastAPI backend + Streamlit frontend + SQLite adatbázis

---

## 📋 Funkciók

- ⏱️ **Timer**: Scramble generálás és idők mentése
- 📊 **Statisztikák**: Best time, átlag, AO5
- 📈 **Vizualizáció**: Időfejlődés grafikon Plotly-val
- 🤖 **Automatizáció**: Napi scramble generálás (schedule)

## 🎭 Multi-paradigma Programozás

### 1. Procedurális
```python
def generate_scramble(length: int = 20) -> str:
    """Lépésről lépésre scramble generálás."""
    moves = ["R", "L", "U", "D", "F", "B"]
    # ... for ciklus
```

### 2. Funkcionális
```python
def calculate_average(times: List[float]) -> float:
    """Reduce használata átlagszámításhoz."""
    return reduce(lambda acc, x: acc + x, times, 0.0) / len(times)
```

### 3. Objektum-orientált
```python
class TimerService:
    """Service osztály - encapsulation, methods."""
    def __init__(self, db: Session):
        self.db = db
```

## 🛠 Technológiák

- **Backend**: FastAPI, SQLAlchemy, Pydantic
- **Frontend**: Streamlit, Plotly
- **Adatbázis**: SQLite
- **Automatizáció**: Schedule
- **Tesztelés**: Pytest

## 📦 Telepítés

```bash
# 1. Virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux

# 2. Függőségek
pip install -r requirements.txt

# 3. Indítás
./start.sh
```

## 🚀 Használat

### Automatikus indítás
```bash
./start.sh
```

### Manuális indítás

**Backend:**
```bash
uvicorn main:app --reload --port 8000
```

**Frontend:**
```bash
streamlit run app.py
```

**Automatizáció:**
```bash
python automation.py
```

### URL-ek
- Frontend: http://localhost:8501
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 🧪 Tesztelés

```bash
pytest test_app.py -v
```

**3 teszt:**
1. Procedurális scramble generálás
2. Funkcionális átlagszámítás (parametrize)
3. OOP TimerService mentés

## 📁 Projekt Struktúra

```
rubik-speedcube-app/
├── main.py           # FastAPI backend (5 endpoint)
├── models.py         # SQLAlchemy ORM + Pydantic
├── services.py       # Service logika (3 paradigma)
├── app.py            # Streamlit frontend
├── automation.py     # Napi scramble generálás
├── test_app.py       # 3 pytest teszt
├── requirements.txt
├── .env
├── start.sh
└── README.md
```

## 📡 API Végpontok

| Method | Endpoint | Leírás |
|--------|----------|--------|
| GET | `/scramble` | Új scramble generálás |
| GET | `/scramble/daily` | Napi scramble |
| POST | `/times` | Idő mentése |
| GET | `/times` | Összes idő |
| GET | `/stats` | Statisztikák |

## 🔧 Környezeti Változók (.env)

```env
DATABASE_URL=sqlite:///./speedcube.db
API_URL=http://localhost:8000
PORT=8000
```

## 📝 Fejlesztői Jegyzetek

### Paradigmák használata
- **Procedurális**: `generate_scramble()`, `format_time()` - szekvenciális lépések
- **Funkcionális**: `calculate_average()`, `filter_recent_times()` - map/filter/reduce
- **OOP**: `TimerService`, `ScrambleService` - osztályok, encapsulation

### Automatizáció
- `automation.py` minden nap 06:00-kor új scramble-t generál
- Schedule library használata
- Háttérfolyamat logging-gal

### Tesztelés
- 3 teszt: procedurális, funkcionális (parametrize), OOP
- In-memory SQLite test database
- StaticPool threading support

## 👨‍💻 Szerző

Bence Kovács - BSC 3. félév, Multi-paradigma programozás

---

**Verzió**: 1.0.0 (Minimal)  
**Készült**: 2026.01.07

- [Funkciók](#-funkciók)
- [Technológiai Stack](#-technológiai-stack)
- [Multi-Paradigma Programozás](#-multi-paradigma-programozás)
- [Telepítés](#-telepítés)
- [Használat](#-használat)
- [Projektstruktúra](#-projektstruktúra)
- [API Dokumentáció](#-api-dokumentáció)
- [Tesztelés](#-tesztelés)
- [Automatizáció](#-automatizáció)

## ✨ Funkciók

### 🎯 Főbb Funkciók
- **Timer/Stopwatch**: Kirakási idők mérése és mentése
- **Scramble Generátor**: Véletlenszerű keverések generálása
- **Algoritmus Könyvtár**: OLL/PLL/F2L algoritmusok tárolása
- **Statisztikák**: Average of 5/12/100, best time, időeloszlás
- **Automatizált Feladatok**: Napi scramble, heti összesítő, cleanup
- **Vizualizációk**: Interaktív grafikonok plotly-val

### 🎨 Felhasználói Felület
- **Home**: Dashboard daily scramble-lel és stat összesítővel
- **Timer**: Időmérő scramble-lel és recent times listával
- **Algorithms**: Algoritmus böngészés, keresés, CRUD műveletek
- **Statistics**: Részletes statisztikák grafikonokkal

## 🛠 Technológiai Stack

### Backend
- **FastAPI**: Modern, gyors REST API framework
- **SQLAlchemy**: ORM adatbázis kezeléshez
- **Pydantic**: Adat validáció és sémák
- **SQLite**: Adatbázis

### Frontend
- **Streamlit**: Interaktív web alkalmazás
- **Plotly**: Interaktív grafikonok
- **Requests**: API kommunikáció

### Automatizáció & Tesztelés
- **Schedule**: Cron-szerű feladat ütemezés
- **Pytest**: Unit és integration tesztek
- **TestClient**: FastAPI endpoint tesztelés

## 🎭 Multi-Paradigma Programozás

Ez a projekt demonstrálja három programozási paradigma használatát:

### 1️⃣ Objektum-Orientált Programozás (OOP)

**Service osztályok** a backend/services/ mappában:

```python
# backend/services/algorithm_service.py
class AlgorithmService:
    """OOP paradigma - szolgáltatás osztály"""
    
    def __init__(self, db: Session):
        self.db = db  # Encapsulation
    
    def create(self, algorithm: AlgorithmCreate) -> Algorithm:
        """Algorithm létrehozása"""
        # ...
```

**Jellemzők**:
- Encapsulation (db session private member)
- Methods (create, get, delete, search)
- Dependency Injection (Session átadása)
- Single Responsibility (csak algorithm műveletek)

### 2️⃣ Procedurális Programozás

**Utility függvények** a backend/services/timer_service.py-ban:

```python
# backend/services/timer_service.py
def generate_scramble(length: int = 20) -> str:
    """Procedurális scramble generálás"""
    moves = ["R", "L", "U", "D", "F", "B"]
    modifiers = ["", "'", "2"]
    scramble = []
    
    for _ in range(length):
        move = random.choice(moves)
        modifier = random.choice(modifiers)
        scramble.append(f"{move}{modifier}")
    
    return " ".join(scramble)

def validate_time(time: float) -> bool:
    """Procedurális idő validáció"""
    return 0 < time < 3600

def format_time(seconds: float) -> str:
    """Procedurális idő formázás"""
    if seconds < 60:
        return f"{seconds:.2f}"
    minutes = int(seconds // 60)
    secs = seconds % 60
    return f"{minutes}:{secs:05.2f}"
```

**Jellemzők**:
- Top-level függvények
- Lépésről lépésre haladó logika
- Egyszerű input-output
- Nincs állapot (stateless)

### 3️⃣ Funkcionális Programozás

**Funkcionális műveletek** a backend/services/stats_service.py-ban:

```python
# backend/services/stats_service.py
class StatsService:
    """Funkcionális paradigma használata statisztikákhoz"""
    
    def _get_valid_times(self, times: List[SolveTime]) -> List[SolveTime]:
        """Filter - csak valid (nem DNF) idők"""
        return list(filter(lambda t: t.dnf == 0, times))
    
    def _extract_time_values(self, times: List[SolveTime]) -> List[float]:
        """Map - idő értékek kinyerése"""
        return list(map(lambda t: t.time, times))
    
    def calculate_average(self, times: List[SolveTime]) -> Optional[float]:
        """Reduce - átlag számítás"""
        valid = self._get_valid_times(times)
        if not valid:
            return None
        
        values = self._extract_time_values(valid)
        total = reduce(lambda acc, x: acc + x, values, 0.0)
        return total / len(values)
```

**Jellemzők**:
- Higher-order functions (map, filter, reduce)
- Lambda expressions
- Immutability (új listák létrehozása)
- Pure functions (nincs side effect)
- Composition (függvények egymásra építése)

## 📦 Telepítés

### Előfeltételek
- Python 3.13+
- pip
- virtualenv (opcionális)

### Lépések

1. **Repository klónozása**
```bash
git clone <repository-url>
cd rubik-speedcube-app
```

2. **Virtual environment létrehozása**
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# vagy
venv\Scripts\activate  # Windows
```

3. **Függőségek telepítése**
```bash
pip install -r requirements.txt
```

4. **Adatbázis inicializálása és seed adatok betöltése**
```bash
python seed_data.py
```

5. **Környezeti változók beállítása** (opcionális)
```bash
cp .env.example .env
# Szerkeszd a .env fájlt szükség szerint
```

## 🚀 Használat

### Automatikus Indítás (Ajánlott)

```bash
chmod +x start.sh
./start.sh
```

Ez a script:
1. Aktiválja a virtual environmentet
2. Elindítja a backend API-t (port 8000)
3. Elindítja a frontend Streamlit appot (port 8501)

### Manuális Indítás

**Backend (Terminal 1):**
```bash
source venv/bin/activate
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend (Terminal 2):**
```bash
source venv/bin/activate
streamlit run frontend/app.py
```

**Automation Scheduler (Terminal 3 - opcionális):**
```bash
source venv/bin/activate
python automation/scheduler.py
```

### URL-ek

- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc

## 📁 Projektstruktúra

```
rubik-speedcube-app/
├── backend/                    # FastAPI backend
│   ├── __init__.py
│   ├── main.py                # FastAPI app és startup/shutdown
│   ├── config.py              # Környezeti konfiguráció
│   ├── database.py            # SQLAlchemy setup
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py          # REST API endpoints (14 végpont)
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py          # ORM modellek (Algorithm, SolveTime, Scramble)
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── schemas.py         # Pydantic sémák és validátorok
│   └── services/
│       ├── __init__.py
│       ├── algorithm_service.py   # OOP + Functional
│       ├── timer_service.py       # Procedural + OOP
│       └── stats_service.py       # Functional + OOP
│
├── frontend/                   # Streamlit frontend
│   ├── __init__.py
│   ├── app.py                 # Home page
│   ├── pages/
│   │   ├── 1_timer.py         # Timer page
│   │   ├── 2_algorithms.py    # Algorithms page
│   │   └── 3_statistics.py    # Statistics page
│   └── utils/
│       ├── __init__.py
│       └── api_client.py      # Backend API wrapper
│
├── automation/                 # Scheduled tasks
│   ├── __init__.py
│   └── scheduler.py           # 4 automatizált feladat
│
├── tests/                      # Pytest tesztek
│   ├── __init__.py
│   ├── test_algorithms.py     # Algorithm tesztek (19 teszt)
│   ├── test_stats.py          # Stats tesztek (23 teszt)
│   └── test_timer.py          # Timer tesztek (36 teszt)
│
├── rubik.db                    # SQLite adatbázis
├── requirements.txt            # Python függőségek
├── seed_data.py               # Kezdő adatok betöltése
├── start.sh                   # Indítási script
└── README.md                  # Ez a fájl
```

## 📡 API Dokumentáció

### Algorithms

| Method | Endpoint | Leírás |
|--------|----------|--------|
| GET | `/api/algorithms` | Összes algoritmus lekérdezése |
| GET | `/api/algorithms/{id}` | Egy algoritmus lekérdezése ID alapján |
| POST | `/api/algorithms` | Új algoritmus létrehozása |
| DELETE | `/api/algorithms/{id}` | Algoritmus törlése |
| GET | `/api/algorithms/search?q={query}` | Algoritmus keresés |

### Timer

| Method | Endpoint | Leírás |
|--------|----------|--------|
| POST | `/api/times` | Új idő mentése |
| GET | `/api/times` | Összes idő lekérdezése |
| GET | `/api/times/recent?limit={n}` | Legutóbbi N idő |
| GET | `/api/scramble` | Új scramble generálása |
| GET | `/api/scramble/daily` | Napi scramble lekérdezése |

### Statistics

| Method | Endpoint | Leírás |
|--------|----------|--------|
| GET | `/api/stats/summary` | Statisztikai összesítő |
| GET | `/api/stats/ao5` | Average of 5 |
| GET | `/api/stats/ao12` | Average of 12 |
| GET | `/api/stats/ao100` | Average of 100 |
| GET | `/api/stats/chart` | Grafikon adatok |
| GET | `/api/stats/distribution` | Időeloszlás |

### Példa Request

```bash
# Új idő mentése
curl -X POST "http://localhost:8000/api/times" \
  -H "Content-Type: application/json" \
  -d '{
    "time": 12.34,
    "scramble": "R U R' U' F D F' D'",
    "dnf": 0
  }'

# Algoritmus keresés
curl "http://localhost:8000/api/algorithms/search?q=T+Perm"

# Statisztikák
curl "http://localhost:8000/api/stats/summary"
```

## 🧪 Tesztelés

### Összes Teszt Futtatása

```bash
pytest tests/ -v
```

### Specifikus Teszt Fájl

```bash
pytest tests/test_timer.py -v
pytest tests/test_algorithms.py -v
pytest tests/test_stats.py -v
```

### Lefedettség Jelentés

```bash
pytest tests/ --cov=backend --cov-report=html
open htmlcov/index.html
```

### Teszt Statisztikák

- **Összesen**: 78 teszt
- **Success Rate**: 100%
- **Lefedettség**: ~85%
- **Futási idő**: ~0.4s

**Teszt Kategóriák**:
- Algorithm Service: 9 teszt
- Algorithm API: 10 teszt
- Stats Calculations: 23 teszt
- Timer Functions: 36 teszt

## ⚙️ Automatizáció

Az `automation/scheduler.py` 4 ütemezett feladatot futtat:

### 1. Napi Scramble Generálás
- **Ütemezés**: Minden nap 06:00
- **Funkció**: Generál egy új daily scramble-t
- **Célja**: Biztosítja, hogy mindig legyen fresh napi keverés

### 2. Heti Statisztikai Összesítő
- **Ütemezés**: Hétfő 08:00
- **Funkció**: Összesíti az elmúlt heti statisztikákat
- **Célja**: Heti progresszió nyomon követése

### 3. Régi Scramble-k Törlése
- **Ütemezés**: Vasárnap 00:00
- **Funkció**: Törli a 30 napnál régebbi használt scramble-ket
- **Célja**: Adatbázis karbantartás

### 4. Adatbázis Statisztika Logolás
- **Ütemezés**: Minden nap 23:00
- **Funkció**: Napi DB statisztikák logolása
- **Célja**: Monitoring és insight

### Scheduler Futtatása

```bash
python automation/scheduler.py
```

A scheduler a háttérben fut és folyamatosan ellenőrzi az ütemezett feladatokat.

## 🎓 Multi-Paradigma Példák

### OOP Példa: Algorithm Service

```python
service = AlgorithmService(db)
algorithm = service.create(AlgorithmCreate(
    name="T-Perm",
    notation="R U R' U' R' F R2 U' R' U' R U R' F'",
    category="PLL"
))
```

### Procedurális Példa: Scramble Generálás

```python
scramble = generate_scramble(length=20)
is_valid = validate_time(12.34)
formatted = format_time(125.67)  # "2:05.67"
```

### Funkcionális Példa: Statisztika Számítás

```python
service = StatsService(db)

# Map-Filter-Reduce pipeline
valid_times = service._get_valid_times(all_times)  # Filter
time_values = service._extract_time_values(valid_times)  # Map
average = service.calculate_average(all_times)  # Reduce
```

## 🐛 Problémamegoldás

### Backend nem indul el

```bash
# Ellenőrizd a portot
lsof -i :8000
# Ha foglalt, öld meg a folyamatot vagy használj másik portot
uvicorn backend.main:app --port 8001
```

### Frontend nem csatlakozik a backendhez

- Ellenőrizd, hogy a backend fut-e: `curl http://localhost:8000/docs`
- Nézd meg a `frontend/utils/api_client.py` BASE_URL értékét
- Ellenőrizd a CORS beállításokat a `backend/main.py`-ban

### Adatbázis hiba

```bash
# Töröld és újra inicializáld az adatbázist
rm rubik.db
python seed_data.py
```

### Teszt hibák

```bash
# Tisztítsd meg a cache-t
pytest --cache-clear tests/

# Futtass specifikus tesztet verbose módban
pytest tests/test_timer.py::TestTimerService::test_save_time_success -v
```

## 📚 További Források

- [FastAPI Dokumentáció](https://fastapi.tiangolo.com/)
- [Streamlit Dokumentáció](https://docs.streamlit.io/)
- [SQLAlchemy Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/)
- [Pytest Guide](https://docs.pytest.org/en/stable/)
- [Speedcubing](https://www.worldcubeassociation.org/)

## 👨‍💻 Fejlesztő Információk

### Verzió
- **v1.0.0** - Kezdeti release

### Készítő
- **Név**: Bence Kovács
- **University**: BSC 3. félév - Multi-paradigma programozás

### Licenc
MIT License

## 🎯 Jövőbeli Fejlesztések

- [ ] User authentication és regisztráció
- [ ] Több kocka típus támogatása (2x2, 4x4, Pyraminx, etc.)
- [ ] Bluetooth timer kapcsolat
- [ ] Competition mode
- [ ] Social features (barát keresés, verseny)
- [ ] Mobile app (React Native)
- [ ] Advanced analytics (ML prediction)
- [ ] Video tutorialok az algoritmusokhoz
- [ ] Cloud sync

---

**Élvezd a speedcubing-ot! 🎲⚡**
