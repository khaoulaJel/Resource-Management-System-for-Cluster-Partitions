from dash import Dash, dcc, html, Input, Output, no_update, State
from flask import session
import pages.login as login
import pages.main as main

app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server
app.title = "HPC Resource Monitor"

server.secret_key = "i]SPxf(U8<3I4GBLQNjJvNhJhjPxeFWK1Y*-dplGfV'uhVSn9J)XX=V`<!X?4A?"

app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Div(id="page-content"),
    dcc.Interval(id='interval-component1', interval=200, n_intervals=0)
])

@app.callback(
    Output("page-content", "children"),
    Output("url", "pathname"),
    Input('interval-component1', 'n_intervals'),
    Input("url", "pathname"),
    [State("page-content", "children")]
)
def display_page(n_intervals, pathname, current_layout):
    if "logged_in" in session and session["logged_in"]:
        if pathname == "/main":
            if current_layout is None:
                return main.layout, "/main"
            return no_update, no_update
        else:
            return main.layout, "/main"
    else:
        if pathname == "/login":
            return no_update, no_update
        else:
            return login.layout, "/login"


if __name__ == "__main__":
    app.run_server(debug=True)
