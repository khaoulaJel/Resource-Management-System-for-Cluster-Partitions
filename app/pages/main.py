from dash import dcc, html, Input, Output, State, callback, no_update  
from flask import session
from modules.User import User
import plotly.express as px
import pandas as pd

def getLoggedUser():
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
        dcc.Interval(
            id="interval-component",
            interval=10 * 1000,  
            n_intervals=0,
        ),
    ],
)

# Callbacks
@callback(
    Output("graph-content", "figure"),
    [Input("dropdown-selection", "value"), Input("interval-component", "n_intervals")],
)
def updateGraph(value, nIntervals):
    user = getLoggedUser()
    gpuData = user.dataFetcher.getGPUData()
    cpuData = user.dataFetcher.getCPUData()

    if value is None:
        return px.pie(title="No Data Available")

    gpuDff = gpuData[gpuData["Partition"] == value].iloc[0]
    cpuDff = cpuData[cpuData["PARTITION"] == value].iloc[0]

    fig = px.pie(
        values=[cpuDff["CPUS_A"], cpuDff["CPUS_I"], cpuDff["CPUS_O"], gpuDff["Available GPU Count"]],
        title=f"Resource Distribution for {value} Partition",
        names=["Allocated CPUs", "Idle CPUs", "Other CPUs", "Available GPUs"],
        hole=0.4,
        color_discrete_sequence=["#FF7F3E", "#80C4E9", "#4335A7", "#4CAF50"],
    )
    return fig


@callback(
    Output("resource-info", "children"),
    [Input("dropdown-selection", "value"), Input("interval-component", "n_intervals")],
)
def updateResourceInfo(value, nIntervals):

    user = getLoggedUser()
    gpuData = user.dataFetcher.getGPUData()
    cpuData = user.dataFetcher.getCPUData()

    if value is None or value not in gpuData["Partition"].values:
        return "No Data Available"

    gpuDff = gpuData[gpuData["Partition"] == value].iloc[0]
    cpuDff = cpuData[cpuData["PARTITION"] == value].iloc[0]

    totalCpus = cpuDff["CPUS_T"]
    idleCpus = cpuDff["CPUS_I"]
    gpuCount = gpuDff["Available GPU Count"]
    gpuNodes = gpuDff["Available GPU Nodes"]

    return html.Div(
        [
            html.Div(f"Total CPUs: {totalCpus}", style={"fontWeight": "bold", "marginBottom": "5px"}),
            html.Div(f"Idle CPUs: {idleCpus}", style={"fontWeight": "bold", "marginBottom": "5px"}),
            html.Div(
                f"Total GPUs Available: {gpuCount}",
                style={"fontWeight": "bold", "marginBottom": "5px", "color": "#4CAF50"},
            ),
            html.Div(
                f"Available GPU Nodes: {gpuNodes}",
                style={"fontWeight": "bold", "marginBottom": "5px", "color": "#007ACC"},
            ),
        ]
    )


@callback(
    Output("user-greeting", "children"),
    Input("interval-component", "n_intervals"),
)
def updateGreeting(nIntervals):
    user = getLoggedUser()
    return f"Hello, {user.username}"


@callback(
    Input("logout-button", "n_clicks"),
    prevent_initial_call=True,
)
def handleLogout(nClicks):
    session.pop("User", None)
    session["logged_in"] = False 
