import pandas as pd


def calculate_monthly_accelerators(deal_data, ae_data, year, month):
    # Filter deals for the given year and AE
    deal_data = deal_data[deal_data["Close_Date"].dt.year == year]
    ae_accelerators = []

    # Iterate through each AE
    for ae in ae_data["AE"].unique():
        # Filter deals for this AE
        ae_deals = deal_data[deal_data["AE"] == ae]
        cumulative_attainment = 0
        cumulative_new_logos = 0
        accelerator_bonus_by_month = {}

        # Iterate month by month up to the selected month
        for current_month in range(1, month + 1):
            # Filter deals up to the current month
            monthly_deals = ae_deals[ae_deals["Close_Date"].dt.month <= current_month]
            current_month_deals = ae_deals[
                ae_deals["Close_Date"].dt.month == current_month
            ]

            # Calculate cumulative attainment and new logo count
            cumulative_attainment = (
                monthly_deals["ACV"].sum()
                / ae_data.loc[ae_data["AE"] == ae, "Quota"].values[0]
            )
            cumulative_new_logos = monthly_deals[monthly_deals["Type"] == "New"].shape[
                0
            ]

            # Check if the accelerator is unlocked
            if cumulative_attainment > 2.0 and cumulative_new_logos >= 5:
                bonus = (
                    current_month_deals["New_Logo_Comp"].sum() * 2.0
                )  # 200% accelerator
            elif cumulative_attainment > 1.5 and cumulative_new_logos >= 4:
                bonus = (
                    current_month_deals["New_Logo_Comp"].sum() * 1.0
                )  # 100% accelerator
            elif cumulative_attainment > 1.25 and cumulative_new_logos >= 4:
                bonus = (
                    current_month_deals["New_Logo_Comp"].sum() * 0.5
                )  # 50% accelerator
            elif cumulative_attainment > 1.0 and cumulative_new_logos >= 3:
                bonus = (
                    current_month_deals["New_Logo_Comp"].sum() * 0.3
                )  # 30% accelerator
            else:
                bonus = 0

            # Pay the bonus in the following month
            payment_month = current_month + 1
            if payment_month <= 12:  # Ensure we don't exceed the year
                if payment_month not in accelerator_bonus_by_month:
                    accelerator_bonus_by_month[payment_month] = 0
                accelerator_bonus_by_month[payment_month] += bonus

        # Store the AE's accelerator bonuses
        for month, bonus in accelerator_bonus_by_month.items():
            ae_accelerators.append(
                {"AE": ae, "Month": month, "Accelerator_Bonus": bonus}
            )

    # Convert to DataFrame
    accelerator_df = pd.DataFrame(ae_accelerators)
    return accelerator_df
