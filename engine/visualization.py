import plotly.graph_objects as go
import plotly.express as px


# ==========================================================
# RenalTwin AI V2
# Visualization Service
# ==========================================================

def probability_gauge(probability):
    """
    Create CKD probability gauge.
    """

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=probability * 100,
            number={"suffix": "%"},
            title={"text": "CKD Probability"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "darkred"},
                "steps": [
                    {"range": [0, 20], "color": "#2ecc71"},
                    {"range": [20, 40], "color": "#f1c40f"},
                    {"range": [40, 70], "color": "#e67e22"},
                    {"range": [70, 100], "color": "#e74c3c"},
                ],
            },
        )
    )

    fig.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=50, b=20),
    )

    return fig


def shap_bar(top_features):
    """
    SHAP feature importance chart.
    """

    fig = px.bar(
        top_features,
        x="Importance",
        y="Feature",
        orientation="h",
        title="Top AI Feature Contributions",
    )

    fig.update_layout(
        height=400,
        yaxis={"categoryorder": "total ascending"},
    )

    return fig


def twin_comparison(original, simulated):
    """
    Before vs after Digital Twin.
    """

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=["Original"],
            y=[original * 100],
            name="Original",
        )
    )

    fig.add_trace(
        go.Bar(
            x=["Simulated"],
            y=[simulated * 100],
            name="Simulated",
        )
    )

    fig.update_layout(
        title="Digital Twin Simulation",
        yaxis_title="CKD Probability (%)",
        height=400,
    )

    return fig