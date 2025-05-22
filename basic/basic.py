import streamlit as st
import palmerpenguins
import plotly.express as px

st.set_page_config(layout="wide", page_title="Basic Webpage")
st.balloons() # for a bit of fun

st.title("Basic Webpage")

st.header("Home section")

st.write("This is the introduction section of the website. Here you can find an introduction.")

tab1, tab2, tab3 = st.tabs(["About", "Contact", "Random stuff"])

with tab1:

    st.header("About section")

    st.markdown("""
    Welcome to this *extremely* **basic** website. Visit our basic page for more basic 
    information.
    """)

with tab2:

    st.header("Contact Section")

    st.write("Feel free to email us for more information")

with tab3:
    
    st.header("Random stuff")

    st.write("Here are some other streamlit bits and bobs")

    st.image("penguin.png")

    st.slider("How many penguins would you like?",
              min_value=0, max_value=100, value=6)
    
    penguins_df = palmerpenguins.load_penguins()

    st.dataframe(penguins_df)

    # Plotly scatter plot
    fig = px.scatter(
        penguins_df,
        x="flipper_length_mm",
        y="bill_length_mm",
        color="species",
        symbol="sex",
        size="body_mass_g",
        title="Palmer Penguins: Flipper vs Bill Length",
        labels={
            "flipper_length_mm": "Flipper Length (mm)",
            "bill_length_mm": "Bill Length (mm)",
            "body_mass_g": "Body Mass (g)"
        }
    )

    # Display Plotly chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)
        
