from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

df = pd.read_csv('sinfo_output.csv')

app = Dash()

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
                'color': '#fffff',
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
                html.Label("Select Partition:", style={"fontWeight": "bold", "fontSize": "16px", "marginDown": "10px"}),
                dcc.Dropdown(
                    df.PARTITION.unique(),
                    'defq*',
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
        dcc.Graph(
            id='graph-content',
            style={
                "padding": "10px",
                "backgroundColor": "white",
                "borderRadius": "8px",
                "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)"
            }
        )
    ]
)

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=True)
