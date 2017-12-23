import folium
import pandas

base_map = folium.Map(location = [48.85,2.29], zoom_start=3, tiles='Mapbox Bright') 
'''
location takes parameters as latitude and longitude coordinates
zoom_start sets starting value for zoom
tiles sets the background/type of the base map
'''

# Function to return colors based on elevation of volcanoes
def color_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'

data = pandas.read_csv("Volcanoes_USA.txt") # Read a csv text file containing details about volcanoes in USA
lat = list(data["LAT"])                     # Store the latitude values in a list
lon = list(data["LON"])                     # Store the longitude values in a list
elev = list(data["ELEV"])                   # Store the elevation values in a list
fgv = folium.FeatureGroup(name="Volcanoes in USA")     
for lt, ln, el in zip(lat, lon, elev):
    fgv.add_child(folium.CircleMarker(location = [lt, ln], popup = folium.Popup(str(el)+" m", parse_html=True), radius = 6, fill = True,
                                    color = 'grey', fill_color = color_producer(el), opacity = 0.7))


# To add a polygon layer, we use geojson objects
# We have a file world.json that we will be using to add a polygon layer
# style_function expects a lambda function. The map color changes based on the attributes
# Adding color-based maps features
fgp = folium.FeatureGroup(name="Population in 2005")     
fgp.add_child(folium.GeoJson(data=open('world.json','r',encoding='utf-8-sig').read(), 
							style_function=lambda x:{'fillColor':'green' if x['properties']['POP2005']<10000000 
							else 'orange' if 10000000 <= x['properties']['POP2005'] <= 50000000 else 'red'}))
base_map.add_child(fgp)
base_map.add_child(fgv)

# Adding a layer control panel:
# It is very important to add the feature group before adding the layer control due to the dependency
# Layer control looks for children added to the map before displaying them as a control
# Ideally every feature should be added as a separate feature group to create individual layer control for them
base_map.add_child(folium.LayerControl())
base_map.save("Map.html") # Creates an HTML file of the map with the specified parameters
