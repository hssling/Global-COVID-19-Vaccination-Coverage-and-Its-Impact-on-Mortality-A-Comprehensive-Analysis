#!/usr/bin/env python3
"""
GitHub Repository Setup for COVID-19 Vaccination Analysis
Author: Dr. Siddalingaiah H S
Email: hssling@yahoo.com
"""

import os
import subprocess
from pathlib import Path

def run_command(command, description=""):
    """Run shell command with error handling"""
    print(f"🔧 {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return None

def setup_git_repository():
    """Setup Git repository and connect to GitHub"""

    print("🚀 Setting up Git repository...")

    # Initialize git if not already done
    if not Path(".git").exists():
        run_command("git init", "Initialize Git repository")

    # Add remote origin
    repo_url = "https://github.com/hssling/Global-COVID-19-Vaccination-Coverage-and-Its-Impact-on-Mortality-A-Comprehensive-Analysis.git"
    run_command(f"git remote add origin {repo_url}", "Add GitHub remote")

    # Create .gitignore
    gitignore_content = """
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
.venv/
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Project specific
*.log
.cache/
*.tmp

# Data (optional - uncomment if you don't want to commit data)
# data/raw/
# *.csv
"""

    with open(".gitignore", "w") as f:
        f.write(gitignore_content)

    print("📝 Created .gitignore")

def create_github_workflow():
    """Create GitHub Actions workflow"""

    workflow_content = '''
name: COVID-19 Vaccination Analysis CI/CD

on:
  push:
    branches: [ main, develop ]
    paths:
      - 'projects/COVID_vaccination_analysis/**'
  pull_request:
    branches: [ main ]
    paths:
      - 'projects/COVID_vaccination_analysis/**'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        cd projects/COVID_vaccination_analysis
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run tests and analysis
      run: |
        cd projects/COVID_vaccination_analysis
        python scripts/analyze_trends.py
        python scripts/vax_vs_deaths.py

    - name: Validate data
      run: |
        cd projects/COVID_vaccination_analysis
        python -c "
        import pandas as pd
        df = pd.read_csv('data/covid_subset.csv')
        print(f'Data shape: {df.shape}')
        print(f'Columns: {list(df.columns)}')
        print('✅ Data validation passed')
        "

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        cd projects/COVID_vaccination_analysis
        pip install --upgrade pip
        pip install -r requirements.txt

    - name: Create deployment package
      run: |
        cd projects/COVID_vaccination_analysis
        mkdir -p deploy
        cp -r data/ deploy/
        cp -r outputs/ deploy/
        cp dashboards/app.py deploy/
        cp requirements.txt deploy/
        echo "from app import *" > deploy/__init__.py

    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: projects/COVID_vaccination_analysis/deploy
        cname: covid-vaccination-analysis.streamlit.app
'''

    # Create workflows directory
    Path(".github/workflows").mkdir(parents=True, exist_ok=True)

    with open(".github/workflows/covid_vaccination_analysis.yml", "w") as f:
        f.write(workflow_content)

    print("⚙️ Created GitHub Actions workflow")

def create_deployment_files():
    """Create deployment configuration files"""

    # Streamlit config
    streamlit_config = """
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

    with open("projects/COVID_vaccination_analysis/streamlit_config.toml", "w") as f:
        f.write(streamlit_config)

    print("📄 Created Streamlit configuration")

def main():
    """Main setup function"""

    print("🌍 COVID-19 Vaccination Analysis - GitHub Setup")
    print("=" * 60)
    print("Author: Dr. Siddalingaiah H S")
    print("Email: hssling@yahoo.com")
    print("Repository: https://github.com/hssling/Global-COVID-19-Vaccination-Coverage-and-Its-Impact-on-Mortality-A-Comprehensive-Analysis")
    print("=" * 60)

    # Setup git repository
    setup_git_repository()

    # Create GitHub workflow
    create_github_workflow()

    # Create deployment files
    create_deployment_files()

    print("\n" + "=" * 60)
    print("🎉 GitHub setup completed!")
    print("\n📋 Next steps:")
    print("1. Review and commit changes:")
    print("   git add .")
    print("   git commit -m 'Initial commit: COVID-19 Vaccination Analysis'")
    print("   git push -u origin main")
    print("\n2. Enable GitHub Pages in repository settings")
    print("3. CI/CD will automatically run on push")
    print("4. Access dashboard at: https://hssling.github.io/Global-COVID-19-Vaccination-Coverage-and-Its-Impact-on-Mortality-A-Comprehensive-Analysis/")

if __name__ == "__main__":
    main()
