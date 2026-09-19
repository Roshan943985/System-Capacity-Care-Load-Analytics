import os
import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="System Capacity & Care Load Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# PATHS
# =========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "Data_Processed",
    "analytics_data.csv"
)

FORECAST_PATH = os.path.join(
    BASE_DIR,
    "data",
    "Data_Processed",
    "6_month_forecast.csv"
)

# =========================================================
# LIGHT PROFESSIONAL STYLING
# =========================================================
st.markdown("""
<style>
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}
.kpi-card {
    padding: 18px 18px 14px 18px;
    border: 1px solid rgba(128,128,128,0.25);
    border-radius: 12px;
    background: rgba(128,128,128,0.06);
    min-height: 105px;
}
.kpi-label {
    font-size: 0.82rem;
    color: #777;
    margin-bottom: 7px;
}
.kpi-value {
    font-size: 1.65rem;
    font-weight: 700;
}
.section-note {
    color: #777;
    font-size: 0.9rem;
}
.insight {
    padding: 12px 15px;
    border-left: 4px solid #888;
    background: rgba(128,128,128,0.06);
    border-radius: 6px;
    margin-bottom: 9px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# VALIDATE FILES
# =========================================================
if not os.path.exists(DATA_PATH):
    st.error(f"Analytics data file not found:\n{DATA_PATH}")
    st.stop()

if not os.path.exists(FORECAST_PATH):
    st.warning("Forecast file not found. Forecast section will be skipped.")

# =========================================================
# LOAD DATA
# =========================================================
@st.cache_data
def load_data():
    data = pd.read_csv(DATA_PATH)
    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
    data = data.dropna(subset=["Date"]).sort_values("Date").copy()
    return data

@st.cache_data
def load_forecast():
    if not os.path.exists(FORECAST_PATH):
        return pd.DataFrame()
    data = pd.read_csv(FORECAST_PATH)
    if "Date" in data.columns:
        data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
        data = data.dropna(subset=["Date"]).sort_values("Date").copy()
    return data

df = load_data()
forecast_df = load_forecast()

# =========================================================
# HEADER
# =========================================================
st.title("📊 System Capacity & Care Load Analytics")
st.markdown("**Executive Analytics Dashboard**")
st.caption(
    "System load, care demand, intake pressure, discharge activity and six-month forecast"
)
st.divider()

# =========================================================
# SIDEBAR FILTERS
# =========================================================
st.sidebar.header("Dashboard Filters")

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

start_date = st.sidebar.date_input(
    "Start Date", min_date, min_value=min_date, max_value=max_date
)
end_date = st.sidebar.date_input(
    "End Date", max_date, min_value=min_date, max_value=max_date
)

if start_date > end_date:
    st.sidebar.error("Start Date cannot be greater than End Date.")
    st.stop()

filtered_df = df[
    (df["Date"].dt.date >= start_date) &
    (df["Date"].dt.date <= end_date)
].copy()

if filtered_df.empty:
    st.warning("No records available for the selected date range.")
    st.stop()

st.sidebar.divider()
st.sidebar.caption(f"Data period: {min_date} to {max_date}")
st.sidebar.caption(f"Records in selection: {len(filtered_df):,}")

# =========================================================
# KPI CALCULATIONS
# =========================================================
peak_idx = filtered_df["Total System Load"].idxmax()
low_idx = filtered_df["Total System Load"].idxmin()

peak_load = filtered_df.loc[peak_idx, "Total System Load"]
peak_date = filtered_df.loc[peak_idx, "Date"].strftime("%d %b %Y")

lowest_load = filtered_df.loc[low_idx, "Total System Load"]
lowest_date = filtered_df.loc[low_idx, "Date"].strftime("%d %b %Y")

avg_load = filtered_df["Total System Load"].mean()
peak_hhs = filtered_df["Children in HHS Care"].max()
avg_hhs = filtered_df["Children in HHS Care"].mean()
total_discharge = filtered_df["Children discharged from HHS Care"].sum()
avg_discharge = filtered_df["Children discharged from HHS Care"].mean()

pressure_days = int((filtered_df["Net Daily Intake"] > 0).sum())
pressure_pct = (
    pressure_days / len(filtered_df) * 100 if len(filtered_df) else 0
)

# =========================================================
# KPI SECTION
# =========================================================
st.subheader("Key Performance Indicators")

kpis = [
    ("Peak System Load", f"{peak_load:,.0f}", peak_date),
    ("Average System Load", f"{avg_load:,.0f}", "Selected period"),
    ("Peak HHS Care", f"{peak_hhs:,.0f}", "Maximum observed"),
    ("Total HHS Discharges", f"{total_discharge:,.0f}", "Selected period"),
    ("Lowest System Load", f"{lowest_load:,.0f}", lowest_date),
    ("Average HHS Care", f"{avg_hhs:,.0f}", "Selected period"),
    ("Average Daily Discharges", f"{avg_discharge:,.0f}", "Per day"),
    ("Pressure Days", f"{pressure_days:,}", f"{pressure_pct:.1f}% of selected days"),
]

cols = st.columns(4)
for i, (label, value, note) in enumerate(kpis):
    with cols[i % 4]:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
                <div class="section-note">{note}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.write("")

# =========================================================
# TREND CHARTS
# =========================================================
st.subheader("Operational Trends")

left, right = st.columns(2)

with left:
    fig_load = px.line(
        filtered_df,
        x="Date",
        y="Total System Load",
        title="Total System Load",
        markers=False,
    )
    fig_load.update_layout(
        xaxis_title="Date",
        yaxis_title="System Load",
        hovermode="x unified",
    )
    st.plotly_chart(fig_load, use_container_width=True)

with right:
    fig_hhs = px.line(
        filtered_df,
        x="Date",
        y="Children in HHS Care",
        title="HHS Care Load",
        markers=False,
    )
    fig_hhs.update_layout(
        xaxis_title="Date",
        yaxis_title="Children in HHS Care",
        hovermode="x unified",
    )
    st.plotly_chart(fig_hhs, use_container_width=True)

# =========================================================
# PRESSURE + DISCHARGE
# =========================================================
left, right = st.columns(2)

with left:
    fig_intake = px.bar(
        filtered_df,
        x="Date",
        y="Net Daily Intake",
        title="Net Daily Intake / Pressure",
    )
    fig_intake.add_hline(y=0, line_dash="dash")
    fig_intake.update_layout(
        xaxis_title="Date",
        yaxis_title="Net Daily Intake",
        hovermode="x unified",
    )
    st.plotly_chart(fig_intake, use_container_width=True)

with right:
    fig_discharge = px.line(
        filtered_df,
        x="Date",
        y="Children discharged from HHS Care",
        title="HHS Discharge Activity",
    )
    fig_discharge.update_layout(
        xaxis_title="Date",
        yaxis_title="Children Discharged",
        hovermode="x unified",
    )
    st.plotly_chart(fig_discharge, use_container_width=True)

# =========================================================
# MONTHLY ANALYSIS
# =========================================================
st.subheader("Monthly Performance")

monthly_df = (
    filtered_df.set_index("Date")
    .resample("MS")["Total System Load"]
    .mean()
    .reset_index()
)

if not monthly_df.empty:
    fig_monthly = px.bar(
        monthly_df,
        x="Date",
        y="Total System Load",
        title="Monthly Average Total System Load",
        text_auto=".0f",
    )
    fig_monthly.update_layout(
        xaxis_title="Month",
        yaxis_title="Average System Load",
    )
    st.plotly_chart(fig_monthly, use_container_width=True)

# =========================================================
# FORECAST
# =========================================================
if not forecast_df.empty:
    forecast_columns = [
        "Forecast Total System Load",
        "Forecast",
        "forecast",
        "Predicted Total System Load",
        "Predicted Load",
    ]
    forecast_column = next(
        (c for c in forecast_columns if c in forecast_df.columns), None
    )

    if forecast_column:
        st.subheader("Six-Month Forecast")

        fig_forecast = px.line(
            forecast_df,
            x="Date",
            y=forecast_column,
            title="Forecasted Total System Load",
            markers=True,
        )
        fig_forecast.update_layout(
            xaxis_title="Forecast Month",
            yaxis_title="Forecast System Load",
            hovermode="x unified",
        )
        st.plotly_chart(fig_forecast, use_container_width=True)

        f_start = forecast_df[forecast_column].iloc[0]
        f_end = forecast_df[forecast_column].iloc[-1]
        f_change = f_end - f_start
        f_change_pct = (f_change / f_start * 100) if f_start else 0

        c1, c2, c3 = st.columns(3)
        c1.metric("Forecast Starting Load", f"{f_start:,.0f}")
        c2.metric("Forecast Ending Load", f"{f_end:,.0f}")
        c3.metric("Forecast Change", f"{f_change_pct:+.1f}%")

        forecast_display = forecast_df.copy()
        forecast_display["Date"] = forecast_display["Date"].dt.strftime("%B %Y")
        forecast_display[forecast_column] = forecast_display[forecast_column].round(2)

        with st.expander("View Forecast Table"):
            st.dataframe(
                forecast_display,
                use_container_width=True,
                hide_index=True,
            )

# =========================================================
# KEY INSIGHTS
# =========================================================
st.subheader("Key Insights")

insight_1 = (
    f"Peak system load was {peak_load:,.0f} on {peak_date}, "
    f"while the lowest observed load was {lowest_load:,.0f} on {lowest_date}."
)

insight_2 = (
    f"HHS care averaged {avg_hhs:,.0f} children during the selected period, "
    f"with a peak of {peak_hhs:,.0f}."
)

insight_3 = (
    f"{pressure_days:,} days showed positive net intake, representing "
    f"{pressure_pct:.1f}% of the selected period."
)

for text in [insight_1, insight_2, insight_3]:
    st.markdown(f'<div class="insight">{text}</div>', unsafe_allow_html=True)

# =========================================================
# DATA QUALITY / DETAIL
# =========================================================
with st.expander("Dataset Details"):
    d1, d2, d3 = st.columns(3)
    d1.metric("Records", f"{len(filtered_df):,}")
    d2.metric("Columns", f"{filtered_df.shape[1]:,}")
    d3.metric("Date Coverage", f"{start_date} → {end_date}")

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
    )

# =========================================================
# DOWNLOAD
# =========================================================
csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇️ Download Filtered Analytics Data",
    data=csv_data,
    file_name="filtered_analytics_data.csv",
    mime="text/csv",
)

# =========================================================
# FOOTER
# =========================================================
st.divider()
st.caption(
    "System Capacity & Care Load Analytics | "
    "Python • Pandas • Streamlit • Plotly"
)
