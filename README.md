# eClipseBord

En dashboard över NASA:s **"Five Millennium Canon of Solar/Lunar Eclipses"** (Fred Espenak), byggd för labben **eClipseBord — FastlyDep**.

Byggd med **FastAPI**, **Streamlit**, **Docker** och **Azure**, med extra fokus på den totala solförmörkelsen **12 augusti 2026**.

---

## Live demo

| | Länk |
|---|---|
| **Dashboard** | https://eclipsebord-frontend.whiteriver-57fab774.swedencentral.azurecontainerapps.io |
| **Backend API (Swagger-dokumentation)** | https://eclipsebord-backend.whiteriver-57fab774.swedencentral.azurecontainerapps.io/docs |

> **Observera:** Container Apps kan vara stoppade för att spara Azure-krediter. Kontakta mig om de behöver startas om.

---

## Om projektet

Dashboarden visar data om sol- och månförmörkelser från år **-1999 till 3000**. Man kan filtrera på årsintervall, se fördelning av förmörkelsetyper, trend över tid, och en lista över enskilda förmörkelser.

---

## Arkitektur

### Lokalt (uv workspace)

- `packages/backend` — FastAPI, serverar eclipse-data via REST-API
- `packages/frontend` — Streamlit, hämtar data från backend via HTTP

### Docker

- **backend-container** (port `8000`)
- **frontend-container** (port `8501`, pratar med backend via docker-compose-nätverk)

### Azure

- **Container Registry** — lagrar Docker-images
- **Container Apps** — kör backend och frontend, kopplade via miljövariabeln `BACKEND_URL`

---

## Projektstruktur

```
eClipseBord/
├── data/                        NASA eclipse-dataset (solar.csv, lunar.csv)
├── EDA/                         Kort exploration av datat
├── packages/
│   ├── backend/                 FastAPI-tjänst
│   │   ├── src/backend/
│   │   │   ├── data.py          Laddar och rensar CSV-data
│   │   │   └── main.py          API-endpoints
│   │   └── Dockerfile
│   └── frontend/                Streamlit-dashboard
│       ├── src/frontend/app.py
│       └── Dockerfile
├── docker-compose.yml
├── pyproject.toml               uv workspace-rot
└── uv.lock
```

---

## Köra lokalt

Kräver [uv](https://docs.astral.sh/uv/).

```bash
uv sync

# Terminal 1 — backend
uv run --package backend uvicorn backend.main:app --reload --port 8000

# Terminal 2 — frontend
uv run --package frontend streamlit run packages/frontend/src/frontend/app.py
```

- **Frontend:** http://localhost:8501
- **Backend-dokumentation:** http://localhost:8000/docs

---

## Köra med Docker

```bash
docker compose up --build
```

- **Frontend:** http://localhost:8501
- **Backend:** http://localhost:8000/docs

---

## Deploy till Azure

Deployat manuellt via Azure Portal:

1. Skapade en Azure Container Registry
2. Byggde Docker-images för `linux/amd64` och pushade dem till registret
3. Skapade en Container Apps-miljö
4. Skapade två Container Apps (backend och frontend), kopplade via miljövariabeln `BACKEND_URL`

---

## API-endpoints (backend)

| Endpoint | Beskrivning |
|---|---|
| `GET /health` | Hälsokontroll |
| `GET /eclipses/solar` | Lista solförmörkelser, filtrerbart på år |
| `GET /eclipses/solar/featured` | Den totala solförmörkelsen 12 augusti 2026 |
| `GET /eclipses/solar/stats` | Statistik: antal per typ och per århundrade |
| `GET /eclipses/lunar` | Lista månförmörkelser (bonus) |

---

## Designprincip: DRY

All logik för att ladda och städa eclipse-datat (till exempel omvandla koordinater som `"65.2N"` till decimaltal, och parsa år ur datumsträngar) ligger på ett enda ställe i `backend/data.py`. Flera API-endpoints återanvänder samma funktioner istället för att koden dupliceras.

---

## LLM usage

Jag använde en AI-assistent (Claude) som hjälp i delar av projektet.
