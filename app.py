import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Student Retention & Welfare Tracker",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS — SCHOOL PERFORMANCE DASHBOARD REFERENCE THEME
# ============================================================

st.markdown(
    """
    <style>
        .stApp {
            background: #f5f7f5;
        }

        .main .block-container {
            padding-top: 1.2rem;
            padding-bottom: 2rem;
        }

        /* DARK TEAL SIDEBAR */
        [data-testid="stSidebar"] {
            background: linear-gradient(
                180deg,
                #063f46 0%,
                #075b5c 50%,
                #064044 100%
            );
        }

        [data-testid="stSidebar"] * {
            color: white !important;
        }

        [data-testid="stSidebar"] label {
            font-weight: 600;
        }

        [data-testid="stSidebar"] .stMultiSelect div,
        [data-testid="stSidebar"] .stSelectbox div,
        [data-testid="stSidebar"] .stDateInput div {
            color: #173c40 !important;
        }

        /* HEADER — TEAL TO ORANGE GRADIENT */
        .dashboard-header {
            background: linear-gradient(
                110deg,
                #075052 0%,
                #087d78 38%,
                #579c75 65%,
                #d28b48 100%
            );
            border-radius: 15px;
            padding: 25px 28px;
            margin-bottom: 24px;
            box-shadow: 0 4px 14px rgba(6, 63, 70, 0.10);
        }

        .brand-name {
            color: #e4f5ef;
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 1.2px;
            text-transform: uppercase;
            margin-bottom: 6px;
        }

        .main-title {
            font-size: 34px;
            font-weight: 800;
            color: #ffffff;
            line-height: 1.2;
            margin-bottom: 6px;
        }

        .subtitle {
            color: #eef8f4;
            font-size: 14px;
            margin-bottom: 0;
        }

        .academic-year {
            display: inline-block;
            background: rgba(255, 255, 255, 0.18);
            color: #ffffff;
            border: 1px solid rgba(255, 255, 255, 0.45);
            border-radius: 8px;
            padding: 8px 14px;
            font-size: 12px;
            font-weight: 700;
            margin-top: 12px;
        }

        .section-title {
            color: #164b4c;
            font-size: 24px;
            font-weight: 800;
            margin-top: 25px;
            margin-bottom: 12px;
        }

        .kpi-card {
            background: #ffffff;
            border-radius: 13px;
            padding: 18px;
            min-height: 140px;
            border: 1px solid #dce8e4;
            box-shadow: 0 3px 12px rgba(6, 63, 70, 0.07);
        }

        .kpi-title {
            color: #607b7b;
            font-size: 13px;
            font-weight: 700;
            margin-bottom: 10px;
        }

        .kpi-value {
            color: #164b4c;
            font-size: 29px;
            font-weight: 800;
            margin-bottom: 5px;
        }

        .kpi-description {
            color: #849696;
            font-size: 11px;
        }

        .info-card {
            background: #e2f3ed;
            border-left: 5px solid #087d78;
            border-radius: 10px;
            padding: 17px;
            box-shadow: 0 3px 12px rgba(6, 63, 70, 0.05);
        }

        .info-title {
            color: #087d78;
            font-weight: 800;
            font-size: 15px;
        }

        .info-text {
            color: #355b5c;
            font-size: 14px;
            margin-top: 5px;
        }

        .risk-high {
            color: #d65b5b;
            font-weight: 800;
        }

        .risk-moderate {
            color: #d88b3d;
            font-weight: 800;
        }

        .risk-low {
            color: #159b86;
            font-weight: 800;
        }

        div[data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid #dce8e4;
            border-radius: 13px;
            padding: 15px;
            box-shadow: 0 3px 12px rgba(6, 63, 70, 0.07);
        }

        div[data-testid="stMetricLabel"] {
            color: #607b7b !important;
        }

        div[data-testid="stMetricValue"] {
            color: #164b4c !important;
        }

        .stDownloadButton button {
            background: #087d78;
            color: white;
            border-radius: 8px;
            border: none;
            font-weight: 700;
        }

        .stDownloadButton button:hover {
            background: #075052;
            color: white;
        }

        [data-testid="stDataFrame"] {
            border: 1px solid #dce8e4;
            border-radius: 10px;
        }

        /* WHITE CHART BOXES WITH READABLE CONTENT */
        [data-testid="stPlotlyChart"] {
            background: #ffffff !important;
            border: 1px solid #e2e8e6;
            border-radius: 12px;
            padding: 8px;
            box-shadow: 0 3px 12px rgba(6, 63, 70, 0.06);
        }

        [data-testid="stPlotlyChart"] > div,
        [data-testid="stPlotlyChart"] .js-plotly-plot,
        [data-testid="stPlotlyChart"] .plot-container {
            background: #ffffff !important;
        }

        /* Keep Plotly text dark and visible against white backgrounds */
        [data-testid="stPlotlyChart"] text,
        [data-testid="stPlotlyChart"] .xtick text,
        [data-testid="stPlotlyChart"] .ytick text,
        [data-testid="stPlotlyChart"] .gtitle,
        [data-testid="stPlotlyChart"] .legendtext {
            fill: #173c40 !important;
            color: #173c40 !important;
        }

        @media (max-width: 768px) {
            .main-title {
                font-size: 25px;
            }

            .dashboard-header {
                padding: 18px;
            }
        }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DATA LOADING
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

possible_paths = [
    BASE_DIR / "data" / "processed" / "school_dashboard.csv",
    BASE_DIR / "data" / "cleaned" / "school_dashboard.csv",
    BASE_DIR / "data" / "school_dashboard.csv",
    BASE_DIR / "school_dashboard.csv"
]

DATA_PATH = None

for path in possible_paths:
    if path.exists():
        DATA_PATH = path
        break

if DATA_PATH is None:
    st.error(
        "school_dashboard.csv was not found. "
        "Please place it inside data/processed/."
    )
    st.stop()


@st.cache_data
def load_data(file_path):
    dataframe = pd.read_csv(file_path)

    dataframe.columns = (
        dataframe.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    return dataframe


df = load_data(DATA_PATH)


# ============================================================
# DATA CLEANING
# ============================================================

numeric_columns = [
    "total_enrolled_students",
    "avg_attendance_rate",
    "total_attendance_records",
    "proxy_attendance_records",
    "proxy_attendance_rate",
    "count_anomaly_records",
    "count_anomaly_rate",
    "total_mdm_quantity_kg",
    "total_mdm_records",
    "total_mdm_cost",
    "avg_mdm_cost",
    "mdm_regularity_rate",
    "unique_vendors",
    "unique_grain_types",
    "assessed_facilities",
    "functional_facilities",
    "infrastructure_deficit_index",
    "average_test_score",
    "total_assessments",
    "subjects_assessed",
    "student_welfare_risk_score"
]

for column in numeric_columns:
    if column in df.columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")


# Create missing columns safely if required
default_columns = {
    "school_id": "Unknown",
    "school_name": "Unknown School",
    "district": "Unknown",
    "block": "Unknown",
    "school_type": "Unknown",
    "medium": "Unknown",
    "risk_level": "Unknown"
}

for column, default_value in default_columns.items():
    if column not in df.columns:
        df[column] = default_value


# Normalize text columns
text_columns = [
    "school_id",
    "school_name",
    "district",
    "block",
    "school_type",
    "medium",
    "risk_level"
]

for column in text_columns:
    if column in df.columns:
        df[column] = (
            df[column]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
        )


# ============================================================
# DERIVED METRICS
# ============================================================

if "infrastructure_deficit_index" not in df.columns:
    if {
        "assessed_facilities",
        "functional_facilities"
    }.issubset(df.columns):
        df["infrastructure_deficit_index"] = np.where(
            df["assessed_facilities"] > 0,
            (
                1
                - (
                    df["functional_facilities"]
                    / df["assessed_facilities"]
                )
            ) * 100,
            np.nan
        )
    else:
        df["infrastructure_deficit_index"] = np.nan


if "high_risk_flag" not in df.columns:
    df["high_risk_flag"] = (
        df["risk_level"]
        .astype(str)
        .str.lower()
        .str.contains("high")
    )


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.markdown(
    """
    <div style="font-size:26px;font-weight:800;margin-bottom:5px;">
        Dashboard Filters
    </div>
    <div style="font-size:13px;margin-bottom:20px;">
        Explore school performance, attendance, infrastructure,
        mid-day meals and high-risk schools.
    </div>
    """,
    unsafe_allow_html=True
)

if "reset_filters" not in st.session_state:
    st.session_state.reset_filters = False


def get_options(column):
    if column in df.columns:
        return sorted(
            df[column]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )
    return []


district_options = get_options("district")
block_options = get_options("block")
school_type_options = get_options("school_type")
medium_options = get_options("medium")
risk_options = get_options("risk_level")
school_options = get_options("school_name")


selected_districts = st.sidebar.multiselect(
    "Select District",
    options=district_options,
    default=[],
    placeholder="All districts"
)

selected_blocks = st.sidebar.multiselect(
    "Select Block",
    options=block_options,
    default=[],
    placeholder="All blocks"
)

selected_school_types = st.sidebar.multiselect(
    "Select School Type",
    options=school_type_options,
    default=[],
    placeholder="All school types"
)

selected_mediums = st.sidebar.multiselect(
    "Select Medium",
    options=medium_options,
    default=[],
    placeholder="All mediums"
)

selected_risk_levels = st.sidebar.multiselect(
    "Select Risk Level",
    options=risk_options,
    default=[],
    placeholder="All risk levels"
)

selected_schools = st.sidebar.multiselect(
    "Select Schools",
    options=school_options,
    default=[],
    placeholder="All schools"
)

st.sidebar.markdown("---")

attendance_min = st.sidebar.slider(
    "Minimum Attendance Rate",
    min_value=0.0,
    max_value=100.0,
    value=0.0,
    step=1.0
)

attendance_max = st.sidebar.slider(
    "Maximum Attendance Rate",
    min_value=0.0,
    max_value=100.0,
    value=100.0,
    step=1.0
)

deficit_min = st.sidebar.slider(
    "Minimum Infrastructure Deficit",
    min_value=0.0,
    max_value=100.0,
    value=0.0,
    step=1.0
)

deficit_max = st.sidebar.slider(
    "Maximum Infrastructure Deficit",
    min_value=0.0,
    max_value=100.0,
    value=100.0,
    step=1.0
)

high_risk_only = st.sidebar.checkbox(
    "Show only high-risk schools",
    value=False
)

st.sidebar.markdown("---")

if st.sidebar.button("Reset Filters", use_container_width=True):
    st.rerun()


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()

if selected_districts:
    filtered_df = filtered_df[
        filtered_df["district"].isin(selected_districts)
    ]

if selected_blocks:
    filtered_df = filtered_df[
        filtered_df["block"].isin(selected_blocks)
    ]

if selected_school_types:
    filtered_df = filtered_df[
        filtered_df["school_type"].isin(selected_school_types)
    ]

if selected_mediums:
    filtered_df = filtered_df[
        filtered_df["medium"].isin(selected_mediums)
    ]

if selected_risk_levels:
    filtered_df = filtered_df[
        filtered_df["risk_level"].isin(selected_risk_levels)
    ]

if selected_schools:
    filtered_df = filtered_df[
        filtered_df["school_name"].isin(selected_schools)
    ]

if "avg_attendance_rate" in filtered_df.columns:
    filtered_df = filtered_df[
        filtered_df["avg_attendance_rate"].between(
            attendance_min,
            attendance_max
        )
    ]

if "infrastructure_deficit_index" in filtered_df.columns:
    filtered_df = filtered_df[
        filtered_df["infrastructure_deficit_index"].between(
            deficit_min,
            deficit_max
        )
    ]

if high_risk_only:
    filtered_df = filtered_df[
        filtered_df["risk_level"]
        .astype(str)
        .str.lower()
        .str.contains("high")
    ]


# ============================================================
# HEADER — SCHOOL PERFORMANCE DASHBOARD STYLE
# ============================================================

st.markdown(
    """
    <div class="dashboard-header">
        <div class="brand-name">
            EduVision | Education & EdTech Analytics
        </div>
        <div class="main-title">
            Student Retention & Welfare Efficacy Tracker
        </div>
        <div class="subtitle">
            Monitoring school attendance, student welfare, infrastructure,
            mid-day meal performance and high-risk schools.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

if filtered_df.empty:
    st.warning("No schools match the selected filters.")
    st.stop()


# ============================================================
# TOP SUMMARY
# ============================================================

total_schools = filtered_df["school_id"].nunique()

total_students = (
    filtered_df["total_enrolled_students"].sum()
    if "total_enrolled_students" in filtered_df.columns
    else 0
)

average_attendance = (
    filtered_df["avg_attendance_rate"].mean()
    if "avg_attendance_rate" in filtered_df.columns
    else np.nan
)

average_test_score = (
    filtered_df["average_test_score"].mean()
    if "average_test_score" in filtered_df.columns
    else np.nan
)

average_mdm_regularity = (
    filtered_df["mdm_regularity_rate"].mean()
    if "mdm_regularity_rate" in filtered_df.columns
    else np.nan
)

average_deficit = (
    filtered_df["infrastructure_deficit_index"].mean()
    if "infrastructure_deficit_index" in filtered_df.columns
    else np.nan
)

high_risk_schools = (
    filtered_df["risk_level"]
    .astype(str)
    .str.lower()
    .str.contains("high")
    .sum()
)


# ============================================================
# KPI CARDS
# ============================================================

st.markdown(
    '<div class="section-title">Key Performance Indicators</div>',
    unsafe_allow_html=True
)

kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5, kpi_col6 = st.columns(6)


def format_number(value):
    if pd.isna(value):
        return "N/A"
    return f"{value:,.0f}"


def format_percent(value):
    if pd.isna(value):
        return "N/A"
    return f"{value:.1f}%"


with kpi_col1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Schools</div>
            <div class="kpi-value">{total_schools:,}</div>
            <div class="kpi-description">Schools in current selection</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi_col2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Enrolled Students</div>
            <div class="kpi-value">{format_number(total_students)}</div>
            <div class="kpi-description">Total enrolled students</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi_col3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Average Attendance</div>
            <div class="kpi-value">{format_percent(average_attendance)}</div>
            <div class="kpi-description">Average school attendance rate</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi_col4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Infrastructure Deficit Index</div>
            <div class="kpi-value">{format_percent(average_deficit)}</div>
            <div class="kpi-description">Higher value means greater deficit</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi_col5:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">High-Risk Schools</div>
            <div class="kpi-value">{high_risk_schools:,}</div>
            <div class="kpi-description">Schools requiring attention</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi_col6:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Average Test Score</div>
            <div class="kpi-value">{format_percent(average_test_score)}</div>
            <div class="kpi-description">Average academic score</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# AUTOMATED INSIGHT
# ============================================================

highest_deficit_school = None
highest_deficit_value = None

if "infrastructure_deficit_index" in filtered_df.columns:
    deficit_data = filtered_df.dropna(
        subset=["infrastructure_deficit_index"]
    )

    if not deficit_data.empty:
        highest_deficit_row = deficit_data.loc[
            deficit_data["infrastructure_deficit_index"].idxmax()
        ]

        highest_deficit_school = highest_deficit_row["school_name"]
        highest_deficit_value = highest_deficit_row[
            "infrastructure_deficit_index"
        ]

highest_attendance_school = None
highest_attendance_value = None

if "avg_attendance_rate" in filtered_df.columns:
    attendance_data = filtered_df.dropna(
        subset=["avg_attendance_rate"]
    )

    if not attendance_data.empty:
        highest_attendance_row = attendance_data.loc[
            attendance_data["avg_attendance_rate"].idxmax()
        ]

        highest_attendance_school = highest_attendance_row["school_name"]
        highest_attendance_value = highest_attendance_row[
            "avg_attendance_rate"
        ]

st.markdown(
    '<div class="section-title">Automated Insights</div>',
    unsafe_allow_html=True
)

insight_text = ""

if highest_deficit_school is not None:
    insight_text += (
        f"The school with the highest infrastructure deficit is "
        f"<b>{highest_deficit_school}</b>, with a deficit index of "
        f"<b>{highest_deficit_value:.1f}%</b>. "
    )

if highest_attendance_school is not None:
    insight_text += (
        f"The highest attendance rate is recorded by "
        f"<b>{highest_attendance_school}</b>, at "
        f"<b>{highest_attendance_value:.1f}%</b>."
    )

if not insight_text:
    insight_text = "Insights are unavailable for the current selection."

st.markdown(
    f"""
    <div class="info-card">
        <div class="info-title">Data-driven observation</div>
        <div class="info-text">{insight_text}</div>
    </div>
    """,
    unsafe_allow_html=True
)



# ============================================================
# PLOTLY CHART THEME — WHITE BOXES AND DARK READABLE TEXT
# ============================================================

def apply_chart_theme(figure):
    figure.update_layout(
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font={
            "family": "Arial, sans-serif",
            "size": 12,
            "color": "#173C40"
        },
        title={
            "font": {
                "family": "Arial, sans-serif",
                "size": 16,
                "color": "#173C40"
            },
            "x": 0.02,
            "xanchor": "left"
        },
        legend={
            "font": {
                "family": "Arial, sans-serif",
                "size": 12,
                "color": "#173C40"
            }
        },
        xaxis={
            "showgrid": True,
            "gridcolor": "#E5E7EB",
            "linecolor": "#94A3B8",
            "tickfont": {"color": "#173C40", "size": 11},
            "title_font": {"color": "#173C40", "size": 12}
        },
        yaxis={
            "showgrid": True,
            "gridcolor": "#E5E7EB",
            "linecolor": "#94A3B8",
            "tickfont": {"color": "#173C40", "size": 11},
            "title_font": {"color": "#173C40", "size": 12}
        }
    )
    return figure


# ============================================================
# ATTENDANCE AND RISK ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">Attendance and Risk Analysis</div>',
    unsafe_allow_html=True
)

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    if {
        "district",
        "avg_attendance_rate"
    }.issubset(filtered_df.columns):

        district_attendance = (
            filtered_df
            .groupby("district", as_index=False)["avg_attendance_rate"]
            .mean()
            .sort_values("avg_attendance_rate", ascending=True)
        )

        fig = px.bar(
            district_attendance,
            x="avg_attendance_rate",
            y="district",
            orientation="h",
            title="Average Attendance Rate by District",
            labels={
                "avg_attendance_rate": "Attendance Rate (%)",
                "district": "District"
            },
            color="avg_attendance_rate",
            color_continuous_scale=["#DCECF8", "#528FC1"]
        )

        fig.update_layout(
            height=430,
            template="plotly_white",
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            coloraxis_showscale=False
        )

        apply_chart_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

