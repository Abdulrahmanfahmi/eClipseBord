from fastapi import FastAPI

from backend.data import load_solar

app = FastAPI()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/eclipses/solar")
def list_solar_eclipses(year_min: int = -1999, year_max: int = 3000) -> list[dict]:
    df = load_solar()
    filtered = df[(df["Year"] >= year_min) & (df["Year"] <= year_max)]
    return filtered.to_dict(orient="records")