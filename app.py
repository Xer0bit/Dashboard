import streamlit as st
import pandas as pd
from helpers.load_data import load_data
from helpers.simulate import simulate_draftkings, simulate_fanduel
from helpers.color_scale import color_scale
from helpers.degen_score import calculate_degen_score  # Import the Degen Score function

# UI Components
st.set_page_config(page_title="Contest Simulation", layout="wide")

st.title("Contest Sims")

# Load and Reset Data
with st.sidebar:
    st.header("Load/Reset Data")
    uploaded_file = st.file_uploader("Choose a file", type="csv")
    if uploaded_file:
        data = load_data(uploaded_file)
        st.success("File loaded successfully!")
        st.write("Column names in the dataset:", data.columns.tolist())
    else:
        data = None
    
    if st.button("Reset Data"):
        data = None

# Main UI
if data is not None:
    st.header("Run Contest Sim")
    st.write("Simulating contest on frames")
    
    if st.button("Reset Sim"):
        st.write("Simulation reset.")
    
    # Data Options
    slate_type = st.radio("Which data are you loading?", ["Large Slate", "Small Slate"], index=0).split()[0]
    
    # Site Options
    site = st.radio("What site are you working with?", ["DraftKings", "FanDuel"], index=0)
    
    # Contest Size
    contest_size = st.selectbox("What contest size are you simulating?", ["100-1k", "1k-10k", "10k-50k"])
    contest_size_map = {
        "100-1k": 1000,
        "1k-10k": 10000,
        "10k-50k": 50000
    }
    contest_size_value = contest_size_map[contest_size]
    
    # Field Sharpness
    field_sharpness = st.selectbox("How sharp is the field in the contest?", ["Very", "Moderate", "Not Sharp"])
    
    # Player Selection
    player_selection = st.radio("Are you wanting to isolate any lineups with specific players?", ["Full Players", "Specific Players"], index=0)
    
    # Number of Simulations
    num_simulations = st.number_input("Number of simulations to run", min_value=1, max_value=1000, value=1, step=1)
    
    if st.button("Run Contest Sim"):
        if 'Pos' not in data.columns or 'Salary' not in data.columns:
            st.error("The dataset must contain 'Pos' and 'Salary' columns.")
        else:
            # Calculate Degen Score
            data['Degen_Score'] = calculate_degen_score(data, slate_type, contest_size_value)
            
            # Simulate data for different tabs
            if site == "DraftKings":
                results = simulate_draftkings(data, num_simulations, slate_type, contest_size_value)
            else:
                results = simulate_fanduel(data, num_simulations, slate_type, contest_size_value)

            # Aggregated results for overall exposures
            overall_results = results.groupby('Name').agg(
                Freq=pd.NamedAgg(column='Name', aggfunc='count'),
                Salary=pd.NamedAgg(column='Salary', aggfunc='mean'),
                Position=pd.NamedAgg(column='Pos', aggfunc='first'),
                Own=pd.NamedAgg(column='Own', aggfunc='mean'),
                Optimal=pd.NamedAgg(column='Optimal', aggfunc='mean'),
                Team=pd.NamedAgg(column='Team', aggfunc='first'),
                Degen_Score=pd.NamedAgg(column='Degen_Score', aggfunc='mean')
            ).reset_index()
            overall_results['Expos%'] = (overall_results['Freq'] / num_simulations) * 100

            # SP Exposures
            sp_exposures = results[results['Pos'] == 'SP'].groupby('Name').agg(
                Freq=pd.NamedAgg(column='Name', aggfunc='count'),
                Salary=pd.NamedAgg(column='Salary', aggfunc='mean'),
                Position=pd.NamedAgg(column='Pos', aggfunc='first'),
                Own=pd.NamedAgg(column='Own', aggfunc='mean'),
                Optimal=pd.NamedAgg(column='Optimal', aggfunc='mean'),
                Team=pd.NamedAgg(column='Team', aggfunc='first'),
                Degen_Score=pd.NamedAgg(column='Degen_Score', aggfunc='mean')
            ).reset_index()
            sp_exposures['Expos%'] = (sp_exposures['Freq'] / num_simulations) * 100

            # Team Exposures
            team_exposures = results.groupby('Team').agg(
                Freq=pd.NamedAgg(column='Team', aggfunc='count'),
                Salary=pd.NamedAgg(column='Salary', aggfunc='mean'),
                Own=pd.NamedAgg(column='Own', aggfunc='mean'),
                Optimal=pd.NamedAgg(column='Optimal', aggfunc='mean'),
                Degen_Score=pd.NamedAgg(column='Degen_Score', aggfunc='mean')
            ).reset_index()
            team_exposures['Expos%'] = (team_exposures['Freq'] / num_simulations) * 100
            
            # Stack Size Exposures
            if site == "DraftKings":
                valid_stacks = ['5', '4', '3', '2']
            else:
                valid_stacks = ['4', '3', '2']
            stack_size_exposures = results[results['Pos'].isin(valid_stacks)].groupby('Pos').agg(
                Freq=pd.NamedAgg(column='Pos', aggfunc='count'),
                Salary=pd.NamedAgg(column='Salary', aggfunc='mean'),
                Own=pd.NamedAgg(column='Own', aggfunc='mean'),
                Optimal=pd.NamedAgg(column='Optimal', aggfunc='mean'),
                Degen_Score=pd.NamedAgg(column='Degen_Score', aggfunc='mean')
            ).reset_index()
            stack_size_exposures['Expos%'] = (stack_size_exposures['Freq'] / num_simulations) * 100

            # Display tabs
            tabs = st.tabs(["Overall Exposures", "SP Exposures", "Team Exposures", "Stack Size Exposures"])
            
            with tabs[0]:
                st.write("### Overall Exposures")
                styled_df = overall_results.style.apply(color_scale, subset=['Expos%'])\
                                                 .apply(color_scale, subset=['Own'])\
                                                 .apply(color_scale, subset=['Optimal'])\
                                                 .apply(color_scale, subset=['Degen_Score'])
                st.dataframe(styled_df, height=600)

            with tabs[1]:
                st.write("### SP Exposures")
                styled_df = sp_exposures.style.apply(color_scale, subset=['Expos%'])\
                                              .apply(color_scale, subset=['Own'])\
                                              .apply(color_scale, subset=['Optimal'])\
                                              .apply(color_scale, subset=['Degen_Score'])
                st.dataframe(styled_df, height=600)

            with tabs[2]:
                st.write("### Team Exposures")
                styled_df = team_exposures.style.apply(color_scale, subset=['Expos%'])\
                                                .apply(color_scale, subset=['Own'])\
                                                .apply(color_scale, subset=['Optimal'])\
                                                .apply(color_scale, subset=['Degen_Score'])
                st.dataframe(styled_df, height=600)

            with tabs[3]:
                st.write("### Stack Size Exposures")
                styled_df = stack_size_exposures.style.apply(color_scale, subset=['Expos%'])\
                                                      .apply(color_scale, subset=['Own'])\
                                                      .apply(color_scale, subset=['Optimal'])\
                                                      .apply(color_scale, subset=['Degen_Score'])
                st.dataframe(styled_df, height=600)

else:
    st.warning("Please upload a CSV file to start the simulation.")
