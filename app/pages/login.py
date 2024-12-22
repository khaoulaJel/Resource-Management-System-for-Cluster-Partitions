from dash import dcc, html, Input, Output, State, callback  
from flask import session
from modules.Commander import verifyAuth
from modules.User import User

layout = html.Div([
    html.Div([
        html.H1("Login Page", style={
            'textAlign': 'center', 
            'fontFamily': 'Arial, sans-serif',
            'color': 'black',
            'fontSize': '3rem',
            'marginBottom': '30px'
        }),
        dcc.Input(
            id="username", 
            type="text", 
            placeholder="Email", 
            style={
                'width': '100%', 
                'padding': '12px 20px', 
                'margin': '10px 0', 
                'border': '2px solid #ccc', 
                'borderRadius': '5px', 
                'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.1)', 
                'fontSize': '1rem'
            }
        ),
        dcc.Input(
            id="password", 
            type="password", 
            placeholder="Password", 
            style={
                'width': '100%', 
                'padding': '12px 20px', 
                'margin': '10px 0', 
                'border': '2px solid #ccc', 
                'borderRadius': '5px', 
                'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.1)', 
                'fontSize': '1rem'
            }
        ),
        html.Button(
            "Login", 
            id="login-button", 
            n_clicks=0, 
            style={
                'backgroundColor': '#FF7F3E', 
                'color': 'white', 
                'border': 'none', 
                'borderRadius': '5px', 
                'padding': '14px 20px', 
                'cursor': 'pointer',
                'fontSize': '1rem',
                'width': '100%',
                'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.1)',
            }
        ),
        html.Div(
            id="login-output", 
            style={
                'marginTop': '20px', 
                'color': 'red', 
                'fontSize': '1rem', 
                'textAlign': 'center', 
                'fontWeight': 'bold'
            }
        ),
    ], style={
        'maxWidth': '400px', 
        'margin': '50px auto', 
        'padding': '30px', 
        'backgroundColor': '#ffffff', 
        'borderRadius': '10px', 
        'boxShadow': '0px 10px 20px rgba(0, 0, 0, 0.1)'
    }),

    html.Div(
        style={
            'position': 'absolute', 
            'top': '0', 
            'left': '0', 
            'width': '100%', 
            'height': '100%', 
            'background': 'linear-gradient(135deg, #78B3CE, #2A80B9)', 
            'zIndex': '-1'
        }
    )
])

@callback(
    Output("login-output", "children"),
    Input("login-button", "n_clicks"),
    State("username", "value"),
    State("password", "value"),
)
def verify_login(n_clicks, username, password):
    if n_clicks > 0:
        if username and password:  
            if verifyAuth(username, password):
                session["logged_in"] = True
                session["User"] = User(username, password).to_dict()
                return "Login successful!"
            else:
                return "Invalid credentials. Please try again."
        else:
            return "Please enter both username and password."
    return ""
