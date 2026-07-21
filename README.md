# Ethiopia Financial Inclusion Forecasting

## Project Overview

This project develops a forecasting system to track Ethiopia's digital financial transformation using time series methods. The system predicts Ethiopia's progress on two core dimensions of financial inclusion as defined by the World Bank's Global Findex:

- **Access** — Account Ownership Rate
- **Usage** — Digital Payment Adoption Rate

The forecasting system was developed for **Selam Analytics**, a financial technology consulting firm specializing in emerging markets, engaged by a consortium of stakeholders including development finance institutions, mobile money operators, and the National Bank of Ethiopia.

## Key Findings

- Account ownership grew from 14% (2011) to 49% (2024)
- Critical slowdown detected: Only +3 percentage points growth between 2021-2024 despite Telebirr (54M+ users) and M-Pesa (10M+ users) expansion
- 2025-2027 Forecast: Account ownership projected to reach 69.4% by 2027 (base case)
- 60% Target: Ethiopia likely to reach the 60% account ownership target by 2027 in base case scenario
- Digital payment adoption shows strong growth potential with mobile money penetration increasing

## Project Structure
ethiopia-fi-forecast/
├── data/
│ ├── raw/ # Starter dataset
│ │ ├── ethiopia_fi_unified_data.xlsx
│ │ └── reference_codes.xlsx
│ └── processed/ # Analysis-ready data
│ └── enriched_dataset.csv # Enriched with new observations, events, impact links
├── notebooks/
│ ├── 01_data_exploration.ipynb # Task 1: Data exploration and enrichment
│ ├── 02_eda.ipynb # Task 2: Exploratory data analysis
│ ├── 03_impact_modeling.ipynb # Task 3: Event impact modeling
│ └── 04_forecasting.ipynb # Task 4: Forecasting access and usage
├── src/
│ ├── init.py
│ └── data_utils.py # Data utility functions
├── dashboard/
│ └── app.py # Streamlit dashboard application
├── reports/
│ ├── figures/ # Generated visualizations
│ │ ├── 01_account_ownership_trend.png
│ │ ├── 02_gender_gap.png
│ │ ├── 03_digital_payment_trends.png
│ │ ├── 04_event_timeline.png
│ │ ├── 05_access_with_events.png
│ │ ├── 06_correlation_matrix.png
│ │ ├── 07_pillar_distribution.png
│ │ └── forecast_scenarios.png
│ ├── data_exploration_summary.txt
│ ├── indicator_coverage.csv
│ ├── eda_summary.txt
│ ├── association_matrix.csv
│ ├── impact_links_created.csv
│ ├── impact_modeling_methodology.txt
│ ├── forecast_summary.csv
│ ├── forecast_report.txt
│ └── forecast_scenarios.png
├── tests/
│ └── init.py
├── models/ # Saved models (gitignored)
├── .github/workflows/ # CI/CD workflows
├── data_enrichment_log.md # Data enrichment tracking
├── README.md
├── requirements.txt
└── .gitignore

## Dashboard Features

The interactive Streamlit dashboard provides:

- **Overview**: Key metrics, account ownership trend, digital payment trend, pillar distribution
- **Trends**: Interactive indicator selection with line/area/bar chart options, growth rates analysis
- **Forecasts**: 2025-2027 forecasts with optimistic, base, and pessimistic scenarios, progress toward 60% target
- **Events**: Event timeline, events by category, events by year
- **Data Explorer**: Filter and explore data by record type, pillar, confidence level, download as CSV

## Forecasting Methodology

### Approach

- **Baseline**: Linear trend regression with 95% confidence intervals
- **Scenario Analysis**: Optimistic, Base, and Pessimistic scenarios
- **Event Impacts**: Incorporated Telebirr, M-Pesa, EthSwitch interoperability, Fayda Digital ID, and 4G network expansion impacts
- **Uncertainty Quantification**: Standard error-based confidence intervals

### Key Assumptions

- Telebirr continues to grow at current pace
- M-Pesa expands user base in Ethiopia
- EthSwitch interoperability improves digital payments
- Fayda Digital ID accelerates account opening
- 4G coverage expansion enables mobile money adoption
- No major economic or political disruptions

### Forecast Results (Base Case)

| Indicator | 2025 | 2026 | 2027 |
|---|---|---|---|
| Access | 63.8% | 66.6% | 69.4% |
| Usage | Based on data trends | Based on data trends | Based on data trends |

### Forecast Ranges

| Indicator | 2025 Range | 2027 Range |
|---|---|---|
| Access | 50.4% - 77.2% | 56.0% - 82.8% |

