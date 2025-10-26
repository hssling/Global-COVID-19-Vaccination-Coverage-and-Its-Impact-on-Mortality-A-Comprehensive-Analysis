import subprocess


def run(c):
    print("==>", c)
    r = subprocess.run(c, shell=True)
    return r


def main():
    print("🚀 Starting COVID-19 Vaccination Analysis Pipeline")
    print("=" * 60)

    # Step 1: Fetch data
    print("\n📊 Step 1: Fetching COVID-19 data...")
    run("python projects/COVID_vaccination_analysis/scripts/fetch_data.py")

    # Step 2: Analyze trends and create visualizations
    print("\n📈 Step 2: Analyzing trends and creating visualizations...")
    run("python projects/COVID_vaccination_analysis/scripts/analyze_trends.py")

    # Step 3: Run regression analysis
    print("\n🔬 Step 3: Running statistical analysis...")
    run("python projects/COVID_vaccination_analysis/scripts/vax_vs_deaths.py")

    print("\n" + "=" * 60)
    print("🎉 Analysis Complete!")
    print("\n📋 Next Steps:")
    print("1. View results in outputs/ directory")
    print("2. Launch dashboard: streamlit run projects/COVID_vaccination_analysis/dashboards/app.py")
    print("3. Check outputs/plots/ for visualizations")
    print("4. Review outputs/tables/ for statistical results")


if __name__ == "__main__":
    main()
