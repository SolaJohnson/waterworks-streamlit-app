import streamlit as st
import pybase64
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
from prophet import Prophet
import randDataProvider as rd

#Create plot
def create_plot(df, area, x, y, y_lim, g0, g1, b0, b1, y0, y1, r0, r1):
    """
        The function creates a plot of the selected parameter and catchment area using the following arguments
        
        Inputs:
        df - dataframe
        area - Selected catchment area
        x - x_axis
        y - y_axis
        y_lim - upper limit of the y_axis
        g0 - lower y value of acceptable rectangle
        g1 - upper y value of acceptable rectangle
        b0 - lower y value of ideal rectangle
        b1 - upper y value of ideal rectangle
        y0 - lower y value of tolerable rectangle
        y1 - upper y value of tolerable rectangle
        r0 - lower y value of unacceptable rectangle
        r1 - upper y value of unacceptable rectangle
    
    """
    fig = go.Figure() 
    #Line chart
    fig.add_trace(go.Scatter(x=df[x], y=df[y], mode='lines',
            line=dict(color='black', width=3),
            connectgaps=True))
    #update axis
    fig.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            tickangle=330),
        yaxis=dict(
            showgrid=False,
            zeroline=True,
            showline=True,
            showticklabels=True,
            title= f'{param} ',
            range=[0, y_lim]) )
    # Add shapes
    fig.add_hrect(y0=g0, y1=g1, 
                annotation_text="Acceptable", annotation_position="right",
                annotation=dict(font_size=20, font_family="Times New Roman"),
                fillcolor="green", opacity=0.3, line_width=0)
    fig.add_hrect(y0=b0, y1=b1, 
                annotation_text="Ideal", annotation_position="right",
                annotation=dict(font_size=20, font_family="Times New Roman"),
                fillcolor="blue", opacity=0.3, line_width=0)
    fig.add_hrect(y0=y0, y1=y1, 
                annotation_text="Tolerable", annotation_position="right",
                annotation=dict(font_size=20, font_family="Times New Roman"),
                fillcolor="yellow", opacity=0.3, line_width=0)
    fig.add_hrect(y0=r0, y1=r1, 
                annotation_text="Unacceptable", annotation_position="right",
                annotation=dict(font_size=20, font_family="Times New Roman"),
                fillcolor="red", opacity=0.3, line_width=0)
    st.plotly_chart(fig)


def make_forecast(df, y ):
    df.reset_index(inplace=True)

    #Prepare data for forecast
    df['day-month'] = ''
    for i, qtr in enumerate(df.qtr):
        if qtr == 1:
            df['day-month'][i] = '31-03'
        elif qtr == 2:
            df['day-month'][i] = '30-06'
        elif qtr == 3:
            df['day-month'][i] = '30-09'
        else:
            df['day-month'][i] = '31-12'
        
    df['date'] = df['day-month'].astype(str) + ' ' + df['year'].astype(str)
    df['date'] = pd.to_datetime(df['date'])

    # define the period for which we want a prediction
    future = pd.date_range('2022-06-30', periods=10, freq='Q').tolist()
    future = pd.DataFrame(future)
    future.columns = ['ds']
    future['ds']= pd.to_datetime(future['ds'])

    
    # prepare expected column names
    data = pd.DataFrame(columns=['ds', 'y'])
    data['ds'] = df['date']
    data['y'] = df[y]
    data['ds']= pd.to_datetime(data['ds'])

    # define the model
    model = Prophet()

    # fit the model
    model.fit(data)

    # use the model to make a forecast
    forecast = model.predict(future)   

    #plot forecast
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
    x = forecast['ds'],
    y = forecast['yhat'],
    mode = 'lines',
    marker = {
        'color': '#3bbed7'
    },
    line = {
        'width': 1.5
    },
    name = 'Forecast',
    ))

    fig.add_trace(go.Scatter(
    x = forecast['ds'],
    y = forecast['yhat_lower'],
    marker = {
        'color': 'rgba(0,0,0,0)'
    },
    showlegend = False,
    hoverinfo = 'none',
    name = 'yhat_lower' ,
    ))

    fig.add_trace(go.Scatter(
    x = forecast['ds'],
    y = forecast['yhat_upper'],
    fill='tonexty',
    fillcolor = 'rgba(26,150,65,0.1)',
    name = 'Confidence',
    mode = 'none'
    ))

    fig.add_trace(go.Scatter(
    x = data['ds'],
    y = data['y'],
    mode = 'lines',
    line=dict(color='blue', width=2),
    connectgaps=True,
    name = 'Actual'
    ))

    fig.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='black',
            linewidth=0.7,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='black',
                        ),
        ),
        yaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            title=para,
            linecolor='black',
            linewidth=0.7,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='black',
            )
        ),
        
        showlegend = True,
    plot_bgcolor='#D3E2F7'
    ) 
    st.plotly_chart(fig)

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = pybase64.b64encode(image_file.read())
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
add_bg_from_local('Images/background img.png')  

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

