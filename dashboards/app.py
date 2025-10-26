import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


st.set_page_config(
    page_title="COVID-19 Global Vaccination Dashboard",
    layout="wide"
)
BASE = Path("projects/COVID_vaccination_analysis")
DATA = BASE/"data"

st.title("🌍 COVID-19 Vaccination & Cases Dashboard")
df = pd.read_csv(DATA/"covid_subset.csv", parse_dates=["date"])

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
