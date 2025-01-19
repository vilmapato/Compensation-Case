from dash import html
from dash import dcc

def Header(app):
    return html.Div([
        html.Div(
            [
                html.A(
                    html.Div(  
                        className="logo",
                    ),
                    href="https://plotly.com/dash",
                ),
                html.Div(
                    [html.H5("Compensation Case Simetrik"), 
                    ],
                    className="main-title",
                ),
                
            ],
            className="row",
        ),
        html.Div(className="greyline"),  # Horizontal line below the header
    ])