with chart_col2:
    if {
        "risk_level",
        "school_id"
    }.issubset(filtered_df.columns):

        risk_distribution = (
            filtered_df
            .groupby("risk_level", as_index=False)["school_id"]
            .nunique()
            .rename(columns={"school_id": "school_count"})
        )

        fig = px.pie(
            risk_distribution,
            names="risk_level",
            values="school_count",
            hole=0.55,
            title="School Risk-Level Distribution",
            color="risk_level",
            color_discrete_map={
                "High": "#D65B5B",
                "Moderate": "#D88B3D",
                "Low": "#159B86"
            }
        )

        fig.update_layout(
            height=430,
            template="plotly_white",
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF"
        )

        apply_chart_theme(fig)
        st.plotly_chart(fig, use_container_width=True)


# ============================================================
# INFRASTRUCTURE ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">Infrastructure Performance</div>',
    unsafe_allow_html=True
)

infra_col1, infra_col2 = st.columns(2)

with infra_col1:
    if {
        "district",
        "infrastructure_deficit_index"
    }.issubset(filtered_df.columns):

        infrastructure_by_district = (
            filtered_df
            .groupby("district", as_index=False)[
                "infrastructure_deficit_index"
            ]
            .mean()
            .sort_values(
                "infrastructure_deficit_index",
                ascending=False
            )
        )

        fig = px.bar(
            infrastructure_by_district,
            x="district",
            y="infrastructure_deficit_index",
            title="Infrastructure Deficit Index by District",
            labels={
                "district": "District",
                "infrastructure_deficit_index":
                    "Infrastructure Deficit (%)"
            },
            color="infrastructure_deficit_index",
            color_continuous_scale=["#FCE5E5", "#D65B5B"]
        )

        fig.update_layout(
            height=430,
            template="plotly_white",
            coloraxis_showscale=False,
            xaxis_tickangle=-35
        )

        apply_chart_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

