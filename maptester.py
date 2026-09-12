import os
from matplotlib.pylab import f
from utils.trainlogger.map.mapimage import MapImageHandler
from utils.trainlogger.map.station_coordinates_log_train_map_pre_munnel import x_offset as x_offset_log_train_map_pre_munnel, y_offset as y_offset_log_train_map_pre_munnel, station_coordinates as station_coordinates_log_train_map_pre_munnel
from utils.trainlogger.map.line_coordinates_log_train_map_pre_munnel import line_coordinates as lines_coordinates_log_train_map_pre_munnel
from utils.trainlogger.map.station_coordinates_log_train_map_post_munnel import x_offset as x_offset_log_train_map_post_munnel, y_offset as y_offset_log_train_map_post_munnel, station_coordinates as station_coordinates_log_train_map_post_munnel
from utils.trainlogger.map.line_coordinates_log_train_map_post_munnel import line_coordinates as lines_coordinates_log_train_map_post_munnel
from utils.lines_dictionaries import *

mode = input("Mode: [time_based_variants/log_train_map_pre_munnel.png], [time_based_variants/log_train_map_post_munnel.png] ")
start = input("Start ")
end = input("End ")
stations = [start, end]
group = input("Line ")

if mode == "time_based_variants/log_train_map_pre_munnel.png":
    lines_dictionary = lines_dictionary_log_train_map_pre_munnel
    x_offset = x_offset_log_train_map_pre_munnel
    y_offset = y_offset_log_train_map_pre_munnel
    station_coordinates = station_coordinates_log_train_map_pre_munnel
    line_coordinates = lines_coordinates_log_train_map_pre_munnel

    expanded_data = []
    
    if group in ['Alamein', 'Belgrave', 'Craigieburn', 'Cranbourne', 'Glen Waverley', 'Mernda', 'Hurstbridge', 'Lilydale', 'Pakenham', 'Sunbury', 'Upfield'] and start in ['Flinders Street','Southern Cross','Flagstaff','Parliament','Melbourne Central']:
        group1 = group + " Loop"
    elif group == 'City Circle' and start in ['Southern Cross','Flagstaff','Parliament','Melbourne Central']:
        group1 = group + " Loop"
    elif group == 'Frankston' and start in lines_dictionary['Werribee'][0]:
        group1 = 'Werribee'
    elif group == 'Frankston' and end in lines_dictionary['Werribee'][0]:
        group1 = 'Werribee'
    elif group == 'Frankston' and start in lines_dictionary['Williamstown'][0]:
        group1 = 'Williamstown'
    elif group == 'Frankston' and end in lines_dictionary['Williamstown'][0]:
        group1 = 'Williamstown'
    elif group == 'Bendigo' and 'Epsom' in [str(start), str(end)]:
        group1 = 'Epsom'
    elif group == 'Bendigo' and 'Eaglehawk' in [str(start), str(end)]:
        group1 = 'Eaglehawk'
    else:
        group1 = group
    if group == 'Werribee' and start not in ['Seaholme', 'Altona', 'Westona'] and end not in ['Seaholme', 'Altona', 'Westona']:
        group = 'Werribee Express'
    print(f"Final Line = {group}")
    for line_name, line_info in lines_dictionary.items():
        if line_name == group1:
            station_list = line_info[0]
            if start in station_list and end in station_list:
                # Get indices of start and end stations
                start_idx = station_list.index(start)
                end_idx = station_list.index(end)
                
                # Determine direction (forward or reverse through station list)
                if start_idx < end_idx:
                    station_sequence = station_list[start_idx:end_idx + 1]
                else:
                    station_sequence = station_list[end_idx:start_idx + 1][::-1]
                
                # Create individual segments
                for i in range(len(station_sequence) - 1):
                    expanded_data.append(f"{1},{1},{2},{3},{group},{station_sequence[i]},{station_sequence[i+1]}")
                break
    data = expanded_data
                    
    affected_lines = []
    for line in data:
        cols = line.strip().split(',')
        if len(cols) >= 6:
            # convert to group names
            if cols[4] in ['Werribee', 'Williamstown','Frankston']:
                group = 'cross_city'
            elif cols[4] in ['Lilydale','Belgrave','Alamein','Glen Waverley']:
                group = 'burnley'
            elif cols[4] in ['Craigieburn','Upfield','Sunbury']:
                group = 'northern'
            elif cols[4] in ['Pakenham','Cranbourne']:
                group = 'dandenong'
            elif cols[4] in ['Sandringham']:
                group = 'sandringham'
            elif cols[4] in ['Stony Point']:
                group = 'stony_point'
            elif cols[4] in ['Hurstbridge', 'Mernda', 'City Circle']:
                group = 'clifton_hill'
            elif cols[4] in ['Flemington Racecourse']:
                group = 'flemington'
            elif cols[4] in ['Albury']:
                group = 'standard_gauge'
            elif cols[4] in ['Traralgon', 'Geelong','Bendigo','Seymour',]:
                group = 'vline_intercity'
            elif cols[4] in ['Shepparton', 'Swan Hill', 'Echuca', 'Warrnambool', 'Bairnsdale']:
                group = 'vline_long_distance'
            elif cols[4] in ['Ballarat']:
                group = 'ballarat_seperate'
            elif cols[4] in ['Ararat', 'Maryborough']:
                group = 'ararat/maryborough_seperate'
            elif cols[4] in ['Puffing Billy Railway', 'Yarra Valley Railway', 'Daylesford Spa Country Railway', 'Mornington Tourist Railway', 'Victorian Goldfields Railway', 'Walhalla Goldfields Railway', 'Bellarine Railway']:
                group = 'heritage'
            else:
                group = cols[4]
            if cols[5] == cols[6] and cols[5] == 'Healesville':
                stop_2 = 'Tunnel Hill'
            else:
                stop_2=cols[6]
            affected_lines.append((cols[5], stop_2, group))
