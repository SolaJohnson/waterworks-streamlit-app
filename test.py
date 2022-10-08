#import libraries
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np

st.markdown("<h1 style='text-align: center; color: white;'>RAND WATER</h1>", unsafe_allow_html=True)
st.write('Hello!')
st.write('This is a test')

#import data
physical = pd.read_csv(r"C:\Users\Othuke (Local)\OneDrive - Trium Limited\Documents\vaal_main_compliance_data\vaal_main\vaalmain_physical_compliance.csv")
bacteriological = pd.read_csv(r"C:\Users\Othuke (Local)\OneDrive - Trium Limited\Documents\vaal_main_compliance_data\vaal_main\vaalmain_bacteriological_complicance.csv")
sample =pd.read_csv(r"C:\Users\Othuke (Local)\OneDrive - Trium Limited\Documents\vaal_main_compliance_data\vaal_main\sample.csv")
chemical =pd.read_csv(r"C:\Users\Othuke (Local)\OneDrive - Trium Limited\Documents\vaal_main_compliance_data\vaal_main\vaalmain_chemical_compliance.csv")

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
    fig, ax = plt.subplots(figsize=(30,12))

    #Line chart
    ax.plot(data['date'], data['cod'], c='black')
    plt.xlim(0,45)
    plt.ylim(0,60)
    plt.xticks(fontsize=25, rotation = 60)
    plt.yticks(fontsize=15)
    plt.title(f'{param} Compliance for {area} Catchment Area', fontsize=30)
    plt.ylabel(f'{param}, (mg/l)', fontsize=30)

    #Acceptable rectangle
    left, bottom, width, height = (0, 10, 45, 10)
    rect=mpatches.Rectangle((left,bottom),width,height, 
                            alpha=0.8,
                            color="green",
                        linewidth = 2)
    plt.gca().add_patch(rect)
    ax.text(40,15,'Acceptable', size='xx-large')

    #Unacceptable rectangle
    left, bottom, width, height = (0, 30, 45, 30)
    rect=mpatches.Rectangle((left,bottom),width,height, 
                            alpha=0.8,
                        color="red",
                       linewidth = 2)
    plt.gca().add_patch(rect)
    ax.text(40,45,'Unacceptable', size='xx-large')

    #Ideal rectangle
    left, bottom, width, height = (0, 0, 45, 10)
    rect=mpatches.Rectangle((left,bottom),width,height, 
                            alpha=0.4,
                            color="blue",
                        linewidth = 2)
    plt.gca().add_patch(rect)
    ax.text(40,5,'Ideal', size='xx-large')

    #Tolerable rectangle
    left, bottom, width, height = (0, 20, 45, 10)
    rect= mpatches.Rectangle((left,bottom),width,height, 
                            alpha=0.8,
                            color="yellow",
                        linewidth = 2)
    plt.gca().add_patch(rect)
    ax.text(40,25,'Tolerable', size='xx-large')
    st.pyplot(fig)

if param == 'Conductivity':

    #catchment area options
    options = data['Sample_pt_desc'].unique().tolist()
    area = st.sidebar.selectbox("Choose Catchment area", options)
    data = data.loc[data['Sample_pt_desc'] == area]

    #Create plot
    fig, ax = plt.subplots(figsize=(30,12))

    #Line chart
    ax.plot(data['date'], data['conductivity'], c='black')
    plt.xticks(fontsize=25, rotation = 60)
    plt.yticks(fontsize=15)
    plt.xlim(0,45)
    plt.ylim(0,140)
    plt.title(f'{param} Compliance for {area} Catchment Area', fontsize=30)
    plt.ylabel(f'{param}, (mS/m)', fontsize=30)

    #Acceptable rectangle
    left, bottom, width, height = (0, 18, 45, 12)
    rect=mpatches.Rectangle((left,bottom),width,height, 
                            alpha=0.8,
                            color="green",
                        linewidth = 2)
    plt.gca().add_patch(rect)
    ax.text(40,24,'Acceptable', size='xx-large')

    #Unacceptable rectangle
    left, bottom, width, height = (0, 70, 45, 70)
    rect=mpatches.Rectangle((left,bottom),width,height, 
                            alpha=0.8,
                        color="red",
                       linewidth = 2)
    plt.gca().add_patch(rect)
    ax.text(40,105,'Unacceptable', size='xx-large')

    #Ideal rectangle
    left, bottom, width, height = (0, 0, 45, 18)
    rect=mpatches.Rectangle((left,bottom),width,height, 
                            alpha=0.4,
                            color="blue",
                        linewidth = 2)
    plt.gca().add_patch(rect)
    ax.text(40,9,'Ideal', size='xx-large')

    #Tolerable rectangle
    left, bottom, width, height = (0, 30, 45, 40)
    rect= mpatches.Rectangle((left,bottom),width,height, 
                            alpha=0.8,
                            color="yellow",
                        linewidth = 2)
    plt.gca().add_patch(rect)
    ax.text(40,50,'Tolerable', size='xx-large')
    st.pyplot(fig)

