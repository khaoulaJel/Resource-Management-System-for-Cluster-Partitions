from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
from DataFetch import GetData, GetGPU

app = Dash()

DropDownVals = GetData().PARTITION.unique()

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
                    DropDownVals[0] if len(DropDownVals) > 0 else None,  # Default to the first value if available
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
            id="gpu-count",
            style={
                "textAlign": "center",
                "fontSize": "20px",
                "color": "#333",
                "marginTop": "20px",
                "backgroundColor": "#F4F4F9",
                "padding": "10px",
                "borderRadius": "5px",
                "boxShadow": "0 2px 4px rgba(0, 0, 0, 0.1)"
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
            interval=10 * 1000,  # Update every 10 seconds
            n_intervals=0
        ),
        dcc.Interval(
            id='interval-component2',
            interval=10 * 1000,  # Update every 10 seconds
            n_intervals=0
        )
    ]
)


@app.callback(
    Output('graph-content', 'figure'),
    [Input('dropdown-selection', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_graph(value, n_intervals):
    df = GetData()
    if value is None or value not in df.PARTITION.values:
        return px.pie(title="No Data Available")
    
    dff = df[df.PARTITION == value].iloc[0]

    fig = px.pie(
        values=[dff['CPUS_A'], dff['CPUS_I'], dff['CPUS_O']],
        title=f"CPU Distribution for {value} Partition",
        names=['Allocated', 'Free to Use', 'Other'],
        hole=.4,
        color_discrete_sequence=['#FF7F3E', '#80C4E9', '#4335A7']
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
    Output('gpu-count', 'children'),
    [Input('dropdown-selection', 'value'),
     Input('interval-component2', 'n_intervals')]
)
def update_gpu_count(value, n_intervals):
    df = GetData()
    if value is None or value not in df.PARTITION.values:
        return "No Data Available"
    
    dff = df[df.PARTITION == value].iloc[0]
    gpu_count = GetGPU()

    s1 = f"Total Available CPUs: {dff['CPUS_I']}"
    s2 = f" | Total GPUs (Idle): {gpu_count}"

    return s1 + s2


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=True)
