
# # %%
import streamlit as st
import pandas as pd
import folium as fl
from streamlit_folium import st_folium
import pandas as pd
import geopandas as gpd
from branca.element import Template, MacroElement
import randDataProvider as RD


#References
"""
- popup: https://towardsdatascience.com/use-html-in-folium-maps-a-comprehensive-guide-for-data-scientists-3af10baf9190
- Legend: https://nbviewer.org/gist/talbertc-usgs/18f8901fc98f109f2b71156cf3ac81cd

- Icons: https://getbootstrap.com/docs/3.3/components/#glyphicons-glyphs
"""


#Legend template
template = """

{% macro html(this, kwargs) %}

<!doctype html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>jQuery UI Draggable - Default functionality</title>
	<link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

	<script src="https://code.jquery.com/jquery-1.12.4.js"></script>
	<script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
	
	<script>
	$( function() {
		$( "#maplegend" ).draggable({
										start: function (event, ui) {
												$(this).css({
														right: "auto",
														top: "auto",
														bottom: "auto"
												});
										}
								});
});

	</script>
</head>
<body>

 
<div id='maplegend' class='maplegend' 
		style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
		 border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 20px;'>
		 
<div class='legend-title'>Overall Compliance Legend</div>
<div class='legend-scale'>
	<ul class='legend-labels'>
		<li><span style='background:red;opacity:0.7;'></span>Unacceptable <50%</li>
		<li><span style='background:#FFA62F;opacity:0.7;'></span>Tolerable 50%-70%</li>
		<li><span style='background:#4AA02C;opacity:0.7;'></span>Acceptable 70%-90%</li>
		<li><span style='background:#3BB9FF;opacity:0.7;'></span>Ideal >90%</li>

	</ul>
</div>
</div>
 
</body>
</html>

<style type='text/css'>
	.maplegend .legend-title {
		text-align: left;
		margin-bottom: 5px;
		font-weight: bold;
		font-size: 90%;
		}
	.maplegend .legend-scale ul {
		margin: 0;
		margin-bottom: 5px;
		padding: 0;
		float: left;
		list-style: none;
		}
	.maplegend .legend-scale ul li {
		font-size: 80%;
		list-style: none;
		margin-left: 0;
		line-height: 18px;
		margin-bottom: 2px;
		}
	.maplegend ul.legend-labels li span {
		display: block;
		float: left;
		height: 16px;
		width: 30px;
		margin-right: 5px;
		margin-left: 0;
		border: 1px solid #999;
		}
	.maplegend .legend-source {
		font-size: 80%;
		color: #777;
		clear: both;
		}
	.maplegend a {
		color: #777;
		}
</style>
{% endmacro %}"""

#Popup function
def popup_html(df):
		site_description=df['sample_pt_desc'] 
		sample_id=df['sample_id']
		institution_img = 'https://financialtribune.com/sites/default/files/field/image/17january/05_wastewater_300_0.jpg'
		institution_url = 'https://www.dws.gov.za/'

		left_col_color = "#7CC4F5"
		right_col_color = "#f2f0d3"


		
		html = """<!DOCTYPE html>

<center><h5 style="margin-bottom:5"; width="200px">{}</h4>""".format(site_description) + """</center>

</html>
"""
		return html

#Compliance color chooser function
def compliance_color(row):
	if row['overall_compliance_percentage'] < 50:
		return 'red'
	elif row['overall_compliance_percentage'] < 70:
		return 'orange'
	elif row['overall_compliance_percentage'] < 90:
		return 'green'
	elif row['overall_compliance_percentage'] > 89:
		return 'blue'
	
#Year and quarter selection function
def display_time_filters(df):
		year_list = list(df['year'].unique())
		year_list.sort()
		year = st.sidebar.selectbox('Year', year_list, len(year_list)-1)
		quarter = st.sidebar.radio('Quarter', ['Jan-Mar', 'Apr-Jun', 'Jul-Sep', 'Oct-Dec'])
		st.header(f'{year} {quarter}')
		return year, quarter

#Site selection function
def display_site_filter(df, site_name):
		site_list = [''] + list(df['sample_pt_desc'].unique())
		site_list.sort()
		site_index = site_list.index(site_name) if site_name and site_name in site_list else 0
		return st.sidebar.selectbox('Site', site_list, site_index)

#Parameter selection function
def display_param_filter():
		param_list = [''] + ['cod', 'conductivity','e_coli','nitrate','pH','phosphate']
		param_list.sort()
		return st.sidebar.selectbox('Parameter', param_list)

#Parameter thresholds function
def param_filter(param):
	if param == 'e_coli':
		return 0,400
	elif param == 'cod':
		return 0,30
	elif param == 'conductivity':
		return 0,70
	elif param == 'nitrate':
		return 0,6
	elif param == 'pH':
		return 6,9
	elif param == 'phosphate':
		return 0,0.05

#Get compliances function
def display_compliance(df, year, quarter, site_name, column, string_format='${:,}', is_median=False):
		df = df[(df['year'] == year) & (df['quarter'] == quarter)]
		if site_name:
				df = df[df['sample_pt_desc'] == site_name]
		df.drop_duplicates(inplace=True)
		
		st.metric(column[1],f"{round(df[column[0]].mean(),2)}%")


