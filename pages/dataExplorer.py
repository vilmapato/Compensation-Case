from dash import html, dash_table

def create_layout(app):
    return html.Div([
        html.H1("Data Explorer"),
        html.P("This page displays the datasets used in the model."),
        
        # Table for Deal Data
        html.H2("Deal Data"),
        dash_table.DataTable(
            id='deal-data-table',
            columns=[{"name": i, "id": i} for i in app.server.deal_data.columns],
            data=app.server.deal_data.to_dict('records'),
            page_size=10,
            style_table={'overflowX': 'auto'},
        ),
        
        # Table for AE Data
        html.H2("AE Data"),
        dash_table.DataTable(
            id='ae-data-table',
            columns=[{"name": i, "id": i} for i in app.server.ae_data.columns],
            data=app.server.ae_data.to_dict('records'),
            page_size=10,
            style_table={'overflowX': 'auto'},
        ),
    ])
