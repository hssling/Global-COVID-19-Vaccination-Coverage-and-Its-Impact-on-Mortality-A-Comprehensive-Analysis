#!/usr/bin/env python3
"""
Deployment script for COVID-19 Vaccination Analysis Dashboard
Author: Dr. Siddalingaiah H S
Email: hssling@yahoo.com
"""

import os
import shutil
import subprocess
from pathlib import Path

def create_deployment_package():
    """Create deployment package for Streamlit sharing"""

    print("🚀 Creating deployment package...")

    # Create deployment directory
    deploy_dir = Path("deploy")
    deploy_dir.mkdir(exist_ok=True)

    # Copy necessary files
    files_to_copy = [
        "data/covid_subset.csv",
        "outputs/reports/covid_vaccination_manuscript.md",
        "outputs/reports/supplementary_materials.md",
        "outputs/reports/validation_report.md",
        "outputs/reports/double_extraction_validation.md",
        "outputs/tables/vax_death_regression.txt",
        "requirements.txt",
        "dashboards/app.py",
        "README.md"
    ]

    for file_path in files_to_copy:
        source = Path(file_path)
        if source.exists():
            shutil.copy2(source, deploy_dir / source.name)
            print(f"✅ Copied {file_path}")

    # Create package info
    package_info = {
        "name": "COVID-19 Vaccination Analysis",
        "version": "1.0.0",
        "author": "Dr. Siddalingaiah H S",
        "email": "hssling@yahoo.com",
        "description": "Comprehensive analysis of global COVID-19 vaccination coverage and mortality",
        "repository": "https://github.com/hssling/Global-COVID-19-Vaccination-Coverage-and-Its-Impact-on-Mortality-A-Comprehensive-Analysis",
        "created": "2023-01-26"
    }

    with open(deploy_dir / "package_info.json", "w") as f:
        import json
        json.dump(package_info, f, indent=2)

    print(f"📦 Deployment package created in {deploy_dir}")
    return deploy_dir

def setup_streamlit():
    """Setup Streamlit configuration"""

    config_content = """
[server]
headless = true
port = 8501
enableCORS = false

[browser]
gatherUsageStats = false

[theme]
base = "light"
primaryColor = "#1f77b4"
"""

    with open("streamlit_config.toml", "w") as f:
        f.write(config_content)

    print("⚙️ Streamlit configuration created")

def run_analysis():
    """Run complete analysis pipeline"""

    print("🔬 Running analysis pipeline...")

    try:
        # Run data analysis
        subprocess.run(["python", "scripts/analyze_trends.py"], check=True)
        subprocess.run(["python", "scripts/vax_vs_deaths.py"], check=True)

        print("✅ Analysis completed successfully")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Analysis failed: {e}")
        return False

def main():
    """Main deployment function"""

    print("🌍 COVID-19 Vaccination Analysis - Deployment Setup")
    print("=" * 60)

    # Setup Streamlit
    setup_streamlit()

    # Run analysis
    if run_analysis():
        # Create deployment package
        deploy_dir = create_deployment_package()

        print("\n" + "=" * 60)
        print("🎉 Deployment setup completed!")
        print(f"📁 Deployment package: {deploy_dir}")
        print("🌐 Repository: https://github.com/hssling/Global-COVID-19-Vaccination-Coverage-and-Its-Impact-on-Mortality-A-Comprehensive-Analysis")
        print("\n📋 Next steps:")
        print("1. Push code to GitHub main branch")
        print("2. CI/CD will automatically deploy")
        print("3. Access dashboard at: https://hssling.github.io/Global-COVID-19-Vaccination-Coverage-and-Its-Impact-on-Mortality-A-Comprehensive-Analysis/")

if __name__ == "__main__":
    main()
