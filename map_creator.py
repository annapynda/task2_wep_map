from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderTimedOut
import folium
import csv


def first_shar(file):
    dct = dict()
    country_1 = []
    country_1_y = []
    country_2 = []
    country_2_y = []
    country_3 = []
    country_3_y = []
    country_4 = []
    country_4_y = []
    lst = []
    with open(file) as needfile:
        csv_f = csv.reader(needfile, delimiter=',')
        for i in csv_f:
            lst.append(i)

        for i in lst:
            if lst_final[0] in i:
                country_1.append(i)
            if lst_final[1] in i:
                country_2.append(i)
            if lst_final[2] in i:
                country_3.append(i)
            if lst_final[3] in i:
                country_4.append(i)
        for i in country_1:
            if year in i:
                country_1_y.append(i)
        for i in country_2:
            if year in i:
                country_2_y.append(i)
        for i in country_3:
            if year in i:
                country_3_y.append(i)
        for i in country_4:
            if year in i:
                country_4_y.append(i)

        dct[lst_final[0]] = len(country_1_y)
        dct[lst_final[1]] = len(country_2_y)
        dct[lst_final[2]] = len(country_3_y)
        dct[lst_final[3]] = len(country_4_y)
        # print(dct)


        return dct

def second_shar(file):
    lst = []
    lst_main = []
    lst_end = []
    with open(file) as needfile:
        csv_f = csv.reader(needfile, delimiter=',')
        for i in csv_f:
            lst.append(i)
        for i in lst:
            for j in i:
                if j.endswith(country_for_3):
                    lst_main.append(i)
        for i in lst_main:
            if year_for_3 in i:
                lst_end.append(i[-1])
        lst_end = set(lst_end)
        lst_end = list(lst_end)

        return lst_end


def map_func(lst, dct):
    geolocator = Nominatim(user_agent="specify_your_app_name_here", timeout = 3)
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    map = folium.Map()
    point_1 = folium.FeatureGroup(name="Map of country films")
    for i in lst:
        try:
            location = geolocator.geocode(i)
            if location != None:
                lat, long = location.latitude, location.longitude
                point_1.add_child(folium.Marker(location=[lat, long], popup = "Film was filmed here" + str(year_for_3), icon = folium.Icon()))
            map.add_child(point_1)
        except GeocoderTimedOut:
            continue

    point_2 =  folium.FeatureGroup(name="Map of four places")

    for d in dct:
        try:
            location = geolocator.geocode(d)
            if location != None:
                lat, long = location.latitude, location.longitude
                point_2.add_child(folium.Marker(location=[lat, long], popup = "There were " + str(dct[d]) + " films filmed in " + str(year),  icon = folium.Icon()))
            map.add_child(point_2)
        except GeocoderTimedOut:
            continue


    fg_pp = folium.FeatureGroup(name="Population")
    fg_pp.add_child(folium.GeoJson(data=open('world.json', 'r',
                                             encoding='utf-8-sig').read(),
                                   style_function=lambda x: {
                                       'fillColor': 'green' if x['properties']['POP2005'] < 10000000
                                       else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000
                                       else 'red'}))
    map.add_child(fg_pp)
    map.add_child(folium.LayerControl())

    map.save('Map_1.html')


if __name__ == "__main__":
    print("Enter information for second layer: ")
    country_for_3 = str(input("Enter a country: "))
    year_for_3 = str(input("Enter a year: "))
    lst_needed = second_shar("locations.csv")
    lst_final = []
    print("Enter information for third layer:")
    for i in range(4):
        country = str(input("country: "))
        lst_final.append(country)
    year = str(input("year: "))
    dct_needed = first_shar("locations.csv")

    map_func(lst_needed, dct_needed)
