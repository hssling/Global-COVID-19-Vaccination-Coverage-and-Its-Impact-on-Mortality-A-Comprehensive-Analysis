import pandas as pd
import requests
from pathlib import Path


BASE = Path("projects/COVID_vaccination_analysis")
DATA = BASE/"data"
DATA.mkdir(parents=True, exist_ok=True)

# Our World in Data CSV URLs
URL_CASES = "https://covid.ourworldindata.org/data/owid-covid-data.csv"


def fetch_csv(url, name):
    out = DATA/f"{name}.csv"
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    out.write_bytes(r.content)
    print("✅ saved", out)


def main():
    fetch_csv(URL_CASES, "owid_covid")
    df = pd.read_csv(DATA/"owid_covid.csv")
    # small filtered subset for speed
    keep = [
        "location", "date", "total_cases", "new_cases", "total_deaths",
        "new_deaths", "people_vaccinated", "people_fully_vaccinated",
        "total_boosters", "population"
    ]
    df = df[keep]
    df.to_csv(DATA/"covid_subset.csv", index=False)
    print("✅ covid_subset.csv ready")


if __name__ == "__main__":
    main()
