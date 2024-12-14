from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from DataFetch import GetData  # Retain CPU data fetching functionality

# Load GPU availability data from CSV
def load_gpu_data():
    try:
        df = pd.read_csv("C:\\Users\\ZBooK\\Desktop\\Resource-Management-System-for-Cluster-Partitions\\app\\gpu_availability.csv")

        df["Available GPU Nodes"] = df["Available GPU Nodes"].fillna("")
        return df
    except Exception as e:
        print(f"Error loading GPU data: {e}")
        return pd.DataFrame(columns=["Partition", "Available GPU Nodes", "Available GPU Count"])

# Initialize Dash app
app = Dash()

# Load GPU and CPU data
gpu_data = load_gpu_data()
cpu_data = GetData()

# Dropdown values based on partitions
DropDownVals = gpu_data["Partition"].unique()

app.layout = html.Div(
    style={
        "fontFamily": "Palatino, serif",
        "backgroundColor": "#FBF8EF",
        "padding": "20px"
    },
    children=[
        html.H1(
            children='Simlab Resource Usage',
            style={
                'textAlign': 'center',
                'padding': '10px',
                'backgroundColor': '#78B3CE',
                'borderRadius': '3px',
                'color': 'white'
            }
        ),
        html.Div(
            style={
                "margin": "20px auto",
                "width": "50%",
                "textAlign": "center"
            },
            children=[
                html.Label("Select Partition:", style={"fontWeight": "bold", "fontSize": "16px", "marginBottom": "10px"}),
                dcc.Dropdown(
                    DropDownVals,
                    DropDownVals[0] if len(DropDownVals) > 0 else None, 
                    id='dropdown-selection',
                    style={
                        "width": "100%",
                        "padding": "10px",
                        "borderRadius": "3px",
                        "boxShadow": "0 2px 4px rgba(0, 0, 0, 0.2)"
                    }
                ),
            ]
        ),
        html.Div(
            id="resource-info",
            style={
                "margin": "20px auto",
                "textAlign": "center",
                "fontSize": "18px",
                "color": "#333",
                "padding": "10px",
                "backgroundColor": "#FFFFFF",
                "borderRadius": "8px",
                "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)"
            },
        ),
        dcc.Graph(
            id='graph-content',
            style={
                "padding": "10px",
                "backgroundColor": "white",
                "borderRadius": "8px",
                "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)"
            }
        ),
        dcc.Interval(
            id='interval-component',
            interval=10 * 1000, 
            n_intervals=0
        ),
    ]
)


@app.callback(
    Output('graph-content', 'figure'),
    [Input('dropdown-selection', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_graph(value, n_intervals):
    # Reload CPU and GPU data
    gpu_df = load_gpu_data()
    cpu_df = GetData()

    if value is None or value not in gpu_df["Partition"].values:
        return px.pie(title="No Data Available")

    # Get GPU and CPU data for the selected partition
    gpu_dff = gpu_df[gpu_df["Partition"] == value].iloc[0]
    cpu_dff = cpu_df[cpu_df["PARTITION"] == value].iloc[0]

    # Create pie chart combining CPU and GPU information
    fig = px.pie(
        values=[
            cpu_dff["CPUS_A"],  # Allocated CPUs
            cpu_dff["CPUS_I"],  # Idle CPUs
            cpu_dff["CPUS_O"],  # Other CPUs
            gpu_dff["Available GPU Count"]  # GPUs Available
        ],
        title=f"Resource Distribution for {value} Partition",
        names=['Allocated CPUs', 'Idle CPUs', 'Other CPUs', 'Available GPUs'],
        hole=.4,
        color_discrete_sequence=['#FF7F3E', '#80C4E9', '#4335A7', '#4CAF50']
    )
    fig.update_layout(
        title=dict(font=dict(size=20), x=0.5, xanchor='center'),
        font=dict(size=14),
        legend=dict(
            title="Resources",
            orientation="h",
            x=0.5,
            xanchor="center",
            y=-0.2
        ),
        paper_bgcolor="#f4f4f9"
    )
    return fig

@app.callback(
    Output('resource-info', 'children'),
    [Input('dropdown-selection', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_resource_info(value, n_intervals):
    gpu_df = load_gpu_data()
    cpu_df = GetData()

    if value is None or value not in gpu_df["Partition"].values:
        return "No Data Available"

    # Get GPU and CPU data for the selected partition
    gpu_dff = gpu_df[gpu_df["Partition"] == value].iloc[0]
    cpu_dff = cpu_df[cpu_df["PARTITION"] == value].iloc[0]

    # Display CPU and GPU availability
    total_cpus = cpu_dff['CPUS_T']
    idle_cpus = cpu_dff['CPUS_I']
    gpu_count = gpu_dff["Available GPU Count"]
    gpu_nodes = gpu_dff["Available GPU Nodes"]

    # Return formatted info
    return html.Div([
        html.Div(
            f"Total CPUs: {total_cpus}",
            style={"fontWeight": "bold", "marginBottom": "5px"}
        ),
        html.Div(
            f"Idle CPUs: {idle_cpus}",
            style={"fontWeight": "bold", "marginBottom": "5px"}
        ),
        html.Div(
            f"Total GPUs Available: {gpu_count}",
            style={"fontWeight": "bold", "marginBottom": "5px", "color": "#4CAF50"}
        ),
        html.Div(
            f"Available GPU Nodes: {gpu_nodes}",
            style={"fontWeight": "bold", "marginBottom": "5px", "color": "#007ACC"}
        ),
    ])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=True)
