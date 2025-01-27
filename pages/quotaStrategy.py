from dash import html


def create_layout(app):
    return html.Div(
        [
            html.H1("Quota Strategy"),
            html.P("This page presents quota distribution and recommendations."),
        ],
        className="header-container",
    )
