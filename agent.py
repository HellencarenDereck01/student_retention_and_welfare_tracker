from chart_engine import (
    summarize_data,
    find_column,
    create_attendance_chart,
    create_infrastructure_chart,
    create_attendance_test_score_chart,
    create_risk_chart
)


class DataAgent:
    """
    Agent for interpreting questions about the school dataset.
    """

    def __init__(self, data):
        self.data = data

    def understand_question(self, question):
        """
        Identify the user's intended analysis.
        """

        question = question.lower()

        if any(word in question for word in [
            "summary",
            "summarize",
            "overview",
            "statistics",
            "describe"
        ]):
            return "summary"

        if any(word in question for word in [
            "risk",
            "welfare",
            "vulnerable",
            "high-risk",
            "high risk"
        ]):
            return "risk"

        if (
            "attendance" in question
            and (
                "test score" in question
                or "test scores" in question
                or "academic" in question
                or "relationship" in question
            )
        ):
            return "attendance_test_score"

        if any(word in question for word in [
            "attendance",
            "absenteeism",
            "present"
        ]):
            return "attendance"

        if any(word in question for word in [
            "infrastructure",
            "facility",
            "facilities",
            "deficit"
        ]):
            return "infrastructure"

        return "summary"

    def generate_explanation(self, action, result_data=None):
        """
        Generate a short explanation for the selected analysis.
        """

        if action == "attendance":
            return (
                "This chart compares the average attendance rate "
                "across districts."
            )

        if action == "infrastructure":
            return (
                "This chart compares the average infrastructure "
                "deficit across districts."
            )

        if action == "attendance_test_score":
            return (
                "This scatter plot shows the relationship between "
                "attendance rates and average test scores."
            )

        if action == "risk":
            return (
                "This chart shows how schools are distributed across "
                "the available welfare-risk categories."
            )

        if action == "summary":
            return (
                "This table provides a statistical summary of the "
                "numeric fields in the school dataset."
            )

        return "The analysis has been completed."

    def process_question(self, question):
        """
        Process the user's question.
        """

        action = self.understand_question(question)

        if action == "summary":
            summary = summarize_data(self.data)

            return {
                "type": "summary",
                "result": summary,
                "explanation": self.generate_explanation(action)
            }

        if action == "attendance":
            chart = create_attendance_chart(self.data)

            if chart is None:
                return {
                    "type": "error",
                    "message": "Attendance or district columns were not found."
                }

            return {
                "type": "chart",
                "chart_type": "bar",
                "figure": chart,
                "explanation": self.generate_explanation(action)
            }

        if action == "infrastructure":
            chart = create_infrastructure_chart(self.data)

            if chart is None:
                return {
                    "type": "error",
                    "message": "Infrastructure or district columns were not found."
                }

            return {
                "type": "chart",
                "chart_type": "bar",
                "figure": chart,
                "explanation": self.generate_explanation(action)
            }

        if action == "attendance_test_score":
            chart = create_attendance_test_score_chart(self.data)

            if chart is None:
                return {
                    "type": "error",
                    "message": (
                        "Attendance and test-score columns were not found."
                    )
                }

            return {
                "type": "chart",
                "chart_type": "scatter",
                "figure": chart,
                "explanation": self.generate_explanation(action)
            }

        if action == "risk":
            chart = create_risk_chart(self.data)

            if chart is None:
                return {
                    "type": "error",
                    "message": "A risk-level column was not found."
                }

            return {
                "type": "chart",
                "chart_type": "pie",
                "figure": chart,
                "explanation": self.generate_explanation(action)
            }

        return {
            "type": "error",
            "message": "I could not understand that question."
        }