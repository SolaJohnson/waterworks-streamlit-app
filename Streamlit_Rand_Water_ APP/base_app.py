from turtle import title
import streamlit as st
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np
from streamlit_option_menu import option_menu
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
import dash_map as dm

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
        "container": {"padding": "0!important", "background-color": "#D3E2F7"},
        "icon": {"color": "#172d90", "font-size": "15px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#ECFFFF"},
        "nav-link-selected": {"background-color": "#7CC4F5"},
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
landing = Image.open('waterworksRS (2).png')
if selection == "Home":
    st.image(landing)



#Time Series Page
if selection == 'Time Series':

    #Data preprocessing
    physical = pd.read_csv(r'vaalmain_physical_compliance.csv')
    sample = pd.read_csv(r'sample.csv')
    chemical = pd.read_csv(r'vaalmain_chemical_compliance.csv')
    bacteriological = pd.read_csv(r'vaalmain_bacteriological_complicance.csv')

    # Step: Sort column(s) year ascending (A-Z), qtr ascending (A-Z)
    data = physical.sort_values(by=['year', 'qtr'], ascending=[True, True])
    data2 = bacteriological.sort_values(by=['year', 'qtr'], ascending=[True, True])
    data3 = chemical.sort_values(by=['year', 'qtr'], ascending=[True, True])

    #Merge data with sample
    data = pd.merge(data, sample, how='left', left_on=['sample_id'], right_on=['Sample_id'])
    data2 = pd.merge(data2, sample, how='left', left_on=['sample_id'], right_on=['Sample_id'])
    data3 = pd.merge(data3, sample, how='left', left_on=['sample_id'], right_on=['Sample_id'])

    # Step: Create new column 'date' from formula 'quarter + " " + year.astype(str)'
    data['date'] = data['quarter'] + " " + data['year'].astype(str)
    data2['date'] = data2['quarter'] + " " + data2['year'].astype(str)
    data3['date'] = data3['quarter'] + " " + data3['year'].astype(str)


    #create sidebar options for parameters
    parameters = ['COD', 'Conductivity','E.coli','Nitrate NO3 as N','pH','Phosphate PO4 as P']
    param = st.sidebar.selectbox("Choose Parameter", parameters)   

    if param == 'COD':

        #create options for catchment area
        options = data['Sample_pt_desc'].unique().tolist()
        area = st.sidebar.selectbox("Choose Catchment area", options)
        data = data.loc[data['Sample_pt_desc'] == area]

        #Create plot
        fig = go.Figure() 

        #Line chart
        fig.add_trace(go.Scatter(x=data['date'], y=data['cod'], mode='lines',
                line=dict(color='black', width=3),
                connectgaps=True))

        #update axis
        fig.update_layout(
            xaxis=dict(
                showline=True,
                showgrid=False,
                showticklabels=True,
                range=[0, 45],
                tickangle=330),
            
            yaxis=dict(
                showgrid=False,
                zeroline=True,
                showline=True,
                showticklabels=True,
                title=f'{param} mg/l',  
                range=[0, 60]) )

                    
        # Add shapes
        fig.add_hrect(y0=20, y1=35, 
                    annotation_text="Acceptable", annotation_position="right",
                    annotation=dict(font_size=20, font_family="Times New Roman"),
                    fillcolor="green", opacity=0.25, line_width=0)

        fig.add_hrect(y0=0, y1=19, 
                    annotation_text="Ideal", annotation_position="right",
                    annotation=dict(font_size=20, font_family="Times New Roman"),
                    fillcolor="blue", opacity=0.25, line_width=0)

        fig.add_hrect(y0=35, y1=55, 
                    annotation_text="Tolerable", annotation_position="right",
                    annotation=dict(font_size=20, font_family="Times New Roman"),
                    fillcolor="yellow", opacity=0.35, line_width=0)

        fig.add_hrect(y0=55, y1=60, 
                    annotation_text="Unacceptable", annotation_position="right",
                    annotation=dict(font_size=20, font_family="Times New Roman"),
                    fillcolor="red", opacity=0.45, line_width=0)
        st.plotly_chart(fig)


    if param == 'Conductivity':

        #catchment area options
        options = data['Sample_pt_desc'].unique().tolist()
        area = st.sidebar.selectbox("Choose Catchment area", options)
        data = data.loc[data['Sample_pt_desc'] == area]

        #Create plot
        fig = go.Figure() 

        #Line chart
        fig.add_trace(go.Scatter(x=data['date'], y=data['conductivity'], mode='lines',
                line=dict(color='black', width=3),
                connectgaps=True))

        #update axis
        fig.update_layout(
            xaxis=dict(
                showline=True,
                showgrid=False,
                showticklabels=True,
                range=[0, 45],
                tickangle=330),
            
            yaxis=dict(
                showgrid=False,
                zeroline=True,
                showline=True,
                showticklabels=True,
                title= f'{param} (mS/m)',
                range=[0, 140]) )

                    
        # Add shapes
        fig.add_hrect(y0=18, y1=30, 
                    annotation_text="Acceptable", annotation_position="right",
                    annotation=dict(font_size=20, font_family="Times New Roman"),
                    fillcolor="green", opacity=0.25, line_width=0)

        fig.add_hrect(y0=0, y1=18, 
                    annotation_text="Ideal", annotation_position="right",
                    annotation=dict(font_size=20, font_family="Times New Roman"),
                    fillcolor="blue", opacity=0.25, line_width=0)

        fig.add_hrect(y0=30, y1=70, 
                    annotation_text="Tolerable", annotation_position="right",
                    annotation=dict(font_size=20, font_family="Times New Roman"),
                    fillcolor="yellow", opacity=0.35, line_width=0)

        fig.add_hrect(y0=70, y1=140, 
                    annotation_text="Unacceptable", annotation_position="right",
                    annotation=dict(font_size=20, font_family="Times New Roman"),
                    fillcolor="red", opacity=0.45, line_width=0)
        st.plotly_chart(fig)

    
    if param == 'pH':

        #options for catchment area
        options = data['Sample_pt_desc'].unique().tolist()
        area = st.sidebar.selectbox("Choose Catchment area", options)
        data = data.loc[data['Sample_pt_desc'] == area]

        #Create plot
        fig = go.Figure() 

        #Line chart
        fig.add_trace(go.Scatter(x=data['date'], y=data['ph'], mode='lines',
                line=dict(color='black', width=3),
                connectgaps=True))

        #update axis
        fig.update_layout(
            xaxis=dict(
                showline=True,
                showgrid=False,
                showticklabels=True,
                range=[0, 45],
                tickangle=330),
            
            yaxis=dict(
                showgrid=False,
                zeroline=True,
                showline=True,
                showticklabels=True,
                title= f'{param} ',
                range=[5, 11]) )

                    
        # Add shapes
        fig.add_hrect(y0=6.5, y1=7, 
                    annotation_text="Acceptable", annotation_position="right",
                    annotation=dict(font_size=20, font_family="Times New Roman"),
                    fillcolor="green", opacity=0.25, line_width=0)
        
        fig.add_hrect(y0=8.4, y1=8.5,
                    fillcolor="green", opacity=0.25, line_width=0)

        fig.add_hrect(y0=7, y1=8.4, 
                    annotation_text="Ideal", annotation_position="right",
                    annotation=dict(font_size=20, font_family="Times New Roman"),
                    fillcolor="blue", opacity=0.25, line_width=0)

        fig.add_hrect(y0=6, y1=6.5, 
                    annotation_text="Tolerable", annotation_position="right",
                    annotation=dict(font_size=20, font_family="Times New Roman"),
                    fillcolor="yellow", opacity=0.35, line_width=0)
        
        fig.add_hrect(y0=8.5, y1=9, 
                    annotation_text="Tolerable", annotation_position="right",
                    annotation=dict(font_size=20, font_family="Times New Roman"),
                    fillcolor="yellow", opacity=0.35, line_width=0)

        fig.add_hrect(y0=0, y1=6, 
                    annotation_text="Unacceptable", annotation_position="right",
                    annotation=dict(font_size=20, font_family="Times New Roman"),
                    fillcolor="red", opacity=0.25, line_width=0)
        fig.add_hrect(y0=9, y1=11, 
                    annotation_text="Unacceptable", annotation_position="right",
                    annotation=dict(font_size=20, font_family="Times New Roman"),
                    fillcolor="red", opacity=0.45, line_width=0)
        st.plotly_chart(fig)

    
    if param == 'E.coli':

        #Catchment area options
        options = data2['Sample_pt_desc'].unique().tolist()
        area = st.sidebar.selectbox("Choose Catchment area", options)
        data2 = data2.loc[data2['Sample_pt_desc'] == area]

        #Create plot
        fig = go.Figure() 

        #Line chart
        fig.add_trace(go.Scatter(x=data2['date'], y=data2['e.coli'], mode='lines',
                line=dict(color='black', width=3),
                connectgaps=True))

        #update axis
        fig.update_layout(
            xaxis=dict(
                showline=True,
                showgrid=False,
                showticklabels=True,
                range=[0, 45],
                tickangle=330),
            
            yaxis=dict(
                showgrid=False,
                zeroline=True,
                showline=True,
                showticklabels=True,
                title= f'{param} (counts/100ml)',
                range=[0, 1000]) )

                    
        # Add shapes
        fig.add_hrect(y0=130, y1=200, 
                    annotation_text="Acceptable", annotation_position="right",
                    annotation=dict(font_size=20, font_family="Times New Roman"),
                    fillcolor="green", opacity=0.25, line_width=0)

        fig.add_hrect(y0=0, y1=130, 
                    annotation_text="Ideal", annotation_position="right",
                    annotation=dict(font_size=20, font_family="Times New Roman"),
                    fillcolor="blue", opacity=0.25, line_width=0)

        fig.add_hrect(y0=200, y1=400, 
                    annotation_text="Tolerable", annotation_position="right",
                    annotation=dict(font_size=20, font_family="Times New Roman"),
                    fillcolor="yellow", opacity=0.35, line_width=0)

        fig.add_hrect(y0=400, y1=1000, 
                    annotation_text="Unacceptable", annotation_position="right",
                    annotation=dict(font_size=20, font_family="Times New Roman"),
                    fillcolor="red", opacity=0.45, line_width=0)
        st.plotly_chart(fig)
        

    if param == 'Nitrate NO3 as N':

        #options for catchment area
        options = data3['Sample_pt_desc'].unique().tolist()
        area = st.sidebar.selectbox("Choose Catchment area", options)
        data3 = data3.loc[data3['Sample_pt_desc'] == area]

        #Create plot
        fig = go.Figure() 

        #Line chart
        fig.add_trace(go.Scatter(x=data3['date'], y=data3['nitrate'], mode='lines',
                line=dict(color='black', width=3),
                connectgaps=True))

        #update axis
        fig.update_layout(
            xaxis=dict(
                showline=True,
                showgrid=False,
                showticklabels=True,
                range=[0, 45],
                tickangle=330),
            
            yaxis=dict(
                showgrid=False,
                zeroline=True,
                showline=True,
                showticklabels=True,
                title= f'{param} (mg/l)',
                range=[0, 8]) )

                    
        # Add shapes
        fig.add_hrect(y0=0.5, y1=3, 
                    annotation_text="Acceptable", annotation_position="right",
                    annotation=dict(font_size=20, font_family="Times New Roman"),
                    fillcolor="green", opacity=0.25, line_width=0)

        fig.add_hrect(y0=0, y1=0.5, 
                    annotation_text="Ideal", annotation_position="right",
                    annotation=dict(font_size=20, font_family="Times New Roman"),
                    fillcolor="blue", opacity=0.25, line_width=0)

        fig.add_hrect(y0=3, y1=6, 
                    annotation_text="Tolerable", annotation_position="right",
                    annotation=dict(font_size=20, font_family="Times New Roman"),
                    fillcolor="yellow", opacity=0.35, line_width=0)

        fig.add_hrect(y0=6, y1=8, 
                    annotation_text="Unacceptable", annotation_position="right",
                    annotation=dict(font_size=20, font_family="Times New Roman"),
                    fillcolor="red", opacity=0.45, line_width=0)
        st.plotly_chart(fig)
        
    if param == 'Phosphate PO4 as P':

        #Catchment area options
        options = data3['Sample_pt_desc'].unique().tolist()
        area = st.sidebar.selectbox("Choose Catchment area", options)
        data3 = data3.loc[data3['Sample_pt_desc'] == area]

        #Create plot
        fig = go.Figure() 

        #Line chart
        fig.add_trace(go.Scatter(x=data3['date'], y=data3['phosphate'], mode='lines',
                line=dict(color='black', width=3),
                connectgaps=True))

        #update axis
        fig.update_layout(
            xaxis=dict(
                showline=True,
                showgrid=False,
                showticklabels=True,
                range=[0, 45],
                tickangle=330),
            
            yaxis=dict(
                showgrid=False,
                zeroline=True,
                showline=True,
                showticklabels=True,
                title= f'{param} (mg/l)',
                range=[0, 3]) )

                    
        # Add shapes
        fig.add_hrect(y0=0, y1=0.03,
                    fillcolor="green", opacity=0.25, line_width=0)


        fig.add_hrect(y0=0.03, y1=0.05, 
                    fillcolor="yellow", opacity=0.35, line_width=0)

        fig.add_hrect(y0=0.05, y1=3, 
                    annotation_text="Unacceptable", annotation_position="right",
                    annotation=dict(font_size=20, font_family="Times New Roman"),
                    fillcolor="red", opacity=0.45, line_width=0)
        st.plotly_chart(fig)


#Interactive map page
if selection == 'Water Quality':
    dm.main()
