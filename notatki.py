import folium
from utils import my_functions
map = folium.Map(location = my_functions.get_coordinates_of(city="Bydgoszcz"), titles='OpesStreetMap', zoom_start=10)
folium.Marker(location= my_functions.get_coordinates_of(city="Bydgoszcz"), popup="Bydgoszcz").add_to(map)
map.save('mapka.html')