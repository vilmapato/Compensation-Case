import pandas as pd


def calculate_monthly_accelerators(deal_data, ae_data, year, month):
    # Filter deals for the given year
    deal_data = deal_data[deal_data["Close_Date"].dt.year == year]
    ae_accelerators = []

    # Iterate through each AE
    for ae in ae_data["AE"].unique():
        # Filter deals for this AE
        ae_deals = deal_data[deal_data["AE"] == ae]
        # Initialize dictionaries to store monthly results
        monthly_attainment = {}
        monthly_new_logos = {}
        accelerator_bonus_by_month = {}

        # Iterate month by month up to the selected month
        for current_month in range(1, month + 1):
            # Filter deals up to the current month
            monthly_deals = ae_deals[ae_deals["Close_Date"].dt.month <= current_month]

            # Calculate monthly attainment
            monthly_attainment[current_month] = (
                monthly_deals["ACV"].sum()
                / ae_data.loc[ae_data["AE"] == ae, "Quota"].values[0]
            )

            # Calculate monthly new logos count
            monthly_new_logos[current_month] = monthly_deals[
                monthly_deals["Type"] == "New"
            ].shape[0]

            # Check if the accelerator is unlocked and calculate the bonus
            if (
                monthly_attainment[current_month] > 2.0
                and monthly_new_logos[current_month] >= 5
            ):
                bonus = monthly_deals["New_Logo_Comp"].sum() * 2.0  # 200% accelerator
            elif (
                monthly_attainment[current_month] > 1.5
                and monthly_new_logos[current_month] >= 4
            ):
                bonus = monthly_deals["New_Logo_Comp"].sum() * 1.0  # 100% accelerator
            elif (
                monthly_attainment[current_month] > 1.25
                and monthly_new_logos[current_month] >= 4
            ):
                bonus = monthly_deals["New_Logo_Comp"].sum() * 0.5  # 50% accelerator
            elif (
                monthly_attainment[current_month] > 1.0
                and monthly_new_logos[current_month] >= 3
            ):
                bonus = monthly_deals["New_Logo_Comp"].sum() * 0.3  # 30% accelerator
            else:
                bonus = 0

            # Pay the bonus in the following month
            payment_month = current_month + 1
            if payment_month <= 12:  # Ensure we don't exceed the year
                if payment_month not in accelerator_bonus_by_month:
                    accelerator_bonus_by_month[payment_month] = 0
                accelerator_bonus_by_month[payment_month] += bonus

        # Store the AE's accelerator bonuses
        for payment_month, bonus in accelerator_bonus_by_month.items():
            ae_accelerators.append(
                {
                    "AE": ae,
                    "Month": payment_month,
                    "Attainment": monthly_attainment.get(payment_month, 0),
                    "cumulative_new_logos": monthly_new_logos.get(payment_month, 0),
                    "Accelerator_Bonus": bonus,
                }
            )

    # Convert to DataFrame
    accelerator_df = pd.DataFrame(ae_accelerators)
    return accelerator_df
