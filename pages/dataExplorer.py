from dash import html, dash_table, dcc, Input, Output, callback, State
import plotly.express as px
import pandas as pd


def create_layout(app):
    return html.Div(
        [
            html.Div(
                [
                    html.P(
                        "This page displays the datasets used in the model and allows you to download the data.",
                        className="page-description",
                    ),
                ],
                className="header-container",
            ),
            html.Div(
                [
                    dcc.Input(id="input-1-state", type="text", value="Montréal"),
                    dcc.Input(id="input-2-state", type="text", value="Canada"),
                    html.Button(
                        id="submit-button-state", n_clicks=0, children="Submit"
                    ),
                    html.Div(id="output-state"),
                ],
            ),
            # Table for Deal Data
            html.H2("Deal Data"),
            dash_table.DataTable(
                id="deal-data-table",
                columns=[{"name": i, "id": i} for i in app.server.deal_data.columns],
                data=app.server.deal_data.to_dict("records"),
                page_size=10,
                style_table={"overflowX": "auto"},
            ),
            # Table for AE Data
            html.H2("AE Data"),
            dash_table.DataTable(
                id="ae-data-table",
                columns=[{"name": i, "id": i} for i in app.server.ae_data.columns],
                data=app.server.ae_data.to_dict("records"),
                page_size=10,
                style_table={"overflowX": "auto"},
            ),
        ]
    )


@callback(
    Output("output-state", "children"),
    Input("submit-button-state", "n_clicks"),
    State("input-1-state", "value"),
    State("input-2-state", "value"),
)
def update_output(n_clicks, deal_data, ae_data):

    return f"""
        The Button has been pressed {n_clicks} times,
        """
