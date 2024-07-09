import streamlit as st
import pandas as pd
from helpers.load_data import load_data
from helpers.simulate import simulate_draftkings, simulate_fanduel
from helpers.color_scale import color_scale

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
    st.radio("Which data are you loading?", ["Main Slate", "Other Main Slate"], index=0)
    
    # Site Options
    site = st.radio("What site are you working with?", ["DraftKings", "FanDuel"], index=0)
    
    # Contest Size
    contest_size = st.selectbox("What contest size are you simulating?", ["Small", "Medium", "Large"])
    
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
            # Simulate data for different tabs
            if site == "DraftKings":
                results = simulate_draftkings(data, num_simulations)
            else:
                results = simulate_fanduel(data, num_simulations)
            
            # Aggregated results for overall exposures
            overall_results = results.groupby('Name').agg(
                Freq=pd.NamedAgg(column='Name', aggfunc='count'),
                Salary=pd.NamedAgg(column='Salary', aggfunc='mean'),
                Position=pd.NamedAgg(column='Pos', aggfunc='first'),
                Proj_Own=pd.NamedAgg(column='Own', aggfunc='mean'),
                Optimal=pd.NamedAgg(column='Optimal', aggfunc='mean'),
                Team=pd.NamedAgg(column='Team', aggfunc='first')
            ).reset_index()

            # SP Exposures
            sp_exposures = results[results['Pos'] == 'SP'].groupby('Name').agg(
                Freq=pd.NamedAgg(column='Name', aggfunc='count'),
                Salary=pd.NamedAgg(column='Salary', aggfunc='mean'),
                Position=pd.NamedAgg(column='Pos', aggfunc='first'),
                Proj_Own=pd.NamedAgg(column='Own', aggfunc='mean'),
                Optimal=pd.NamedAgg(column='Optimal', aggfunc='mean'),
                Team=pd.NamedAgg(column='Team', aggfunc='first')
            ).reset_index()

            # Team Exposures
            team_exposures = results.groupby('Team').agg(
                Freq=pd.NamedAgg(column='Team', aggfunc='count'),
                Salary=pd.NamedAgg(column='Salary', aggfunc='mean'),
                Proj_Own=pd.NamedAgg(column='Own', aggfunc='mean'),
                Optimal=pd.NamedAgg(column='Optimal', aggfunc='mean')
            ).reset_index()

            # Stack Size Exposures
            stack_size_exposures = results.groupby('Pos').agg(
                Freq=pd.NamedAgg(column='Pos', aggfunc='count'),
                Salary=pd.NamedAgg(column='Salary', aggfunc='mean'),
                Proj_Own=pd.NamedAgg(column='Own', aggfunc='mean'),
                Optimal=pd.NamedAgg(column='Optimal', aggfunc='mean')
            ).reset_index()

            # Display tabs
            tabs = st.tabs(["Overall Exposures", "SP Exposures", "Team Exposures", "Stack Size Exposures"])
            
            with tabs[0]:
                st.write("### Overall Exposures")
                styled_df = overall_results.style.apply(color_scale, subset=['Freq'])\
                                                 .apply(color_scale, subset=['Proj_Own'])\
                                                 .apply(color_scale, subset=['Optimal'])
                st.dataframe(styled_df, height=600)

            with tabs[1]:
                st.write("### SP Exposures")
                styled_df = sp_exposures.style.apply(color_scale, subset=['Freq'])\
                                              .apply(color_scale, subset=['Proj_Own'])\
                                              .apply(color_scale, subset=['Optimal'])
                st.dataframe(styled_df, height=600)

            with tabs[2]:
                st.write("### Team Exposures")
                styled_df = team_exposures.style.apply(color_scale, subset=['Freq'])\
                                                .apply(color_scale, subset=['Proj_Own'])\
                                                .apply(color_scale, subset=['Optimal'])
                st.dataframe(styled_df, height=600)

            with tabs[3]:
                st.write("### Stack Size Exposures")
                styled_df = stack_size_exposures.style.apply(color_scale, subset=['Freq'])\
                                                     .apply(color_scale, subset=['Proj_Own'])\
                                                     .apply(color_scale, subset=['Optimal'])
                st.dataframe(styled_df, height=600)

else:
    st.warning("Please upload a CSV file to start the simulation.")
