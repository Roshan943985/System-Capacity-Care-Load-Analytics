# System Capacity & Care Load Analytics

## Project Overview

**System Capacity & Care Load Analytics** is a data analytics and forecasting project designed to analyze operational workload and capacity pressure within the Unaccompanied Children (UAC) care system.

The project uses historical data related to children in CBP custody, HHS care, transfers, and discharges to understand system load, identify high-pressure periods, measure operational trends, and forecast future care-system demand.

## Business Problem

A sudden increase in children entering the care system can create operational pressure on available resources and care capacity.

This project answers questions such as:

- What is the overall system care load?
- When does the system experience peak pressure?
- How does HHS care load change over time?
- Are inflows consistently higher than outflows?
- Which periods require greater operational attention?
- What could future system load look like?

## Project Objectives

- Clean and prepare historical UAC data.
- Calculate important operational KPIs.
- Analyze system capacity and care-load trends.
- Identify pressure and high-load periods.
- Study relationships between operational variables.
- Perform monthly performance analysis.
- Forecast future system load using ARIMA.
- Build an interactive Streamlit dashboard.

## Dataset & Preprocessing

The processed dataset contains:

- **720 records**
- **12 analytical columns**
- Date range: **January 2023 – December 2025**

Derived analytical metrics include:

- Total System Load
- Net Daily Intake
- Care Load Growth Rate
- 7-Day Rolling Load
- 14-Day Rolling Load
- Backlog Indicator

## Key KPIs

| KPI | Result |
|---|---:|
| Peak System Load | **11,762** |
| Lowest System Load | **2,002** |
| Average System Load | **6,232.77** |
| Peak HHS Care | **11,516** |
| Average HHS Care | **6,061.28** |
| Total HHS Discharges | **124,853** |
| Average Daily Discharges | **173.41** |
| Pressure Days | **238** |

The highest recorded system load occurred on **20 December 2023**.

## Pressure Analysis

**Net Daily Intake** was used to understand changes in system pressure from daily inflow relative to outflow.

Key results:

- Positive intake days: **238**
- Negative intake days: **475**
- Zero intake days: **7**
- Highest-pressure day: **12 February 2024**
- Highest Net Daily Intake: **206**

This analysis helps identify periods where additional operational capacity may be required.

## Monthly Analysis

Monthly aggregation was performed to identify long-term trends and changes in system workload.

### Highest Monthly Average System Load

**December 2023 — 11,255.26**

### Lowest Monthly Average System Load

**August 2025 — 2,026.90**

The analysis shows a substantial reduction in system load from the peak period to later periods.

## Correlation Analysis

Correlation analysis was performed to understand relationships between operational variables and Total System Load.

The strongest relationship was observed between:

**HHS Care ↔ Total System Load: 0.9995**

This is expected because HHS Care forms the largest component of the calculated Total System Load in the analyzed dataset.

## Forecasting

An **ARIMA time-series model** was used to generate a six-month forecast.

### Forecast Period

**January 2026 – June 2026**

| Month | Forecast |
|---|---:|
| Jan 2026 | 2,718.97 |
| Feb 2026 | 2,970.64 |
| Mar 2026 | 3,204.21 |
| Apr 2026 | 3,421.01 |
| May 2026 | 3,622.21 |
| Jun 2026 | 3,808.96 |

The forecast indicates an approximately **40.09% increase** from the first to the final forecasted month.

## Interactive Dashboard

The project includes a professional **Streamlit + Plotly dashboard** with:

- KPI cards
- System Load Trend
- HHS Care Trend
- Pressure Analysis
- Discharge Analysis
- Monthly Performance
- Six-Month Forecast
- Date filters
- Key business insights
- Dataset information
- CSV download functionality

## Technology Stack

- **Python**
- **Pandas**
- **NumPy**
- **Plotly**
- **Streamlit**
- **Statsmodels / ARIMA**
- **Jupyter Notebook**
- **VS Code**
- **CSV**

## Project Workflow

```text
Raw Dataset
     ↓
Data Cleaning
     ↓
Data Validation
     ↓
Feature Engineering
     ↓
EDA
     ↓
KPI Analysis
     ↓
Pressure Analysis
     ↓
Correlation Analysis
     ↓
Monthly Analysis
     ↓
ARIMA Forecasting
     ↓
Streamlit Dashboard
     ↓
Business Insights
```

## Project Structure

```text
System_Capacity_Care_Load_Analytics 1
│
├── Dashboard
│   └── app.py
│
├── Data
│   └── Data_Processed
│       ├── analytics_data.csv
│       ├── 6_month_forecast.csv
│       ├── cleaned_data.csv
│       ├── kpi_summary.csv
│       └── monthly_dashboard_data.csv
│
├── Notebooks
│
├── Requirements
│
└── Src
```

## How to Run

### 1. Install dependencies

```bash
pip install pandas numpy plotly streamlit statsmodels
```

### 2. Open the project directory

```bash
cd "C:\Intership\System_Capacity_Care_Load_Analytics 1"
```

### 3. Run the dashboard

```bash
streamlit run Dashboard\app.py
```

The dashboard will open in your browser.

## Key Business Insights

1. The system reached its highest recorded load of **11,762** on 20 December 2023.
2. The average system load across the analyzed period was **6,232.77**.
3. HHS Care showed a very strong relationship with overall system load.
4. December 2023 recorded the highest monthly average system load at **11,255.26**.
5. August 2025 recorded the lowest monthly average system load at **2,026.90**.
6. The ARIMA forecast projects increasing system load from **2,718.97 in January 2026** to **3,808.96 in June 2026**.

## Conclusion

This project demonstrates an end-to-end data analytics workflow covering **data cleaning, exploratory analysis, KPI development, pressure analysis, correlation analysis, time-series forecasting, and dashboard development**.

The final dashboard converts historical operational data into an interactive analytical tool that can support capacity monitoring, trend identification, and forward-looking planning.

## Author

**Roshan Korde**

**Data Analytics Project — Python | SQL | Excel | Power BI | Streamlit | Plotly**
