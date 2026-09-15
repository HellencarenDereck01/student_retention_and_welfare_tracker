import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from textwrap import dedent
from urllib.parse import quote
from agent import DataAgent


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

               /* ============================================================
   PREMIUM KPI CARDS — CLEAN ICON DESIGN
   ============================================================ */

.kpi-card {
    position: relative;
    min-height: 150px;
    padding: 18px 20px;
    border-radius: 17px;
    overflow: hidden;
    border: 1px solid rgba(210, 225, 225, 0.95);
    box-shadow: 0 5px 18px rgba(15, 73, 80, 0.07);
    font-family: Arial, sans-serif;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
    box-sizing: border-box;
}

.kpi-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 9px 25px rgba(15, 73, 80, 0.12);
}

.kpi-card-teal {
    background: linear-gradient(135deg, #f5fffc 0%, #e9faf6 100%);
}

.kpi-card-blue {
    background: linear-gradient(135deg, #f6fbff 0%, #eaf5ff 100%);
}

.kpi-card-red {
    background: linear-gradient(135deg, #fffafa 0%, #fff0f0 100%);
}

.kpi-card-green {
    background: linear-gradient(135deg, #f7fffb 0%, #e9faf1 100%);
}

.kpi-card-orange {
    background: linear-gradient(135deg, #fffdf7 0%, #fff5df 100%);
}

.kpi-card-purple {
    background: linear-gradient(135deg, #fcfaff 0%, #f3efff 100%);
}

.kpi-top {
    display: flex;
    align-items: center;
    gap: 13px;
    position: relative;
    z-index: 2;
    min-width: 0;
}

.kpi-icon-circle {
    width: 52px;
    height: 52px;
    min-width: 52px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    box-sizing: border-box;
}

.kpi-icon-image {
    width: 27px;
    height: 27px;
    display: block;
    object-fit: contain;
}

.kpi-title {
    font-size: 14px;
    font-weight: 800;
    color: #123f54;
    line-height: 1.28;
    overflow-wrap: anywhere;
    min-width: 0;
}

.kpi-value {
    position: relative;
    z-index: 2;
    margin-top: 11px;
    font-size: 31px;
    line-height: 1;
    font-weight: 800;
    color: #103f55;
    white-space: nowrap;
}

.kpi-description {
    position: relative;
    z-index: 2;
    margin-top: 8px;
    font-size: 12px;
    line-height: 1.35;
    color: #657d91;
    max-width: 78%;
}

.kpi-watermark {
    position: absolute;
    right: 17px;
    bottom: 14px;
    width: 50px;
    height: 50px;
    opacity: 0.13;
    z-index: 1;
    pointer-events: none;
}

.kpi-watermark-image {
    width: 100%;
    height: 100%;
    display: block;
    object-fit: contain;
}

@media (max-width: 1100px) {
    .kpi-title {
        font-size: 13px;
    }

    .kpi-icon-circle {
        width: 48px;
        height: 48px;
        min-width: 48px;
    }

    .kpi-icon-image {
        width: 25px;
        height: 25px;
    }

    .kpi-card {
        padding: 16px;
    }

    .kpi-value {
        font-size: 28px;
    }
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


        /* AI ASSISTANT POPOVER */
        [data-testid="stPopover"] {
            position: relative;
            z-index: 999999;
        }

        [data-testid="stPopover"] > button {
            border-radius: 50%;
            width: 52px;
            height: 52px;
            padding: 0;
            font-size: 25px;
            background: #123f54;
            color: white;
            border: none;
            box-shadow: 0 4px 12px rgba(0,0,0,0.18);
        }

        [data-testid="stPopover"] > button:hover {
            background: #075052;
            color: white;
        }

        [data-testid="stPopoverBody"] {
            width: 410px;
            max-width: 90vw;
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
# AI EDUCATION ASSISTANT
# ============================================================

# The AI assistant uses the FULL school dataset.
# Dashboard filters below do not change the data available to the AI.

if "ai_messages" not in st.session_state:
    st.session_state.ai_messages = []

agent = DataAgent(df)

# Small AI icon at the top-left of the main dashboard area.
with st.popover("🤖", help="Open AI Education Assistant"):

    st.markdown(
        """
        <div style="
            padding: 4px 0 10px 0;
        ">
            <div style="
                font-size:20px;
                font-weight:800;
                color:#123f54;
            ">
                AI Education Assistant
            </div>
            <div style="
                font-size:13px;
                color:#64748b;
                margin-top:4px;
            ">
                Ask questions about attendance, infrastructure,
                academic performance, or student welfare.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="
            background:#f4f8f7;
            border-radius:10px;
            padding:10px 12px;
            margin-bottom:12px;
            font-size:12px;
            color:#355b5c;
        ">
            <b>Try asking:</b><br>
            • Show attendance by district<br>
            • Show the relationship between attendance and test scores<br>
            • Compare infrastructure deficits<br>
            • Show welfare risk levels<br>
            • Give me a summary of the school dataset
        </div>
        """,
        unsafe_allow_html=True
    )

    # Display previous AI conversation
    for message in st.session_state.ai_messages:

        if message["role"] == "user":
            st.markdown(
                f"""
                <div style="
                    background:#e7f3f1;
                    border-radius:10px;
                    padding:9px 11px;
                    margin:7px 0;
                    color:#123f54;
                    font-size:13px;
                ">
                    <b>You:</b> {message["content"]}
                </div>
                """,
                unsafe_allow_html=True
            )

        else:
            st.markdown(
                f"""
                <div style="
                    background:#f7f8fa;
                    border-radius:10px;
                    padding:9px 11px;
                    margin:7px 0;
                    color:#355b5c;
                    font-size:13px;
                ">
                    <b>AI:</b> {message["content"]}
                </div>
                """,
                unsafe_allow_html=True
            )

            if message.get("figure") is not None:
                st.plotly_chart(
                    message["figure"],
                    use_container_width=True
                )

            if message.get("table") is not None:
                st.dataframe(
                    message["table"],
                    use_container_width=True,
                    hide_index=True
                )

    with st.form("ai_question_form", clear_on_submit=True):

        question = st.text_input(
            "Ask a question",
            placeholder="e.g. Show attendance by district",
            label_visibility="collapsed"
        )

        submitted = st.form_submit_button(
            "Ask AI",
            use_container_width=True
        )

    if submitted and question.strip():

        question = question.strip()

        st.session_state.ai_messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.spinner("Analyzing the full school dataset..."):

            result = agent.process_question(question)

        if result["type"] == "error":

            st.error(result["message"])

            st.session_state.ai_messages.append(
                {
                    "role": "assistant",
                    "content": result["message"]
                }
            )

        elif result["type"] == "summary":

            st.session_state.ai_messages.append(
                {
                    "role": "assistant",
                    "content": result["explanation"],
                    "table": result["result"]
                }
            )

            st.rerun()

        elif result["type"] == "chart":

            st.session_state.ai_messages.append(
                {
                    "role": "assistant",
                    "content": result["explanation"],
                    "figure": result["figure"]
                }
            )

            st.rerun()



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

def format_percent(value):
    if pd.isna(value):
        return "N/A"

    return f"{value:.1f}%"


# ------------------------------------------------------------
# KPI ICONS
# ------------------------------------------------------------

KPI_ICONS = {
    'school': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><path fill="CURRENT" d="M8 58h48v-5h-5V25l-19-14L13 25v28H8v5zm10-5V28l14-10 14 10v25H18zm6-17h7v7h-7v-7zm15 0h7v7h-7v-7zm-15 12h7v7h-7v-7zm15 0h7v7h-7v-7zM29 7h6v7h-6z"/></svg>',
    'students': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><circle fill="CURRENT" cx="23" cy="20" r="10"/><circle fill="CURRENT" cx="44" cy="22" r="8"/><path fill="CURRENT" d="M5 51c0-10 8-18 18-18s18 8 18 18H5z"/><path fill="CURRENT" d="M36 51c0-8 6-15 14-15s14 7 14 15H36z"/></svg>',
    'risk': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><path fill="CURRENT" d="M32 6 4 55h56L32 6zm0 14 15 27H17L32 20zm-4 7h8v12h-8V27zm0 16h8v6h-8v-6z"/></svg>',
    'attendance': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><circle fill="CURRENT" cx="20" cy="21" r="9"/><circle fill="CURRENT" cx="44" cy="21" r="9"/><circle fill="CURRENT" cx="32" cy="31" r="9"/><path fill="CURRENT" d="M4 52c0-9 7-16 16-16 5 0 9 2 12 6 3-4 7-6 12-6 9 0 16 7 16 16H4z"/></svg>',
    'meal': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><path fill="CURRENT" d="M14 7h5v17h-5V7zm-6 0h5v13c0 3 2 5 5 5s5-2 5-5V7h5v13c0 5-3 9-8 10v27h-5V30c-5-1-8-5-8-10V7zM43 7c9 5 13 12 13 22v28h-6V37h-7V7z"/></svg>',
    'infrastructure': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><path fill="CURRENT" d="M6 56h52v-5h-6V21l-20-14L12 21v30H6v5zm13-5V24l13-9 13 9v27H19zM25 31h6v20h-6V31zm8 0h6v20h-6V31zM15 21h34v5H15z"/></svg>',
    'score': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><path fill="CURRENT" d="M8 56h48v4H8zM12 34h10v22H12zm15-13h10v35H27zm15-11h10v46H42z"/></svg>',
}

def svg_to_data_uri(svg):
    return "data:image/svg+xml," + quote(svg, safe="")


def get_kpi_icon(icon_name, color="#123F54", watermark=False):
    svg = KPI_ICONS.get(icon_name, KPI_ICONS["score"])
    svg = svg.replace("CURRENT", color)
    src = svg_to_data_uri(svg)

    if watermark:
        return f'<img class="kpi-watermark-image" src="{src}" alt="">'

    return f'<img class="kpi-icon-image" src="{src}" alt="">'


# ------------------------------------------------------------
# KPI CARD BUILDER
# ------------------------------------------------------------

def create_kpi_card(
    title,
    value,
    description,
    icon,
    card_class,
    icon_bg,
    icon_color,
    watermark_icon=None
):
    watermark = ""

    if watermark_icon:
        watermark = f"""
        <div class="kpi-watermark">
            {get_kpi_icon(watermark_icon, icon_color, watermark=True)}
        </div>
        """

    return dedent(f"""
        <div class="kpi-card {card_class}">

            {watermark}

            <div class="kpi-top">

                <div class="kpi-icon-circle"
                     style="background:{icon_bg}; color:{icon_color};">
                    {get_kpi_icon(icon, icon_color)}
                </div>

                <div class="kpi-title">
                    {title}
                </div>

            </div>

            <div class="kpi-value">
                {value}
            </div>

            <div class="kpi-description">
                {description}
            </div>

        </div>
    """)


# ------------------------------------------------------------
# FIRST ROW — OVERVIEW
# ------------------------------------------------------------

kpi_col1, kpi_col2, kpi_col3 = st.columns(3)

with kpi_col1:
    st.html(
        create_kpi_card(
            title="Total Schools",
            value=f"{total_schools:,}",
            description="Schools in current selection",
            icon="school",
            card_class="kpi-card-teal",
            icon_bg="#d5f5ee",
            icon_color="#087d78",
            watermark_icon="school"
        )
    )

with kpi_col2:
    st.html(
        create_kpi_card(
            title="Enrolled Students",
            value=f"{total_students:,.0f}",
            description="Total enrolled students",
            icon="students",
            card_class="kpi-card-blue",
            icon_bg="#dceeff",
            icon_color="#1688d4",
            watermark_icon="students"
        )
    )

with kpi_col3:
    st.html(
        create_kpi_card(
            title="High-Risk Schools",
            value=f"{high_risk_schools:,}",
            description="Schools requiring attention",
            icon="risk",
            card_class="kpi-card-red",
            icon_bg="#ffe0e0",
            icon_color="#d94841",
            watermark_icon="score"
        )
    )


st.markdown(
    "<div style='height:14px;'></div>",
    unsafe_allow_html=True
)


# ------------------------------------------------------------
# SECOND ROW — PERFORMANCE
# ------------------------------------------------------------

kpi_col4, kpi_col5, kpi_col6, kpi_col7 = st.columns(4)

with kpi_col4:
    st.html(
        create_kpi_card(
            title="Average Attendance",
            value=format_percent(average_attendance),
            description="Average school attendance rate",
            icon="attendance",
            card_class="kpi-card-green",
            icon_bg="#d7f6e8",
            icon_color="#159b57",
            watermark_icon="score"
        )
    )

with kpi_col5:
    st.html(
        create_kpi_card(
            title="MDM Regularity",
            value=format_percent(average_mdm_regularity),
            description="Relative meal procurement regularity",
            icon="meal",
            card_class="kpi-card-orange",
            icon_bg="#ffedc9",
            icon_color="#e58a00",
            watermark_icon="meal"
        )
    )

with kpi_col6:
    st.html(
        create_kpi_card(
            title="Infrastructure Deficit",
            value=format_percent(average_deficit),
            description="Higher value means greater deficit",
            icon="infrastructure",
            card_class="kpi-card-purple",
            icon_bg="#eee5ff",
            icon_color="#7355c7",
            watermark_icon="infrastructure"
        )
    )

with kpi_col7:
    st.html(
        create_kpi_card(
            title="Average Test Score",
            value=format_percent(average_test_score),
            description="Average academic score",
            icon="score",
            card_class="kpi-card-blue",
            icon_bg="#dceeff",
            icon_color="#1785d1",
            watermark_icon="score"
        )
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
