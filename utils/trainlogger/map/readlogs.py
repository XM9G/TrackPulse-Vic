import os
from matplotlib.pylab import f
from utils.trainlogger.map.mapimage import MapImageHandler
from utils.trainlogger.map.station_coordinates_log_train_map_pre_munnel import x_offset as x_offset_log_train_map_pre_munnel, y_offset as y_offset_log_train_map_pre_munnel, station_coordinates as station_coordinates_log_train_map_pre_munnel
from utils.trainlogger.map.line_coordinates_log_train_map_pre_munnel import line_coordinates as lines_coordinates_log_train_map_pre_munnel
from utils.trainlogger.map.station_coordinates_log_train_map_post_munnel import x_offset as x_offset_log_train_map_post_munnel, y_offset as y_offset_log_train_map_post_munnel, station_coordinates as station_coordinates_log_train_map_post_munnel
from utils.trainlogger.map.line_coordinates_log_train_map_post_munnel import line_coordinates as lines_coordinates_log_train_map_post_munnel
from utils.trainlogger.map.station_coordinates_log_sydney_tram_map import x_offset as x_offset_log_sydney_tram, y_offset as y_offset_log_sydney_tram, station_coordinates as station_coordinates_log_sydney_tram
from utils.trainlogger.map.line_coordinates_log_sydney_tram_map import line_coordinates as lines_coordinates_log_sydney_tram

metro_date = '2026-02-01' # this refers to the big switch date, which was assumed to be the opening date when this was coded in march. any "pre munnel" "post munnel" stuff refers to the big switch and not the acutal munnel

