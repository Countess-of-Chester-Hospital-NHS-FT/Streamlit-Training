import streamlit as st

pg = st.navigation([
        st.Page("home_page.py", title="Welcome!", icon=":material/add_circle:"),
        st.Page("basic.py", title="See Basic Stuff", icon=":material/laptop:")
     ])

pg.run()