import os

import pandas as pd
import requests
import streamlit as st

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="eClipseBord", page_icon="", layout="wide")

st.title("eClipseBord")
st.caption("Solar eclipse dashboard — NASA Five Millennium Canon (-1999 till 3000)")

featured = requests.get(f"{BACKEND_URL}/eclipses/solar/featured").json()

with st.container(border=True):
    st.subheader("Featured: totala solförmörkelsen 12 augusti 2026")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Datum", featured["Calendar Date"])
    col2.metric("Typ", "Total" if featured["Eclipse Type"] == "T" else featured["Eclipse Type"])
    col3.metric("Magnitud", featured["Eclipse Magnitude"])
    col4.metric("Path width", f"{featured['Path Width (km)']:.0f} km")

st.divider()


st.sidebar.header("Filter")
year_min, year_max = st.sidebar.slider(
    "Årsintervall", min_value=-1999, max_value=3000, value=(1900, 2100)
)


stats = requests.get(
    f"{BACKEND_URL}/eclipses/solar/stats",
    params={"year_min": year_min, "year_max": year_max},
).json()

st.subheader(f"Förmörkelser {year_min}–{year_max}")
st.metric("Antal förmörkelser i valt intervall", stats["total"])
with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Typfördelning**")
        type_df = pd.DataFrame(stats["by_type"]).set_index("type")
        st.bar_chart(type_df, color="#F2A65A")

    with col2:
        st.markdown("**Per århundrade**")
        century_df = pd.DataFrame(stats["by_century"]).set_index("century")
        st.line_chart(century_df, color="#F2A65A")


st.divider()
st.markdown(f"**Lista över förmörkelser ({year_min}–{year_max})**")

listing = requests.get(
    f"{BACKEND_URL}/eclipses/solar",
    params={"year_min": year_min, "year_max": year_max},
).json()

listing_df = pd.DataFrame(listing)

listing_df = listing_df.fillna("–")

if not listing_df.empty:
    display_df = listing_df[
        ["Calendar Date", "Eclipse Type", "Eclipse Magnitude", "Path Width (km)", "Central Duration"]
    ].rename(columns={
        "Calendar Date": "Datum",
        "Eclipse Type": "Typ",
        "Eclipse Magnitude": "Magnitud",
        "Path Width (km)": "Path width (km)",
        "Central Duration": "Central duration",
    })
    display_df["Path width (km)"] = display_df["Path width (km)"].astype(str)
    st.dataframe(display_df, use_container_width=True, hide_index=True)
else:
    st.info("Inga förmörkelser i det valda intervallet.")