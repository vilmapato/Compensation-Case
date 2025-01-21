from dash import dcc
from dash import html
from dash.dependencies import Input, Output

def NavigationBar():
    return html.Div(
        [
            dcc.Location(id="url", refresh=False),
            dcc.Link("Overview", href="/overview", className="tab", id="tab-overview"),
            dcc.Link("AE Compensation", href="/aeCompensation", className="tab", id="tab-ae"),
            dcc.Link("Market & Deal Insights", href="/insights", className="tab", id="tab-insights"),
            dcc.Link("Quota Strategy", href="/quotaStrategy", className="tab", id="tab-quota"),
            dcc.Link("Model Overview", href="/modelOverview", className="tab", id="tab-model"),
            dcc.Link("Data Explorer", href="/dataExplorer", className="tablast", id="tab-data"),
        ],
        className="row all-tabs",
    )

def register_callbacks(app):
    @app.callback(
        [Output("tab-overview", "className"),
         Output("tab-ae", "className"),
         Output("tab-insights", "className"),
         Output("tab-quota", "className"),
         Output("tab-model", "className"),
         Output("tab-data", "className")],
        [Input("url", "pathname")]
    )
    def update_active_tab(pathname):
        return [
            "tab active" if pathname == "/overview" else "tab",
            "tab active" if pathname == "/aeCompensation" else "tab",
            "tab active" if pathname == "/insights" else "tab",
            "tab active" if pathname == "/quotaStrategy" else "tab",
            "tab active" if pathname == "/modelOverview" else "tab",
            "tablast active" if pathname == "/dataExplorer" else "tablast",
        ]
