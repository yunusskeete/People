### Module containing custom functions for PEople by PHilita.
# Imports

import os, sys, json, requests, math
import pandas as pd





################################################################################

def load_csv(name):

    # if file is not in directory, we source it from github

    if not os.path.exists(name):

        github_url = 'https://raw.githubusercontent.com/yunusskeete/People/main/'

        url = github_url + name.replace('\\', '/').replace(' ', '%20') # directories use '\', whereas urls use '//'

        df = pd.read_csv(url) # create dataframe from online csv (github)

        try:

            df.to_csv(name, index=False) # save

        except:

            pass

        

    try:

        df = pd.read_csv(name) # read

    except:

        pass

    

    return df

################################################################################
# if file is not in directory, we source it from github
def load_geojson(name):
    if not os.path.exists(name):
        url = 'https://raw.githubusercontent.com/yunusskeete/People/main/' + name
        r = requests.get(url) # attain the server's response to the HTTP request

        # write file to file name:
        with open(name, "w") as f:
            f.write(r.content.decode("utf-8")) # decoding

    # once file has been created/located, we read it
    with open(name, 'r') as f:
        geojson_data = json.load(f)

    return geojson_data

################################################################################

# def update_figure(station_name, geojson_data):
    
#     lines.y = next((e for e in geojson_data['features'] if e.get('id')[0] == station_name))['properties']['series']

#     ax_y.label = 'Entries'#data_name.capitalize()

#     figure.title = station_name

################################################################################

class click_location(object):
    """ returns a coordinate with attributes of lat, lng. 

    Args:
        (
            latitude,
            longitude
        )

    Returns:
        coordinate class

    Ammend:
        change class name: coordinates <-- click_location
    """

    def __init__(self, lat, lng):

        self.lat = lat

        self.lng = lng



################################################################################

def distance(click_location, circle_layer):
    """ returns the distance between two latitude-longitude pairs. 

    Args:
        lat-lng 1: click_location - class: click_location
        lat-lng 2: circle_layer - list [lat, lng] or tuple (lat, lng)

    Returns:
        (int or float?): The distance between the two points

    Ammend:
        change circle_layer to class: coordinates (click_location)
    """

    R = 6373.0 # radius of the Earth



    lat_click = math.radians(click_location.lat)

    lng_click = math.radians(click_location.lng)

    lat_stat = math.radians(circle_layer[0])

    lng_stat = math.radians(circle_layer[1])



    d_lat = lat_stat - lat_click

    d_lng = lng_stat - lng_click



    a = a = math.sin(d_lat / 2)**2 + math.cos(lat_click) * math.cos(lat_stat) * math.sin(d_lng / 2)**2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c / 1.60934 # 1609.34 metres in a mile



    return distance



################################################################################

def centroid(quadrant):
    """ returns the centroid of a quadrant.

    Args:
        quadrant: e.g. geo_json_quadrants.data['features'][10]:
                        {'type': 'Feature',
                        'id': '10',
                        'properties': {'id': [],
                        'series': {'entries': [], 'exits': {}, 'busyness': {}, 'other': {}},
                        'stations': {'details': {},
                        'series': {'entries': {}, 'exits': {}, 'busyness': {}, 'other': {}}},
                        'style': {'color': 'white',
                        'opacity': 0,
                        'weight': 1.0,
                        'dashArray': '3',
                        'fillOpacity': 0}},
                        'geometry': {'type': 'Polygon',
                        'coordinates': [[[-0.3808747973970611, 51.3785],
                            [-0.35752227713676726, 51.3785],
                            [-0.35752227713676726, 51.39212083333334],
                            [-0.3808747973970611, 51.39212083333334],
                            [-0.3808747973970611, 51.3785]]]}}                            

    Returns:
        centroid - set of coordinates of class: coordinates (click_location) - of a quadrant

    Ammend:
        NA
    """

    lat_min = quadrant['geometry']['coordinates'][0][0][1]
    lat_max = quadrant['geometry']['coordinates'][0][1][1]

    lng_min = quadrant['geometry']['coordinates'][0][0][0]
    lng_max = quadrant['geometry']['coordinates'][0][1][0]
    
    lat_avg = (lat_min+lat_max)/2
    lng_avg = (lng_min+lng_max)/2

    centroid = click_location(lat_avg, lng_avg)


    return centroid



################################################################################

class local(object):

    def __init__(self, point, id):

        self.point = point

        self.id = id



################################################################################

class times(object):

    def __init__(self, timeint, timestep):

        self.timeint = timeint

        self.timestep = timestep



