from fastapi import FastAPI, HTTPException

from backend.data import load_solar

FEATURED_CATALOG_NUMBER = 9566

app = FastAPI()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/eclipses/solar")
def list_solar_eclipses(year_min: int = -1999, year_max: int = 3000) -> list[dict]:
    df = load_solar()
    filtered = df[(df["Year"] >= year_min) & (df["Year"] <= year_max)]
    return filtered.to_dict(orient="records")


@app.get("/eclipses/solar/featured")
def featured_solar_eclipse() -> dict:
    df = load_solar()
    row = df[df["Catalog Number"] == FEATURED_CATALOG_NUMBER]
    if row.empty:
        raise HTTPException(status_code=404, detail="Featured eclipse not found")
    return row.to_dict(orient="records")[0]

@app.get("/eclipses/solar/stats")
def solar_stats(year_min: int = -1999, year_max: int = 3000) -> dict:
    df = load_solar()
    filtered = df[(df["Year"] >= year_min) & (df["Year"] <= year_max)]

    by_type = filtered["Eclipse Type"].value_counts()
    by_century = filtered.groupby("Century").size()

    return {
        "total": len(filtered),
        "by_type": [{"type": t, "count": int(c)} for t, c in by_type.items()],
        "by_century": [{"century": int(cent), "count": int(c)} for cent, c in by_century.items()],
    }