if param == 'pH':

    #options for catchment area
    options = data['Sample_pt_desc'].unique().tolist()
    area = st.sidebar.selectbox("Choose Catchment area", options)
    data = data.loc[data['Sample_pt_desc'] == area]

    #Create plot
    fig, ax = plt.subplots(figsize=(30,12))

    #Line chart
    ax.plot(data['date'], data['ph'], c='black')
    plt.xticks(fontsize=25, rotation = 60)
    plt.yticks(fontsize=15)
    plt.xlim(0,45)
    plt.ylim(5,10)
    plt.title(f'{param} Compliance for {area} Catchment Area', fontsize=30)
    plt.ylabel(f'{param}', fontsize=30)

    #Unacceptable Rectangle
    left, bottom, width, height = (0, 0, 45, 6)
    rect=mpatches.Rectangle((left,bottom),width,height, 
                            alpha=0.8,
                        color="red",
                       linewidth = 2)
    plt.gca().add_patch(rect)
    ax.text(40,5.5,'Unacceptable', size='xx-large')

    #Unacceptable rectangle
    left, bottom, width, height = (0, 9, 45, 2)
    rect=mpatches.Rectangle((left,bottom),width,height, 
                            alpha=0.8,
                        color="red",
                       linewidth = 2)
    plt.gca().add_patch(rect)
    ax.text(40,9.5,'Unacceptable', size='xx-large')

    #Tolerable rectangle
    left, bottom, width, height = (0, 6, 45, 0.5)
    rect= mpatches.Rectangle((left,bottom),width,height, 
                            alpha=0.8,
                            color="yellow",
                        linewidth = 2)
    plt.gca().add_patch(rect)
    ax.text(40,6.25,'Tolerable', size='xx-large')

    #Acceptable rectangle
    left, bottom, width, height = (0, 6.5, 45, 0.5)
    rect=mpatches.Rectangle((left,bottom),width,height, 
                            alpha=0.8,
                            color="green",
                        linewidth = 2)
    plt.gca().add_patch(rect)
    ax.text(40,6.75,'Acceptable', size='xx-large')

    #Acceptable rectangle
    left, bottom, width, height = (0, 8.5, 45, 0.5)
    rect=mpatches.Rectangle((left,bottom),width,height, 
                            alpha=0.8,
                            color="green",
                        linewidth = 2)
    plt.gca().add_patch(rect)
    ax.text(40,8.75,'Acceptable', size='xx-large')

    #ideal rectangle
    left, bottom, width, height = (0, 7, 45, 1.5)
    rect=mpatches.Rectangle((left,bottom),width,height, 
                            alpha=0.4,
                            color="blue",
                        linewidth = 2)
    plt.gca().add_patch(rect)
    ax.text(40,7.75,'Ideal', size='xx-large')
    st.pyplot(fig)

if param == 'E.coli':

    #Catchment area options
    options = data2['Sample_pt_desc'].unique().tolist()
    area = st.sidebar.selectbox("Choose Catchment area", options)
    data2 = data2.loc[data2['Sample_pt_desc'] == area]

    #Create plot
    fig, ax = plt.subplots(figsize=(30,12))

    #Line chart
    ax.plot(data2['date'], data2['e.coli'], c='black')
    plt.xticks(fontsize=25, rotation = 60)
    plt.yticks(fontsize=15)
    plt.title(f'{param} Compliance for {area} Catchment Area', fontsize=30)
    plt.ylabel(f'{param}', fontsize=30)

    #Acceptable rectangle
    left, bottom, width, height = (0, 131, 45, 69)
    rect=mpatches.Rectangle((left,bottom),width,height, 
                            alpha=0.8,
                            color="green",
                        linewidth = 2)
    plt.gca().add_patch(rect)
    #ax.text(40,165,'Acceptable', size='xx-large')

    #Unacceptable rectangle
    left, bottom, width, height = (0, 400, 45, 999600)
    rect=mpatches.Rectangle((left,bottom),width,height, 
                            alpha=0.8,
                        color="red",
                       linewidth = 2)
    plt.gca().add_patch(rect)
    ax.text(40,30000,'Unacceptable', size='xx-large')

    #Ideal rectangle
    left, bottom, width, height = (0, 0, 45, 130)
    rect=mpatches.Rectangle((left,bottom),width,height, 
                            alpha=0.4,
                            color="blue",
                        linewidth = 2)
    plt.gca().add_patch(rect)
    #ax.text(40,65,'Ideal', size='xx-large')

    #Tolerable rectangle
    left, bottom, width, height = (0, 200, 45, 200)
    rect= mpatches.Rectangle((left,bottom),width,height, 
                            alpha=0.8,
                            color="yellow",
                        linewidth = 2)
    plt.gca().add_patch(rect)
    #ax.text(40,300,'Tolerable', size='xx-large')
    st.pyplot(fig)

