import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

from model import g, Trial

st.set_page_config(
     layout="wide"
 )

#Initialise session state
if 'button_click_count' not in st.session_state:
  st.session_state.button_click_count = 0
if 'session_results' not in st.session_state:
    st.session_state['session_results'] = []
if 'session_inputs' not in st.session_state:
    st.session_state['session_inputs'] = []

st.title("Example Non-Elective Flow Simulation")
st.header("(template)")

with st.sidebar:
    num_receptionists_slider = st.slider("Adjust the number of receptionists",
                                min_value=1, max_value=10, value=1)
    num_runs_slider = st. slider("Adjust the number of runs the model does",
                                 min_value=10, max_value=100, value=10)

# This overwrites the g class with inputs from the user
g.number_of_receptionists = num_receptionists_slider
g.number_of_runs = num_runs_slider

tab1, tab2 = st.tabs(["Run the model", "Compare scenarios"])


with tab1:

    button_run_pressed = st.button("Run simulation")

    if button_run_pressed:
        with st.spinner("Simulating the system"):
            all_event_logs, patient_df, run_summary_df, trial_summary_df = Trial().run_trial()
            
            # Comparing inputs
            st.session_state.button_click_count += 1
            col_name = f"Scenario {st.session_state.button_click_count}"
            # make dataframe with inputs, set an index, select as a series
            inputs_for_state = pd.DataFrame({
            'Input': ['Receptionsists' , 'Number of runs'],
            col_name: [num_receptionists_slider, 
                 num_runs_slider]
            }).set_index('Input')[col_name]
            # Append input series to the session state
            st.session_state['session_inputs'].append(inputs_for_state)
            
            # Comparing results
            results_for_state = trial_summary_df['Mean']
            results_for_state.name = col_name
            st.session_state['session_results'].append(results_for_state)
        
            ################
            st.write(f"You've run {st.session_state.button_click_count} scenarios")
            st.write("These metrics are for a 60 day period")

            st.dataframe(trial_summary_df)
            ###################
            
            #
            st.write("Good place to put a histogram")
            # ###################
        
with tab2:
    st.write(f"You've run {st.session_state.button_click_count} scenarios")

    # Convert series back to df, transpose, display
    if st.session_state.button_click_count > 0:
        st.write("Here are your inputs for each scenario")
        current_i_df = pd.DataFrame(st.session_state['session_inputs']).T
        st.dataframe(current_i_df)
        
        st.write("Here are your results for each scenario")
        current_state_df = pd.DataFrame(st.session_state['session_results']).T
        st.dataframe(current_state_df)