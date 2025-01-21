from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from components.card import Card


def create_summary(deal_data, ae_data, year, month=None):
    """
    Generates a global and per-AE summary of compensation metrics for a given year and optional month.

    Parameters:
    - deal_data: DataFrame containing deal information.
    - ae_data: DataFrame containing AE information.
    - year: Year to filter compensation calculations.
    - month: Optional month (1-12) to filter within the specified year.

    Returns:
    - global_summary: Dictionary containing global compensation metrics.
    - summary_by_ae: DataFrame containing compensation metrics for each AE.
    """
    
    # Ensure Payment_Date is valid (not NaN)
    deal_data = deal_data[~deal_data['Payment_Date'].isna()]

    # Add a payment_date_service column for services, retroactive by one month
    deal_data['Payment_Date_Service'] = deal_data['Close_Date'] + pd.DateOffset(months=1)
    print("deal_data columns:", deal_data.columns)
    # Filter deals and AE info based on year and optional month
    filtered_deals = deal_data[deal_data['Payment_Date'].dt.year == year]
    if month:
        filtered_deals = filtered_deals[filtered_deals['Payment_Date'].dt.month == month]

    # Filter services compensation using payment_date_service
    filtered_services = deal_data[
        (deal_data['Payment_Date_Service'].dt.year == year)
        & (month is None or deal_data['Payment_Date_Service'].dt.month == month)
    ]

    # Global Summary
    global_summary = {
        'total_upsell_comp': filtered_deals['Upsell_Comp'].sum(),
        'total_new_logo_comp': filtered_deals['New_Logo_Comp'].sum(),
        'total_services_comp': filtered_services['Services_Comp'].sum(),
        'total_accelerator_bonus': ae_data['Accelerator_Bonus'].sum(),
        'total_acv': filtered_deals['ACV'].sum(),
        'total_compensation': (
            filtered_deals['Upsell_Comp'].sum()
            + filtered_deals['New_Logo_Comp'].sum()
            + filtered_services['Services_Comp'].sum()
            + ae_data['Accelerator_Bonus'].sum()
            + (ae_data['Base_Salary_Annual'].sum() / 12 if month else ae_data['Base_Salary_Annual'].sum())
        ),
    }

    # Summary by AE
    summary_by_ae = ae_data[['AE', 'Accelerator_Bonus', 'Base_Salary_Annual']].copy()

    # Adjust accelerator bonus and base salary for monthly view
    if month:
        summary_by_ae['Accelerator_Bonus'] /= 12
        summary_by_ae['Base_Salary_Annual'] /= 12

    # Group filtered_deals by AE for variable compensation components
    variable_comp_by_ae = filtered_deals.groupby('AE').agg(
        total_upsell_comp=('Upsell_Comp', 'sum'),
        total_new_logo_comp=('New_Logo_Comp', 'sum'),
        total_services_comp=('Services_Comp', 'sum'),
        total_acv=('ACV', 'sum'),
    ).reset_index()

    # Merge variable compensation into summary_by_ae
    summary_by_ae = pd.merge(
        summary_by_ae,
        variable_comp_by_ae,
        on='AE',
        how='left'
    ).fillna(0)  # Fill missing values with 0 for AEs without deals

    # Calculate total compensation
    summary_by_ae['total_compensation'] = (
        summary_by_ae['total_upsell_comp']
        + summary_by_ae['total_new_logo_comp']
        + summary_by_ae['total_services_comp']
        + summary_by_ae['Accelerator_Bonus']
        + summary_by_ae['Base_Salary_Annual']
    )

    return global_summary, summary_by_ae

