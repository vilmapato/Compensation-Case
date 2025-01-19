from dash import html, dcc
import plotly.express as px
from components.card import Card

def create_summary(deal_data):
    """
    Generate a summary dictionary with metrics derived from the deal_data dataset.
    """
    # Total metrics
    total_acv = deal_data['ACV'].sum()
    total_services = deal_data['Services'].sum()

    # Count metrics
    new_logos_count = len(deal_data[deal_data['Type'] == 'New'])-1
    upsells_count = len(deal_data[deal_data['Type'] == 'Upsell'])

    # Group data by AE to find the top AE
    ae_grouped = deal_data.groupby('AE')['Total_Comp'].sum().reset_index()
    top_ae_row = ae_grouped.loc[ae_grouped['Total_Comp'].idxmax()]
    top_ae = top_ae_row['AE']

    # Group data by Market to find the top performing market
    market_grouped = deal_data.groupby('Market')['ACV'].sum()
    top_market = market_grouped.idxmax()

    # Find the most successful lead source
    most_successful_lead_source = deal_data['Lead_Source'].value_counts().idxmax()

    # Create a summary dictionary
    summary = {
        'total_acv': total_acv,
        'total_services': total_services,
        'new_logos_count': new_logos_count,
        'upsells_count': upsells_count,
        'top_ae': top_ae,
        'top_market': top_market,
        'most_successful_lead_source': most_successful_lead_source,
    }

    return summary

