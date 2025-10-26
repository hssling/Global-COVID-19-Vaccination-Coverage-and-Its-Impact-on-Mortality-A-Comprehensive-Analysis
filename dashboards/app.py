import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import os


st.set_page_config(
    page_title="COVID-19 Global Vaccination Dashboard",
    layout="wide"
)

# Handle different deployment environments
current_dir = Path(__file__).parent
project_root = current_dir.parent

# Try multiple possible data locations
possible_paths = [
    project_root / "data" / "covid_subset.csv",  # Local development
    current_dir / "data" / "covid_subset.csv",   # Same directory
    Path("data") / "covid_subset.csv",           # Relative path
    Path("covid_subset.csv")                     # Direct path
]

df = None
for data_path in possible_paths:
    try:
        df = pd.read_csv(data_path, parse_dates=["date"])
        print(f"✅ Successfully loaded data from: {data_path}")
        break
    except FileNotFoundError:
        continue

if df is None:
    st.error("❌ Could not find covid_subset.csv file. Please ensure data files are in the correct location.")
    st.stop()

st.title("🌍 COVID-19 Vaccination & Cases Dashboard")

countries = st.multiselect(
    "Select countries",
    sorted(df["location"].unique()),
    ["India", "United States"]
)
metric = st.selectbox(
    "Metric",
    ["people_fully_vaccinated", "total_cases", "total_deaths"]
)
df_sub = df[df["location"].isin(countries)]

fig = px.line(
    df_sub,
    x="date",
    y=metric,
    color="location",
    title=f"{metric.replace('_', ' ').title()} over Time"
)
st.plotly_chart(fig, use_container_width=True)

df_last = df.groupby("location").last().reset_index()
df_last["vax_pct"] = 100 * df_last["people_fully_vaccinated"] / df_last["population"]
fig2 = px.bar(
    df_last.sort_values("vax_pct", ascending=False).head(20),
    x="location",
    y="vax_pct",
    title="Top 20 Vaccination Coverage (%)"
)
st.plotly_chart(fig2, use_container_width=True)
