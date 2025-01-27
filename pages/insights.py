from dash import html


def create_layout(app):
    return html.Div(
        [
            html.H1("Market & Deal Insights"),
            html.P("This page highlights trends in deals and markets."),
        ],
        className="header-container",
    )
