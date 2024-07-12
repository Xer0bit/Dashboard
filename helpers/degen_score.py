import pandas as pd

def calculate_degen_score(data, slate_type, contest_size):
    """
    Calculate the Degen Score for each player.

    Parameters:
    - data (pd.DataFrame): DataFrame containing player data with columns for Proj., Ceiling, Own, and any other relevant metrics.
    - slate_type (str): Either 'Large' or 'Small'.
    - contest_size (int): Size of the contest, e.g., 1000, 10000, 50000.

    Returns:
    - pd.Series: A Series containing the Degen Score for each player.
    """
    
    # Check for necessary columns
    required_columns = ['Proj.', 'Ceiling', 'Own']
    for col in required_columns:
        if col not in data.columns:
            raise KeyError(f"Column '{col}' is missing from the data")

    # Define the weightings based on slate type and contest size
    weightings = {
        ('Large', 1000): (0.3, 0.7, -0.5),
        ('Large', 10000): (0.3, 0.7, -0.5),
        ('Large', 50000): (0.3, 0.7, -0.6),
        ('Small', 1000): (0.5, 0.5, -0.6),
        ('Small', 10000): (0.4, 0.6, -0.7),
        ('Small', 50000): (0.4, 0.6, -0.8),
    }
    
    weights = weightings.get((slate_type, contest_size), (0.3, 0.7, -0.5))  # Default weights if not found

    # Extract columns from data
    sum_my_proj = data['Proj.']
    ceiling = data['Ceiling']
    average_adj_own = data['Own']

    # Calculate the Degen Score
    degen_score = (weights[0] * sum_my_proj) + (weights[1] * ceiling) + (weights[2] * average_adj_own)
    
    return degen_score
