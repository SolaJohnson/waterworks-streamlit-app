import streamlit as st
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np
from streamlit_option_menu import option_menu
from PIL import Image


def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size:180%;
        background-color:#CDE5F3;
  
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('robert-anderson-aJ-UU_9F9ko-unsplash.jpg')  

# Design horizontal bar
menu = ["Home", "Water Quality", "Time Series", "About us"]
selection = option_menu(None, ["Home", "Water Quality", "Time Series", 'About us'], 
    icons=['house', "bi bi-droplet", "bi bi-graph-up", 'bi bi-info-square'], 
    menu_icon="cast", default_index=0, orientation="horizontal",styles={
        "container": {"padding": "0!important", "background-color": "#c1ddea"},
        "icon": {"color": "#172d90", "font-size": "15px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#ECFFFF"},
        "nav-link-selected": {"background-color": "#19a2a2"},
    })

 
if selection == "Home":
    st.markdown('')
elif selection == "Water Quality":
    st.subheader("Geospatial Data")
elif selection == "Time Series":
    st.subheader("Water quality over time")
else:
    st.subheader('')

#Landing page
landing = Image.open('Rand_Water_logo.svg.png')
if selection == "Home":
        st.image(landing)#, height=1500,
        st.markdown("<h1 style='font-size:20px; text-align: center; color:#19a2a2;'>CATCHMENT MONITORING APPLICATION</h1>", unsafe_allow_html=True)
        