#load data from sql table
query = '''

    SELECT sp.sample_pt_desc, ra.year, ra.qtr, ra.quarter, ra.cod, ra.conductivity, ra.e_coli,
            ra.pH, nitrate, phosphate, ra.physical_compliance_percentage, ra.chemical_compliance_percentage,
            ra.bacteriological_compliance_percentage, 
            ra.biological_compliance_percentage, ra.overall_compliance_percentage, ri.river_id

    FROM rand ra
    INNER JOIN sampling_points sp
    ON ra.sample_id = sp.sample_id
    INNER JOIN rivers ri
    ON ra.river_id = ri.river_id

    '''
data = rd.get_data(query)

data = data.fillna(0)

 
if selection == "Home":
    st.markdown('')
    

elif selection == "Water Quality":
    st.subheader("Geospatial Data")

elif selection == "Time Series":
    st.subheader("Water quality over time")

else:
    st.subheader('')
    st.subheader("About Team")
    st.markdown(" ")
    mikey_pic = Image.open("Images/MIKEY.jpg")
    emeka_pic = Image.open("Images/EMEKA.jpeg")
    bodine_pic = Image.open("Images/bodine.jpeg")
    othuke_pic = Image.open("Images/Othuke.jpeg")
    joseph_pic = Image.open("Images/Joseph.jpeg")
    ehi_pic = Image.open("Images/Ehi.jpg")


    st.header("Bodine Mazibuko - Team Leader")
    bodine, text = st.columns((1,2))

    with bodine:
        st.image(bodine_pic)

    with text:
        st.write("""
            Project management, analytical reporting and research skills, data visualization, UIUX.""")
    
    st.header("Michael Ndirangu -  Data Engineer")
    mikey, text1 = st.columns((1,2))

    with mikey:
        st.image(mikey_pic)

    with text1:
        st.write("""
            Michael is well versed in creating ETL pipelines in AWS Cloud, Azure Cloud, as well as in on premise environment with python 
            """)

    st.header("Odimegwu David - Data Scientist")
    emeka, text2 = st.columns((1,2))
    
    with emeka:
        st.image(emeka_pic)

    with text2:
        st.write("""
            David's skills include machine learning, SQL, and making predictions on given data.
            """)

    st.header("Othuke Ajaye- Data Scientist")
    othuke, text3 = st.columns((1,2))
    
    with othuke:
        st.image(othuke_pic)

    with text3:
        st.write("""
            Othuke is a Motivated, teamwork-oriented, and responsible Data Scientist who strives to provide insights to help make informed decisions with skills in 
            data analytics, communication and problem solving.
            """)

    st.header("Joseph Aromeh - Data Scientist")
    joseph, text4 = st.columns((1,2))
    
    with joseph:
        st.image(joseph_pic)

    with text4:
        st.write("""
            A data enthusiast, skilled in Data Visualization with Pandas, Power BI and Machine Learning using Python, PySpark, ScikitLearn, Tensorflow, Serverless Machine Learning.
            """)

    st.header("Ehibhahiemen Ughele - Data Engineer")
    ehi, text5 = st.columns((1,2))
    
    with ehi:
        st.image(ehi_pic)

    with text5:
        st.write("""
            A detail-oriented data engineer highly proficient in the architecture of data oriented infrastructure and solutions to problem utilising skills such as Python, SQL,
             Spark as well as a careful integration of pipelines or cloud related services solutions leveraging on AWS and AZURE.""")

#Landing page
landing = Image.open('Images/waterworksRS (2).png')
if selection == "Home":
    st.image(landing)



