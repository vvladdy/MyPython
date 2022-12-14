from geopy.geocoders import Nominatim
from pprint import pprint
import folium
from geopy.distance import geodesic # модуль для рассчета расстояния

nominatin = Nominatim(user_agent='user')
place = 'Kramatorsk'

# Нахождение координат по городу
location = nominatin.geocode(place).raw
# pprint(location)
print('широта, долгота', location['lat'], location['lon'])

# 48.7389415 37.5843812
# Зaпишем локацию в .html файл

area = folium.Map(location=[location['lat'], location['lon']])
area.save(fr'D:\MyPythonFolder\MyPython\.venv\Dif_files\Locat\{place}.html')

# Нахождение места по координатам
coordinates = '48.74 37.55'

loc = nominatin.geocode(coordinates)
print(loc)


place1 = 'Краматорск'
place2 = 'Рим'

nominatin_dist = Nominatim(user_agent='user')
location_place1 = nominatin_dist.geocode(place1).raw
location_place2 = nominatin_dist.geocode(place2).raw

place1_lat = location_place1['lat']
place1_lon = location_place1['lon']

place2_lat = location_place2['lat']
place2_lon = location_place2['lon']

print(place1, place1_lat, place1_lon)
print(place2, place2_lat, place2_lon)

coord_pl1 = (place1_lat, place1_lon)
coord_pl2 = (place2_lat, place2_lon)

distance_km = geodesic(coord_pl1, coord_pl2).kilometers
print('Расстояние по прямой от {} до {} состявляет {} км'.format(
    place1, place2, round(distance_km, 2)))
