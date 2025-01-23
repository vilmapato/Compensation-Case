from dash import html, dash_table, dcc, Input, Output, callback


def create_layout(app):
    return html.Div(
        [
            html.Div(
                [
                    html.P(
                        "This page displays the datasets used in the model and allows you to download the data. is is a test3",
                        className="page-description",
                    ),
                ],
                className="header-container",
            ),
            html.Div(
                [
                    dcc.Input(id="input-1", type="text", value="pato"),
                    dcc.Input(id="input-2", type="text", value="Canada"),
                    html.Div(id="number-output"),
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
    Output("number-output", "children"),
    Input("input-1", "value"),
    Input("input-2", "value"),
)
def update_output(input1, input2):
    return f'Input 1 is "{input1}" and Input 2 is "{input2}"'
