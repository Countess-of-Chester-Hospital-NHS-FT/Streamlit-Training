import streamlit as st

st.title("More Information")

st.markdown("""
##### Conceptual model

Replace this text with your own text!

The process map for our clinic is as below:
""")

st.image("img/model_diagram.png")

st.markdown("""

In the system described above there are 3 things that affect waiting times:
            
* Number of receptionists
* Number of doctors
* How long it takes to see a receptionist and a doctor
            

            
This tool enables you to try out different scenarios to estimate the effect any
strategy will have on ED admission delays.
            
##### Computer model

The above conceptual model is represented inside the computer as a 'Discrete
Event Simulation'. The computer generates synthetic patients (just like in a
video game) and sends them through the system.
            
In the real system there is random variation in how frequently patients arrive 
and how long they stay in a bed and this is mirrored in the simulated system. 
The simulation runs for 10 * 8hr periods and then shows waiting time metrics
for that period, alongside confidence intervals. The number of runs can be 
increased by the user from 10 to 100 for greater confidence (but the model will
take longer to run).
            
##### How confident are we in the model results?
            
At the moment the model is work in progress and requires further validation.

"""
)