def create_layout(app):
    # Access deal_data from app.server
    # deal_data = app.server.deal_data
    # ae_data = app.server.ae_data

    # Generate the summary and grouped data
    #summary, summary_by_ae = create_summary(deal_data, ae_data, year=2024, month=0)
    #print("Global Summary:", summary)
    #print("Summary by AE:")
    #print(summary)

    # Bar Chart: Total Compensation by AE
    # bar_chart = px.bar(
    #     ae_grouped,
    #     x="AE",
    #     y="Total_Comp",
    #     title="Total Compensation by AE",
    #     labels={"Total_Comp": "Compensation ($)", "AE": "Account Executive"},
    #     color="AE",
    # )

    # # Pie Chart: Breakdown of Variable Compensation
    # pie_data = ae_grouped[['AE', 'Upsell_Comp', 'New_Logo_Comp', 'Services_Comp', 'Accelerator_Bonus']].copy()
    # pie_data = pie_data.melt(
    #     id_vars="AE",
    #     value_vars=["Upsell_Comp", "New_Logo_Comp", "Services_Comp", "Accelerator_Bonus"],
    #     var_name="Variable Component",
    #     value_name="Amount",
    # )
    # pie_chart = px.pie(
    #     pie_data,
    #     names="Variable Component",
    #     values="Amount",
    #     title="Breakdown of Variable Compensation",
    # )

    return html.Div(
        [
            html.Div(
                [
                    html.H1("", className="page-title"),
                    html.P(
                        "SOLA-3 stands out with a consistent sales strategy, closing deals in 8 out of 12 months, which indicates a steady and effective sales plan. Additionally, SOLA-3 demonstrates a diverse channel mix, with customer referrals as the primary lead source, supported by IVAs and sales investors, aligning well with overall lead source trends. ",
                        
                        className="page-description",
                    ),
                ],
                className="header-container",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Label("Select Year:"),
                            dcc.Dropdown(
                                id="year-input",
                                options=[{"label": year, "value": year} for year in range(2020, 2026)],
                                placeholder="Select Year"
                            ),
                        ],
                        className="filter-dropdown",
                    ),
                    html.Div(
                        [
                            html.Label("Select Month (Optional):"),
                            dcc.Dropdown(
                                id="month-input",
                                options=[
                                    {"label": "January", "value": 1}, {"label": "February", "value": 2},
                                    {"label": "March", "value": 3}, {"label": "April", "value": 4},
                                    {"label": "May", "value": 5}, {"label": "June", "value": 6},
                                    {"label": "July", "value": 7}, {"label": "August", "value": 8},
                                    {"label": "September", "value": 9}, {"label": "October", "value": 10},
                                    {"label": "November", "value": 11}, {"label": "December", "value": 12},
                                ],
                                placeholder="Select Month (Optional)"
                            ),
                        ],
                        className="filter-dropdown",
                    ),
                    html.Div(
                        [
                            html.Button("Download Data", id="download-ae-data-btn", className="download-ae-data-btn"),
                            dcc.Download(id="download-ae-data"),
                        ],
                        className="download-container",
                    ),
                ],
                className="filters-container",
            ),
            html.Div(
                [
                    html.Div(id="summary-container"),
                ],
                className="summary-container",
            ),
            html.Div(
                [
                    
                    #dcc.Graph(id="total-compensation-bar-chart", style={'width': '48%', 'display': 'inline-block'}),
                    dcc.Graph(id="stacked-compensation-bar-chart"),
                ],
                className="graphs-container",
            ),
            
        ],
        className="size-page-container",
    )

