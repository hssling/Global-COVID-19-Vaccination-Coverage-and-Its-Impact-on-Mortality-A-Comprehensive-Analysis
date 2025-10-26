import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


BASE = Path("projects/COVID_vaccination_analysis")
DATA = BASE/"data"
OUTP = BASE/"outputs"/"plots"
OUTP.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA/"covid_subset.csv")
print("Columns:", df.columns.tolist())
print("First few rows:")
print(df.head())
print("Data types:")
print(df.dtypes)
df["date"] = pd.to_datetime(df["date"])
# pick a few key countries for demo
countries = ["India", "United States", "Brazil", "United Kingdom", "Germany"]
sub = df[df["location"].isin(countries)]

# vaccination % of population
sub["vax_pct"] = 100 * sub["people_fully_vaccinated"] / sub["population"]

sns.lineplot(data=sub, x="date", y="vax_pct", hue="location")
plt.title("COVID-19 Vaccination Coverage (%)")
plt.xlabel("Date")
plt.ylabel("% Fully Vaccinated")
plt.tight_layout()
plt.savefig(OUTP/"vaccination_trend.png")
plt.close()

# cases per million
sub["cases_pm"] = sub["new_cases"] / (sub["population"]/1e6)
sns.lineplot(data=sub, x="date", y="cases_pm", hue="location")
plt.title("Daily COVID-19 Cases per Million")
plt.xlabel("Date")
plt.ylabel("Cases / million")
plt.tight_layout()
plt.savefig(OUTP/"cases_trend.png")
plt.close()

print("✅ saved plots in outputs/plots/")