def precompat(data:list, lines_dictionary:dict):
    newdata = []
    for line in data:
        cols = line.strip().split(',')
        if len(cols) >= 6:
            trip_date = cols[3]
            group = cols[4]
            station1=cols[5]
            station2=cols[6]
            trip_year = int(trip_date.split('-')[0])
            trip_month = int(trip_date.split('-')[1])
            metro_year = int(metro_date.split('-')[0])
            metro_month = int(metro_date.split('-')[1])
            if trip_year > metro_year or (trip_year == metro_year and trip_month > metro_month):
                if group == 'Frankston':
                    if station1 in ['Flagstaff','Parliament','Melbourne Central'] and station2 in ['Flagstaff','Parliament','Melbourne Central']:
                        group = 'Unknown'
                    elif station1 in ['Flagstaff','Parliament','Melbourne Central']:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Unknown,{station1},{station2},')
                        station1 = '*Southern Cross'
                    elif station2 in ['Flagstaff','Parliament','Melbourne Central']:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Unknown,{station1},{station2},')
                        station2 = '*Richmond'
                elif group == 'Sandringham':
                    if station1 in lines_dictionary['Werribee'][0] and station1 not in lines_dictionary['Sandringham'][0] and station2 in lines_dictionary['Werribee'][0] and station2 not in lines_dictionary['Sandringham'][0]:
                        group = 'Werribee'
                    elif station1 in lines_dictionary['Williamstown'][0] and station1 not in lines_dictionary['Sandringham'][0] and station2 in lines_dictionary['Williamstown'][0] and station2 not in lines_dictionary['Sandringham'][0]:
                        group = 'Williamstown'
                    elif station1 in lines_dictionary['Werribee'][0] and station2 in lines_dictionary['Werribee'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Werribee,{station1},{station2},')
                        if station1 in lines_dictionary['Werribee'][0] and station1 not in lines_dictionary['Sandringham'][0]:
                            station1 = '*Flinders Street'
                        elif station2 in lines_dictionary['Werribee'][0] and station2 not in lines_dictionary['Sandringham'][0]:
                            station2 = '*Flinders Street'
                    elif station1 in lines_dictionary['Williamstown'][0] and station2 in lines_dictionary['Williamstown'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Williamstown,{station1},{station2},')
                        if station1 in lines_dictionary['Williamstown'][0] and station1 not in lines_dictionary['Sandringham'][0]:
                            station1 = '*Flinders Street'
                        elif station2 in lines_dictionary['Williamstown'][0] and station2 not in lines_dictionary['Sandringham'][0]:
                            station2 = '*Flinders Street'
                    elif station1 in lines_dictionary['Werribee'][0] and station1 not in lines_dictionary['Sandringham'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Werribee,{station1},*South Yarra,')
                        station1 = '*Flinders Street'
                    elif station1 in lines_dictionary['Williamstown'][0] and station1 not in lines_dictionary['Sandringham'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Williamstown,{station1},*South Yarra,')
                        station1 = '*Flinders Street'
                    elif station2 in lines_dictionary['Werribee'][0] and station2 not in lines_dictionary['Sandringham'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Werribee,*South Yarra,{station2},')
                        station2 = '*Flinders Street'
                    elif station2 in lines_dictionary['Williamstown'][0] and station2 not in lines_dictionary['Sandringham'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Williamstown,*South Yarra,{station2},')
                        station2 = '*Flinders Street'
                    elif station1 in lines_dictionary['Werribee'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Werribee,{station1},*South Yarra,')
                    elif station1 in lines_dictionary['Williamstown'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Williamstown,{station1},*South Yarra,')
                    elif station2 in lines_dictionary['Werribee'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Werribee,*South Yarra,{station2},')
                    elif station2 in lines_dictionary['Williamstown'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Williamstown,*South Yarra,{station2},')
                elif group == 'Werribee':
                    if station1 in lines_dictionary['Sandringham'][0] and station1 not in lines_dictionary['Werribee'][0] and station2 in lines_dictionary['Sandringham'][0] and station2 not in lines_dictionary['Werribee'][0]:
                        group = 'Sandringham'
                    if station1 in lines_dictionary['Sandringham'][0] and station2 in lines_dictionary['Sandringham'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Sandringham,{station1},{station2},')
                        if station1 in lines_dictionary['Sandringham'][0] and station1 not in lines_dictionary['Werribee'][0]:
                            station1 = '*South Yarra'
                        elif station2 in lines_dictionary['Sandringham'][0] and station2 not in lines_dictionary['Werribee'][0]:
                            station2 = '*South Yarra'
                    elif station1 in lines_dictionary['Sandringham'][0] and station1 not in lines_dictionary['Werribee'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Sandringham,{station1},*Flinders Street,')
                        station1 = '*South Yarra'
                    elif station2 in lines_dictionary['Sandringham'][0] and station2 not in lines_dictionary['Werribee'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Sandringham,*Flinders Street,{station2},')
                        station2 = '*South Yarra'
                    elif station1 in lines_dictionary['Sandringham'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Sandringham,{station1},*Flinders Street,')
                    elif station2 in lines_dictionary['Sandringham'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Sandringham,*Flinders Street,{station2},')
                elif group == 'Williamstown':
                    if station1 in lines_dictionary['Sandringham'][0] and station1 not in lines_dictionary['Williamstown'][0] and station2 in lines_dictionary['Sandringham'][0] and station2 not in lines_dictionary['Williamstown'][0]:
                        group = 'Sandringham'
                    if station1 in lines_dictionary['Sandringham'][0] and station2 in lines_dictionary['Sandringham'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Sandringham,{station1},{station2},')
                        if station1 in lines_dictionary['Sandringham'][0] and station1 not in lines_dictionary['Williamstown'][0]:
                            station1 = '*South Yarra'
                        elif station2 in lines_dictionary['Sandringham'][0] and station2 not in lines_dictionary['Williamstown'][0]:
                            station2 = '*South Yarra'
                    elif station1 in lines_dictionary['Sandringham'][0] and station1 not in lines_dictionary['Williamstown'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Sandringham,{station1},*Flinders Street,')
                        station1 = '*South Yarra'
                    elif station2 in lines_dictionary['Sandringham'][0] and station2 not in lines_dictionary['Williamstown'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Sandringham,*Flinders Street,{station2},')
                        station2 = '*South Yarra'
                    elif station1 in lines_dictionary['Sandringham'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Sandringham,{station1},*Flinders Street,')
                    elif station2 in lines_dictionary['Sandringham'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Sandringham,*Flinders Street,{station2},')
                elif group == 'Pakenham':
                    if station1 in lines_dictionary['Sunbury'][0] and station1 not in lines_dictionary['Pakenham'][0] and station2 in lines_dictionary['Sunbury'][0] and station2 not in lines_dictionary['Pakenham'][0]:
                        group = 'Sunbury'
                    elif station1 in lines_dictionary['Sunbury'][0] and station2 in lines_dictionary['Sunbury'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Sunbury,{station1},{station2},')
                        if station1 in lines_dictionary['Sunbury'][0] and station1 not in lines_dictionary['Pakenham'][0]:
                            station1 = '*Malvern'
                        elif station2 in lines_dictionary['Sunbury'][0] and station2 not in lines_dictionary['Pakenham'][0]:
                            station2 = '*Malvern'
                    elif station1 in lines_dictionary['Sunbury'][0] and station1 not in lines_dictionary['Pakenham'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Sunbury,{station1},*Footscray,')
                        station1 = '*Malvern'
                    elif station2 in lines_dictionary['Sunbury'][0] and station2 not in lines_dictionary['Pakenham'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Sunbury,*Footscray,{station2},')
                        station2 = '*Malvern'
                    elif station1 in lines_dictionary['Sunbury'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Sunbury,{station1},*Footscray,')
                    elif station2 in lines_dictionary['Sunbury'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Sunbury,*Footscray,{station2},')
                    elif station1 in ['Anzac','Town Hall','State Library','Parkville','Arden'] and station2 in ['Anzac','Town Hall','State Library','Parkville','Arden']:
                        group = 'Unknown'
                    elif station1 in ['Anzac','Town Hall','State Library','Parkville','Arden']:
                        if station2 in lines_dictionary['Pakenham'][0]:
                            station1 = '*Malvern'
                        else:
                            group = 'Sunbury'
                            station1 = '*Footscray'
                    elif station2 in ['Anzac','Town Hall','State Library','Parkville','Arden']:
                        if station1 in lines_dictionary['Pakenham'][0]:
                            station2 = '*Malvern'
                        else:
                            group = 'Sunbury'
                            station2 = '*Footscray'
                elif group == 'Cranbourne':
                    if station1 in lines_dictionary['Sunbury'][0] and station1 not in lines_dictionary['Cranbourne'][0] and station2 in lines_dictionary['Sunbury'][0] and station2 not in lines_dictionary['Cranbourne'][0]:
                        group = 'Sunbury'
                    elif station1 in lines_dictionary['Sunbury'][0] and station2 in lines_dictionary['Sunbury'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Sunbury,{station1},{station2},')
                        if station1 in lines_dictionary['Sunbury'][0] and station1 not in lines_dictionary['Cranbourne'][0]:
                            station1 = '*Malvern'
                        elif station2 in lines_dictionary['Sunbury'][0] and station2 not in lines_dictionary['Cranbourne'][0]:
                            station2 = '*Malvern'
                    elif station1 in lines_dictionary['Sunbury'][0] and station1 not in lines_dictionary['Cranbourne'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Sunbury,{station1},*Footscray,')
                        station1 = '*Malvern'
                    elif station2 in lines_dictionary['Sunbury'][0] and station2 not in lines_dictionary['Cranbourne'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Sunbury,*Footscray,{station2},')
                        station2 = '*Malvern'
                    elif station1 in lines_dictionary['Sunbury'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Sunbury,{station1},*Footscray,')
                    elif station2 in lines_dictionary['Sunbury'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Sunbury,*Footscray,{station2},')
                    elif station1 in ['Anzac','Town Hall','State Library','Parkville','Arden'] and station2 in ['Anzac','Town Hall','State Library','Parkville','Arden']:
                        group = 'Unknown'
                    elif station1 in ['Anzac','Town Hall','State Library','Parkville','Arden']:
                        if station2 in lines_dictionary['Cranbourne'][0]:
                            station1 = '*Malvern'
                        else:
                            group = 'Sunbury'
                            station1 = '*Footscray'
                    elif station2 in ['Anzac','Town Hall','State Library','Parkville','Arden']:
                        if station1 in lines_dictionary['Cranbourne'][0]:
                            station2 = '*Malvern'
                        else:
                            group = 'Sunbury'
                            station2 = '*Footscray'
                elif group == 'Sunbury':
                    if station1 in lines_dictionary['Pakenham'][0] and station1 not in lines_dictionary['Sunbury'][0] and station2 in lines_dictionary['Pakenham'][0] and station2 not in lines_dictionary['Sunbury'][0]:
                        group = 'Pakenham'
                    elif station1 in lines_dictionary['Cranbourne'][0] and station1 not in lines_dictionary['Sunbury'][0] and station2 in lines_dictionary['Cranbourne'][0] and station2 not in lines_dictionary['Sunbury'][0]:
                        group = 'Cranbourne'
                    elif station1 in lines_dictionary['Pakenham'][0] and station2 in lines_dictionary['Pakenham'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Pakenham,{station1},{station2},')
                        if station1 in lines_dictionary['Pakenham'][0] and station1 not in lines_dictionary['Sunbury'][0]:
                            station1 = '*Footscray'
                        elif station1 in lines_dictionary['Cranbourne'][0] and station1 not in lines_dictionary['Sunbury'][0]:
                            station1 = '*Footscray'
                        elif station2 in lines_dictionary['Pakenham'][0] and station2 not in lines_dictionary['Sunbury'][0]:
                            station2 = '*Footscray'
                        elif station2 in lines_dictionary['Cranbourne'][0] and station2 not in lines_dictionary['Sunbury'][0]:
                            station2 = '*Footscray'
                    elif station1 in lines_dictionary['Cranbourne'][0] and station2 in lines_dictionary['Cranbourne'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Cranbourne,{station1},{station2},')
                        if station1 in lines_dictionary['Pakenham'][0] and station1 not in lines_dictionary['Sunbury'][0]:
                            station1 = '*Footscray'
                        elif station1 in lines_dictionary['Cranbourne'][0] and station1 not in lines_dictionary['Sunbury'][0]:
                            station1 = '*Footscray'
                        elif station2 in lines_dictionary['Pakenham'][0] and station2 not in lines_dictionary['Sunbury'][0]:
                            station2 = '*Footscray'
                        elif station2 in lines_dictionary['Cranbourne'][0] and station2 not in lines_dictionary['Sunbury'][0]:
                            station2 = '*Footscray'
                    elif station1 in lines_dictionary['Pakenham'][0] and station1 not in lines_dictionary['Sunbury'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Pakenham,{station1},*Malvern,')
                        station1 = '*Footscray'
                    elif station1 in lines_dictionary['Cranbourne'][0] and station1 not in lines_dictionary['Sunbury'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Cranbourne,{station1},*Malvern,')
                        station1 = '*Footscray'
                    elif station2 in lines_dictionary['Pakenham'][0] and station2 not in lines_dictionary['Sunbury'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Pakenham,*Malvern,{station2},')
                        station2 = '*Footscray'
                    elif station2 in lines_dictionary['Cranbourne'][0] and station2 not in lines_dictionary['Sunbury'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Cranbourne,*Malvern,{station2},')
                    elif station1 in lines_dictionary['Pakenham'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Pakenham,{station1},*Malvern,')
                    elif station1 in lines_dictionary['Cranbourne'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Cranbourne,{station1},*Malvern,')
                    elif station2 in lines_dictionary['Pakenham'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Pakenham,*Malvern,{station2},')
                    elif station2 in lines_dictionary['Cranbourne'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Cranbourne,*Malvern,{station2},')
                        station2 = '*Footscray'
                    elif station1 in ['Anzac','Town Hall','State Library','Parkville','Arden'] and station2 in ['Anzac','Town Hall','State Library','Parkville','Arden']:
                        group = 'Unknown'
                    elif station1 in ['Anzac','Town Hall','State Library','Parkville','Arden']:
                        if station2 in lines_dictionary['Sunbury'][0]:
                            station1 = '*Footscray'
                        elif station2 in lines_dictionary['Pakenham'][0]:
                            group = 'Pakenham'
                            station1 = '*Malvern'
                        else:
                            group = 'Cranbourne'
                            station1 = '*Malvern'
                    elif station2 in ['Anzac','Town Hall','State Library','Parkville','Arden']:
                        if station1 in lines_dictionary['Sunbury'][0]:
                            station2 = '*Footscray'
                        elif station1 in lines_dictionary['Pakenham'][0]:
                            group = 'Pakenham'
                            station2 = '*Malvern'
                        else:
                            group = 'Cranbourne'
                            station2 = '*Malvern'
            line = f"{cols[0]},{cols[1]},{cols[2]},{trip_date},{group},{station1},{station2},"
        newdata.append(line)
    return newdata

def postcompat(data:list, lines_dictionary:dict):
    newdata = []
    for line in data:
        cols = line.strip().split(',')
        if len(cols) >= 6:
            trip_date = cols[3]
            group = cols[4]
            station1=cols[5]
            station2=cols[6]
            trip_year = int(trip_date.split('-')[0])
            trip_month = int(trip_date.split('-')[1])
            metro_year = int(metro_date.split('-')[0])
            metro_month = int(metro_date.split('-')[1])
            if trip_year < metro_year or (trip_year == metro_year and trip_month < metro_month):
                if group == 'Frankston':
                    if station1 in lines_dictionary['Werribee'][0] and station1 not in lines_dictionary['Frankston'][0] and station2 in lines_dictionary['Werribee'][0] and station2 not in lines_dictionary['Frankston'][0]:
                        group = 'Werribee'
                    elif station1 in lines_dictionary['Williamstown'][0] and station1 not in lines_dictionary['Frankston'][0] and station2 in lines_dictionary['Williamstown'][0] and station2 not in lines_dictionary['Frankston'][0]:
                        group = 'Williamstown'
                    elif station1 in lines_dictionary['Werribee'][0] and station2 in lines_dictionary['Werribee'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Werribee,{station1},{station2}')
                        if station1 in lines_dictionary['Werribee'][0] and station1 not in lines_dictionary['Frankston'][0]:
                            station1 = '*Southern Cross'
                        elif station2 in lines_dictionary['Werribee'][0] and station2 not in lines_dictionary['Frankston'][0]:
                            station2 = '*Southern Cross'
                    elif station1 in lines_dictionary['Williamstown'][0] and station2 in lines_dictionary['Williamstown'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Williamstown,{station1},{station2}')
                        if station1 in lines_dictionary['Williamstown'][0] and station1 not in lines_dictionary['Frankston'][0]:
                            station1 = '*Southern Cross'
                        elif station2 in lines_dictionary['Williamstown'][0] and station2 not in lines_dictionary['Frankston'][0]:
                            station2 = '*Southern Cross'
                    elif station1 in lines_dictionary['Werribee'][0] and station1 not in lines_dictionary['Frankston'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Werribee,{station1},*South Yarra,')
                        station1 = '*Southern Cross'
                    elif station1 in lines_dictionary['Williamstown'][0] and station1 not in lines_dictionary['Frankston'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Williamstown,{station1},*South Yarra,')
                        station1 = '*Southern Cross'
                    elif station2 in lines_dictionary['Werribee'][0] and station2 not in lines_dictionary['Frankston'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Werribee,*South Yarra,{station2},')
                        station2 = '*Southern Cross'
                    elif station2 in lines_dictionary['Williamstown'][0] and station2 not in lines_dictionary['Frankston'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Williamstown,*South Yarra,{station2},')
                        station2 = '*Southern Cross'
                    elif station1 in lines_dictionary['Werribee'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Werribee,{station1},*South Yarra,')
                    elif station1 in lines_dictionary['Williamstown'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Williamstown,{station1},*South Yarra,')
                    elif station2 in lines_dictionary['Werribee'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Werribee,*South Yarra,{station2},')
                    elif station2 in lines_dictionary['Williamstown'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Williamstown,*South Yarra,{station2},')            
                    if station1 in ['Flinders Street','Southern Cross','*Southern Cross'] or station2 in ['Flinders Street','Southern Cross','*Southern Cross']:
                        group = 'Frankston Loop'
                elif group == 'Werribee':
                    if station1 in lines_dictionary['Frankston'][0] and station1 not in lines_dictionary['Werribee'][0] and station2 in lines_dictionary['Frankston'][0] and station2 not in lines_dictionary['Werribee'][0]:
                        group = 'Frankston Loop'
                    elif station1 in lines_dictionary['Frankston'][0] and station2 in lines_dictionary['Frankston'][0]:
                        if station1 in ['Flinders Street','Southern Cross','*Southern Cross'] or station2 in ['Flinders Street','Southern Cross','*Southern Cross']:
                            newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Frankston Loop,{station1},{station2}')
                        else:
                            newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Frankston Loop,{station1},{station2}')
                        if station1 in lines_dictionary['Frankston'][0] and station1 not in lines_dictionary['Werribee'][0]:
                            station1 = '*South Yarra'
                        elif station2 in lines_dictionary['Frankston'][0] and station2 not in lines_dictionary['Werribee'][0]:
                            station2 = '*South Yarra'
                    elif station1 in lines_dictionary['Frankston'][0] and station1 not in lines_dictionary['Werribee'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Frankston Loop,{station1},*Southern Cross,')
                        station1 = '*South Yarra'
                    elif station2 in lines_dictionary['Frankston'][0] and station2 not in lines_dictionary['Werribee'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Frankston Loop,*Southern Cross,{station2},')
                        station2 = '*South Yarra'
                    elif station1 in lines_dictionary['Frankston'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Frankston Loop,{station1},*Southern Cross,')
                    elif station2 in lines_dictionary['Frankston'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Frankston Loop,*Southern Cross,{station2},')
                elif group == 'Williamstown':
                    if station1 in lines_dictionary['Frankston'][0] and station1 not in lines_dictionary['Williamstown'][0] and station2 in lines_dictionary['Frankston'][0] and station2 not in lines_dictionary['Williamstown'][0]:
                        group = 'Frankston Loop'
                    elif station1 in lines_dictionary['Frankston'][0] and station2 in lines_dictionary['Frankston'][0]:
                        if station1 in ['Flinders Street','Southern Cross','*Southern Cross'] or station2 in ['Flinders Street','Southern Cross','*Southern Cross']:
                            newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Frankston Loop,{station1},{station2}')
                        else:
                            newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Frankston Loop,{station1},{station2}')
                        if station1 in lines_dictionary['Frankston'][0] and station1 not in lines_dictionary['Williamstown'][0]:
                            station1 = '*South Yarra'
                        elif station2 in lines_dictionary['Frankston'][0] and station2 not in lines_dictionary['Williamstown'][0]:
                            station2 = '*South Yarra'
                    elif station1 in lines_dictionary['Frankston'][0] and station1 not in lines_dictionary['Williamstown'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Frankston Loop,{station1},*Southern Cross,')
                        station1 = '*South Yarra'
                    elif station2 in lines_dictionary['Frankston'][0] and station2 not in lines_dictionary['Williamstown'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Frankston Loop,*Southern Cross,{station2},')
                        station2 = '*South Yarra'
                    elif station1 in lines_dictionary['Frankston'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Frankston Loop,{station1},*Southern Cross,')
                    elif station2 in lines_dictionary['Frankston'][0]:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Frankston Loop,*Southern Cross,{station2},')
                elif group == 'Pakenham':
                    if station1 in ['Armadale','Toorak','Hawksburn','South Yarra','Richmond','Flinders Street','Southern Cross','Flagstaff','Parliament','Melbourne Central'] and station2 in ['Armadale','Toorak','Hawksburn','South Yarra','Richmond','Flinders Street','Southern Cross','Flagstaff','Parliament','Melbourne Central']:
                        group = 'Unknown'
                    elif station1 in ['Armadale','Toorak','Hawksburn','South Yarra','Richmond','Flinders Street','Southern Cross','Flagstaff','Parliament','Melbourne Central']:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Unknown,{station1},{station2},')
                        station1 = '*Malvern'
                    elif station2 in ['Armadale','Toorak','Hawksburn','South Yarra','Richmond','Flinders Street','Southern Cross','Flagstaff','Parliament','Melbourne Central']:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Unknown,{station1},{station2},')
                        station2 = '*Malvern'
                elif group == 'Cranbourne':
                    if station1 in ['Armadale','Toorak','Hawksburn','South Yarra','Richmond','Flinders Street','Southern Cross','Flagstaff','Parliament','Melbourne Central'] and station2 in ['Armadale','Toorak','Hawksburn','South Yarra','Richmond','Flinders Street','Southern Cross','Flagstaff','Parliament','Melbourne Central']:
                        group = 'Unknown'
                    elif station1 in ['Armadale','Toorak','Hawksburn','South Yarra','Richmond','Flinders Street','Southern Cross','Flagstaff','Parliament','Melbourne Central']:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Unknown,{station1},{station2},')
                        station1 = '*Malvern'
                    elif station2 in ['Armadale','Toorak','Hawksburn','South Yarra','Richmond','Flinders Street','Southern Cross','Flagstaff','Parliament','Melbourne Central']:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Unknown,{station1},{station2},')
                        station2 = '*Malvern'
                elif group == 'Sunbury':
                    if station1 in ['North Melbourne','Flinders Street','Southern Cross','Flagstaff','Parliament','Melbourne Central'] and station2 in ['North Melbourne','Flinders Street','Southern Cross','Flagstaff','Parliament','Melbourne Central']:
                        group = 'Unknown'
                    elif station1 in ['North Melbourne','Flinders Street','Southern Cross','Flagstaff','Parliament','Melbourne Central']:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Unknown,{station1},{station2},')
                        station1 = '*Footscray'
                    elif station2 in ['North Melbourne','Flinders Street','Southern Cross','Flagstaff','Parliament','Melbourne Central']:
                        newdata.append(f'{cols[0]},{cols[1]},{cols[2]},{trip_date},Unknown,{station1},{station2},')
                        station2 = '*Footscray'
                elif group == 'Summer Start Metro Tunnel Service':
                    group = 'Pakenham'
            line = f"{cols[0]},{cols[1]},{cols[2]},{trip_date},{group},{station1},{station2},"
        newdata.append(line)
    return newdata


def logMap(user:str, lines_dictionary:dict, mode:str='time_based_variants/log_train_map_pre_munnel.png', line_choice:str="All", year:int=0, modeName:str='vic', trainType:str='all', global_stats:bool=False, no_compression:bool=False):
    if global_stats == True:
        try:
            file = open(f"cache\\{modeName}-{year}-{trainType}-{line_choice}-{str(no_compression)}_stations.txt",'r')
            old_stations = []
            for line in file:
                line = line.strip()
                old_stations = line.split(",")
            file.close()

            file = open(f"cache\\{modeName}-{year}-{trainType}-{line_choice}-{str(no_compression)}_affected_lines.txt",'r')
            old_affected_lines = []
            for line in file:
                line = line.strip()
                line = tuple(line.split(","))
                old_affected_lines.append(line)
            file.close()
        except:
            old_stations = [None]
            old_affected_lines = [None]
    else:
        try:
            file = open(f"cache\\{user}-{modeName}-{year}-{trainType}-{line_choice}_stations.txt",'r')
            old_stations = []
            for line in file:
                line = line.strip()
                old_stations = line.split(",")
            file.close()

            file = open(f"cache\\{user}-{modeName}-{year}-{trainType}-{line_choice}_affected_lines.txt",'r')
            old_affected_lines = []
            for line in file:
                line = line.strip()
                line = tuple(line.split(","))
                old_affected_lines.append(line)
            file.close()
        except:
            old_stations = [None]
            old_affected_lines = [None]
    
    if mode == 'time_based_variants/log_train_map_pre_munnel.png':
        if global_stats == True:
            data = []
            folder_path = "utils/trainlogger/userdata"
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)  
                try:
                    if os.path.isfile(file_path):
                        file = open(file_path, 'r')
                        pre_data = file.readlines()
                        for datum in pre_data:
                            data.append(datum)
                        file.close()
                except Exception as e:  
                    print(f"Error accesssing {file_path}: {e}")
        else:
            file = open(f'utils/trainlogger/userdata/{user}.csv', 'r')
            data = file.readlines()
            file.close()

        data = precompat(data, lines_dictionary)

        stations = []
        for line in data:
            cols = line.strip().split(',')
            
            if len(cols) >= 6:
                # Extract year from the date in column 3 (index 2)
                trip_year = int(cols[3].split('-')[0])
                print(f"Trip year: {trip_year}")
                print(f"Year: {year}")
                # Extract line from the date in column 4 (index 3)
                trip_line = cols[4]
                trip_train = cols[2]
                print(f"Trip line: {trip_line}")
                print(f"Line: {line_choice}")
                print(f"Train type: {trip_train}")    
                print(f"TraiRequested type: {trainType}")           
            # Only process if year is 0 (all years) or matches the specified year and line is all line or matches the specified line
            if (year == 0 or trip_year == year) and (line_choice == 'All' or trip_line == line_choice) and (trainType == 'all' or (trainType == 'Other' and trip_train not in ['Alstom Comeng', 'EDI Comeng', "X'Trapolis 100", "Siemens Nexas", "VLocity", 'Sprinter', 'N Class', 'HCMT', "X'Trapolis 2.0"]) or trip_train == trainType):
                station1, station2 = cols[5], cols[6]
                # McKinnon correction
                if station1 == "Mckinnon":
                    station1 = "McKinnon"
                if station2 == "Mckinnon":
                    station2 = "McKinnon"
                if station1 not in stations:
                    stations.append(station1)
                if station2 not in stations:
                    stations.append(station2)
                    
        # split trips into individual segments
        expanded_data = []
        for line in data:
            cols = line.strip().split(',')
            if len(cols) >= 6:
                # Extract year from the date in column 3 (index 2)
                trip_year = int(cols[3].split('-')[0])
                # Extract line from the date in column 4 (index 3)
                trip_line = cols[4]
                trip_train = cols[2]

                
                # Only process if year is 0 (all years) or matches the specified year and line is all line or matches the specified line
                if (year == 0 or trip_year == year) and (line_choice == 'All' or trip_line == line_choice) and (trainType == 'all' or trainType == trip_train):
                    start, end, group = cols[5], cols[6], cols[4]
                    start = start.replace('*','')
                    end = end.replace('*','')

                    # McKinnon correction
                    if start == "Mckinnon":
                        start = "McKinnon"

                    # Find the line that contains these stations
                    if group in ['Alamein', 'Belgrave', 'Craigieburn', 'Cranbourne', 'Glen Waverley', 'Mernda', 'Hurstbridge', 'Lilydale', 'Pakenham', 'Sunbury', 'Upfield'] and cols[5] in ['Flinders Street','Southern Cross','Flagstaff','Parliament','Melbourne Central']:
                        group = group + " Loop"
                    elif group == 'City Circle' and start in ['Southern Cross','Flagstaff','Parliament','Melbourne Central']:
                        group = group + " Loop"
                    elif group == 'Frankston' and start in lines_dictionary['Werribee'][0]:
                        group = 'Werribee'
                    elif group == 'Frankston' and end in lines_dictionary['Werribee'][0]:
                        group = 'Werribee'
                    elif group == 'Frankston' and start in lines_dictionary['Williamstown'][0]:
                        group = 'Williamstown'
                    elif group == 'Frankston' and end in lines_dictionary['Williamstown'][0]:
                        group = 'Williamstown'
                    elif group == 'Bendigo' and 'Epsom' in [str(start), str(end)]:
                        group = 'Epsom'
                    elif group == 'Bendigo' and 'Eaglehawk' in [str(start), str(end)]:
                        group = 'Eaglehawk'
                    if group == 'Werribee' and start not in ['Seaholme', 'Altona', 'Westona'] and end not in ['Seaholme', 'Altona', 'Westona']:
                        group = 'Werribee Express'
                    print(group)
                    for line_name, line_info in lines_dictionary.items():
                        if line_name == group:
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
                                    expanded_data.append(f"{cols[0]},{cols[1]},{cols[2]},{cols[3]},{cols[4]},{station_sequence[i]},{station_sequence[i+1]}")
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

        x_offset = x_offset_log_train_map_pre_munnel
        y_offset = y_offset_log_train_map_pre_munnel
        station_coordinates = station_coordinates_log_train_map_pre_munnel
        line_coordinates = lines_coordinates_log_train_map_pre_munnel

    if mode == 'time_based_variants/log_train_map_post_munnel.png':
        if global_stats == True:
            data = []
            folder_path = "utils/trainlogger/userdata"
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)  
                try:
                    if os.path.isfile(file_path):
                        file = open(file_path, 'r')
                        pre_data = file.readlines()
                        for datum in pre_data:
                            data.append(datum)
                        file.close()
                except Exception as e:  
                    print(f"Error accesssing {file_path}: {e}")
        else:
            file = open(f'utils/trainlogger/userdata/{user}.csv', 'r')
            data = file.readlines()
            file.close()

        data = postcompat(data, lines_dictionary)

        stations = []
        for line in data:
            cols = line.strip().split(',')
            
            if len(cols) >= 6:
                # Extract year from the date in column 3 (index 2)
                trip_year = int(cols[3].split('-')[0])
                print(f"Trip year: {trip_year}")
                print(f"Year: {year}")
                # Extract line from the date in column 4 (index 3)
                trip_line = cols[4]
                trip_train = cols[2]
                print(f"Trip line: {trip_line}")
                print(f"Line: {line_choice}")
            
            # Only process if year is 0 (all years) or matches the specified year and line is all line or matches the specified line
            if (year == 0 or trip_year == year) and (line_choice == 'All' or trip_line == line_choice) and (trainType == 'all' or trainType == trip_train):
                station1, station2 = cols[5], cols[6]
                # McKinnon correction
                if station1 == "Mckinnon":
                    station1 = "McKinnon"
                if station2 == "Mckinnon":
                    station2 = "McKinnon"
                if station1 not in stations:
                    stations.append(station1)
                if station2 not in stations:
                    stations.append(station2)
                    
        # split trips into individual segments
        expanded_data = []
        for line in data:
            cols = line.strip().split(',')
            if len(cols) >= 6:
                # Extract year from the date in column 3 (index 2)
                trip_year = int(cols[3].split('-')[0])
                # Extract line from the date in column 4 (index 3)
                trip_line = cols[4]
                trip_train = cols[2]

                
                # Only process if year is 0 (all years) or matches the specified year and line is all line or matches the specified line
                if (year == 0 or trip_year == year) and (line_choice == 'All' or trip_line == line_choice) and (trainType == 'all' or trainType == trip_train):
                    start, end, group = cols[5], cols[6], cols[4]
                    start = start.replace('*','')
                    end = end.replace('*','')

                    # McKinnon correction
                    if start == "Mckinnon":
                        start = "McKinnon"

                    # Find the line that contains these stations
                    if group in ['Alamein', 'Belgrave', 'Craigieburn', 'Frankston', 'Glen Waverley', 'Mernda', 'Hurstbridge', 'Lilydale', 'Sunbury', 'Upfield'] and cols[5] in ['Flinders Street','Southern Cross','Flagstaff','Parliament','Melbourne Central']:
                        group = group + " Loop"
                    elif group == 'City Circle' and start in ['Southern Cross','Flagstaff','Parliament','Melbourne Central']:
                        group = group + " Loop"
                    elif group == 'Sandringham' and start in lines_dictionary['Werribee'][0]:
                        group = 'Werribee'
                    elif group == 'Sandringham' and end in lines_dictionary['Werribee'][0]:
                        group = 'Werribee'
                    elif group == 'Sandringham' and start in lines_dictionary['Williamstown'][0]:
                        group = 'Williamstown'
                    elif group == 'Sandringham' and end in lines_dictionary['Williamstown'][0]:
                        group = 'Williamstown'
                    elif group == 'Sunbury' and start in lines_dictionary['Pakenham'][0]:
                        group = 'Pakenham'
                    elif group == 'Sunbury' and end in lines_dictionary['Pakenham'][0]:
                        group = 'Pakenham'
                    elif group == 'Sunbury' and start in lines_dictionary['Cranbourne'][0]:
                        group = 'Cranbourne'
                    elif group == 'Sunbury' and end in lines_dictionary['Cranbourne'][0]:
                        group = 'Cranbourne'
                    elif group == 'Bendigo' and 'Epsom' in [str(start), str(end)]:
                        group = 'Epsom'
                    elif group == 'Bendigo' and 'Eaglehawk' in [str(start), str(end)]:
                        group = 'Eaglehawk'
                    if group == 'Werribee' and start not in ['Seaholme', 'Altona', 'Westona'] and end not in ['Seaholme', 'Altona', 'Westona']:
                        group = 'Werribee Express'
                    print(group)
                    for line_name, line_info in lines_dictionary.items():
                        if line_name == group:
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
                                    expanded_data.append(f"{cols[0]},{cols[1]},{cols[2]},{cols[3]},{cols[4]},{station_sequence[i]},{station_sequence[i+1]}")
                                break
        data = expanded_data
                    
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

        x_offset = x_offset_log_train_map_post_munnel
        y_offset = y_offset_log_train_map_post_munnel
        station_coordinates = station_coordinates_log_train_map_post_munnel
        line_coordinates = lines_coordinates_log_train_map_post_munnel

    if mode == 'log_sydney-tram_map.png':
        if global_stats == True:
            data = []
            folder_path = "utils/trainlogger/userdata/sydney-trams"
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)  
                try:
                    if os.path.isfile(file_path):
                        file = open(file_path, 'r')
                        pre_data = file.readlines()
                        for datum in pre_data:
                            data.append(datum)
                        file.close()
                except Exception as e:  
                    print(f"Error accesssing {file_path}: {e}")
        else:
            file = open(f'utils/trainlogger/userdata/sydney-trams/{user}.csv', 'r')
            data = file.readlines()
            file.close()

        stations = []
        for line in data:
            cols = line.strip().split(',')
            
            if len(cols) >= 6:
                # Extract year from the date in column 3 (index 2)
                trip_year = int(cols[3].split('-')[0])
                print(f"Trip year: {trip_year}")
                print(f"Year: {year}")
                # Extract line from the date in column 4 (index 3)
                trip_line = cols[4]
                trip_train = cols[2]
                print(f"Trip line: {trip_line}")
                print(f"Line: {line_choice}")
            
            # Only process if year is 0 (all years) or matches the specified year and line is all line or matches the specified line
            if (year == 0 or trip_year == year) and (line_choice == 'All' or trip_line == line_choice) and (trainType == 'all' or trainType == trip_train):
                station1, station2 = cols[5], cols[6]
                if station1 not in stations:
                    stations.append(station1)
                if station2 not in stations:
                    stations.append(station2)
                    
        # split trips into individual segments
        expanded_data = []
        for line in data:
            cols = line.strip().split(',')
            if len(cols) >= 6:
                # Extract year from the date in column 3 (index 2)
                trip_year = int(cols[3].split('-')[0])
                # Extract line from the date in column 4 (index 3)
                trip_line = cols[4]
                trip_train = cols[2]
                
                # Only process if year is 0 (all years) or matches the specified year and line is all line or matches the specified line
                if (year == 0 or trip_year == year) and (line_choice == 'All' or trip_line == line_choice) and (trainType == 'all' or trainType == trip_train):
                    start, end, group = cols[5], cols[6], cols[4]
                    start = start.replace('*','')
                    end = end.replace('*','')

                    # Find the line that contains these stations
                    print(group)
                    for line_name, line_info in lines_dictionary.items():
                        if line_name == group:
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
                                    expanded_data.append(f"{cols[0]},{cols[1]},{cols[2]},{cols[3]},{cols[4]},{station_sequence[i]},{station_sequence[i+1]}")
                                break
        data = expanded_data
                    
        affected_lines = []
        for line in data:
            cols = line.strip().split(',')
            if len(cols) >= 6:
                group = cols[4]
                # convert to group names
                affected_lines.append((cols[5], cols[6], group))

        x_offset = x_offset_log_sydney_tram
        y_offset = y_offset_log_sydney_tram
        station_coordinates = station_coordinates_log_sydney_tram
        line_coordinates = lines_coordinates_log_sydney_tram
        
    # do the map gen
    map_handler = MapImageHandler(f"utils/trainlogger/map/{mode}", lines_dictionary, x_offset, y_offset, station_coordinates, line_coordinates)
    stations = list(sorted(set(stations)))
    affected_lines = list(sorted(set(affected_lines)))
    print(stations)
    print(affected_lines)

    if old_stations == stations and old_affected_lines == affected_lines:
        print("using cached version")
    else:
        if global_stats == True:
            map_handler.highlight_map(affected_lines, f"cache/{modeName}-{year}-{trainType}-{line_choice}-{str(no_compression)}.png", stations, no_compression)

            station_txt = open(f"cache\\{modeName}-{year}-{trainType}-{line_choice}-{str(no_compression)}_stations.txt","w")
            station_txt.write(','.join(stations))

            affected_lines_writable = []
            for affected_line in affected_lines:
                affected_lines_writable.append(f"{','.join(affected_line)}\n")
            affected_lines_txt = open(f"cache\\{modeName}-{year}-{trainType}-{line_choice}-{str(no_compression)}_affected_lines.txt","w")
            affected_lines_txt.write(''.join(''.join(affected_lines_writable)))
        else:
            map_handler.highlight_map(affected_lines, f"cache/{user}-{modeName}-{year}-{trainType}-{line_choice}-{str(no_compression)}.png", stations, no_compression)

            station_txt = open(f"cache\\{user}-{modeName}-{year}-{trainType}-{line_choice}-{str(no_compression)}_stations.txt","w")
            station_txt.write(','.join(stations))

            affected_lines_writable = []
            for affected_line in affected_lines:
                affected_lines_writable.append(f"{','.join(affected_line)}\n")
            affected_lines_txt = open(f"cache\\{user}-{modeName}-{year}-{trainType}-{line_choice}-{str(no_compression)}_affected_lines.txt","w")
            affected_lines_txt.write(''.join(''.join(affected_lines_writable)))

    return(len(affected_lines))