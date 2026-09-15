import pandas as pd
import streamlit as st

from agent import DataAgent
from chart_engine import find_column


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Agentic Graph AI",
    page_icon="🏫",
    layout="wide"
)


# --------------------------------------------------
# Custom page heading
# --------------------------------------------------

st.title("🏫 Agentic Graph AI")
st.write(
    "An intelligent school-data assistant for analyzing attendance, "
    "academic performance, infrastructure, and student welfare."
)


# --------------------------------------------------
# Load the default dataset
# --------------------------------------------------

DEFAULT_FILE = "school_dashboard.csv"

data = pd.read_csv(DEFAULT_FILE)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.header("⚙️ Data Controls")

    st.subheader("Upload another dataset")

    uploaded_file = st.file_uploader(
        "Upload a CSV file",
        type=["csv"]
    )

    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.success("Uploaded dataset loaded successfully.")

    st.divider()

    st.subheader("Dataset Information")

    st.write("Dataset records:")
    st.write(f"{len(data):,}")

    st.write("Dataset columns:")
    st.write(f"{len(data.columns):,}")

    st.divider()

    st.subheader("Filters")

    district_column = find_column(
        data,
        ["district", "district_name"]
    )

    risk_column = find_column(
        data,
        ["risk_level", "welfare_risk_level", "risk"]
    )

    selected_district = "All districts"
    selected_risk = "All risk levels"

    if district_column is not None:

        district_options = sorted(
            data[district_column]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_district = st.selectbox(
            "Select district",
            ["All districts"] + district_options
        )

    if risk_column is not None:

        risk_options = sorted(
            data[risk_column]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_risk = st.selectbox(
            "Select risk level",
            ["All risk levels"] + risk_options
        )


# --------------------------------------------------
# Apply filters
# --------------------------------------------------

filtered_data = data.copy()

if (
    district_column is not None
    and selected_district != "All districts"
):
    filtered_data = filtered_data[
        filtered_data[district_column].astype(str)
        == selected_district
    ]

if (
    risk_column is not None
    and selected_risk != "All risk levels"
):
    filtered_data = filtered_data[
        filtered_data[risk_column].astype(str)
        == selected_risk
    ]


# --------------------------------------------------
# Find important columns
# --------------------------------------------------

enrollment_column = find_column(
    filtered_data,
    [
        "total_enrolled_students",
        "total_students",
        "enrollment",
        "enrolled_students"
    ]
)

attendance_column = find_column(
    filtered_data,
    [
        "avg_attendance_rate",
        "average_attendance_rate",
        "attendance_rate"
    ]
)

test_score_column = find_column(
    filtered_data,
    [
        "average_test_score",
        "avg_test_score",
        "test_score"
    ]
)

risk_score_column = find_column(
    filtered_data,
    [
        "student_welfare_risk_score",
        "welfare_risk_score",
        "risk_score"
    ]
)


# --------------------------------------------------
# KPI calculations
# --------------------------------------------------

total_students = (
    filtered_data[enrollment_column].sum()
    if enrollment_column is not None
    else None
)

average_attendance = (
    filtered_data[attendance_column].mean()
    if attendance_column is not None
    else None
)

average_test_score = (
    filtered_data[test_score_column].mean()
    if test_score_column is not None
    else None
)

average_risk_score = (
    filtered_data[risk_score_column].mean()
    if risk_score_column is not None
    else None
)


# --------------------------------------------------
# KPI section
# --------------------------------------------------

st.subheader("📊 School Performance Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🏫 Schools",
        f"{len(filtered_data):,}"
    )

with col2:
    if total_students is not None:
        st.metric(
            "👨‍🎓 Enrolled Students",
            f"{total_students:,.0f}"
        )
    else:
        st.metric("👨‍🎓 Enrolled Students", "N/A")

with col3:
    if average_attendance is not None:
        st.metric(
            "📅 Average Attendance",
            f"{average_attendance:.2f}%"
        )
    else:
        st.metric("📅 Average Attendance", "N/A")

with col4:
    if average_test_score is not None:
        st.metric(
            "📝 Average Test Score",
            f"{average_test_score:.2f}"
        )
    elif average_risk_score is not None:
        st.metric(
            "⚠️ Average Risk Score",
            f"{average_risk_score:.2f}"
        )
    else:
        st.metric("📈 Main Metric", "N/A")


# --------------------------------------------------
# Dataset preview
# --------------------------------------------------

with st.expander("🔍 View Filtered Dataset"):

    st.write(
        f"Showing {len(filtered_data):,} records."
    )

    st.dataframe(
        filtered_data,
        use_container_width=True
    )


# --------------------------------------------------
# Suggested questions
# --------------------------------------------------

st.subheader("💬 Ask the School Data Agent")

st.write("Try one of these questions:")

st.markdown(
    """
    - Show attendance by district
    - Show the relationship between attendance and test scores
    - Compare infrastructure deficits
    - Show welfare risk levels
    - Give me a summary of the school dataset
    """
)


# --------------------------------------------------
# Chat history
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])

        if message.get("figure") is not None:
            st.plotly_chart(
                message["figure"],
                use_container_width=True
            )

        if message.get("table") is not None:
            st.dataframe(
                message["table"],
                use_container_width=True
            )


# --------------------------------------------------
# Chat input
# --------------------------------------------------

question = st.chat_input(
    "Ask something about the school dataset..."
)


# --------------------------------------------------
# Process question
# --------------------------------------------------

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.write(question)

    agent = DataAgent(filtered_data)

    with st.chat_message("assistant"):

        with st.spinner("Analyzing your question..."):

            result = agent.process_question(question)

        if result["type"] == "error":

            st.error(result["message"])

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": result["message"]
                }
            )

        else:

            st.write(result["explanation"])

            if result["type"] == "summary":

                st.dataframe(
                    result["result"],
                    use_container_width=True
                )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": result["explanation"],
                        "table": result["result"]
                    }
                )

            elif result["type"] == "chart":

                st.plotly_chart(
                    result["figure"],
                    use_container_width=True
                )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": result["explanation"],
                        "figure": result["figure"]
                    }
                )