with infra_col2:
    if {
        "infrastructure_deficit_index",
        "avg_attendance_rate"
    }.issubset(filtered_df.columns):

        fig = px.scatter(
            filtered_df,
            x="infrastructure_deficit_index",
            y="avg_attendance_rate",
            size="total_enrolled_students"
            if "total_enrolled_students" in filtered_df.columns
            else None,
            color="risk_level"
            if "risk_level" in filtered_df.columns
            else None,
            hover_name="school_name",
            title="Infrastructure Deficit vs Attendance",
            labels={
                "infrastructure_deficit_index":
                    "Infrastructure Deficit Index (%)",
                "avg_attendance_rate":
                    "Average Attendance Rate (%)"
            },
            color_discrete_map={
                "High": "#D65B5B",
                "Moderate": "#D88B3D",
                "Low": "#159B86"
            }
        )

        fig.update_layout(
            height=430,
            template="plotly_white",
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF"
        )

        apply_chart_theme(fig)
        st.plotly_chart(fig, use_container_width=True)


# ============================================================
# MID-DAY MEAL ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">Mid-Day Meal Performance</div>',
    unsafe_allow_html=True
)

mdm_col1, mdm_col2 = st.columns(2)

with mdm_col1:
    if {
        "district",
        "mdm_regularity_rate"
    }.issubset(filtered_df.columns):

        mdm_by_district = (
            filtered_df
            .groupby("district", as_index=False)["mdm_regularity_rate"]
            .mean()
            .sort_values("mdm_regularity_rate", ascending=False)
        )

        fig = px.bar(
            mdm_by_district,
            x="district",
            y="mdm_regularity_rate",
            title="Mid-Day Meal Regularity by District",
            labels={
                "district": "District",
                "mdm_regularity_rate": "Regularity Rate (%)"
            },
            color="mdm_regularity_rate",
            color_continuous_scale=["#E1F4EE", "#159B86"]
        )

        fig.update_layout(
            height=430,
            template="plotly_white",
            coloraxis_showscale=False,
            xaxis_tickangle=-35
        )

        apply_chart_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

