import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from dash import dcc, html, Input, Output, callback
from flask import session
from modules.User import User
import plotly.express as px
import pandas as pd

def getLoggedUser():
    """Retrieve the logged-in user from the session."""
    logged_user = session.get("User")
    if not logged_user:
        raise ValueError("User session data is missing.")
    return User.from_dict(logged_user)

dropdown_values = ["defq*", "gpu", "shortq", "longq", "visu", "special"]

# Layout definition
layout = html.Div(
    style={
        "fontFamily": "Roboto, sans-serif",
        "backgroundColor": "#2E2E2E",
        "padding": "20px",
        "minHeight": "100vh",
        "color": "#FFFFFF",
    },
    children=[
        dcc.Interval(
            id="update-interval",
            interval=10 * 1000,  # 10 seconds
            n_intervals=0
        ),
        html.Div(
            style={
                "display": "flex",
                "justifyContent": "space-between",
                "alignItems": "center",
                "marginBottom": "20px",
                "padding": "15px",
                "backgroundColor": "#D74A2A",
                "borderRadius": "8px",
                "boxShadow": "0 4px 10px rgba(0, 0, 0, 0.2)",
                "color": "#FFFFFF",
            },
            children=[
                html.H2(
                    id="user-greeting",
                    style={"margin": 0, "fontSize": "22px", "fontWeight": "400", "color": "#000000"},
                ),
                html.Button(
                    "Logout",
                    id="logout-button",
                    style={
                        "padding": "10px 20px",
                        "backgroundColor": "#D74A2A",
                        "color": "#FFFFFF",
                        "border": "none",
                        "borderRadius": "5px",
                        "cursor": "pointer",
                        "fontSize": "16px",
                        "boxShadow": "0 2px 5px rgba(0, 0, 0, 0.2)"
                    },
                ),
            ],
        ),
        html.H1(
            children="Simlab Resource Usage",
            style={
                "textAlign": "center",
                "padding": "20px",
                "marginBottom": "20px",
                "color": "#FFFFFF",
            },
        ),
        html.Div(
            style={"margin": "20px auto", "width": "50%", "textAlign": "center"},
            children=[
                html.Div(
                    "Selected Partition:",
                    style={"fontWeight": "bold", "fontSize": "18px", "marginBottom": "10px", "color": "#FFFFFF"},
                ),
                dcc.Dropdown(
                    options=[{"label": val, "value": val} for val in dropdown_values],
                    value=dropdown_values[0],
                    id="dropdown-selection",
                    style={
                        "width": "100%",
                        "padding": "12px",
                        "borderRadius": "5px",
                        "boxShadow": "0 4px 10px rgba(0, 0, 0, 0.3)",
                        "backgroundColor": "#FFFFFF",
                        "color": "black",
                        "border": "1px solid #D74A2A"
                    },
                ),
            ],
        ),
        html.Div(
            id="resource-info",
            style={
                "margin": "20px auto",
                "textAlign": "center",
                "fontSize": "18px",
                "padding": "15px",
                "backgroundColor": "#3A3A3A",
                "borderRadius": "10px",
                "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.3)",
            },
        ),
        dcc.Graph(
            id="graph-content",
            style={
                "padding": "20px",
                "backgroundColor": "#3A3A3A",
                "borderRadius": "10px",
                "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.3)",
            },
        ),
    ],
)


@callback(
    Output("graph-content", "figure"),
    [
        Input("dropdown-selection", "value"),
        Input("update-interval", "n_intervals"),
    ],
)
def updateGraph(value, n_intervals):
    user = getLoggedUser()
    cpuData = user.dataFetcher.getCPUData()

    if value is None:
        return px.pie(title="No Data Available")

    cpuDff = cpuData[cpuData["PARTITION"] == value].iloc[0]

    fig = px.pie(
        values=[cpuDff["CPUS_A"], cpuDff["CPUS_I"], cpuDff["CPUS_O"]],
        title=f"Resource Distribution for {value} Partition",
        names=["Allocated CPUs", "Idle CPUs", "Other CPUs"],
        hole=0.4,
        color_discrete_sequence=["#FF7F3E", "#80C4E9", "#4335A7", "#4CAF50"],
    )
    return fig


@callback(
    Output("resource-info", "children"),
    [
        Input("dropdown-selection", "value")
    ],
)
def updateResourceInfo(value):
    user = getLoggedUser()

    if value == "gpu":
        gpuData = user.dataFetcher.getGPUData()
        if gpuData.empty:
            return "No Data Available"

        totalGpuCount = gpuData["Available GPU Count"].sum()

        availableGpuNodes = gpuData["Available GPU Nodes"].tolist()
        availableGpuNodesStr = ", ".join(availableGpuNodes) if availableGpuNodes else "None"

        return html.Div([
            html.Div(f"Total GPUs Available: {totalGpuCount}", style={"fontWeight": "bold", "marginBottom": "5px", "color": "#4CAF50"}),
            html.Div(f"Available GPU Nodes: {availableGpuNodesStr}", style={"fontWeight": "bold", "marginBottom": "5px", "color": "#007ACC"})
        ])
    
    cpuData = user.dataFetcher.getCPUData()

    if cpuData.empty or value not in cpuData["PARTITION"].values:
        return "No Data Available"

    cpuDff = cpuData[cpuData["PARTITION"] == value].iloc[0]

    return html.Div([
        html.Div(f"Total CPUs: {cpuDff['CPUS_T']}", style={"fontWeight": "bold", "marginBottom": "5px"}),
        html.Div(f"Idle CPUs: {cpuDff['CPUS_I']}", style={"fontWeight": "bold", "marginBottom": "5px"}),
    ])






@callback(
    Output("user-greeting", "children"),
    Input("dropdown-selection", "value"),
)
def updateGreeting(value):
    user = getLoggedUser()
    return f"Hello, {' '.join(user.username.split('.'))}!"


@callback(
    Input("logout-button", "n_clicks"),
    prevent_initial_call=True,
)
def handleLogout(nClicks):
    session.pop("User", None)
    session["logged_in"] = False