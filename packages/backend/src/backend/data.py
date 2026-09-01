from functools import lru_cache

import pandas as pd

def parse_year(data_str: str) -> int:
    return int(data_str.split(" ")[0])
def parse_coord(coord: str) -> float:
    direction = coord[-1]
    value = float(coord[:-1])
    if direction in ("S", "W"):
        value = -value
    return value

@lru_cache(maxsize=1)
def load_solar() -> pd.DataFrame:
    df = pd.read_csv("data/archive-4/solar.csv")
    df["Year"] = df["Calendar Date"].apply(parse_year) 
    df["Latitude (deg)"] = df["Latitude"].apply(parse_coord)
    df["Longitude (deg)"] = df["Longitude"].apply(parse_coord)
    df["Path Width (km)"] = df["Path Width (km)"].replace("-", pd.NA)
    df["Path Width (km)"] = pd.to_numeric(df["Path Width (km)"], errors="coerce")
    return df