with mdm_col2:
    if {
        "mdm_regularity_rate",
        "avg_attendance_rate"
    }.issubset(filtered_df.columns):

        fig = px.scatter(
            filtered_df,
            x="mdm_regularity_rate",
            y="avg_attendance_rate",
            color="risk_level"
            if "risk_level" in filtered_df.columns
            else None,
            hover_name="school_name",
            title="Mid-Day Meal Regularity vs Attendance",
            labels={
                "mdm_regularity_rate": "MDM Regularity Rate (%)",
                "avg_attendance_rate": "Average Attendance Rate (%)"
            },
            color_discrete_map={
                "High": "#D65B5B",
                "Moderate": "#D88B3D",
                "Low": "#159B86"
            }
        )

        fig.update_layout(
            height=430,
            template="plotly_white",
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF"
        )

        apply_chart_theme(fig)
        st.plotly_chart(fig, use_container_width=True)


# ============================================================
# ACADEMIC PERFORMANCE
# ============================================================

st.markdown(
    '<div class="section-title">Academic Performance</div>',
    unsafe_allow_html=True
)

academic_col1, academic_col2 = st.columns(2)

with academic_col1:
    if {
        "district",
        "average_test_score"
    }.issubset(filtered_df.columns):

        score_by_district = (
            filtered_df
            .groupby("district", as_index=False)["average_test_score"]
            .mean()
            .sort_values("average_test_score", ascending=False)
        )

        fig = px.bar(
            score_by_district,
            x="district",
            y="average_test_score",
            title="Average Test Score by District",
            labels={
                "district": "District",
                "average_test_score": "Average Test Score"
            },
            color="average_test_score",
            color_continuous_scale="Purples"
        )

        fig.update_layout(
            height=430,
            template="plotly_white",
            coloraxis_showscale=False,
            xaxis_tickangle=-35
        )

        apply_chart_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

