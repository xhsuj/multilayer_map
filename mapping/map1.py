import folium #folium is a python library to visualize the geospatial data
import pandas # a python library for creating and manipulating data
data=pandas.read_csv("/Users/yhb/Desktop/mapping/Volcanoes.txt") # create a dataframe object which includes the data in txt file
lat=list(data["LAT"]) #get needed columns of data of the object data
lon=list(data["LON"])
ele=list(data["ELEV"])
# following code create a html pattern in which %s represents the later-inserted data from column's data, which would
#save us a lot of time avoiding repeated writing the format
html="""<h4>Volcano information:</h4>
Height: %s m
"""
def color_producer(elevation): #create a color_produceing function, return color string according to the maginitude of passed
#elevation value
    if elevation>3000:
        return 'red'
    elif elevation>=1000:
        return 'orange'
    else:
        return 'green'

map = folium.Map(location=[31.575150648983485, 105.96398260588428],zoom_start=20,tiles="Stamen Terrain") #get a map object from folium
#, location is the center of our map, zoom_start determines how large we will zoom the initial location, tiles determine the kind of the map tiles we want to choose
fgv=folium.FeatureGroup(name="My Map") #use a featuregroup to specifically and grouply adjust the map's fitures and apply
#the changes only once to the map though add_child(fg)
"""for lt,lo,el in zip(lat,lon,ele): #zip would combine lt and lo in one operation
    iframe=folium.IFrame(html=html % str(el),width=200,height=100)
    fg.add_child(folium.Marker(location=[lt, lo],popup=folium.Popup(iframe), icon=folium.Icon(color=color_producer(el)))) #this method only
#allow one marker added once, to add multiple markers, we need to use for loop and use this command line for multiple times
#note that ELEV in numpy data is a float number, but popup in folium marker should be string, so use str() to convert it
"""
for lt,lo,el in zip(lat,lon,ele): #zip would combine lt and lo and ele in one operation
    iframe=folium.IFrame(html=html % str(el),width=200,height=100) #use the format designed and other parameters to determine the popup window's format
    #use IFrame function of folium to create a iframe object
    #add the marker with changes to the featuregroup object, modify the Popup with the deigned pattern using Popup method, other parameters are
    # ones of the particular kind of marker, in this case, the CircleMarker
    fgv.add_child(folium.CircleMarker(location=[lt, lo],popup=folium.Popup(iframe), color="gray",fill_color=color_producer(el),fill_opacity=0.7))

fgp=folium.FeatureGroup(name="Population") #create another feature group to add population layer
#add the layer through geojson method, using the data from population file and change the color of the
#filed through a function relating to color and population size
fgp.add_child(folium.GeoJson(data=(open('world.json','r',encoding='utf-8-sig').read()),
style_function=lambda x:{'fillColor':'green' if x['properties']['POP2005']< 10000000
else 'orange' if 10000000<=x['properties']['POP2005']< 20000000 else 'red'}))



map.add_child(fgv) #add the two feature groups; we do not combine the feature groups together since we want to control them respectively
map.add_child(fgp)
map.add_child(folium.LayerControl()) #Layer Control method, providing the user buttons to control the view of layers
map.save("Map1.html") #save the python's transmitted html code to the file Map1.html
