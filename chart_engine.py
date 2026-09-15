import pandas as pd
import plotly.express as px


def load_data(file_path):
    """
    Load a CSV dataset.
    """
    return pd.read_csv(file_path)


def summarize_data(data):
    """
    Generate a statistical summary for numeric columns.
    """
    numeric_data = data.select_dtypes(include="number")

    if numeric_data.empty:
        return pd.DataFrame(
            {"Message": ["No numeric columns were found in the dataset."]}
        )

    return numeric_data.describe().transpose()


def find_column(data, possible_names):
    """
    Find a column using several possible names or keywords.
    """
    column_names = {column.lower(): column for column in data.columns}

    # First, check for exact matches
    for name in possible_names:
        if name.lower() in column_names:
            return column_names[name.lower()]

    # Then, check whether a keyword appears in a column name
    for column in data.columns:
        column_lower = column.lower()

        for name in possible_names:
            if name.lower() in column_lower:
                return column

    return None


def create_bar_chart(data, x_column, y_column, title):
    """
    Create a bar chart.
    """
    figure = px.bar(
        data,
        x=x_column,
        y=y_column,
        title=title,
        text_auto=".2f"
    )

    figure.update_layout(
        xaxis_title=x_column.replace("_", " ").title(),
        yaxis_title=y_column.replace("_", " ").title(),
        template="plotly_dark"
    )

    return figure


def create_line_chart(data, x_column, y_column, title):
    """
    Create a line chart.
    """
    figure = px.line(
        data,
        x=x_column,
        y=y_column,
        title=title,
        markers=True
    )

    figure.update_layout(
        xaxis_title=x_column.replace("_", " ").title(),
        yaxis_title=y_column.replace("_", " ").title(),
        template="plotly_dark"
    )

    return figure


def create_scatter_chart(data, x_column, y_column, title):
    """
    Create a scatter plot.
    """
    figure = px.scatter(
        data,
        x=x_column,
        y=y_column,
        title=title,
        hover_name="school_name" if "school_name" in data.columns else None
    )

    figure.update_layout(
        xaxis_title=x_column.replace("_", " ").title(),
        yaxis_title=y_column.replace("_", " ").title(),
        template="plotly_dark"
    )

    return figure


def create_pie_chart(data, column, title):
    """
    Create a pie chart showing category proportions.
    """
    category_data = (
        data[column]
        .value_counts()
        .reset_index()
    )

    category_data.columns = [column, "count"]

    figure = px.pie(
        category_data,
        names=column,
        values="count",
        title=title
    )

    figure.update_layout(template="plotly_dark")

    return figure


def create_grouped_average_chart(data, group_column, value_column, title):
    """
    Calculate an average metric by group and display it as a bar chart.
    """
    grouped_data = (
        data.groupby(group_column, dropna=False)[value_column]
        .mean()
        .reset_index()
        .sort_values(value_column, ascending=False)
    )

    return create_bar_chart(
        grouped_data,
        group_column,
        value_column,
        title
    )


def create_risk_chart(data):
    """
    Display schools by welfare risk level.
    """
    risk_column = find_column(
        data,
        ["risk_level", "welfare_risk_level", "risk"]
    )

    if risk_column is None:
        return None

    return create_pie_chart(
        data,
        risk_column,
        "Schools by Welfare Risk Level"
    )


def create_attendance_chart(data):
    """
    Display average attendance by district.
    """
    district_column = find_column(
        data,
        ["district", "district_name"]
    )

    attendance_column = find_column(
        data,
        ["avg_attendance_rate", "average_attendance_rate", "attendance_rate"]
    )

    if district_column is None or attendance_column is None:
        return None

    return create_grouped_average_chart(
        data,
        district_column,
        attendance_column,
        "Average Attendance Rate by District"
    )


def create_infrastructure_chart(data):
    """
    Display infrastructure deficit by district.
    """
    district_column = find_column(
        data,
        ["district", "district_name"]
    )

    infrastructure_column = find_column(
        data,
        [
            "infrastructure_deficit_index",
            "infrastructure_deficit",
            "deficit_index"
        ]
    )

    if district_column is None or infrastructure_column is None:
        return None

    return create_grouped_average_chart(
        data,
        district_column,
        infrastructure_column,
        "Average Infrastructure Deficit by District"
    )


def create_attendance_test_score_chart(data):
    """
    Display the relationship between attendance and test scores.
    """
    attendance_column = find_column(
        data,
        ["avg_attendance_rate", "average_attendance_rate", "attendance_rate"]
    )

    test_score_column = find_column(
        data,
        ["average_test_score", "avg_test_score", "test_score"]
    )

    if attendance_column is None or test_score_column is None:
        return None

    return create_scatter_chart(
        data,
        attendance_column,
        test_score_column,
        "Attendance Rate vs Average Test Score"
    )