def create_layout(app):
    # Access deal_data from app.server
    deal_data = app.server.deal_data

    # Generate the summary
    summary = create_summary(deal_data)

    # Add a 'Month' column for time-based aggregation
    deal_data['Month'] = deal_data['Close_Date'].dt.to_period('M').astype(str)

    # Line Chart: Monthly Trends
    monthly_trends = deal_data.groupby('Month')[['ACV', 'Services']].sum().reset_index()
    line_chart = px.line(
        monthly_trends,
        x='Month',
        y=['ACV', 'Services'],
        title="Monthly Trends of Revenue",
        labels={'value': 'Revenue ($)', 'variable': 'Type'},
        markers=True,
    )

    # Apply layout updates
    line_chart.update_layout(
        title=dict(
            text="Monthly Trends of Revenue",
            x=0.5,  # Center the title
            font=dict(size=18)
        ),
        legend=dict(
            title_text=None,  # Remove legend title
            orientation="h",  # Horizontal legend
            yanchor="bottom", y=-0.2,  # Position below the chart
            xanchor="center", x=0.5
        ),
        margin=dict(l=5, r=10, t=40, b=40),  # Adjust margins for full use of space
        yaxis_title="Revenue ($)",  # Update y-axis title
        xaxis_title="Month",  # Update x-axis title
        autosize=True,  # Allow resizing
          # Set the height of the chart
    )
  

    # Bar Chart: Revenue by Type
    revenue_by_type = deal_data.groupby('Type')[['ACV', 'Services']].sum().reset_index()
    revenue_by_type['Total_Revenue'] = revenue_by_type['ACV'] + revenue_by_type['Services']
    bar_chart = px.bar(
        revenue_by_type,
        x='Type',
        y='Total_Revenue',
        title="Revenue Breakdown by Deal Type",
        labels={'Total_Revenue': '($)', 'Type': 'Deal Type'},
        color='Type',
    )

    # Apply layout updates
    bar_chart.update_layout(
        title=dict(
            text="Revenue Breakdown by Deal Type",
            x=0.5,  # Center the title
            font=dict(size=19)
        ),
        showlegend=False,  # Hide the legend
        margin=dict(l=5, r=10, t=40, b=40),
        yaxis_title="Revenue ($)",  # Update y-axis title
        xaxis_title="Deal Type",  # Update x-axis title
        autosize=True,  # Allow resizing
        bargap=0.1,  # Adjust bar spacing
        height=435,  # Set the height of the chart
        width=350,  # Set the width of the chart
    )
    # Heatmap: Market Performance
    market_performance = deal_data.groupby(['Market', 'Type'])['ACV'].sum().reset_index()
    heatmap = px.density_heatmap(
        market_performance,
        x='Market',
        y='Type',
        z='ACV',
        title="Market Performance Heatmap",
        labels={'Market': 'Market', 'Type': 'Deal Type', 'ACV': 'Revenue ($)'},
        color_continuous_scale=['rgba(13, 17, 201, 1)', 'rgba(56, 96, 229, 1)', 'rgba(83, 123, 225, 1)', 'rgba(160, 192, 250, 1)'],
    )

    heatmap.update_layout(
        title=dict(
            text="Market Performance Heatmap",
            x=0.5,  # Center the title
            font=dict(size=19)
        ),
        legend=dict(
            yanchor="middle",
            y=0.5,  # Position legend vertically aligned in the middle
            xanchor="left",
            x=1.02,  # Move legend to the right of the plot
            title=dict(text="")  # Remove the legend title
        ),
        margin=dict(l=5, r=10, t=40, b=10),  # Adjust margins
        xaxis=dict(title="Deal Type"),  # Properly set x-axis title
        yaxis=dict(title="Revenue ($)"),  # Properly set y-axis title
        autosize=True,  # Allow resizing
        height=425,  # Set the height of the chart
        coloraxis_colorbar=dict(
            title="Revenue ($)",  # Custom title for the color bar
            tickprefix="$",  # Prefix for color bar ticks
            thickness=15,  # Thickness of the color bar
            lenmode="fraction",
            len=0.6  # Fraction of the height
        )
    )


    # Funnel Chart: Lead Source Conversion
    lead_source_conversion = deal_data['Lead_Source'].value_counts().reset_index()
    lead_source_conversion.columns = ['Lead Source', 'Count']
    funnel_chart = px.funnel(
        lead_source_conversion,
        x='Count',
        y='Lead Source',
        title="Lead Source Conversion Funnel",
        labels={'Count': 'Number of Deals', 'Lead Source': 'Source'},
    )
    funnel_chart.update_layout(
        title=dict(
            text="Lead Source Conversion Funnel",
            x=0.5,  # Center the title
            font=dict(size=19)  # Adjust title font size
        ),
        margin=dict(
            l=10,  # Left margin
            r=10,  # Right margin
            t=50,  # Top margin
            b=10   # Bottom margin
        ),
        height=400,  # Adjust the height to fill space
        width=350,  # Adjust the width to fill space
        autosize=True,  # Allow resizing for better responsiveness
        xaxis=dict(
            title="",  # Remove x-axis title
            showticklabels=False  # Hide x-axis labels
        ),
        yaxis=dict(
            title="Source",  # Keep y-axis title
            automargin=True,  # Adjust margins automatically
        ),
        showlegend=False,  # Hide the legend for a cleaner look
    )

    return html.Div(
        [
            html.Div(
                [
                    html.H1("Summary", className="page-title"),
                    html.P(
                        "The data reveals that NOLA and SOLA regions lead in deal value and opportunity closures, driven primarily by Enterprise Upsells, which dominate the compensation structure. Customer referrals is the most productive lead source, contributing significantly to high-value deals, while cold calls show lower conversion rates. New Logo Deals yield higher ACV per deal but occur less frequently, emphasizing the need for focused acquisition strategies. Top-performing AEs exceed quotas by over 150%, benefiting from substantial accelerator bonuses, highlighting the importance of aligning incentives with high productivity. Balancing quota allocations among regions and lead sources can optimize overall performance and target attainment.",
                        className="page-description",
                    ),
                ],
                className="header-container",
            ),
            html.Div(
                [
                    Card("General Performance",
                    [
                        html.Div(f"Total ACV Revenue: ${summary['total_acv']:,.2f}"),
                    ]),
                    Card("AE Performance",
                    [
                        html.Div(f"Top-Performing AE: {summary['top_ae']}"),
                        html.Div(f"New Logos Closed: {summary['new_logos_count']}"),
                    
                    ]),
                    Card("Regional Insights",
                    [
                        html.Div(f"Top Performing Market: {summary['top_market']}"),
                    ]),
                    Card("Lead Source Highlights",
                    [
                        html.Div(f"Most Successful Lead Source: {summary['most_successful_lead_source']}"),
                    ]),

                    # html.Div(f"Total ACV Revenue: ${summary['total_acv']:,.2f}"),
                    # html.Div(f"Total Services Revenue: ${summary['total_services']:,.2f}"),
                    
                    
                    
                ],
                className="cards-container",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            dcc.Graph(figure=line_chart),
                        ],
                        className="line-chart-box",
                    ),
                    html.Div(
                        [               
                            dcc.Graph(figure=bar_chart),   
                        ],
                        className="bar-chart-box",),
                ],
                className="graphs-container",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            dcc.Graph(figure=heatmap),
                        ],
                        className="heatmap-box",
                    ),
                    html.Div(
                        [               
                            dcc.Graph(figure=funnel_chart),   
                        ],
                        className="funnel-box",),
                    
                ],
                className="graphs-container",
            ),
        ],
        className="size-page-container",
    )