else:
    mode = "time_based_variants/log_train_map_post_munnel.png"
    lines_dictionary = lines_dictionary_log_train_map_post_munnel
    x_offset = x_offset_log_train_map_post_munnel
    y_offset = y_offset_log_train_map_post_munnel
    station_coordinates = station_coordinates_log_train_map_post_munnel
    line_coordinates = lines_coordinates_log_train_map_post_munnel

    expanded_data = []

    if group in ['Alamein', 'Belgrave', 'Craigieburn', 'Frankston', 'Glen Waverley', 'Mernda', 'Hurstbridge', 'Lilydale', 'Sunbury', 'Upfield'] and start in ['Flinders Street','Southern Cross','Flagstaff','Parliament','Melbourne Central']:
        group1 = group + " Loop"
    elif group == 'City Circle' and start in ['Southern Cross','Flagstaff','Parliament','Melbourne Central']:
        group1 = group + " Loop"
    elif group == 'Sandringham' and start in lines_dictionary['Werribee'][0]:
        group1 = 'Werribee'
    elif group == 'Sandringham' and end in lines_dictionary['Werribee'][0]:
        group1 = 'Werribee'
    elif group == 'Sandringham' and start in lines_dictionary['Williamstown'][0]:
        group1 = 'Williamstown'
    elif group == 'Sandringham' and end in lines_dictionary['Williamstown'][0]:
        group1 = 'Williamstown'
    elif group == 'Sunbury' and start in lines_dictionary['Pakenham'][0]:
        group1 = 'Pakenham'
    elif group == 'Sunbury' and end in lines_dictionary['Pakenham'][0]:
        group1 = 'Pakenham'
    elif group == 'Sunbury' and start in lines_dictionary['Cranbourne'][0]:
        group1 = 'Cranbourne'
    elif group == 'Sunbury' and end in lines_dictionary['Cranbourne'][0]:
        group1 = 'Cranbourne'
    elif group == 'Bendigo' and 'Epsom' in [str(start), str(end)]:
        group1 = 'Epsom'
    elif group == 'Bendigo' and 'Eaglehawk' in [str(start), str(end)]:
        group1 = 'Eaglehawk'
    else:
        group1 = group
    if group == 'Werribee' and start not in ['Seaholme', 'Altona', 'Westona'] and end not in ['Seaholme', 'Altona', 'Westona']:
        group1 = 'Werribee Express'
    print(f"Final Line = {group1}")
    for line_name, line_info in lines_dictionary.items():
        if line_name == group1:
            station_list = line_info[0]
            if start in station_list and end in station_list:
                # Get indices of start and end stations
                start_idx = station_list.index(start)
                end_idx = station_list.index(end)
                
                # Determine direction (forward or reverse through station list)
                if start_idx < end_idx:
                    station_sequence = station_list[start_idx:end_idx + 1]
                else:
                    station_sequence = station_list[end_idx:start_idx + 1][::-1]
                
                # Create individual segments
                for i in range(len(station_sequence) - 1):
                    expanded_data.append(f"{1},{1},{2},{3},{group},{station_sequence[i]},{station_sequence[i+1]}")
                break
    data = expanded_data
    print(expanded_data)
                    
    affected_lines = []
    for line in data:
        cols = line.strip().split(',')
        if len(cols) >= 6:
            # convert to group names
            if cols[4] in ['Werribee', 'Williamstown', 'Sandringham']:
                group = 'cross_city'
            elif cols[4] in ['Lilydale','Belgrave','Alamein','Glen Waverley']:
                group = 'burnley'
            elif cols[4] in ['Craigieburn','Upfield']:
                group = 'northern'
            elif cols[4] in ['Pakenham','Cranbourne','Sunbury']:
                group = 'dandenong'
            elif cols[4] in ['Frankston', 'Frankston Loop']:
                group = 'frankston'
            elif cols[4] in ['Stony Point']:
                group = 'stony_point'
            elif cols[4] in ['Hurstbridge', 'Mernda', 'City Circle']:
                group = 'clifton_hill'
            elif cols[4] in ['Flemington Racecourse']:
                group = 'flemington'
            elif cols[4] in ['Albury']:
                group = 'standard_gauge'
            elif cols[4] in ['Traralgon', 'Geelong','Bendigo','Seymour',]:
                group = 'vline_intercity'
            elif cols[4] in ['Shepparton', 'Swan Hill', 'Echuca', 'Warrnambool', 'Bairnsdale']:
                group = 'vline_long_distance'
            elif cols[4] in ['Ballarat']:
                group = 'ballarat_seperate'
            elif cols[4] in ['Ararat', 'Maryborough']:
                group = 'ararat/maryborough_seperate'
            elif cols[4] in ['Puffing Billy Railway', 'Yarra Valley Railway', 'Daylesford Spa Country Railway', 'Mornington Tourist Railway', 'Victorian Goldfields Railway', 'Walhalla Goldfields Railway', 'Bellarine Railway']:
                group = 'heritage'
            else:
                group = cols[4]
            if cols[5] == cols[6] and cols[5] == 'Healesville':
                stop_2 = 'Tunnel Hill'
            else:
                stop_2=cols[6]
            affected_lines.append((cols[5], stop_2, group))

print(stations)
print(affected_lines)

map_handler = MapImageHandler(f"utils/trainlogger/map/{mode}", lines_dictionary, x_offset, y_offset, station_coordinates, line_coordinates)
map_handler.highlight_map(affected_lines, f"cache/test.png", stations, False)