if param == 'Nitrate NO3 as N':

    #options for catchment area
    options = data3['Sample_pt_desc'].unique().tolist()
    area = st.sidebar.selectbox("Choose Catchment area", options)
    data3 = data3.loc[data3['Sample_pt_desc'] == area]

    #Create plot
    fig, ax = plt.subplots(figsize=(30,12))

    #Line chart
    ax.plot(data3['date'], data3['nitrate'], c='black')
    plt.xlim(0,45)
    plt.ylim(0,8)
    plt.xticks(fontsize=25, rotation = 60)
    plt.yticks(fontsize=15)
    plt.title(f'{param} Compliance for {area} Catchment Area', fontsize=30)
    plt.ylabel(f'{param}, (mg/l)', fontsize=30)

    #Acceptable rectangle
    left, bottom, width, height = (0, 0.5, 45, 2.5)
    rect=mpatches.Rectangle((left,bottom),width,height, 
                            alpha=0.8,
                            color="green",
                        linewidth = 2)
    plt.gca().add_patch(rect)
    ax.text(40,1.5,'Acceptable', size='xx-large')

    #unacceptable rectangle
    left, bottom, width, height = (0, 6, 45, 2)
    rect=mpatches.Rectangle((left,bottom),width,height, 
                            alpha=0.8,
                        color="red",
                       linewidth = 2)
    plt.gca().add_patch(rect)
    ax.text(40,7,'Unacceptable', size='xx-large')

    #Ideal rectangle
    left, bottom, width, height = (0, 0, 45, 0.5)
    rect=mpatches.Rectangle((left,bottom),width,height, 
                            alpha=0.4,
                            color="blue",
                        linewidth = 2)
    plt.gca().add_patch(rect)
    ax.text(40,0.25,'Ideal', size='xx-large')

    #Tolerable rectangle
    left, bottom, width, height = (0, 3, 45, 3)
    rect= mpatches.Rectangle((left,bottom),width,height, 
                            alpha=0.8,
                            color="yellow",
                        linewidth = 2)
    plt.gca().add_patch(rect)
    ax.text(40,4.5,'Tolerable', size='xx-large')
    st.pyplot(fig)

if param == 'Phosphate PO4 as P':

    #Catchment area options
    options = data3['Sample_pt_desc'].unique().tolist()
    area = st.sidebar.selectbox("Choose Catchment area", options)
    data3 = data3.loc[data3['Sample_pt_desc'] == area]

    #Create plot
    fig, ax = plt.subplots(figsize=(30,12))

    #Line chart
    ax.plot(data3['date'], data3['phosphate'], c='black')
    plt.xlim(0,45)
    plt.ylim(0,8)
    plt.xticks(fontsize=25, rotation = 60)
    plt.yticks(fontsize=15)
    plt.title(f'{param} Compliance for {area} Catchment Area', fontsize=30)
    plt.ylabel(f'{param}, (mg/l)', fontsize=30)

    #Acceptable rectangle
    left, bottom, width, height = (0, 0.5, 45, 2.5)
    rect=mpatches.Rectangle((left,bottom),width,height, 
                            alpha=0.8,
                            color="green",
                        linewidth = 2)
    plt.gca().add_patch(rect)
    ax.text(40,1.5,'Acceptable', size='xx-large')

    #unacceptable rectangle
    left, bottom, width, height = (0, 6, 45, 2)
    rect=mpatches.Rectangle((left,bottom),width,height, 
                            alpha=0.8,
                        color="red",
                       linewidth = 2)
    plt.gca().add_patch(rect)
    ax.text(40,7,'Unacceptable', size='xx-large')

    #Ideal rectangle
    left, bottom, width, height = (0, 0, 45, 0.5)
    rect=mpatches.Rectangle((left,bottom),width,height, 
                            alpha=0.4,
                            color="blue",
                        linewidth = 2)
    plt.gca().add_patch(rect)
    ax.text(40,0.25,'Ideal', size='xx-large')

    #Tolerable rectangle
    left, bottom, width, height = (0, 3, 45, 3)
    rect= mpatches.Rectangle((left,bottom),width,height, 
                            alpha=0.8,
                            color="yellow",
                        linewidth = 2)
    plt.gca().add_patch(rect)
    ax.text(40,4.5,'Tolerable', size='xx-large')
    st.pyplot(fig)



 # Design horizontal bar
    menu = ["Home", "EDA", "Prediction", "About"]
    selection = option_menu( menu_title=None,
    options=menu,
    icons=["house", "graph-up", "textarea-t",  "file-person"],
    orientation='horizontal',
    styles={
                "container": {"padding": "0!important"},
                "icon": {"color": "orange", "font-size": "25px",  },
                "nav-link": {
                    "font-size": "20px",
                    "text-align": "center",
                    "margin": "5px",
                    "--hover-color": "#ccc",
                },
                "nav-link-selected": {"background-color": "green"},
            },
        )    



    if selection == "Home":
        st.markdown('')

    elif selection == "Prediction":
        st.subheader("Prediction")

    elif selection == "EDA":
        st.subheader("Exploration of Sentiment and Tweets")

    else:
        st.subheader('')



    #Landing page
    landing = Image.open("resources/imgs/backgroundpix.png")
    if selection == "Home":
        st.image(landing)#, height=1500

