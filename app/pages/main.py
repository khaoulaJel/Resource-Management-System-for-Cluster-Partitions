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
    loggedUser = session.get("User")
    if not loggedUser:
        raise ValueError("User session data is missing.")
    return User.from_dict(loggedUser)

dropdownVals = ["defq*", "gpu", "shortq", "longq", "visu", "special"]

layout = html.Div(
    style={
        "fontFamily": "Roboto, sans-serif",
        "backgroundColor": "#141414",
        "padding": "20px",
        "minHeight": "100vh",
        "color": "white"
    },
    children=[
        dcc.Interval(
            id="update-interval",
            interval=10 * 1000,  
            n_intervals=0
        ),
        html.Div(
            style={
                "display": "flex",
                "justifyContent": "space-between",
                "alignItems": "center",
                "marginBottom": "20px",
                "padding": "15px",
                "background": "linear-gradient(45deg, #4CAF50, #FFC107)",
                "borderRadius": "8px",
                "color": "white",
                "boxShadow": "0 4px 10px rgba(0, 0, 0, 0.2)",
            },
            children=[
                html.H2(
                    id="user-greeting",
                    style={"margin": 0, "fontSize": "22px", "fontWeight": "300"},
                ),
                html.Button(
                    "Logout",
                    id="logout-button",
                    style={
                        "padding": "10px 20px",
                        "backgroundColor": "#FF6F61",
                        "color": "white",
                        "border": "none",
                        "borderRadius": "5px",
                        "cursor": "pointer",
                        "fontSize": "16px",
                    },
                ),
            ],
        ),
        html.H1(
            children="Simlab Resource Usage",
            style={
                "textAlign": "center",
                "padding": "20px",
                "background": "linear-gradient(45deg, #3F51B5, #FF4081)",
                "borderRadius": "5px",
                "color": "white",
                "marginBottom": "20px",
            },
        ),
        html.Div(
            style={
                "margin": "20px auto",
                "width": "50%",
                "textAlign": "center",
            },
            children=[
                html.Div(
                    "Selected Partition:",
                    style={"fontWeight": "bold", "fontSize": "18px", "marginBottom": "10px", "color": "white"},
                ),
                dcc.Dropdown(
                    options=[{"label": val, "value": val} for val in dropdownVals],
                    value=dropdownVals[0],
                    id="dropdown-selection",
                    style={
                        "width": "100%",
                        "padding": "12px",
                        "borderRadius": "5px",
                        "boxShadow": "0 4px 10px rgba(0, 0, 0, 0.3)",
                        "backgroundColor": "#333",
                        "color": "black",
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
                "color": "white",
                "padding": "15px",
                "backgroundColor": "#2C2C2C",
                "borderRadius": "10px",
                "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.3)",
            },
        ),
        dcc.Graph(
            id="graph-content",
            style={
                "padding": "20px",
                "backgroundColor": "#333",
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
        Input("dropdown-selection", "value"),
        Input("update-interval", "n_intervals"),
    ],
)
def updateResourceInfo(value, n_intervals):
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