# def display_site_type_filter():
#     return st.sidebar.radio('Site Type', ['test', 'effluent'])

#Map creation function 
def map(df,only1,only2,only3,only4,only5):
	vaal_map = fl.Map(location=[-26.454, 28.085], zoom_start=9, scrollWheelZoom=False, tiles='Stamen Terrain')
			
	river = fl.FeatureGroup(name='River')
	river.add_children(fl.GeoJson(data=only1["geometry"],name="Streams",style_function=lambda x:{'weight':1}))
	river.add_children(fl.GeoJson(data=only2["geometry"],name="Tributaries",style_function=lambda x:{'weight':1}))
	river.add_children(fl.GeoJson(data=only3["geometry"],name="River branches",style_function=lambda x:{'weight':2}))
	river.add_children(fl.GeoJson(data=only4["geometry"],name="Main river",style_function=lambda x:{'weight':3}))
	river.add_children(fl.GeoJson(data=only5["geometry"],name="Main river",style_function=lambda x:{'weight':3}))
	vaal_map.add_children(river)

	vaal = fl.FeatureGroup(name='Vaal')

	for _, site in df.iterrows():
			vaal.add_children(fl.Marker(
			location=[site['latitude'], site['longitude']],
			popup = fl.Popup(fl.Html(popup_html(site), script=True), max_width=500),
			tooltip = site['sample_pt_desc'],
							icon = fl.Icon(color = compliance_color(site), icon='glyphicon glyphicon-tint',)
	))
	vaal_map.add_children(vaal)

	macro = MacroElement()
	macro._template = Template(template)

	vaal_map.get_root().add_child(macro)

	fl.LayerControl().add_to(vaal_map)
	
	st_map = st_folium(vaal_map, width=700, height=450)

	site_name = ''
	if st_map['last_active_drawing']:
			coordinates = st_map['last_active_drawing']['geometry']['coordinates']
			site_name = df['sample_pt_desc'][(df['latitude']==coordinates[1]) & (df['longitude']==coordinates[0])].item()
			
	return site_name

#Map display function
def display_map(df, year, quarter,param,only1,only2,only3,only4,only5):
		if param == '':
			df = df[(df['year'] == year) & (df['quarter'] == quarter)]

			return map(df,only1,only2,only3,only4,only5)
		else:
			low_end,high_end = param_filter(param)
			df = df[(df['year'] == year) & (df['quarter'] == quarter) & ((df[param] < low_end) | (df[param] > high_end))]

			return map(df,only1,only2,only3,only4,only5)



#Load data from databricks function  
@st.cache(persist=True,ttl=3600)
def get_data_from_databricks(query): 
	data = RD.get_data(query)
	data.to_csv('data/merged.csv', index = False)
	return data



def main():

		#Load Data
		query = '''

        SELECT sp.sample_pt_desc, sp.latitude, sp.longitude, sp.sample_id, ra.year, ra.quarter, ra.cod, ra.conductivity, ra.e_coli,
                ra.pH, ra.nitrate, ra.phosphate, ra.physical_compliance_percentage, ra.chemical_compliance_percentage,
                ra.bacteriological_compliance_percentage, 
                ra.biological_compliance_percentage, ra.overall_compliance_percentage, ri.river

        FROM rand as ra
        INNER JOIN sampling_points as sp
        ON ra.sample_id = sp.sample_id
        INNER JOIN rivers as ri
        ON ra.river_id = ri.river_id

        '''

		#Load data
		vaal_df = get_data_from_databricks(query)
		# vaal_df = pd.read_csv('data/merged.csv')
		only1 = gpd.read_file('data/river/only1.shp')
		only2 = gpd.read_file('data/river/only2.shp')
		only3 = gpd.read_file('data/river/only3.shp')
		only4 = gpd.read_file('data/river/only4.shp')
		only5 = gpd.read_file('data/river/only5.shp')

		#Display Filters and Map
		year, quarter = display_time_filters(vaal_df)
		param = display_param_filter()
		site_name = display_map(vaal_df, year, quarter,param,only1,only2,only3,only4,only5)
		site_name = display_site_filter(vaal_df, site_name)
		# site_type = display_site_type_filter()

		#Display Metrics
		st.subheader(f'{site_name} Compliance')
		# st.subheader(f'{site_name} {site_type} Facts')

		#col titles
		phys = ['physical_compliance_percentage', 'Physical']
		chem = ['chemical_compliance_percentage', 'Chemical']
		bact = ['bacteriological_compliance_percentage', 'Bacteriological']
		bio = ['biological_compliance_percentage', 'Biological']
		overall = ['overall_compliance_percentage', 'Overall']
		col1, col2, col3, col4, col5 = st.columns(5)
		with col1:
				display_compliance(df=vaal_df, year=year, quarter=quarter, site_name=site_name, column=phys)
		with col2:
				display_compliance(df=vaal_df, year=year, quarter=quarter, site_name=site_name, column=chem)
		with col3:
				display_compliance(df=vaal_df, year=year, quarter=quarter, site_name=site_name, column=bact)        
		with col4:
				display_compliance(df=vaal_df, year=year, quarter=quarter, site_name=site_name, column=bio)  
		with col5:
				display_compliance(df=vaal_df, year=year, quarter=quarter, site_name=site_name, column=overall)  


if __name__ == "__main__":
		main()