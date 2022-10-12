from audioop import avg
from turtle import title
import streamlit as st
import pandas as pd
import folium as fl
from streamlit_folium import st_folium
import pandas as pd
import geopandas as gpd
from branca.element import Template, MacroElement  

#References
"""
- Popup: https://towardsdatascience.com/folium-map-how-to-create-a-table-style-pop-up-with-html-code-76903706b88a
- popup+: https://towardsdatascience.com/use-html-in-folium-maps-a-comprehensive-guide-for-data-scientists-3af10baf9190
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
		<li><span style='background:yellow;opacity:0.7;'></span>Tolerable 50%-70%</li>
		<li><span style='background:green;opacity:0.7;'></span>Acceptable 70%-90%</li>
		<li><span style='background:blue;opacity:0.7;'></span>Ideal >90%</li>

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

#Popup
def popup_html(df):
		site_description=df['Sample_pt_desc'] 
		sample_id=df['sample_id']
		year = df['year']
		quarter = df['quarter']
		physical =df['physical_compliance_%']                    
		chemical = df['chemical_compliance_%']
		bacteorological = df['bacteriological_compliance_%']
		biological = df['biological_compliance_%']
		institution_img = 'https://financialtribune.com/sites/default/files/field/image/17january/05_wastewater_300_0.jpg'
		institution_url = 'https://www.dws.gov.za/'

		left_col_color = "#19a7bd"
		right_col_color = "#f2f0d3"


		
		html = """<!DOCTYPE html>

<center><img src=\"""" + institution_img + """\" alt="logo" width=100 height=100 ></center>
<center><h4 style="margin-bottom:5"; width="200px">{}</h4>""".format(site_description) + """</center>
<center><a href=\"""" + institution_url + """\">Go to the Institution's Website</a></center>
<center> <table style="height: 126px; width: 350px;">
<tbody>
<tr>
<td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Year</span></td>
<td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(year) + """
</tr>
<tr>
<td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Quarter</span></td>
<td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(quarter) + """
</tr>
<tr>
<td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Sample ID</span></td>
<td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(sample_id) + """
</tr>
<tr>
<td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Physical compliance</span></td>
<td style="width: 150px;background-color: """+ right_col_color +""";">{}%</td>""".format(physical) + """
</tr>
<tr>
<td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Chemical compliance</span></td>
<td style="width: 150px;background-color: """+ right_col_color +""";">{}%</td>""".format(chemical) + """
</tr>
<tr>
<td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Bacteriological compliance</span></td>
<td style="width: 150px;background-color: """+ right_col_color +""";">{}%</td>""".format(bacteorological) + """
</tr>
<tr>
<td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Biological compliance</span></td>
<td style="width: 150px;background-color: """+ right_col_color +""";">{}%""".format(biological) + """
</tr>
</tbody>
</table>
<br />
<br />
</center>
</html>
"""
		return html

#Compliance color chooser
def compliance_color(row):
	if row['overall_compliance_%'] < 50:
		return 'red'
	elif row['overall_compliance_%'] < 70:
		return 'yellow'
	elif row['overall_compliance_%'] < 90:
		return 'green'
	elif row['overall_compliance_%'] > 89:
		return 'blue'
	

def display_time_filters(df):
		year_list = list(df['year'].unique())
		year_list.sort()
		year = st.sidebar.selectbox('year', year_list, len(year_list)-1)
		quarter = st.sidebar.radio('quarter', ['Jan-Mar', 'Apr-Jun', 'Jul-Sep', 'Oct-Dec'])
		st.header(f'{year} Q{quarter}')
		return year, quarter

def display_site_filter(df, site_name):
		site_list = [''] + list(df['Sample_pt_desc'].unique())
		site_list.sort()
		site_index = site_list.index(site_name) if site_name and site_name in site_list else 0
		return st.sidebar.selectbox('Site', site_list, site_index)

# def display_site_type_filter():
#     return st.sidebar.radio('Site Type', ['test', 'effluent'])

def display_map(df, year, quarter,only1,only2,only3,only4,only5):
		df = df[(df['year'] == year) & (df['quarter'] == quarter)]

		vaal_map = fl.Map(location=[-26.799, 27.908], zoom_start=8, scrollWheelZoom=False, tiles='Stamen Terrain')
		
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
				tooltip = site['Sample_pt_desc'],
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
				site_name = df['Sample_pt_desc'][(df['latitude']==coordinates[1]) & (df['longitude']==coordinates[0])].item()
				
		return site_name

def display_compliance(df, year, quarter, site_name, column, string_format='${:,}', is_median=False):
		df = df[(df['year'] == year) & (df['quarter'] == quarter)]
		if site_name:
				df = df[df['Sample_pt_desc'] == site_name]
		df.drop_duplicates(inplace=True)
		
		st.metric(column[1],f"{round(df[column[0]].mean(),2)}%")



def main():

		#Load Data
		vaal_df = pd.read_csv('data/vaal_overall_final.csv')
		only1 = gpd.read_file('data/river/only1.shp')
		only2 = gpd.read_file('data/river/only2.shp')
		only3 = gpd.read_file('data/river/only3.shp')
		only4 = gpd.read_file('data/river/only4.shp')
		only5 = gpd.read_file('data/river/only5.shp')

		#Display Filters and Map
		year, quarter = display_time_filters(vaal_df)
		site_name = display_map(vaal_df, year, quarter,only1,only2,only3,only4,only5)
		site_name = display_site_filter(vaal_df, site_name)
		# site_type = display_site_type_filter()

		#Display Metrics
		st.subheader(f'{site_name} Compliance')
		# st.subheader(f'{site_name} {site_type} Facts')
		#col titles
		phys = ['physical_compliance_%', 'Physical']
		chem = ['chemical_compliance_%', 'Chemical']
		bact = ['bacteriological_compliance_%', 'Bacteriological']
		bio = ['biological_compliance_%', 'Biological']
		overall = ['overall_compliance_%', 'Overall']
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