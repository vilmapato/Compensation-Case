import pandas as pd

def calculate_compensation(deal_data, ae_data, exceptions):
    """
    Calculate compensation for Account Executives based on provided deal and AE data.

    Parameters:
    - deal_data: DataFrame containing deal information.
    - ae_data: DataFrame containing AE information (base salary, quota, etc.).
    - exceptions: List of exceptions to apply to specific deals.

    Returns:
    - ae_summary: DataFrame summarizing compensation by AE.
    """
    
    #print("ae_data columns:", ae_data.columns)
    # Rename columns
    deal_data.columns = deal_data.columns.str.replace(' ', '_')
    ae_data.columns = ae_data.columns.str.replace(' ', '_')
    ae_data.rename(columns={'Base_Salary_(Annual)': 'Base_Salary_Annual'}, inplace=True)
    deal_data.rename(columns={'Opportunity_Owner': 'AE'}, inplace=True)

    #print("deal_data columns:", deal_data.columns)
    # Clean and preprocess data
    deal_data['Close_Date'] = pd.to_datetime(deal_data['Close_Date'], errors='coerce')
    deal_data['Invoice_Date'] = pd.to_datetime(deal_data['Invoice_Date'], errors='coerce')
    deal_data['ACV'] = pd.to_numeric(deal_data['ACV'], errors='coerce')
    deal_data['Services'] = pd.to_numeric(deal_data['Services'], errors='coerce')

    ae_data['Base_Salary_Annual'] = pd.to_numeric(ae_data['Base_Salary_Annual'], errors='coerce')
    ae_data['Quota'] = pd.to_numeric(ae_data['Quota'], errors='coerce')

    # Calculate ACV Rate for each AE
    ae_data['ACV_Rate'] = ae_data['Base_Salary_Annual'] / ae_data['Quota']

    # Initialize compensation components
    deal_data['Upsell_Comp'] = 0
    deal_data['New_Logo_Comp'] = 0
    deal_data['Payment_Date'] = deal_data['Close_Date'] + pd.DateOffset(months=1)
    deal_data['Services_Comp'] = deal_data['Services'] * 0.015  # 1.5% commission on services

    # Calculate Upsell and New Logo compensations
    deal_data['Upsell_Comp'] = deal_data.apply(
        lambda x: x['ACV'] * ae_data.loc[ae_data['AE'] == x['AE'], 'ACV_Rate'].values[0]
        if x['Type'] == 'Upsell' else 0,
        axis=1
    )
    deal_data['New_Logo_Comp'] = deal_data.apply(
        lambda x: x['ACV'] * ae_data.loc[ae_data['AE'] == x['AE'], 'ACV_Rate'].values[0] * 1.1
        if x['Type'] == 'New' else 0,
        axis=1
    )

    # Apply exceptions dynamically
    for exception in exceptions:
        if exception['type'] == 'shared_opportunity':
            deal_id = exception['deal_id']
            shares = exception['shares']  # Dict of AE -> share percentage
            for ae, share in shares.items():
                if ae == deal_data.loc[deal_data['Opportunity_ID'] == deal_id, 'AE'].values[0]:
                    # Modify original AE's ACV and Services
                    deal_data.loc[deal_data['Opportunity_ID'] == deal_id, 'ACV'] *= share
                    deal_data.loc[deal_data['Opportunity_ID'] == deal_id, 'Services'] *= share
                else:
                    # Add a new row for the shared AE
                    original_row = deal_data.loc[deal_data['Opportunity_ID'] == deal_id].iloc[0].copy()
                    original_row['AE'] = ae
                    original_row['ACV'] *= share
                    original_row['Services'] *= share
                    deal_data = pd.concat([deal_data, pd.DataFrame([original_row])], ignore_index=True)

        elif exception['type'] == 'adjust_acv':
            deal_id = exception['deal_id']
            adjustment_factor = exception['adjustment_factor']
            deal_data.loc[deal_data['Opportunity_ID'] == deal_id, 'ACV'] *= adjustment_factor

        elif exception['type'] == 'close_date_payment':
            
            for _, row in deal_data.iterrows():
                if (
                    row['Opp_Global_Region'] in ['NOLA', 'SOLA'] and
                    row['Type'] == 'Upsell' and
                    pd.isna(row['Invoice_Date'])
                ):
                    # Update Invoice Date to the next month after Close Date
                    deal_data.loc[deal_data['Opportunity_ID'] == row['Opportunity_ID'], 'Payment_Date'] = row['Close_Date'] + pd.DateOffset(months=1)

    # Recalculate Services Compensation after adjustments
    deal_data['Services_Comp'] = deal_data['Services'] * 0.015

    # Combine all compensation components
    deal_data['Total_Comp'] = (
        deal_data['Upsell_Comp'] + deal_data['New_Logo_Comp'] + deal_data['Services_Comp']
    )

    # Adding the number of new logos for each AE
    new_counts = deal_data[deal_data['Type'] == 'New'].groupby('AE').size().reset_index(name='New_Count')
    ae_data = pd.merge(ae_data, new_counts, on='AE', how='left')
    

    # Adding the number of new logos ACV for each AE
    new_acv = deal_data[deal_data['Type'] == 'New'].groupby('AE')['ACV'].sum().reset_index(name='New_ACV')
    ae_data = pd.merge(ae_data, new_acv, on='AE', how='left')
    

    # Aggregate compensation by AE
    ae_compensation = deal_data.groupby('AE').agg({
        'Upsell_Comp': 'sum',
        'New_Logo_Comp': 'sum',
        'Services_Comp': 'sum',
        'Total_Comp': 'sum',
        'ACV': 'sum',
    }).reset_index()

    # Merge AE data with calculated compensation
    ae_data = pd.merge(ae_data, ae_compensation, on='AE', how='left').fillna(0)

    # Calculate OTE and attainments
    ae_data['OTE'] = ae_data['Base_Salary_Annual'] * 2
    ae_data['Attainment'] = ae_data['New_ACV'] / ae_data['Quota']
    #print("ae_data after atta:")
    #print(ae_data.head())
    
    # Calculate accelerators for new logo attainment
    def calculate_accelerators(row):
        if row['Attainment'] > 2.0 and row['New_Count'] >= 5:
            return row['New_Logo_Comp'] * 2.0  # 200% accelerator
        elif row['Attainment'] > 1.5 and row['New_Count'] >= 4:
            return row['New_Logo_Comp'] * 1.0  # 100% accelerator
        elif row['Attainment'] > 1.25 and row['New_Count'] >= 4:
            return row['New_Logo_Comp'] * 0.5  # 50% accelerator
        elif row['Attainment'] > 1.0 and row['New_Count'] >= 3:
            return row['New_Logo_Comp'] * 0.3  # 30% accelerator
        return 0

    ae_data['Accelerator_Bonus'] = ae_data.apply(calculate_accelerators, axis=1)
    
    # Update Total Compensation with Accelerator
    ae_data['Total_Comp'] += ae_data['Accelerator_Bonus']

    return deal_data, ae_data