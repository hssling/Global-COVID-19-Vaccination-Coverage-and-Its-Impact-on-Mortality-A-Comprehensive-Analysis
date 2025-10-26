import pandas as pd
import statsmodels.api as sm
from pathlib import Path


BASE = Path("projects/COVID_vaccination_analysis")
DATA = BASE/"data"
OUTT = BASE/"outputs"/"tables"
OUTT.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA/"covid_subset.csv")
df = df[df["date"] > "2021-01-01"]
df["vax_rate"] = df["people_fully_vaccinated"]/df["population"]
df["death_rate"] = df["total_deaths"]/df["population"]
agg = df.groupby("location", as_index=False)[["vax_rate", "death_rate"]] \
    .max().dropna()

X = sm.add_constant(agg["vax_rate"])
model = sm.OLS(agg["death_rate"], X).fit()
with open(OUTT/"vax_death_regression.txt", "w") as f:
    f.write(model.summary().as_text())
print("✅ regression saved -> outputs/tables/vax_death_regression.txt")