################################################################################

def findtimeint(search_timestep):

    global times_dict

    for tint, tstp in times_dict.items():

        if tstp == search_timestep:

            output = tint

    return output

    

################################################################################

def findtimestep(search_timeint):

    global times_dict

    return times_dict[search_timeint]



################################################################################

# # correct times for display
# times_dict = {}

# timestamps = tapi.columns.to_list()[10:]
# timeits = list(range(0,96))

# i = 0

# for timestamp in timestamps:
#     timestamp = timestamp[:2] + ':' + timestamp[2:4] + " " + timestamp[4:5] + " " + timestamp[5:7] + ":" + timestamp[7:]
#     timestamps[i] = timestamp
#     time = People.times(i, timestamp)
#     times_dict[time.timeint] = time.timestep
#     i += 1
# # timestamps
# # timeits

times_dict = {0: '05:00 - 05:15', 1: '05:15 - 05:30', 2: '05:30 - 05:45', 3: '05:45 - 06:00', 4: '06:00 - 06:15', 5: '06:15 - 06:30', 6: '06:30 - 06:45', 7: '06:45 - 07:00', 8: '07:00 - 07:15', 9: '07:15 - 07:30', 10: '07:30 - 07:45', 11: '07:45 - 08:00', 12: '08:00 - 08:15', 13: '08:15 - 08:30', 14: '08:30 - 08:45', 15: '08:45 - 09:00', 16: '09:00 - 09:15', 17: '09:15 - 09:30', 18: '09:30 - 09:45', 19: '09:45 - 10:00', 20: '10:00 - 10:15', 21: '10:15 - 10:30', 22: '10:30 - 10:45', 23: '10:45 - 11:00', 24: '11:00 - 11:15', 25: '11:15 - 11:30', 26: '11:30 - 11:45', 27: '11:45 - 12:00', 28: '12:00 - 12:15', 29: '12:15 - 12:30', 30: '12:30 - 12:45', 31: '12:45 - 13:00', 32: '13:00 - 13:15', 33: '13:15 - 13:30', 34: '13:30 - 13:45', 35: '13:45 - 14:00', 36: '14:00 - 14:15', 37: '14:15 - 14:30', 38: '14:30 - 14:45', 39: '14:45 - 15:00', 40: '15:00 - 15:15', 41: '15:15 - 15:30', 42: '15:30 - 15:45', 43: '15:45 - 16:00', 44: '16:00 - 16:15', 45: '16:15 - 16:30', 46: '16:30 - 16:45', 47: '16:45 - 17:00', 48: '17:00 - 17:15', 49: '17:15 - 17:30', 50: '17:30 - 17:45', 51: '17:45 - 18:00', 52: '18:00 - 18:15', 53: '18:15 - 18:30', 54: '18:30 - 18:45', 55: '18:45 - 19:00', 56: '19:00 - 19:15', 57: '19:15 - 19:30', 58: '19:30 - 19:45', 59: '19:45 - 20:00', 60: '20:00 - 20:15', 61: '20:15 - 20:30', 62: '20:30 - 20:45', 63: '20:45 - 21:00', 64: '21:00 - 21:15', 65: '21:15 - 21:30', 66: '21:30 - 21:45', 67: '21:45 - 22:00', 68: '22:00 - 22:15', 69: '22:15 - 22:30', 70: '22:30 - 22:45', 71: '22:45 - 23:00', 72: '23:00 - 23:15', 73: '23:15 - 23:30', 74: '23:30 - 23:45', 75: '23:45 - 00:00', 76: '00:00 - 00:15', 77: '00:15 - 00:30', 78: '00:30 - 00:45', 79: '00:45 - 01:00', 80: '01:00 - 01:15', 81: '01:15 - 01:30', 82: '01:30 - 01:45', 83: '01:45 - 02:00', 84: '02:00 - 02:15', 85: '02:15 - 02:30', 86: '02:30 - 02:45', 87: '02:45 - 03:00', 88: '03:00 - 03:15', 89: '03:15 - 03:30', 90: '03:30 - 03:45', 91: '03:45 - 04:00', 92: '04:00 - 04:15', 93: '04:15 - 04:30', 94: '04:30 - 04:45', 95: '04:45 - 05:00'}



################################################################################

def findtimeint(search_timestep):
    global times_dict
    for tint, tstp in times_dict.items():
        if tstp == search_timestep:
            output = tint
    return output

def findtimestep(search_timeint):
    global times_dict
    return times_dict[search_timeint]



################################################################################