### Event Impact Association Matrix

| Event | ACC_OWNERSHIP | ACC_MM_ACCOUNT | USG_DIGITAL_PAYMENT |
|---|---|---|---|
| Telebirr Launch | +3.0 (12mo) | +4.5 (6mo) | +5.0 (12mo) |
| M-Pesa Entry | - | +3.0 (6mo) | +4.0 (12mo) |
| EthSwitch Interoperability | - | - | +2.0 (3mo) |
| Fayda Digital ID | +1.5 (12mo) | +2.0 (6mo) | - |
| 4G Network Expansion | - | +1.0 (18mo) | +1.5 (12mo) |

## Data Sources

| Source | Type | Coverage |
|---|---|---|
| Global Findex Database | Survey | 2011-2024 |
| National Bank of Ethiopia (NBE) | Regulatory | Various |
| GSMA State of the Industry | Industry | Annual |
| IMF Financial Access Survey | Supply-side | Annual |
| Ethio Telecom | Operator | Telebirr data |
| Safaricom | Operator | M-Pesa data |

## Key Indicators

| Code | Description | Pillar |
|---|---|---|
| ACC_OWNERSHIP | Account Ownership Rate | Access |
| ACC_MM_ACCOUNT | Mobile Money Account Ownership | Access |
| USG_DIGITAL_PAYMENT | Digital Payment Adoption Rate | Usage |
| ACC_OWN_FEMALE | Female Account Ownership | Gender |
| ACC_OWN_MALE | Male Account Ownership | Gender |
| ACC_URBAN | Urban Account Ownership | Access |
| ACC_RURAL | Rural Account Ownership | Access |

## Installation and Setup

### Prerequisites

- Python 3.9+
- pip package manager

### Clone the Repository

```bash
git clone https://github.com/nardos-tsige/ethiopia-fi-forecast.git
cd ethiopia-fi-forecast
```

### Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate        # On macOS/Linux
venv\Scripts\activate           # On Windows
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Dashboard

```bash
streamlit run dashboard/app.py
```

### Run Jupyter Notebooks

```bash
jupyter notebook notebooks/
```

## Dependencies
pandas>=2.0.0
numpy>=1.24.0
scipy>=1.10.0
matplotlib>=3.7.0
seaborn>=0.12.0
plotly>=5.14.0
scikit-learn>=1.3.0
statsmodels>=0.14.0
streamlit>=1.25.0
jupyter>=1.0.0
openpyxl>=3.0.0

## Key Insights

- **Slowdown Paradox**: Account ownership grew only +3pp (2021-2024) despite 65M+ mobile money accounts being opened. Mobile money registration does not automatically translate to active financial inclusion.
- **Gender Disparity**: Persistent gender gap in access requires targeted interventions.
- **Event-Inclusion Relationship**: Product launches (Telebirr, M-Pesa) and policy changes (NBE Interoperability Directive) significantly influence inclusion outcomes with varying lags.
- **Infrastructure Importance**: 4G coverage, agent density, and mobile penetration correlate with adoption rates.
- **Target Progress**: Ethiopia projected to reach 69.4% account ownership by 2027 (base case), exceeding the 60% target.

## Task Summary

| Task | Description | Status |
|---|---|---|
| Task 1 | Data Exploration and Enrichment |  Complete |
| Task 2 | Exploratory Data Analysis |  Complete |
| Task 3 | Event Impact Modeling |  Complete |
| Task 4 | Forecasting Access and Usage |  Complete |
| Task 5 | Dashboard Development |  Complete |

## Technologies Used

- **Python** — Data analysis and modeling
- **Pandas** — Data manipulation
- **NumPy** — Numerical computing
- **Matplotlib/Seaborn** — Static visualizations
- **Plotly** — Interactive visualizations
- **Scikit-learn** — Linear regression modeling
- **Statsmodels** — Statistical analysis
- **Streamlit** — Interactive dashboard
- **Jupyter** — Exploratory analysis notebooks

## Contributors

- **Nardos Tsige** — Data Scientist, Selam Analytics

## License

This project is for educational purposes as part of the 10 Academy Artificial Intelligence Mastery program.

## Acknowledgments

- 10 Academy — AI Mastery Program
- Selam Analytics — Project sponsor
- Global Findex — Data provider
- National Bank of Ethiopia — Data provider
- GSMA — Mobile money data provider

## Contact

- **Name**: Nardos Tsige
- **GitHub**: [nardos-tsige](https://github.com/nardos-tsige)

---

*Last Updated: July 2026*