#Time Series Page
if selection == 'Time Series':
    
    
    #Select river
    rivers = ['Vaal', 'Klip', 'Blesbokspruit']
    river = st.sidebar.selectbox("Select a river", rivers)

    if river == 'Vaal':
        df = data.copy()
        df = df.loc[df['river_id'] == 1]
        

        # Step: Sort column(s) year ascending (A-Z), qtr ascending (A-Z)
        df = df.sort_values(by=['year', 'qtr'], ascending=[True, True])


        # Step: Create new column 'date' from formula 'quarter + " " + year.astype(str)'
        df['date'] = df['quarter'] + " " + df['year'].astype(str)

        #create sidebar options for parameters
        parameters = ['COD', 'Conductivity','E.coli','Nitrate NO3 as N','pH','Phosphate PO4 as P', 'Overall Compliance']
        param = st.sidebar.selectbox("Choose Parameter", parameters)   

        if param == 'Overall Compliance':

            para = st.sidebar.radio('', ['Physical', 'Chemical', 'Overall']) 

            #create options for catchment area
            options = df['sample_pt_desc'].unique().tolist()
            area = st.sidebar.selectbox("Choose Catchment area", options)
            
        
            #filter by catchment area
            df = df.loc[df['sample_pt_desc'] == area]

            
            
            if para == 'Physical':

                make_forecast(df, 'physical_compliance_percentage')

            if para == 'Chemical':

                make_forecast(df, 'chemical_compliance_percentage')

            if para == 'Overall':
                
                make_forecast(df, 'overall_compliance_percentage')

        if param == 'COD':

            #create date slider
            year = [f'{i}' for i in range(2011, 2023) ]
            start, stop = st.select_slider('Select time frame', options=year, value=('2011', '2022'))

            #create options for catchment area
            options = df['sample_pt_desc'].unique().tolist()
            area = st.sidebar.selectbox("Choose Catchment area", options)

            #Filter data by catchment area
            df = df.loc[df['sample_pt_desc'] == area]

            #Filter data by year
            df = df.loc[(df['year'].astype(str) >= start) & (df['year'].astype(str) <= stop)]

            #Create plot
            create_plot(df = df, area=area, x='date', y = 'cod', y_lim = 60, g0 = 20, g1=35, b0=0, b1=19, y0=35, y1=55, r0=55, r1=60)


        if param == 'Conductivity':

            #create date slider
            year = [f'{i}' for i in range(2011, 2023) ]
            start, stop = st.select_slider('Select time frame', options=year, value=('2011', '2022'))

            #catchment area options
            options = df['sample_pt_desc'].unique().tolist()
            area = st.sidebar.selectbox("Choose Catchment area", options)

            #filter by catchment area
            df = df.loc[df['sample_pt_desc'] == area]

            #Filter data by year
            df = df.loc[(df['year'].astype(str) >= start) & (df['year'].astype(str) <= stop)]

            #Create plot
            create_plot(df = df, area=area, x='date', y = 'conductivity', y_lim = 140, g0 = 18, g1=30, b0=0, b1=18, y0=30, y1=70, r0=70, r1=140)

        
        if param == 'pH':

            #create date slider
            year = [f'{i}' for i in range(2011, 2023) ]
            start, stop = st.select_slider('Select time frame', options=year, value=('2011', '2022'))

            #options for catchment area
            options = df['sample_pt_desc'].unique().tolist()
            area = st.sidebar.selectbox("Choose Catchment area", options)

            #filter by catchment area
            df = df.loc[df['sample_pt_desc'] == area]

            #Filter data by year
            df = df.loc[(df['year'].astype(str) >= start) & (df['year'].astype(str) <= stop)]

            #Create plot
            fig = go.Figure() 

            #Line chart
            fig.add_trace(go.Scatter(x=df['date'], y=df['pH'], mode='lines',
                    line=dict(color='black', width=3),
                    connectgaps=True))

            #update axis
            fig.update_layout(
                xaxis=dict(
                    showline=True,
                    showgrid=False,
                    showticklabels=True,
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
                        fillcolor="green", opacity=0.3, line_width=0)
            
            fig.add_hrect(y0=8.4, y1=8.5,
                        fillcolor="green", opacity=0.3, line_width=0)

            fig.add_hrect(y0=7, y1=8.4, 
                        annotation_text="Ideal", annotation_position="right",
                        annotation=dict(font_size=20, font_family="Times New Roman"),
                        fillcolor="blue", opacity=0.3, line_width=0)

            fig.add_hrect(y0=6, y1=6.5, 
                        annotation_text="Tolerable", annotation_position="right",
                        annotation=dict(font_size=20, font_family="Times New Roman"),
                        fillcolor="yellow", opacity=0.3, line_width=0)
            
            fig.add_hrect(y0=8.5, y1=9, 
                        annotation_text="Tolerable", annotation_position="right",
                        annotation=dict(font_size=20, font_family="Times New Roman"),
                        fillcolor="yellow", opacity=0.3, line_width=0)

            fig.add_hrect(y0=0, y1=6, 
                        annotation_text="Unacceptable", annotation_position="right",
                        annotation=dict(font_size=20, font_family="Times New Roman"),
                        fillcolor="red", opacity=0.3, line_width=0)
            fig.add_hrect(y0=9, y1=11, 
                        annotation_text="Unacceptable", annotation_position="right",
                        annotation=dict(font_size=20, font_family="Times New Roman"),
                        fillcolor="red", opacity=0.3, line_width=0)
            st.plotly_chart(fig)

        
        if param == 'E.coli':

            #create date slider
            year = [f'{i}' for i in range(2011, 2023) ]
            start, stop = st.select_slider('Select time frame', options=year, value=('2011', '2022'))

            #Catchment area options
            options = df['sample_pt_desc'].unique().tolist()
            area = st.sidebar.selectbox("Choose Catchment area", options)

            #filter by catchment area
            df = df.loc[df['sample_pt_desc'] == area]

            #Filter data by year
            df = df.loc[(df['year'].astype(str) >= start) & (df['year'].astype(str) <= stop)]

            #Create plot
            fig = go.Figure() 
            #Line chart
            fig.add_trace(go.Scatter(x=df['date'], y=df['e_coli'], mode='lines',
                    line=dict(color='black', width=3),
                    connectgaps=True))
            #update axis
            fig.update_layout(
                xaxis=dict(
                    showline=True,
                    showgrid=False,
                    showticklabels=True,
                    tickangle=330),
                yaxis=dict(
                    showgrid=False,
                    zeroline=True,
                    showline=True,
                    showticklabels=True,
                    title= f'{param} (mg/l)',
                    type='log',
                    range=[2, 5]) )
            # Add shapes
            fig.add_hrect(y0=130, y1=200, 
                        annotation_text="Acceptable", annotation_position="right",
                        annotation=dict(font_size=20, font_family="Times New Roman"),
                        fillcolor="green", opacity=0.3, line_width=0)
            fig.add_hrect(y0=0, y1=130, 
                        annotation_text="Ideal", annotation_position="right",
                        annotation=dict(font_size=20, font_family="Times New Roman"),
                        fillcolor="blue", opacity=0.3, line_width=0)
            fig.add_hrect(y0=200, y1=400, 
                        annotation_text="Tolerable", annotation_position="right",
                        annotation=dict(font_size=20, font_family="Times New Roman"),
                        fillcolor="yellow", opacity=0.3, line_width=0)
            fig.add_hrect(y0=400, y1=100000, 
                        annotation_text="Unacceptable", annotation_position="right",
                        annotation=dict(font_size=20, font_family="Times New Roman"),
                        fillcolor="red", opacity=0.3, line_width=0)
            
            st.plotly_chart(fig)

        if param == 'Nitrate NO3 as N':

            #create date slider
            year = [f'{i}' for i in range(2011, 2023) ]
            start, stop = st.select_slider('Select time frame', options=year, value=('2011', '2022'))

            #options for catchment area
            options = df['sample_pt_desc'].unique().tolist()
            area = st.sidebar.selectbox("Choose Catchment area", options)

            #filter by catchment area
            df = df.loc[df['sample_pt_desc'] == area]

            #Filter data by year
            df = df.loc[(df['year'].astype(str) >= start) & (df['year'].astype(str) <= stop)]

            #create plot
            create_plot(df = df, area=area, x='date', y = 'nitrate', y_lim = 8, g0 = 0.5, g1=3, b0=0, b1=0.5, y0=3, y1=6, r0=6, r1=8)
        
            
        if param == 'Phosphate PO4 as P':

            #create date slider
            year = [f'{i}' for i in range(2011, 2023) ]
            start, stop = st.select_slider('Select time frame', options=year, value=('2011', '2022'))

            #Catchment area options
            options = df['sample_pt_desc'].unique().tolist()
            area = st.sidebar.selectbox("Choose Catchment area", options)

            #filter by catchment area
            df = df.loc[df['sample_pt_desc'] == area]

            #Filter data by year
            df = df.loc[(df['year'].astype(str) >= start) & (df['year'].astype(str) <= stop)]

            #Create plot
            fig = go.Figure() 
            
            fig.add_trace(go.Scatter(x=df['date'], y=df['phosphate'], mode='lines',
                    line=dict(color='black', width=3),
                    connectgaps=True))
            #update axis
            fig.update_layout(
                xaxis=dict(
                    showline=True,
                    showgrid=False,
                    showticklabels=True,
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
                        fillcolor="green", opacity=0.3, line_width=0)
            fig.add_hrect(y0=0, y1=0, 
                        fillcolor="blue", opacity=0.3, line_width=0)
            fig.add_hrect(y0=0.03, y1=0.05, 
                        fillcolor="yellow", opacity=0.3, line_width=0)

            fig.add_hrect(y0=0.05, y1=3, 
                        annotation_text="Unacceptable", annotation_position="right",
                        annotation=dict(font_size=20, font_family="Times New Roman"),
                        fillcolor="red",opacity=0.3, line_width=0)
            st.plotly_chart(fig)
    
    if river == 'Blesbokspruit':

        df = data.copy()
        df = df.loc[df['river_id'] == 2]

        # Step: Sort column(s) year ascending (A-Z), qtr ascending (A-Z)
        df = df.sort_values(by=['year', 'qtr'], ascending=[True, True])

        # Step: Create new column 'date' from formula 'quarter + " " + year.astype(str)'
        df['date'] = df['quarter'] + " " + df['year'].astype(str)

        #create sidebar options for parameters
        parameters = ['Conductivity','E.coli','Nitrate NO3 as N','pH','Phosphate PO4 as P', 'Overall Compliance']
        param = st.sidebar.selectbox("Choose Parameter", parameters)   

        if param == 'Overall Compliance':

            para = st.sidebar.radio('', ['Physical', 'Chemical', 'Overall']) 

            #create options for catchment area
            options = df['sample_pt_desc'].unique().tolist()
            area = st.sidebar.selectbox("Choose Catchment area", options)
    
        
            #filter by catchment area
            df = df.loc[df['sample_pt_desc'] == area]
            
            
            if para == 'Physical':

                make_forecast(df, 'physical_compliance_percentage')

            if para == 'Chemical':

                make_forecast(df, 'chemical_compliance_percentage')

            if para == 'Overall':
                
                make_forecast(df, 'overall_compliance_percentage')

        if param == 'COD':

            #create date slider
            year = [f'{i}' for i in range(2011, 2023) ]
            start, stop = st.select_slider('Select time frame', options=year, value=('2011', '2022'))

            
            #create options for catchment area
            options = df['sample_pt_desc'].loc[df['cod'] > 0].unique().tolist()
            area = st.sidebar.selectbox("Choose Catchment area", options)

            #Filter data by catchment area
            df = df.loc[df['sample_pt_desc'] == area]

            #Filter data by year
            df = df.loc[(df['year'].astype(str) >= start) & (df['year'].astype(str) <= stop)]

            #Create plot
            create_plot(df = df, area=area, x='date', y = 'cod', y_lim = 60, g0 = 20, g1=35, b0=0, b1=19, y0=35, y1=55, r0=55, r1=60)


        if param == 'Conductivity':

            #create date slider
            year = [f'{i}' for i in range(2011, 2023) ]
            start, stop = st.select_slider('Select time frame', options=year, value=('2011', '2022'))

            #catchment area options
            options = df['sample_pt_desc'].loc[df['conductivity'] > 0].unique().tolist()
            area = st.sidebar.selectbox("Choose Catchment area", options)

            #filter by catchment area
            df = df.loc[df['sample_pt_desc'] == area]

            #Filter data by year
            df = df.loc[(df['year'].astype(str) >= start) & (df['year'].astype(str) <= stop)]

            #Create plot
            create_plot(df = df, area=area, x='date', y = 'conductivity', y_lim = 140, g0 = 18, g1=30, b0=0, b1=18, y0=30, y1=70, r0=70, r1=140)

        
        if param == 'pH':

            #create date slider
            year = [f'{i}' for i in range(2011, 2023) ]
            start, stop = st.select_slider('Select time frame', options=year, value=('2011', '2022'))

            #options for catchment area
            options = df['sample_pt_desc'].loc[df['pH'] > 0].unique().tolist()
            area = st.sidebar.selectbox("Choose Catchment area", options)

            #filter by catchment area
            df = df.loc[df['sample_pt_desc'] == area]

            #Filter data by year
            df = df.loc[(df['year'].astype(str) >= start) & (df['year'].astype(str) <= stop)]

            #Create plot
            fig = go.Figure() 

            #Line chart
            fig.add_trace(go.Scatter(x=df['date'], y=df['pH'], mode='lines',
                    line=dict(color='black', width=3),
                    connectgaps=True))

            #update axis
            fig.update_layout(
                xaxis=dict(
                    showline=True,
                    showgrid=False,
                    showticklabels=True,
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
                        fillcolor="green", opacity=0.3, line_width=0)
            
            fig.add_hrect(y0=8.4, y1=8.5,
                        fillcolor="green", opacity=0.3, line_width=0)

            fig.add_hrect(y0=7, y1=8.4, 
                        annotation_text="Ideal", annotation_position="right",
                        annotation=dict(font_size=20, font_family="Times New Roman"),
                        fillcolor="blue", opacity=0.3, line_width=0)

            fig.add_hrect(y0=6, y1=6.5, 
                        annotation_text="Tolerable", annotation_position="right",
                        annotation=dict(font_size=20, font_family="Times New Roman"),
                        fillcolor="yellow", opacity=0.3, line_width=0)
            
            fig.add_hrect(y0=8.5, y1=9, 
                        annotation_text="Tolerable", annotation_position="right",
                        annotation=dict(font_size=20, font_family="Times New Roman"),
                        fillcolor="yellow", opacity=0.3, line_width=0)

            fig.add_hrect(y0=0, y1=6, 
                        annotation_text="Unacceptable", annotation_position="right",
                        annotation=dict(font_size=20, font_family="Times New Roman"),
                        fillcolor="red", opacity=0.3, line_width=0)
            fig.add_hrect(y0=9, y1=11, 
                        annotation_text="Unacceptable", annotation_position="right",
                        annotation=dict(font_size=20, font_family="Times New Roman"),
                        fillcolor="red", opacity=0.3, line_width=0)
            st.plotly_chart(fig)

        
        if param == 'E.coli':

            #create date slider
            year = [f'{i}' for i in range(2011, 2023) ]
            start, stop = st.select_slider('Select time frame', options=year, value=('2011', '2022'))

            #Catchment area options
            options = df['sample_pt_desc'].loc[df['e_coli'] > 0].unique().tolist()
            area = st.sidebar.selectbox("Choose Catchment area", options)

            #filter by catchment area
            df = df.loc[df['sample_pt_desc'] == area]

            #Filter data by year
            df = df.loc[(df['year'].astype(str) >= start) & (df['year'].astype(str) <= stop)]

            #Create plot
            fig = go.Figure() 
            #Line chart
            fig.add_trace(go.Scatter(x=df['date'], y=df['e_coli'], mode='lines',
                    line=dict(color='black', width=3),
                    connectgaps=True))
            #update axis
            fig.update_layout(
                xaxis=dict(
                    showline=True,
                    showgrid=False,
                    showticklabels=True,
                    tickangle=330),
                yaxis=dict(
                    showgrid=False,
                    zeroline=True,
                    showline=True,
                    showticklabels=True,
                    title= f'{param} (mg/l)',
                    type='log',
                    range=[0, 5]) )
            # Add shapes
            fig.add_hrect(y0=130, y1=200, 
                        annotation_text="Acceptable", annotation_position="right",
                        annotation=dict(font_size=20, font_family="Times New Roman"),
                        fillcolor="green", opacity=0.3, line_width=0)
            fig.add_hrect(y0=0, y1=130, 
                        annotation_text="Ideal", annotation_position="right",
                        annotation=dict(font_size=20, font_family="Times New Roman"),
                        fillcolor="blue", opacity=0.3, line_width=0)
            fig.add_hrect(y0=200, y1=400, 
                        annotation_text="Tolerable", annotation_position="right",
                        annotation=dict(font_size=20, font_family="Times New Roman"),
                        fillcolor="yellow", opacity=0.3, line_width=0)
            fig.add_hrect(y0=400, y1=100000, 
                        annotation_text="Unacceptable", annotation_position="right",
                        annotation=dict(font_size=20, font_family="Times New Roman"),
                        fillcolor="red", opacity=0.3, line_width=0)
            
            st.plotly_chart(fig)

        if param == 'Nitrate NO3 as N':

            #create date slider
            year = [f'{i}' for i in range(2011, 2023) ]
            start, stop = st.select_slider('Select time frame', options=year, value=('2011', '2022'))

            #options for catchment area
            options = df['sample_pt_desc'].loc[df['nitrate'] > 0].unique().tolist()
            area = st.sidebar.selectbox("Choose Catchment area", options)

            #filter by catchment area
            df = df.loc[df['sample_pt_desc'] == area]

            #Filter data by year
            df = df.loc[(df['year'].astype(str) >= start) & (df['year'].astype(str) <= stop)]

            #create plot
            create_plot(df = df, area=area, x='date', y = 'nitrate', y_lim = 8, g0 = 0.5, g1=3, b0=0, b1=0.5, y0=3, y1=6, r0=6, r1=8)
        
            
        if param == 'Phosphate PO4 as P':

            #create date slider
            year = [f'{i}' for i in range(2011, 2023) ]
            start, stop = st.select_slider('Select time frame', options=year, value=('2011', '2022'))

            #Catchment area options
            options = df['sample_pt_desc'].loc[df['phosphate'] > 0].unique().tolist()
            area = st.sidebar.selectbox("Choose Catchment area", options)

            #filter by catchment area
            df = df.loc[df['sample_pt_desc'] == area]

            #Filter data by year
            df = df.loc[(df['year'].astype(str) >= start) & (df['year'].astype(str) <= stop)]

            #Create plot
            fig = go.Figure() 
            
            fig.add_trace(go.Scatter(x=df['date'], y=df['phosphate'], mode='lines',
                    line=dict(color='black', width=3),
                    connectgaps=True))
            #update axis
            fig.update_layout(
                xaxis=dict(
                    showline=True,
                    showgrid=False,
                    showticklabels=True,
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
                        fillcolor="green", opacity=0.3, line_width=0)
            fig.add_hrect(y0=0, y1=0, 
                        fillcolor="blue", opacity=0.3, line_width=0)
            fig.add_hrect(y0=0.03, y1=0.05, 
                        fillcolor="yellow", opacity=0.3, line_width=0)

            fig.add_hrect(y0=0.05, y1=3, 
                        annotation_text="Unacceptable", annotation_position="right",
                        annotation=dict(font_size=20, font_family="Times New Roman"),
                        fillcolor="red",opacity=0.3, line_width=0)
            st.plotly_chart(fig)

    if river == 'Klip':
        df = data.copy()
        df = df.loc[df['river_id'] == 3]

        # Step: Sort column(s) year ascending (A-Z), qtr ascending (A-Z)
        df = df.sort_values(by=['year', 'qtr'], ascending=[True, True])

        # Step: Create new column 'date' from formula 'quarter + " " + year.astype(str)'
        df['date'] = df['quarter'] + " " + df['year'].astype(str)

        #create sidebar options for parameters
        parameters = ['COD', 'Conductivity','E.coli','Nitrate NO3 as N','pH','Phosphate PO4 as P', 'Overall Compliance']
        param = st.sidebar.selectbox("Choose Parameter", parameters)   

        if param == 'Overall Compliance':

            para = st.sidebar.radio('', ['Physical', 'Chemical', 'Overall']) 
            
            #create options for catchment area
            options = df['sample_pt_desc'].unique().tolist()
            area = st.sidebar.selectbox("Choose Catchment area", options)
            
        
            #filter by catchment area
            df = df.loc[df['sample_pt_desc'] == area]

        
            if para == 'Physical':

                make_forecast(df, 'physical_compliance_percentage')

            if para == 'Chemical':

                make_forecast(df, 'chemical_compliance_percentage')

            if para == 'Overall':
                
                make_forecast(df, 'overall_compliance_percentage')

        if param == 'COD':

            #create date slider
            year = [f'{i}' for i in range(2011, 2023) ]
            start, stop = st.select_slider('Select time frame', options=year, value=('2011', '2022'))


            #create options for catchment area
            options = df['sample_pt_desc'].loc[df['cod'] > 0].unique().tolist()
            area = st.sidebar.selectbox("Choose Catchment area", options)

            #Filter data by catchment area
            df = df.loc[df['sample_pt_desc'] == area]

            #Filter data by year
            df = df.loc[(df['year'].astype(str) >= start) & (df['year'].astype(str) <= stop)]

            #Create plot
            create_plot(df = df, area=area, x='date', y = 'cod', y_lim = 60, g0 = 20, g1=35, b0=0, b1=19, y0=35, y1=55, r0=55, r1=60)


        if param == 'Conductivity':

            #create date slider
            year = [f'{i}' for i in range(2011, 2023) ]
            start, stop = st.select_slider('Select time frame', options=year, value=('2011', '2022'))

            #catchment area options
            options = df['sample_pt_desc'].loc[df['conductivity'] > 0].unique().tolist()
            area = st.sidebar.selectbox("Choose Catchment area", options)

            #filter by catchment area
            df = df.loc[df['sample_pt_desc'] == area]

            #Filter data by year
            df = df.loc[(df['year'].astype(str) >= start) & (df['year'].astype(str) <= stop)]

            #Create plot
            create_plot(df = df, area=area, x='date', y = 'conductivity', y_lim = 140, g0 = 18, g1=30, b0=0, b1=18, y0=30, y1=70, r0=70, r1=140)

        
        if param == 'pH':

            #create date slider
            year = [f'{i}' for i in range(2011, 2023) ]
            start, stop = st.select_slider('Select time frame', options=year, value=('2011', '2022'))

            #options for catchment area
            options = df['sample_pt_desc'].loc[df['pH'] > 0].unique().tolist()
            area = st.sidebar.selectbox("Choose Catchment area", options)

            #filter by catchment area
            df = df.loc[df['sample_pt_desc'] == area]

            #Filter data by year
            df = df.loc[(df['year'].astype(str) >= start) & (df['year'].astype(str) <= stop)]

            #Create plot
            fig = go.Figure() 

            #Line chart
            fig.add_trace(go.Scatter(x=df['date'], y=df['pH'], mode='lines',
                    line=dict(color='black', width=3),
                    connectgaps=True))

            #update axis
            fig.update_layout(
                xaxis=dict(
                    showline=True,
                    showgrid=False,
                    showticklabels=True,
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
                        fillcolor="green", opacity=0.3, line_width=0)
            
            fig.add_hrect(y0=8.4, y1=8.5,
                        fillcolor="green", opacity=0.3, line_width=0)

            fig.add_hrect(y0=7, y1=8.4, 
                        annotation_text="Ideal", annotation_position="right",
                        annotation=dict(font_size=20, font_family="Times New Roman"),
                        fillcolor="blue", opacity=0.3, line_width=0)

            fig.add_hrect(y0=6, y1=6.5, 
                        annotation_text="Tolerable", annotation_position="right",
                        annotation=dict(font_size=20, font_family="Times New Roman"),
                        fillcolor="yellow", opacity=0.3, line_width=0)
            
            fig.add_hrect(y0=8.5, y1=9, 
                        annotation_text="Tolerable", annotation_position="right",
                        annotation=dict(font_size=20, font_family="Times New Roman"),
                        fillcolor="yellow", opacity=0.3, line_width=0)

            fig.add_hrect(y0=0, y1=6, 
                        annotation_text="Unacceptable", annotation_position="right",
                        annotation=dict(font_size=20, font_family="Times New Roman"),
                        fillcolor="red", opacity=0.3, line_width=0)
            fig.add_hrect(y0=9, y1=11, 
                        annotation_text="Unacceptable", annotation_position="right",
                        annotation=dict(font_size=20, font_family="Times New Roman"),
                        fillcolor="red", opacity=0.3, line_width=0)
            st.plotly_chart(fig)

        
        if param == 'E.coli':

            #create date slider
            year = [f'{i}' for i in range(2011, 2023) ]
            start, stop = st.select_slider('Select time frame', options=year, value=('2011', '2022'))

            #Catchment area options
            options = df['sample_pt_desc'].loc[df['e_coli'] > 0].unique().tolist()
            area = st.sidebar.selectbox("Choose Catchment area", options)

            #filter by catchment area
            df = df.loc[df['sample_pt_desc'] == area]

            #Filter data by year
            df = df.loc[(df['year'].astype(str) >= start) & (df['year'].astype(str) <= stop)]

            #Create plot
            fig = go.Figure() 
            #Line chart
            fig.add_trace(go.Scatter(x=df['date'], y=df['e_coli'], mode='lines',
                    line=dict(color='black', width=3),
                    connectgaps=True))
            #update axis
            fig.update_layout(
                xaxis=dict(
                    showline=True,
                    showgrid=False,
                    showticklabels=True,
                    tickangle=330),
                yaxis=dict(
                    showgrid=False,
                    zeroline=True,
                    showline=True,
                    showticklabels=True,
                    title= f'{param} (mg/l)',
                    type='log',
                    range=[0, 5]) )
            # Add shapes
            fig.add_hrect(y0=130, y1=200, 
                        annotation_text="Acceptable", annotation_position="right",
                        annotation=dict(font_size=20, font_family="Times New Roman"),
                        fillcolor="green", opacity=0.3, line_width=0)
            fig.add_hrect(y0=0, y1=130, 
                        annotation_text="Ideal", annotation_position="right",
                        annotation=dict(font_size=20, font_family="Times New Roman"),
                        fillcolor="blue", opacity=0.3, line_width=0)
            fig.add_hrect(y0=200, y1=400, 
                        annotation_text="Tolerable", annotation_position="right",
                        annotation=dict(font_size=20, font_family="Times New Roman"),
                        fillcolor="yellow", opacity=0.3, line_width=0)
            fig.add_hrect(y0=400, y1=100000, 
                        annotation_text="Unacceptable", annotation_position="right",
                        annotation=dict(font_size=20, font_family="Times New Roman"),
                        fillcolor="red", opacity=0.3, line_width=0)
            
            st.plotly_chart(fig)

        if param == 'Nitrate NO3 as N':

            #create date slider
            year = [f'{i}' for i in range(2011, 2023) ]
            start, stop = st.select_slider('Select time frame', options=year, value=('2011', '2022'))

            #options for catchment area
            options = df['sample_pt_desc'].loc[df['nitrate'] > 0].unique().tolist()
            area = st.sidebar.selectbox("Choose Catchment area", options)

            #filter by catchment area
            df = df.loc[df['sample_pt_desc'] == area]

            #Filter data by year
            df = df.loc[(df['year'].astype(str) >= start) & (df['year'].astype(str) <= stop)]

            #create plot
            create_plot(df = df, area=area, x='date', y = 'nitrate', y_lim = 8, g0 = 0.5, g1=3, b0=0, b1=0.5, y0=3, y1=6, r0=6, r1=8)
        
            
        if param == 'Phosphate PO4 as P':

            #create date slider
            year = [f'{i}' for i in range(2011, 2023) ]
            start, stop = st.select_slider('Select time frame', options=year, value=('2011', '2022'))

            #Catchment area options
            options = df['sample_pt_desc'].loc[df['phosphate'] > 0].unique().tolist()
            area = st.sidebar.selectbox("Choose Catchment area", options)

            #filter by catchment area
            df = df.loc[df['sample_pt_desc'] == area]

            #Filter data by year
            df = df.loc[(df['year'].astype(str) >= start) & (df['year'].astype(str) <= stop)]

            #Create plot
            fig = go.Figure() 
            
            fig.add_trace(go.Scatter(x=df['date'], y=df['phosphate'], mode='lines',
                    line=dict(color='black', width=3),
                    connectgaps=True))
            #update axis
            fig.update_layout(
                xaxis=dict(
                    showline=True,
                    showgrid=False,
                    showticklabels=True,
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
                        fillcolor="green", opacity=0.3, line_width=0)
            fig.add_hrect(y0=0, y1=0, 
                        fillcolor="blue", opacity=0.3, line_width=0)
            fig.add_hrect(y0=0.03, y1=0.05, 
                        fillcolor="yellow", opacity=0.3, line_width=0)

            fig.add_hrect(y0=0.05, y1=3, 
                        annotation_text="Unacceptable", annotation_position="right",
                        annotation=dict(font_size=20, font_family="Times New Roman"),
                        fillcolor="red",opacity=0.3, line_width=0)
            st.plotly_chart(fig)

#Interactive map page
if selection == 'Water Quality':
    dm.main()