with academic_col2:
    if {
        "average_test_score",
        "avg_attendance_rate"
    }.issubset(filtered_df.columns):

        fig = px.scatter(
            filtered_df,
            x="avg_attendance_rate",
            y="average_test_score",
            color="risk_level"
            if "risk_level" in filtered_df.columns
            else None,
            hover_name="school_name",
            title="Attendance Rate vs Average Test Score",
            labels={
                "avg_attendance_rate": "Attendance Rate (%)",
                "average_test_score": "Average Test Score"
            },
            color_discrete_map={
                "High": "#D65B5B",
                "Moderate": "#D88B3D",
                "Low": "#159B86"
            }
        )

        fig.update_layout(
            height=430,
            template="plotly_white",
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF"
        )

        apply_chart_theme(fig)
        st.plotly_chart(fig, use_container_width=True)


# ============================================================
# HIGH-RISK SCHOOL TABLE
# ============================================================

st.markdown(
    '<div class="section-title">High-Risk Schools Requiring Attention</div>',
    unsafe_allow_html=True
)

high_risk_df = filtered_df[
    filtered_df["risk_level"]
    .astype(str)
    .str.lower()
    .str.contains("high")
].copy()

if high_risk_df.empty:
    st.success("No high-risk schools are present in the current selection.")