def register_callbacks(app):
    @app.callback(
        [
            Output("summary-container", "children"),  # Update the summary
            #Output("total-compensation-bar-chart", "figure"),  # Bar chart
            Output("stacked-compensation-bar-chart", "figure"),  # Stacked bar chart
            #Output("download-ae-data", "data"),  # Data for downloading
        ],
        [Input("year-input", "value"), Input("month-input", "value")],#, Input("download-ae-data-btn", "n_clicks")],
        prevent_initial_call=True,
    )
    def update_content(selected_year, selected_month):
        print(f"Selected Year: {selected_year}, Selected Month: {selected_month}")
        if not selected_year:
            return "Please select a year.", {}  # Default response if no year is selected

        # Access deal_data and ae_data from app.server
        deal_data = app.server.deal_data
        ae_data = app.server.ae_data

        # Generate the summary and grouped data
        global_summary, summary_by_ae = create_summary(
            deal_data, ae_data, year=selected_year, month=selected_month
        )
        #print("Global Summary:", summary)
        #print(summary_by_ae)
        #print(global_summary)
        # Prepare the summary as a list of HTML Divs
        summary_content = html.Div(
            [
                Card("Total Upsell Compensation", f"${global_summary['total_upsell_comp']:,.2f}"),
                Card("Total New Logo Compensation", f"${global_summary['total_new_logo_comp']:,.2f}"),
                Card("Total Services Compensation", f"${global_summary['total_services_comp']:,.2f}"),
                Card("Total Accelerator Bonus", f"${global_summary['total_accelerator_bonus']:,.2f}"),
                Card("Total Compensation", f"${global_summary['total_compensation']:,.2f}"),
            ],
            className="summary-metrics",
        )

        # Create the bar chart for total compensation by AE
        # figure = px.bar(
        #     summary_by_ae,
        #     x="AE",
        #     y="total_compensation",
        #     title=f"Total Compensation by AE ({selected_year}, {selected_month or 'All Months'})",
        #     labels={"total_compensation": "Compensation ($)", "AE": "Account Executive"},
        #     color="AE",
        # )
        color_mapping = {
            "total_upsell_comp": "rgba(13, 32, 190, 1)",  # Blue
            "total_new_logo_comp": "rgba(56, 96, 229, 1)",  # Light Blue
            "total_services_comp": "rgba(83, 123, 225, 1)",  # Medium Blue
            "Accelerator_Bonus": "rgba(179, 63, 246, 1)",  # purple
            "Base_Salary_Annual": "rgba(160, 192, 250, 1)",  # light blue
        }
        # Stacked Bar Chart: Breakdown of Total Compensation by Component
        stacked_bar_chart = px.bar(
            summary_by_ae.melt(
                id_vars="AE",
                value_vars=["total_upsell_comp", "total_new_logo_comp", "total_services_comp", "Accelerator_Bonus", "Base_Salary_Annual"],
                var_name="Compensation Component",
                value_name="Amount"
            ),
            x="AE",
            y="Amount",
            color="Compensation Component",
            color_discrete_map=color_mapping,
            title=f"Compensation Breakdown by Component ({selected_year}, {selected_month or 'All Months'})",
            labels={"Amount": "Compensation ($)", "AE": "Account Executive"},
            barmode="stack"
        )

        stacked_bar_chart.update_layout(
            title=dict(
                text=f"Compensation Breakdown by Component ({selected_year}, {selected_month or 'All Months'})",
                x=0.5,  # Center the title
                font=dict(size=19)
            ),
            legend=dict(
                orientation="h",  # Horizontal legend
                yanchor="bottom", y=-0.3,  # Position below the chart
                xanchor="center", x=0.5,
                title=None  # Remove the legend title
            ),
            xaxis=dict(
                title="",
                tickangle=45  # Tilt x-axis labels for better readability
            ),
            yaxis=dict(
                title="Compensation ($)"
            ),
            margin=dict(l=10, r=10, t=40, b=80),  # Adjust margins for better spacing
            height=500,  # Set the height of the chart
            autosize=True,  # Allow resizing
        )

        # Prepare data for download
        """ downloadable_data = None
        if n_clicks:
            # Combine global_summary and summary_by_ae into one downloadable dataset
            summary_by_ae_csv = summary_by_ae.copy()
            summary_by_ae_csv["total_upsell_comp"] = global_summary["total_upsell_comp"]
            summary_by_ae_csv["total_new_logo_comp"] = global_summary["total_new_logo_comp"]
            summary_by_ae_csv["total_services_comp"] = global_summary["total_services_comp"]
            summary_by_ae_csv["total_accelerator_bonus"] = global_summary["total_accelerator_bonus"]
            summary_by_ae_csv["total_acv"] = global_summary["total_acv"]
            summary_by_ae_csv["total_compensation"] = global_summary["total_compensation"]

            # Return downloadable data
            return summary_content, stacked_bar_chart, dcc.send_data_frame(summary_by_ae_csv.to_csv, "ae_compensation_summary.csv" """

        return summary_content, stacked_bar_chart#, downloadable_data
        