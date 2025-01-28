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
                    html.Button(
                        id="submit-button-state", n_clicks=0, children="Download Data"
                    ),
                    dcc.Download(id="download-dataframe"),
                ],
                className="download-container-de",
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


def register_callbacks_data_explorer(app):

    @app.callback(
        Output("download-dataframe", "data"),
        Input("submit-button-state", "n_clicks"),
        prevent_initial_call=True,
    )
    def update_output_button(n_clicks):

        # Access deal_data and ae_data from app.server
        deal_data = app.server.deal_data
        ae_data = app.server.ae_data

        return dcc.send_data_frame(deal_data.to_csv, "deal_data.csv")
