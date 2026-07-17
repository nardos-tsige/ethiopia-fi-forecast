# Ethiopia Financial Inclusion Forecasting

## Project Overview
Forecasting Ethiopia's financial inclusion progress (Access and Usage) for 2025-2027 using time series methods.

## Project Structure
ethiopia-fi-forecast/
├── data/
│   ├── raw/            # Starter dataset
│   └── processed/      # Analysis-ready data
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_impact_modeling.ipynb
│   └── 04_forecasting.ipynb
├── src/                # Source code modules
├── dashboard/
│   └── app.py           # Streamlit dashboard
├── tests/               # Unit tests
├── models/              # Saved models
├── reports/             # Generated reports and figures
└── .github/workflows/   # CI/CD workflows

## Setup Instructions

### 1. Clone the repository
```bash
git clone <repository-url>
cd ethiopia-fi-forecast
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the dashboard
```bash
streamlit run dashboard/app.py
```

## Team
- Kerod
- Mahbubah
- Feven

## Timeline
- Challenge Start: 15 Jul 2026
- Interim Submission: 19 Jul 2026
- Final Submission: 21 Jul 2026