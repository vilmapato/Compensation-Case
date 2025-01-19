from dash import html

def create_layout(app):
    return html.Div([
        html.H1("Model Overview and Calculations"),
        html.P("This page explains details of the model and calculations."),
    ])
