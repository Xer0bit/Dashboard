import pandas as pd

def calculate_degen_score(data):
    """
    Calculate the Degen Score for each player.

    Parameters:
    - data (pd.DataFrame): DataFrame containing player data with columns for Salary, Proj_Own, Optimal, and any other relevant metrics.

    Returns:
    - pd.Series: A Series containing the Degen Score for each player.
    """
    # Example calculation for Degen Score. Adjust the formula based on actual criteria.
    degen_score = (data['Salary'] * 0.5) + (data['Own'] * 0.3) + (data['Optimal'] * 0.2)
    return degen_score

# Usage within the simulation functions:
# simulation_df['Degen_Score'] = calculate_degen_score(simulation_df)
