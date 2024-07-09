import pandas as pd

def simulate_draftkings(data, num_simulations):
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
            results.append(simulation_df)
    
    return pd.concat(results).reset_index(drop=True)

def simulate_fanduel(data, num_simulations):
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
            results.append(simulation_df)
    
    return pd.concat(results).reset_index(drop=True)
