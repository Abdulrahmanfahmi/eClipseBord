import requests
import streamlit as st
import pandas as pd

BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="eClipseBord", page_icon="🌑", layout="wide")

st.title("eClipseBord")
st.caption("Solar eclipse dashboard — NASA Five Millennium Canon")

featured = requests.get(f"{BACKEND_URL}/eclipses/solar/featured").json()

st.subheader("Featured: totala solförmörkelsen 12 augusti 2026")
col1, col2, col3 = st.columns(3)
col1.metric("Datum", featured["Calendar Date"])
col2.metric("Typ", featured["Eclipse Type"])
col3.metric("Magnitud", featured["Eclipse Magnitude"])
st.divider()

st.sidebar.header("Filter")
year_min, year_max = st.sidebar.slider(
    "Årsintervall", min_value=-1999, max_value=3000, value=(1900, 2100)
)

st.subheader(f"Förmörkelser {year_min}–{year_max}")

stats = requests.get(
    f"{BACKEND_URL}/eclipses/solar/stats",
    params={"year_min": year_min, "year_max": year_max},
).json()

st.metric("Antal förmörkelser i valt intervall", stats["total"])

col1, col2 = st.columns(2)

with col1:
    st.subheader("Typfördelning")
    type_df = pd.DataFrame(stats["by_type"]).set_index("type")
    st.bar_chart(type_df)

with col2:
    st.subheader("Per århundrade")
    century_df = pd.DataFrame(stats["by_century"]).set_index("century")
    st.line_chart(century_df)