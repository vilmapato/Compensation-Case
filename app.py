import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from pages import (
    overview,
    aeCompensation,
    insights,
    quotaStrategy,
    modelOverview,
    dataExplorer,
)
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.io as pio
from components.header import Header
from components.navigationBar import NavigationBar
from compensation_model.calculations import calculate_compensation
from pages.aeCompensation import register_callbacks
from pages.dataExplorer import register_callbacks_data_explorer

# Defining custom colors
custom_colors = [
    "rgba(13, 17, 201, 1)",
    "rgba(56, 96, 229, 1)",
    "rgba(83, 123, 225, 1)",
    "rgba(160, 192, 250, 1)",
]

# Setting the default theme for all charts
pio.templates["custom"] = pio.templates["plotly"]
pio.templates["custom"].layout.font = dict(
    family="Clear Sans, Arial, sans-serif",  # Replace "Clear Sans" with your desired font
    size=12,  # Default font size
    color="#3a3a3a",  # Default font color
)
pio.templates["custom"].layout.colorway = custom_colors
pio.templates["custom"].layout.legend = dict(
    orientation="h",  # Horizontal legend
    x=0.5,  # Center the legend
    xanchor="center",  # Anchor the legend to its center
    y=-0.2,  # Position the legend below the chart
)
pio.templates.default = "custom"

# Initialize the app
app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    suppress_callback_exceptions=True,
)
register_callbacks(app)
register_callbacks_data_explorer(app)
app.title = "Compensation Dashboard"
server = app.server

# Load raw data
deal_data = pd.read_excel(
    "./data/compensationModelTaskData.xlsx", sheet_name="Deal Data"
)
ae_data = pd.read_excel("./data/compensationModelTaskData.xlsx", sheet_name="AE Data")


# Run the compensation calculation
deal_data, ae_data = calculate_compensation(
    deal_data,
    ae_data,
    exceptions=[
        {  # here I am building the model without catching the error that the deal_id is not in the data
            "type": "shared_opportunity",
            "deal_id": "006Qo000006yD5N",
            "shares": {"NOLA-3": 0.3, "NOLA-2": 0.7},
        },
        {
            "type": "adjust_acv",
            "deal_id": "006Qo0000097tx3",
            "adjustment_factor": 0.5,
        },
        {
            "type": "close_date_payment",
        },
    ],
)

# print("deal_data after atta:")
# print(deal_data.head())
# Verify the updated Invoice_Date values
enterprise_upsells = deal_data[
    (deal_data["Market"].isin(["NOLA", "SOLA"]))
    & (deal_data["Type"] == "Upsell")
    & (deal_data["Invoice_Date"].dt.year == 2025)
]
# print(enterprise_upsells[['Opportunity_ID', 'Close_Date', 'Invoice_Date']])

# Attach data to app.server for global access
app.server.deal_data = deal_data
app.server.ae_data = ae_data
# print("deal_data columns:", deal_data.columns)
# print("ae_data columns:", ae_data.columns)
# print("deal_data after atta:")
# print(deal_data.head())

# Define the layout
app.layout = html.Div(
    className="page",
    children=[
        Header(app),
        NavigationBar(),
        dcc.Location(id="url", refresh=False),
        html.Div(id="page-content"),
        # Footer(),
    ],
)


# Callback for dynamic page rendering
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/aeCompensation":
        return aeCompensation.create_layout(app)
    elif pathname == "/insights":
        return insights.create_layout(app)
    elif pathname == "/quotaStrategy":
        return quotaStrategy.create_layout(app)
    elif pathname == "/modelOverview":
        return modelOverview.create_layout(app)
    elif pathname == "/dataExplorer":
        return dataExplorer.create_layout(app)
    else:
        # Default to overview
        return overview.create_layout(app)


if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=True)
