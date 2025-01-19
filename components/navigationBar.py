from dash import dcc
from dash import html

def NavigationBar():
    return html.Div(
        [
            dcc.Link(
                "Overview",
                href="/overview",
                className="tab first",
            ),
            dcc.Link(
                "AE Compensation",
                href="/aeCompensation",
                className="tab",
            ),
            dcc.Link(
                "Market & Deal Insights",
                href="/insights",
                className="tab",
            ),
            dcc.Link(
                "Quota Strategy",
                href="/quotaStrategy",
                className="tab",
            ),
            dcc.Link(
                "Model Overview",
                href="/modelOverview",
                className="tab",
            ),
            dcc.Link(
                "Data Explorer",
                href="/dataExplorer",
                className="tablast",
            ),
        ],
        className="row all-tabs",
    )