else:
    display_columns = [
        "school_id",
        "school_name",
        "district",
        "block",
        "avg_attendance_rate",
        "infrastructure_deficit_index",
        "mdm_regularity_rate",
        "average_test_score",
        "risk_level"
    ]

    available_display_columns = [
        column for column in display_columns
        if column in high_risk_df.columns
    ]

    high_risk_df = high_risk_df[
        available_display_columns
    ].sort_values(
        by="infrastructure_deficit_index"
        if "infrastructure_deficit_index" in high_risk_df.columns
        else available_display_columns[0],
        ascending=False
    )

    st.dataframe(
        high_risk_df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# SCHOOL PERFORMANCE TABLE
# ============================================================

st.markdown(
    '<div class="section-title">School-Level Performance</div>',
    unsafe_allow_html=True
)

school_table_columns = [
    "school_id",
    "school_name",
    "district",
    "school_type",
    "total_enrolled_students",
    "avg_attendance_rate",
    "mdm_regularity_rate",
    "infrastructure_deficit_index",
    "average_test_score",
    "risk_level"
]

available_school_columns = [
    column for column in school_table_columns
    if column in filtered_df.columns
]

st.dataframe(
    filtered_df[available_school_columns],
    use_container_width=True,
    hide_index=True
)


# ============================================================
# DOWNLOAD DATA
# ============================================================

st.markdown(
    '<div class="section-title">Export Filtered Data</div>',
    unsafe_allow_html=True
)

csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered CSV",
    data=csv_data,
    file_name="filtered_school_dashboard.csv",
    mime="text/csv"
)


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center;color:#64748b;font-size:13px;">
        Student Retention & Welfare Efficacy Tracker |
        Education and EdTech Analytics
    </div>
    """,
    unsafe_allow_html=True
)