# def update_wms(change):

# #     print(change)

#     global slider, slider_timeint, slider_timestep

#     time_wms.time = '2021-06-01T{}'.format(slider.value)

#     slider_timeint = findtimeint(slider.value)

#     slider_timestep = slider.value



################################################################################

# def slider_update(change, **kwargs):

#     # when the user changes the slider, we run the following:

#     global keywordarguments#, radius_layer_group

#     keywordarguments = kwargs

# #     print('kwaygs: ', keywordarguments)



# # html information box:

#     html1.value = '''

#     <style> 

#     #myDIV {

#       max-height: 500px;

#       max-width: 200px;

#       max-height: 40vh;

#       max-width: 20vw;

#       background-color: white;

#       overflow: auto;

#     }

#     </style>

#     <div id="myDIV">

#       <h4>Station Information:</h4>

#     '''



#     html1.value += '''

#     <h5>({})</h5>

#     '''.format(slider_timestep)



#     # search through local stations, find current entries, update html1

#     for radius_layer in radius_layer_group.layers:

#         local_station = next((e for e in geojson_data['features'] if e.get('id')[0] == radius_layer.name))

#         local_station_name = local_station['properties']['Station']

#         local_station_entry = local_station['properties']['series'][slider_timeint]

#         circle_id = local_station['properties']['Station ASC']

#         local_station = local(local_station_name, circle_id)



#         html1.value += '''

#         <h4><b>{} ({})</b></h4>

#         Entries: {}

#         '''.format(local_station.point, local_station.id, local_station_entry)



#     html1.value += '''

#     </div>

#     '''



################################################################################

# def handle_click(**kwargs):

#     # when the user interaction is a click, we run the following:

#     global keywordarguments

#     keywordarguments = kwargs

# #     print(keywordarguments)

#     if kwargs.get('type') == 'click':

# #         keywordarguments = kwargs

# #         print(keywordarguments)

#         try: # clear the layers we create on click - historic click aren't saved or displayed

#             click_layer_group.clear_layers()

#             radius_layer_group.clear_layers()

#         except:

#             pass

        

#         global click_radius, radius_selector, click_location, circle_layer_group, mystats, points, slider_timeint, slider_timestep

        

#         click_loc = kwargs.get('coordinates') # locate click

#         click_marker = Marker(name='click_marker', location=click_loc) # create click marker

#         click_radius = radius_selector.value # user-specified click "search" radius

        

#         # define a circle around the click of specified radius

#         click_circle = Circle(

#             name = 'click_circle',

#             location = click_loc,

#             radius = int(click_radius * 1609.34)  # click_radius = miles. radius = metres. 1609.34 metres in a mile,

# #             color = "red",

# #             fill_color = "red"

#         )

        

#         # add layers to map

#         click_layer_group.add_layer(click_marker)

#         click_layer_group.add_layer(click_circle)

        

#         # glean latitude and longitude from click

#         click_location.lat = click_loc[0]

#         click_location.lng = click_loc[1]

        

#         # html information box:

#         html1.value = '''

#         <style> 

#         #myDIV {

#           max-height: 500px;

#           max-width: 200px;

#           max-height: 40vh;

#           max-width: 20vw;

#           background-color: white;

#           overflow: auto;

#         }

#         </style>

#         <div id="myDIV">

#           <h4>Station Information:</h4>

#         '''

        

#         html1.value += '''

#         <h5>({})</h5>

#         '''.format(slider_timestep)

        

#         # search through stations, find distance to click, if within radius, store point

#         for circle_layer in circle_layer_group.layers:

#             location = circle_layer.location # location of station

#             dist = distance(click_location, location) # find the distance between click and station

            

#             # logical criteria - if station is within radius

#             if dist <= click_radius:

#                 circle_marker_r = CircleMarker(name = circle_layer.name, location = circle_layer.location, radius = circle_layer.radius, color = "blue", fill_color = "blue")

#                 radius_layer_group.add_layer(circle_marker_r)

#                 local_station = next((e for e in geojson_data['features'] if e.get('id')[0] == circle_layer.name))

#                 local_station_name = local_station['properties']['Station']

#                 local_station_entry = local_station['properties']['series'][slider_timeint]

#                 circle_id = circle_marker_r.name

#                 local_station = local(local_station_name, circle_id)

                

#                 html1.value += '''

#                 <h4><b>{} ({})</b></h4>

#                 Entries: {}

#                 '''.format(local_station.point, local_station.id, local_station_entry)

        

#         html1.value += '''

#         </div>

#         '''



################################################################################