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

class click_location(object): # why an object?

    def __init__(self, lat, lng):

        self.lat = lat

        self.lng = lng



################################################################################

def distance(click_location, circle_layer):

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