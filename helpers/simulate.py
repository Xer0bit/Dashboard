import pandas as pd
from helpers.degen_score import calculate_degen_score

def simulate_draftkings(data, num_simulations, slate_type, contest_size):
    results = []
    salary_cap = 50000
    positions = ['SP', 'SP', 'C', '1B', '2B', '3B', 'SS', 'OF', 'OF', 'OF']
    
    for _ in range(num_simulations):
        simulation = []
        for pos in positions:
            pos_data = data[data['Pos'] == pos]
            if not pos_data.empty:
                selected_player = pos_data.sample(1)
                simulation.append(selected_player)
        
        simulation_df = pd.concat(simulation)
        if simulation_df['Salary'].sum() <= salary_cap:
            # Ensure necessary columns are present
            simulation_df['sum_my_proj'] = simulation_df['Salary']  # Example calculation, replace with actual logic
            simulation_df['ceiling'] = simulation_df['Salary'] * 1.1  # Example calculation, replace with actual logic
            simulation_df['average_adj_own'] = simulation_df['Own']  # Example calculation, replace with actual logic

            simulation_df['Optimal'] = calculate_degen_score(simulation_df, slate_type, contest_size)
            results.append(simulation_df)
    
    return pd.concat(results).reset_index(drop=True)

def simulate_fanduel(data, num_simulations, slate_type, contest_size):
    results = []
    salary_cap = 35000
    positions = ['SP', 'C/1B', '2B', '3B', 'SS', 'OF', 'OF', 'OF', 'UTIL']
    
    for _ in range(num_simulations):
        simulation = []
        for pos in positions:
            pos_data = data[data['Pos'] == pos]
            if not pos_data.empty:
                selected_player = pos_data.sample(1)
                simulation.append(selected_player)
        
        simulation_df = pd.concat(simulation)
        if simulation_df['Salary'].sum() <= salary_cap:
            # Ensure necessary columns are present
            simulation_df['sum_my_proj'] = simulation_df['Salary']  # Example calculation, replace with actual logic
            simulation_df['ceiling'] = simulation_df['Salary'] * 1.1  # Example calculation, replace with actual logic
            simulation_df['average_adj_own'] = simulation_df['Proj_Own']  # Example calculation, replace with actual logic

            simulation_df['Optimal'] = calculate_degen_score(simulation_df, slate_type, contest_size)
            results.append(simulation_df)
    
    return pd.concat(results).reset_index(drop=True)
