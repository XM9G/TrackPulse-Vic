import csv
from collections import Counter
from datetime import datetime
from io import StringIO
from utils.trainlogger.stationDistance import *
from collections import Counter
import os

def topStats(user, stat, year, mode):
    if mode == 'train':
        folder = ''
    else:
        folder = f'{mode}/'
        
    with open(f'utils/trainlogger/userdata/{folder}{user}.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        
        # Counters to keep track of line, station, set, date, type, and station pair frequencies
        line_counter = Counter()
        station_counter = Counter()
        set_counter = Counter()
        date_counter = Counter()
        type_counter = Counter()
        pair_counter = Counter()

        # Process each row in the CSV
        print(f"Year: {year}")
        for row in reader:
            # Row format: LogID, TrainID, TrainType, Date, Line, Start, End
            date = row[3]
            if year == 0 or date.startswith(str(year)):
                print(f'Log is in the right year, {year} is in {date}')
                line = row[4]
                start_station = row[5]
                end_station = row[6]
                train_set = row[1]  # Changed to 'train_set' since 'set' is a Python keyword
                train_type = row[2]
                pair = (start_station, end_station)

                # Only update counters if value is not 'unknown' or 'N/A' (case-insensitive)
                if line and line.lower() not in ['unknown', 'n/a']:
                    line_counter.update([line])
                if start_station and start_station.lower() not in ['unknown', 'n/a']:
                    station_counter.update([start_station])
                if end_station and end_station.lower() not in ['unknown', 'n/a']:
                    station_counter.update([end_station])
                if train_set and train_set.lower() not in ['unknown', 'n/a']:
                    set_counter.update([train_set])
                if train_type and train_type.lower() not in ['unknown', 'n/a']:
                    type_counter.update([train_type])
                if date and date.lower() not in ['unknown', 'n/a']:
                    date_counter.update([date])
                if (start_station and end_station and
                    start_station.lower() not in ['unknown', 'n/a'] and
                    end_station.lower() not in ['unknown', 'n/a']):
                    pair_counter.update([pair])

        # Get the 10 most common entries
        most_common_lines = line_counter.most_common(100000)
        most_common_stations = station_counter.most_common(100000)
        most_common_sets = set_counter.most_common(100000)
        most_common_types = type_counter.most_common(100000)
        most_common_dates = date_counter.most_common(100000)
        most_common_pairs = pair_counter.most_common(100000)

        # Prepare the results as a list
        results = []
                
        # Append the most common stats to the results list
        if stat == "lines":
            for line, count in most_common_lines:
                results.append(f"{line}: {count} times")
        elif stat == "stations":
            for station, count in most_common_stations:
                results.append(f"{station}: {count} times")
        elif stat == "sets":
            for train_set, count in most_common_sets:
                results.append(f"{train_set}: {count} times")
        elif stat == "types":
            for train_type, count in most_common_types:
                results.append(f"{train_type}: {count} times")
        elif stat == "dates":
            for date, count in most_common_dates:
                results.append(f"{date}: {count} times")
        elif stat == "pairs":
            for (start, end), count in most_common_pairs:
                results.append(f"{start} to {end}: {count} times")

        print(results)
        return results

def allTopStats(user, stat, year):
    file_pathsChecker = [
        f'utils/trainlogger/userdata/{user}.csv',
        f'utils/trainlogger/userdata/tram/{user}.csv',
        f'utils/trainlogger/userdata/sydney-trains/{user}.csv',
        f'utils/trainlogger/userdata/sydney-trams/{user}.csv',
        f'utils/trainlogger/userdata/bus/{user}.csv',
        f'utils/trainlogger/userdata/adelaide-trains/{user}.csv',
        f'utils/trainlogger/userdata/adelaide-trams/{user}.csv',
        f'utils/trainlogger/userdata/perth-trains/{user}.csv',
        f'utils/trainlogger/userdata/flights/{user}.csv',

    ]
    file_paths = [path for path in file_pathsChecker if os.path.exists(path)]

    line_counter = Counter()
    station_counter = Counter()
    set_counter = Counter()
    date_counter = Counter()
    type_counter = Counter()
    pair_counter = Counter()

    # Process each file in the list
    for file_path in file_paths:
        if file_path.endswith('.csv'):
            with open(file_path, newline='') as csvfile:
                reader = csv.reader(csvfile)

                # Process each row in the CSV
                for row in reader:
                    # Row format: LogID, TrainID, TrainType, Date, Line, Start, End
                    date = row[3]
                    if year == 0 or date.startswith(str(year)):
                        line = row[4]
                        start_station = row[5]
                        end_station = row[6]
                        train_set = row[1]
                        train_type = row[2]
                        pair = (start_station, end_station)

                        # Update counters
                        line_counter.update([line])
                        station_counter.update([start_station, end_station])
                        set_counter.update([train_set])
                        type_counter.update([train_type])
                        date_counter.update([date])
                        pair_counter.update([pair])

    # Get the most common entries
    most_common_lines = line_counter.most_common(100000)
    most_common_stations = station_counter.most_common(100000)
    most_common_sets = set_counter.most_common(100000)
    most_common_types = type_counter.most_common(100000)
    most_common_dates = date_counter.most_common(100000)
    most_common_pairs = pair_counter.most_common(100000)

    # Prepare the results as a list
    results = []

    # Append the most common entries to the results list based on the specified stat
    if stat == "lines":
        for line, count in most_common_lines:
            results.append(f"{line}: {count} times")
    elif stat == "stations":
        for station, count in most_common_stations:
            results.append(f"{station}: {count} times")
    elif stat == "sets":
        for train_set, count in most_common_sets:
            results.append(f"{train_set}: {count} times")
    elif stat == "types":
        for train_type, count in most_common_types:
            results.append(f"{train_type}: {count} times")
    elif stat == "dates":
        for date, count in most_common_dates:
            results.append(f"{date}: {count} times")
    elif stat == "pairs":
        for (start, end), count in most_common_pairs:
            results.append(f"{start} to {end}: {count} times")

    print(results)
    return results



def globalTopStats(stat):
    base_paths = [
        f'utils/trainlogger/userdata/',
        # f'utils/trainlogger/userdata/tram/',
        # f'utils/trainlogger/userdata/sydney-trains/',
        # f'utils/trainlogger/userdata/sydney-trams/'
    ]

    file_paths = []
    for base_path in base_paths:
        if os.path.exists(base_path):
            for root, _, files in os.walk(base_path):
                for file in files:
                    if file.endswith('.csv'):
                        if file != 'XXm9G.csv' and file != 'comeng_17.csv':
                            print(file)
                            file_paths.append(os.path.join(root, file))

    line_counter = Counter()
    station_counter = Counter()
    set_counter = Counter()
    date_counter = Counter()
    type_counter = Counter()

    for file_path in file_paths:
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                line = row[4]
                start_station = row[5]
                end_station = row[6]
                set = row[1]
                train_type = row[2]
                date = row[3]

                line_counter.update([line])
                station_counter.update([start_station, end_station])
                set_counter.update([set])
                type_counter.update([train_type])
                date_counter.update([date])

    most_common_lines = line_counter.most_common()
    most_common_stations = station_counter.most_common()
    most_common_sets = set_counter.most_common()
    most_common_types = type_counter.most_common()
    most_common_dates = date_counter.most_common()

    results = []

    if stat == "lines":
        for line, count in most_common_lines:
            results.append(f"{line}: {count} times")
    elif stat == "stations":
        for station, count in most_common_stations:
            results.append(f"{station}: {count} times")
    elif stat == "sets":
        for set, count in most_common_sets:
            results.append(f"{set}: {count} times")
    elif stat == "types":
        for train_type, count in most_common_types:
            results.append(f"{train_type}: {count} times")
    elif stat == "dates":
        for date, count in most_common_dates:
            results.append(f"{date}: {count} times")
    if stat == "pairs":
        results.append('Global trips unavailable')
            # for (start, end), count in most_common_pairs:
            #     results.append(f"{start} to {end}: {count} times")

    print(results)
    return results
def stationPercent(user):
    file_path = f'utils/trainlogger/userdata/{user}.csv'
    unique_items = set()
    
    # Read the CSV content
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        
        for row in reader:
            # Extract the last two items from each row
            last_two_items = row[-2:]
            
            # Add each item to the set (sets only keep unique items)
            unique_items.update(last_two_items)
    
    # The number of unique items is the length of the set
    numberOfStations = 320
    
    total = len(unique_items)
    print(f'number of stations visited: {total}')
    percent = round((total/numberOfStations)*100, 2)
    return f'{percent}%'

def linePercent(user):
    file = f'utils/trainlogger/userdata/{user}.csv'
    unique_items = set()
    
    # Read the CSV content
    with open(file, mode='r') as csvfile:
        reader = csv.reader(csvfile)
        
        for row in reader:
            # Extract the fifth item from each row (index 4)
            fifth_item = row[4]
            
            # Add the item to the set (sets only keep unique items)
            unique_items.add(fifth_item)
    
    # The number of unique items is the length of the set
    numberOfLines = 32
    
    total = len(unique_items)
    percent = round((total / numberOfLines) * 100, 2)
    return f'{percent}%'

def lowestDate(user, mode):
    if mode == 'train':
        filename = f'utils/trainlogger/userdata/{user}.csv'
    else:
        filename = f'utils/trainlogger/userdata/{mode}/{user}.csv'
    # Initialize an empty list to store the dates
    dates = []

    # Read the CSV file
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            # Extract the date string from each row and add it to the dates list
            dates.append(row[3])

    # Remove dashes from each date and convert them to integers
    cleaned_dates = [int(date.replace('-', '')) for date in dates]

    # Empty files/users with no logs should be treated as missing data by callers.
    if not cleaned_dates:
        raise FileNotFoundError(f'No log entries found for user {user} in mode {mode}')

    # Find the lowest number in the cleaned_dates list
    lowest_number = min(cleaned_dates)

    # Convert the lowest number back to the date format 'yyyy-mm-dd'
    lowest_date = str(lowest_number)[:4] + '-' + str(lowest_number)[4:6] + '-' + str(lowest_number)[6:]

    return lowest_date

def highestDate(user, mode):
    if mode == 'train':
        filename = f'utils/trainlogger/userdata/{user}.csv'
    else:
        filename = f'utils/trainlogger/userdata/{mode}/{user}.csv'    # Initialize an empty list to store the dates
    dates = []

    # Read the CSV file
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            # Extract the date string from each row and add it to the dates list
            dates.append(row[3])

    # Remove dashes from each date and convert them to integers
    cleaned_dates = [int(date.replace('-', '')) for date in dates]

    # Empty files/users with no logs should be treated as missing data by callers.
    if not cleaned_dates:
        raise FileNotFoundError(f'No log entries found for user {user} in mode {mode}')

    # Find the highest number in the cleaned_dates list
    highest_number = max(cleaned_dates)

    # Convert the highest number back to the date format 'yyyy-mm-dd'
    highest_date = str(highest_number)[:4] + '-' + str(highest_number)[4:6] + '-' + str(highest_number)[6:]

    return highest_date

def logAmounts(user, mode):
    if mode == 'train':
        filename = f'utils/trainlogger/userdata/{user}.csv'
    else:
        filename = f'utils/trainlogger/userdata/{mode}/{user}.csv'    
    with open(filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        line_count = sum(1 for row in csv_reader)
    return line_count

def getTotalTravelDistance(user):
    filename = f'utils/trainlogger/userdata/{user}.csv'
    distance = 0
    
    # Open and read the CSV file
    with open(filename, newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            col6 = row[5]
            col7 = row[6]
            try:
                distance += getStationDistance(load_station_data('utils/trainlogger/stationDistances.csv'), col6, col7)
                print(f"{col6} to {col7}: {distance}")
            except:
                print(f'{col6} to {col7} could not be calculated!')
    
    return distance

def getLongestTrips(user):
    filename = f'utils/trainlogger/userdata/{user}.csv'
    distance_list = []
    
    # Open and read the CSV file
    with open(filename, newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            col6 = row[5]
            col7 = row[6]
            try:
                distance = getStationDistance(load_station_data('utils/trainlogger/stationDistances.csv'), col6, col7)
                distance_list.append((row, distance))
                print(f"{col6} to {col7}: {distance}")
            except:
                print(f'{col6} to {col7} could not be calculated!')
    
    # Sort the list by distance in descending order (longest to shortest)
    # Ensure all distances are floats
    distance_list = [(row, float(distance)) for row, distance in distance_list if isinstance(distance, (int, float, str)) and str(distance).replace('.', '', 1).isdigit()]
    distance_list.sort(key=lambda x: x[1], reverse=True)
    # Convert the list
    formatted_trips = ''
    for distance_list in distance_list:
        trip_details = distance_list[0]
        distance = distance_list[1]

        # Check if the trip details list has at least 5 elements
        count=1
        if len(trip_details) > 4:
            formatted_trips += f'`{round(distance,2)}km` - {trip_details[5]} to {trip_details[6]} `Log {trip_details[0]}`\n'
        else:
            formatted_trips += f'{distance}km - Incomplete Data `Log Number {trip_details[0]}`\n'
        count +=1
    return formatted_trips

def distanceOverTime(user, year, globalStats=False):
    if globalStats:
        base_path = 'utils/trainlogger/userdata/'
        file_paths = []
        if os.path.exists(base_path):
            for file in os.listdir(base_path):
                if file.endswith('.csv'):
                    file_paths.append(os.path.join(base_path, file))
        
        all_trips = []
        for filename in file_paths:
            try:
                with open(filename, newline='') as csvfile:
                    csv_reader = csv.reader(csvfile)
                    for row in csv_reader:
                        if len(row) >= 4 and row[3].strip() != '':
                            all_trips.append(row)
            except Exception as e:
                print(f"Error reading {filename}: {e}")
                continue
        
        # sort by date
        all_trips.sort(key=lambda x: x[3])
        
        distance_data = []
        cumulative_distance = 0
        
        for row in all_trips:
            if (year == 0 or row[3].startswith(str(year))) and len(row) >= 7:
                try:
                    trip_distance = getStationDistance(load_station_data('utils/trainlogger/stationDistances.csv'), row[5], row[6])
                    if trip_distance is not None:
                        cumulative_distance += trip_distance
                        distance_data.append([row[3], round(cumulative_distance, 2)])
                    else:
                        print(f'Distance for {row[5]} to {row[6]} is None')
                except Exception as e:
                    print(f'Error calculating distance from {row[5]} to {row[6]}: {str(e)}')
            else:
                if len(row) < 7:
                    print(f"Skipping incomplete row: {row}")
        
        daily_distances = {}
        for date, distance in distance_data:
            daily_distances[date] = distance
        
        aggregated_data = sorted([[date, distance] for date, distance in daily_distances.items()])
        
        output_file = f'temp/GlobalDistanceOverTime.csv'
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(aggregated_data)
        
        return output_file
    else:
        filename = f'utils/trainlogger/userdata/{user}.csv'
        distance_data = []
        cumulative_distance = 0
        
        with open(filename, newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            trips = [row for row in csv_reader if len(row) >= 4 and row[3].strip() != '']
            trips.sort(key=lambda x: x[3])
            
            for row in trips:
                if (year == 0 or row[3].startswith(str(year))) and len(row) >= 7:
                    try:
                        trip_distance = getStationDistance(load_station_data('utils/trainlogger/stationDistances.csv'), row[5], row[6])
                        if trip_distance is not None:
                            cumulative_distance += trip_distance
                            distance_data.append([row[3], round(cumulative_distance, 2)])
                        else:
                            print(f'Distance for {row[5]} to {row[6]} is None')
                    except Exception as e:
                        print(f'Error calculating distance from {row[5]} to {row[6]}: {str(e)}')
                else:
                    if len(row) < 7:
                        print(f"Skipping incomplete row: {row}")
        
        daily_distances = {}
        for date, distance in distance_data:
            daily_distances[date] = distance

        aggregated_data = [[date, distance] for date, distance in daily_distances.items()]
        
        output_file = f'temp/{user}DistanceOverTime.csv'
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(sorted(aggregated_data))
        
        return output_file

def topOperators(user):
    metroTrains = ["X'Trapolis 100", "HCMT", 'EDI Comeng', 'Alstom Comeng', 'Siemens Nexas', "X'Trapolis 2.0"]
    vlineTrains = ['VLocity', 'N Class', 'Sprinter']
    heritage = ['Tait', 'K Class']
    
    sydneyTrainsLines = ['T1', 'T2', 'T3', "T4", 'T5', "T6", 'T7', 'T8', 'T9']
    nswTrainsLines = ['Blue Mountains Line', 'Central Coast & Newcastle Line', 'Hunter Line', "South Coast Line", 'Southern Highlands Line', "North Coast Region", 'North Western Region', 'Southern Region', 'Western Region']
    sydneyMetroLines = ['Metro North West Line',]
    
    metro_count = 0
    vline_count = 0
    yarra_trams_count=0
    sydney_trams_count=0
    heritage_count=0

    sydney_trains_count=0
    nsw_trainlink_count=0
    sydney_metro_count=0
    
    jbr_count=0
    adelaideMetro_count=0
    adelaide_trams_count=0
    
    transperth_count = 0
    
    other_count = 0
    try:
        with open(f'utils/trainlogger/userdata/{user}.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                train_type = row[2]
                if train_type in metroTrains:
                    metro_count += 1
                elif train_type in vlineTrains:
                    vline_count += 1
                elif train_type in heritage:
                    heritage_count+=1
                else:
                    other_count += 1
    except:
        pass
    
    # sydney trains
    try:
        with open(f'utils/trainlogger/userdata/sydney-trains/{user}.csv') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                line = row[4]
                if line in sydneyTrainsLines:
                    sydney_trains_count +=1
                elif line in nswTrainsLines:
                    nsw_trainlink_count +=1
                elif line in sydneyMetroLines:
                    sydney_metro_count +=1
    except:
        pass
    
    # sydney tram
    try:
        with open(f'utils/trainlogger/userdata/sydney-trams/{user}.csv') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                sydney_trams_count +=1
    except:
        pass    
    
    # melbourne tram
    try:
        with open(f'utils/trainlogger/userdata/tram/{user}.csv') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                yarra_trams_count +=1    
    except:
        pass   
    # adelaide train
    try:
        with open(f'utils/trainlogger/userdata/adelaide-trains/{user}.csv') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                train_type = row[2]
                if train_type == 'NR Class':
                    jbr_count +=1
                elif train_type in ['3000 Class', '3100 Class','4000 Class']:
                    adelaideMetro_count +=1
                else:
                    other_count += 1
    except:
        pass 
    # adelaide tram
    try:
        with open(f'utils/trainlogger/userdata/adelaide-trams/{user}.csv') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                adelaide_trams_count +=1
    except:
        pass    
     # perth train
    try:
        with open(f'utils/trainlogger/userdata/perth-trains/{user}.csv') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                transperth_count +=1    
    except:
        pass
      
    # Write the results to a new CSV file
    output = f'temp/{user}TopOperators.csv'
    
    with open(output, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if metro_count > 0:
            writer.writerow(['Metro', metro_count])
        if vline_count > 0:
            writer.writerow(['V/Line', vline_count])
        if sydney_trains_count > 0:
            writer.writerow(['Sydney Trains', sydney_trains_count])
        if nsw_trainlink_count > 0:
            writer.writerow(['NSW Trainlink', nsw_trainlink_count])
        if sydney_metro_count > 0:
            writer.writerow(['Sydney Metro', sydney_metro_count])
        if yarra_trams_count > 0:
            writer.writerow(['Yarra Trams', yarra_trams_count])
        if sydney_trams_count > 0:
            writer.writerow(['Sydney Light Rail', sydney_trams_count])
        if heritage_count > 0:
            writer.writerow(['Heritage', heritage_count])
        if jbr_count > 0:
            writer.writerow(['Journey Beyond', jbr_count])
        if adelaideMetro_count > 0:
            writer.writerow(['Adelaide Metro', adelaideMetro_count])
        if adelaide_trams_count > 0:
            writer.writerow(['Adelaide Trams', adelaide_trams_count])
        if transperth_count > 0:
            writer.writerow(['Transperth', transperth_count])
        if other_count > 0:
            writer.writerow(['Other', other_count])
                
    return output

def completionList(user, line, summary:bool = False):
    if line == "Lilydale":
        stations = [
            "Lilydale",
            "Mooroolbark",
            "Croydon",
            "Ringwood East",
            "Ringwood",
            "Heatherdale",
            "Mitcham",
            "Nunawading",
            "Blackburn",
            "Laburnum",
            "Box Hill",
            "Union",
            "Chatham",
            "Canterbury",
            "East Camberwell",
            "Camberwell",
            "Auburn",
            "Glenferrie",
            "Hawthorn",
            "Burnley",
            "East Richmond",
            "Richmond"
        ] 
    elif line == "Belgrave":
        stations = [
            "Belgrave",
            "Tecoma",
            "Upwey",
            "Upper Ferntree Gully",
            "Ferntree Gully",
            "Boronia",
            "Bayswater",
            "Heathmont",
            "Ringwood",
            "Heatherdale",
            "Mitcham",
            "Nunawading",
            "Blackburn",
            "Laburnum",
            "Box Hill",
            "Union",
            "Chatham",
            "Canterbury",
            "East Camberwell",
            "Camberwell",
            "Auburn",
            "Glenferrie",
            "Hawthorn",
            "Burnley",
            "East Richmond",
            "Richmond"
        ]
    elif line == "Alamein":
        stations = [
            "Alamein",
            "Ashburton",
            "Burwood",
            "Hartwell",
            "Willison",
            "Riversdale",
            "Camberwell",
            "Auburn",
            "Glenferrie",
            "Hawthorn",
            "Burnley",
            "East Richmond",
            "Richmond"
        ]
    elif line == "Glen Waverley":
        stations = [
            "Glen Waverley",
            "Syndal",
            "Mount Waverley",
            "Jordanville",
            "Holmesglen",
            "East Malvern",
            "Darling",
            "Glen Iris",
            "Gardiner",
            "Tooronga",
            "Kooyong",
            "Heyington",
            "Burnley",
            "East Richmond",
            "Richmond"
        ]
    elif line == "Hurstbridge":
        stations = [
            "Hurstbridge",
            "Wattle Glen",
            "Diamond Creek",
            "Eltham",
            "Montmorency",
            "Greensborough",
            "Watsonia",
            "Macleod",
            "Rosanna",
            "Heidelberg",
            "Eaglemont",
            "Ivanhoe",
            "Darebin",
            "Alphington",
            "Fairfield",
            "Dennis",
            "Westgarth",
            "Clifton Hill",
            "Victoria Park",
            "Collingwood",
            "North Richmond",
            "West Richmond",
            "Jolimont"
        ]
    elif line == "Mernda": 
        stations = [
            "Mernda", 
            "Hawkstowe",
            "Middle Gorge", 
            "South Morang",
            "Epping", 
            "Lalor", 
            "Thomastown", 
            "Keon Park", 
            "Ruthven", 
            "Reservoir", 
            "Regent", 
            "Preston", 
            "Bell", 
            "Thornbury", 
            "Croxton", 
            "Northcote", 
            "Merri", 
            "Rushall", 
            "Clifton Hill",
            "Victoria Park",
            "Collingwood",
            "North Richmond",
            "West Richmond",
            "Jolimont"
        ]
    elif line == "Frankston":
        stations = [
            "Frankston", "Kananook", "Seaford", "Carrum", "Bonbeach",
            "Chelsea", "Edithvale", "Aspendale", "Mordialloc", "Parkdale", 
            "Mentone", "Cheltenham", "Southland", "Highett", "Moorabbin", "Patterson", 
            "Bentleigh", "McKinnon", "Ormond", "Glen Huntly", "Caulfield", "Malvern", 
            "Armadale", "Toorak", "Hawksburn", "South Yarra", "Richmond"
        ]
    elif line == "Craigieburn":
        stations = [
            "Craigieburn", "Roxburgh Park", "Coolaroo", "Broadmeadows", "Jacana", 
            "Glenroy", "Oak Park", "Pascoe Vale", "Strathmore", "Glenbervie", 
            "Essendon", "Moonee Ponds", "Ascot Vale", "Newmarket", "Kensington", "North Melbourne"
        ]
    elif line == "Upfield":
        stations = [
            "Upfield", "Gowrie", "Fawkner", "Merlynston", "Batman", 
            "Coburg", "Moreland", "Anstey", "Brunswick", "Jewell", 
            "Royal Park", "Flemington Bridge", "Macaulay", "North Melbourne"
        ]
    elif line == "Sandringham":
        stations = [
            "Sandringham", "Hampton", "Brighton Beach", "Middle Brighton", "North Brighton", 
            "Gardenvale", "Elsternwick", "Ripponlea", "Balaclava", "Windsor", 
            "Prahran", "South Yarra", "Richmond"
        ]
    elif line == "Werribee":
        stations = [
            "Werribee", "Hoppers Crossing", "Williams Landing",
            "Aircraft", "Laverton", "Westona",  "Altona", "Seaholme",
            "Newport", "Spotswood", "Yarraville", "Seddon", "Footscray", "South Kensington", "North Melbourne"
        ]
    elif line == "Williamstown":
        stations = [
            "Williamstown", "Williamstown Beach", "North Williamstown", "Newport", 
            "Spotswood", "Yarraville", "Seddon", "Footscray", "South Kensington", "North Melbourne"
        ]
    elif line == "Sunbury":
        stations = [
            "Sunbury",
            "Diggers Rest",
            "Watergardens",
            "Keilor Plains",
            "St Albans",
            "Ginifer",
            "Albion",
            "Sunshine",
            "Tottenham",
            "West Footscray",
            "Middle Footscray",
            "Footscray"
        ]
    elif line == "Cranbourne":
        stations = [
            "Cranbourne",
            "Merinda Park",
            "Lynbrook",
            "Dandenong",
            "Yarraman",
            "Noble Park",
            "Sandown Park",
            "Springvale",
            "Westall",
            "Clayton",
            "Huntingdale",
            "Oakleigh",
            "Hughesdale",
            "Murrumbeena",
            "Carnegie",
            "Caulfield",
            "Malvern"
        ]
    elif line == "Pakenham":
        stations = [
            "East Pakenham",
            "Pakenham",
            "Cardinia Road",
            "Officer",
            "Beaconsfield",
            "Berwick",
            "Narre Warren",
            "Hallam",
            "Dandenong",
            "Yarraman",
            "Noble Park",
            "Sandown Park",
            "Springvale",
            "Westall",
            "Clayton",
            "Huntingdale",
            "Oakleigh",
            "Hughesdale",
            "Murrumbeena",
            "Carnegie",
            "Caulfield",
            "Malvern"
        ]
    elif line == "Stony Point":
        stations = [
            "Stony Point",
            "Crib Point",
            "Morradoo",
            "Bittern",
            "Hastings",
            "Tyabb",
            "Somerville",
            "Baxter",
            "Leawarra",
            "Frankston"
        ]
    elif line == "Flemington Racecourse":
        stations = [
            "Flemington Racecourse",
            "Showgrounds",
            "North Melbourne"
        ]
    elif line == "Metro Tunnel":
        stations = [
            "Arden",
            "Parkville",
            "State Library",
            "Town Hall",
            "Anzac"
        ]
    elif line == "City Loop":
        stations = [
            "Flinders Street",
            "Southern Cross",
            "Flagstaff",
            "Melbourne Central",
            "Parliament"
        ]
    elif line == "All":
        stations = [
            "Aircraft", "Alamein", "Albion", "Alphington", "Altona", "Anstey", "Anzac", "Arden", 
            "Armadale", "Ascot Vale", "Ashburton", "Aspendale", "Auburn", "Balaclava", "Batman", "Baxter", "Bayswater",
            "Beaconsfield", "Belgrave", "Bell", "Bentleigh", "Berwick", "Bittern", "Blackburn", "Bonbeach", "Boronia", 
            "Box Hill", "Brighton Beach", "Broadmeadows", "Brunswick", "Burnley", "Burwood", "Camberwell", 
            "Canterbury", "Cardinia Road", "Carnegie", "Carrum", "Caulfield", "Chatham", "Chelsea", "Cheltenham", "Clayton",
            "Clifton Hill", "Coburg", "Collingwood", "Coolaroo", "Craigieburn", "Cranbourne", 
            "Crib Point", "Croxton", "Croydon", "Dandenong", "Darebin", "Darling", "Dennis", 
            "Diamond Creek", "Diggers Rest", "Eaglemont", "East Camberwell", "East Malvern", "East Pakenham", 
            "East Richmond", "Edithvale", "Elsternwick", "Eltham", "Epping", "Essendon", "Fairfield", "Fawkner", 
            "Ferntree Gully", "Flagstaff", "Flemington Bridge", "Flemington Racecourse", "Flinders Street", 
            "Footscray", "Frankston", "Gardiner", "Gardenvale", "Ginifer", "Glen Huntly", "Glen Iris", 
            "Glen Waverley", "Glenbervie", "Glenferrie", "Glenroy", "Gowrie", "Greensborough", "Hallam", 
            "Hampton", "Hartwell", "Hastings", "Hawkstowe", "Hawksburn", "Hawthorn", "Heatherdale", "Heathmont", 
            "Heidelberg", "Heyington", "Highett", "Holmesglen", "Hoppers Crossing", "Hughesdale", "Huntingdale", 
            "Hurstbridge", "Ivanhoe", "Jacana", "Jewell", "Jolimont", "Jordanville", "Kananook", "Keilor Plains", 
            "Kensington", "Keon Park", "Kooyong", "Laburnum", "Lalor", "Laverton", "Leawarra", "Lilydale", 
            "Lynbrook", "Macaulay", "Macleod", "Malvern", "McKinnon", "Melbourne Central", "Mentone", 
            "Merinda Park", "Merylnston", "Mernda", "Merri", "Middle Brighton", "Middle Gorge", "Middle Footscray", "Mitcham", "Montmorency", "Moonee Ponds", "Moorabbin", 
            "Mooroolbark", "Morradoo", "Mount Waverley", "Mordialloc", "Moreland", "Murrumbeena", "Narre Warren", 
            "Newmarket", "Newport", "Noble Park", "North Brighton", "North Melbourne", "North Richmond", 
            "North Williamstown", "Northcote", "Nunawading", "Oak Park", "Oakleigh", "Officer", "Ormond", 
            "Pakenham", "Parkdale", "Parkville", "Parliament", "Pascoe Vale", "Patterson", "Prahran", 
            "Preston", "Regent", "Reservoir", "Richmond", "Ringwood", "Ringwood East", "Ripponlea", "Riversdale", 
            "Rosanna", "Roxburgh Park", "Royal Park", "Rushall", "Ruthven", "Sandown Park", 
            "Sandringham", "Seaford", "Seaholme", "Seddon", "Showgrounds", "Somerville", "South Kensington", "Southland", 
            "South Morang", "South Yarra", "Southern Cross", "Spotswood", "Springvale", "St Albans", 
            "State Library", "Stony Point", "Strathmore", "Sunbury", "Sunshine", "Syndal", "Tecoma", 
            "Thomastown", "Thornbury", "Toorak", "Tooronga", "Tottenham", "Town Hall", "Tyabb", "Union", 
            "Upfield", "Upper Ferntree Gully", "Upwey", "Victoria Park", "Watergardens", "Watsonia", "Wattle Glen", 
            "Werribee", "West Footscray", "West Richmond", "Westall", "Westgarth", "Westona", "Williams Landing", 
            "Williamstown", "Williamstown Beach", "Willison", "Windsor", "Yarraman", "Yarraville"
        ]
    else:
        line = ['Invalid Line:', f'{line}']

    with open(f'utils/trainlogger/userdata/{user}.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        csv_data = list(reader)



   # Create a dictionary to count the occurrences of each item
    item_counts = {}
    for row in csv_data:
        # practically random variables for "Location 1" and "Location 2"
        l1 = row[5]
        l2 = row[6]

        if 'jolimont' in l1.lower():
            l1 = "Jolimont"
        if 'jolimont' in l2.lower():
            l2 = "Jolimont"

        if l1 in item_counts:
            item_counts[l1] += 1
        else:
            item_counts[l1] = 1
        if l2 in item_counts:
            item_counts[l2] += 1
        else:
            item_counts[l2] = 1

    if summary == False:
        # Create a string with ticks for matching items
        result_string = '\n'.join([f"`{item}` {'✅️' if item in item_counts else ''} {item_counts[item]} times" if item in item_counts else f"`{item}`" for item in stations])
    else:
        result_string = ''
      
    # Calculate the percentage of stations that have been ticked
    # ticked_stations = [item for item in stations if item in [row[5] for row in csv_data] or item for item in stations if item in [row[6] for row in csv_data]]
    ticked_stations = [item for item in stations if item in item_counts]
    percent_ticked = round(len(ticked_stations) / len(stations) * 100, 2)

    # Add the percentage to the end of the string
    result_string += f"\n\n{len(ticked_stations)}/{len(stations)} ({percent_ticked}%) of stations visited" if summary == False else f"{len(ticked_stations)}/{len(stations)} `{percent_ticked}%`"
    
    return(result_string)

def setlist(user, train, summary:bool = False): # probably shouldn't make this hard coded but use the trainsets csv.
    # List of items
    if train == "X'Trapolis 100":
        sets = [
        "1M-1301T-2M", "3M-1302T-4M", "5M-1303T-6M", "7M-1304T-8M", "9M-1305T-10M",
        "11M-1306T-12M", "13M-1307T-14M", "15M-1308T-16M", "17M-1309T-18M", "19M-1310T-20M",
        "21M-1311T-22M", "23M-1312T-24M", "25M-1313T-26M", "27M-1314T-28M", "29M-1315T-30M",
        "31M-1316T-32M", "33M-1317T-34M", "35M-1318T-36M", "37M-1319T-38M", "39M-1320T-40M",
        "41M-1321T-42M", "43M-1322T-44M", "45M-1323T-46M", "47M-1324T-48M", "49M-1325T-50M",
        "51M-1326T-52M", "53M-1327T-54M", "55M-1328T-56M", "57M-1329T-58M", "59M-1330T-60M",
        "61M-1331T-62M", "63M-1332T-64M", "65M-1333T-66M", "67M-1334T-68M", "69M-1335T-70M",
        "71M-1336T-72M", "73M-1337T-74M", "75M-1338T-76M", "77M-1339T-78M", "79M-1340T-80M",
        "81M-1341T-82M", "83M-1342T-84M", "85M-1343T-86M", "87M-1344T-88M", "89M-1345T-90M",
        "91M-1346T-92M", "93M-1347T-94M", "95M-1348T-96M", "97M-1349T-98M", "99M-1350T-100M",
        "101M-1351T-102M", "103M-1352T-104M", "105M-1353T-106M", "107M-1354T-108M", "109M-1355T-110M",
        "111M-1356T-112M", "113M-1357T-114M", "115M-1358T-116M", "117M-1359T-118M", "119M-1360T-120M",
        "121M-1361T-122M", "123M-1362T-124M", "125M-1363T-126M", "127M-1364T-128M", "129M-1365T-130M",
        "131M-1366T-132M", "133M-1367T-134M", "135M-1368T-136M", "137M-1369T-138M", "139M-1370T-140M",
        "141M-1371T-142M", "143M-1372T-144M", "145M-1373T-146M", "147M-1374T-148M", "149M-1375T-150M",
        "151M-1376T-152M", "153M-1377T-154M", "155M-1378T-156M", "157M-1379T-158M", "159M-1380T-160M",
        "161M-1381T-162M", "163M-1382T-164M", "165M-1383T-166M", "167M-1384T-168M", "169M-1385T-170M",
        "171M-1386T-172M", "173M-1387T-174M", "175M-1388T-176M", "177M-1389T-178M", "179M-1390T-180M",
        "181M-1391T-182M", "183M-1392T-184M", "185M-1393T-186M", "187M-1394T-188M", "189M-1395T-190M",
        "191M-1396T-192M", "193M-1397T-194M", "195M-1398T-196M", "197M-1399T-198M", "199M-1400T-200M",
        "201M-1401T-202M", "203M-1402T-204M", "205M-1403T-206M", "207M-1404T-208M", "209M-1405T-210M",
        "211M-1406T-212M", "213M-1407T-214M", "215M-1408T-216M", "217M-1409T-218M", "219M-1410T-220M",
        "221M-1411T-222M", "223M-1412T-224M", "225M-1413T-226M", "227M-1414T-228M", "229M-1415T-230M",
        "231M-1416T-232M", "233M-1417T-234M", "235M-1418T-236M", "237M-1419T-238M", "239M-1420T-240M",
        "241M-1421T-242M", "243M-1422T-244M", "245M-1423T-246M", "247M-1424T-248M", "249M-1425T-250M",
        "251M-1426T-252M", "253M-1427T-254M", "255M-1428T-256M", "257M-1429T-258M", "259M-1430T-260M",
        "261M-1431T-262M", "263M-1432T-264M", "265M-1433T-266M", "267M-1434T-268M", "269M-1435T-270M",
        "271M-1436T-272M", "273M-1437T-274M", "275M-1438T-276M", "277M-1439T-278M", "279M-1440T-280M",
        "281M-1441T-282M", "283M-1442T-284M", "285M-1443T-286M", "287M-1444T-288M", "851M-1626T-852M",
        "853M-1627T-854M", "855M-1628T-856M", "857M-1629T-858M", "859M-1630T-860M", "861M-1631T-862M",
        "863M-1632T-864M", "865M-1633T-866M", "867M-1634T-868M", "869M-1635T-870M", "871M-1636T-872M",
        "873M-1637T-874M", "875M-1638T-876M", "877M-1639T-878M", "879M-1640T-880M", "881M-1641T-882M",
        "883M-1642T-884M", "885M-1643T-886M", "887M-1644T-888M", "889M-1645T-890M", "891M-1646T-892M",
        "893M-1647T-894M", "895M-1648T-896M", "897M-1649T-898M", "899M-1650T-900M", "901M-1651T-902M",
        "903M-1652T-904M", "905M-1653T-906M", "907M-1654T-908M", "909M-1655T-910M", "911M-1656T-912M",
        "913M-1657T-914M", "915M-1658T-916M", "917M-1659T-918M", "919M-1660T-920M", "921M-1661T-922M",
        "923M-1662T-924M", "925M-1663T-926M", "927M-1664T-928M", "929M-1665T-930M", "931M-1666T-932M",
        "933M-1667T-934M", "935M-1668T-936M", "937M-1669T-938M", "939M-1670T-940M", "941M-1671T-942M",
        "943M-1672T-944M", "945M-1673T-946M", "947M-1674T-948M", "949M-1675T-950M", "951M-1676T-952M",
        "953M-1677T-954M", "955M-1678T-956M", "957M-1679T-958M", "959M-1680T-960M", "961M-1681T-962M",
        "963M-1682T-964M", "965M-1683T-966M", "967M-1684T-968M", "969M-1685T-970M", "971M-1686T-972M",
        "973M-1687T-974M", "975M-1688T-976M", "977M-1689T-978M", "979M-1690T-980M", "981M-1691T-982M",
        "983M-1692T-984M", "985M-1693T-986M",
    ]
    elif train == "X'Trapolis 2.0":
        sets = [
            "8101-8201-8301-8401-8501-8601",
            "8102-8202-8302-8402-8502-8602",
            "8103-8203-8303-8403-8503-8603",
            "8104-8204-8304-8404-8504-8604",
            "8105-8205-8305-8405-8505-8605",
            "8106-8206-8306-8406-8506-8606",
            "8107-8207-8307-8407-8507-8607",
            "8108-8208-8308-8408-8508-8608",
            "8109-8209-8309-8409-8509-8609",
            "8110-8210-8310-8410-8510-8610",
            "8111-8211-8311-8411-8511-8611",
            "8112-8212-8312-8412-8512-8612",
            "8113-8213-8313-8413-8513-8613",
            "8114-8214-8314-8414-8514-8614",
            "8115-8215-8315-8415-8515-8615",
            "8116-8216-8316-8416-8516-8616",
            "8117-8217-8317-8417-8517-8617",
            "8118-8218-8318-8418-8518-8618",
            "8119-8219-8319-8419-8519-8619",
            "8120-8220-8320-8420-8520-8620",
            "8121-8221-8321-8421-8521-8621",
            "8122-8222-8322-8422-8522-8622",
            "8123-8223-8323-8423-8523-8623",
            "8124-8224-8324-8424-8524-8624",
            "8125-8225-8325-8425-8525-8625",
            "8126-8226-8326-8426-8526-8626",
            "8127-8227-8327-8427-8527-8627",
            "8128-8228-8328-8428-8528-8628",
            "8129-8229-8329-8429-8529-8629",
            "8130-8230-8330-8430-8530-8630",
            "8131-8231-8331-8431-8531-8631",
            "8132-8232-8332-8432-8532-8632",
            "8133-8233-8333-8433-8533-8633",
            "8134-8234-8334-8434-8534-8634",
            "8135-8235-8335-8435-8535-8635",
            "8136-8236-8336-8436-8536-8636",
            "8137-8237-8337-8437-8537-8637",
            "8138-8238-8338-8438-8538-8638",
            "8139-8239-8339-8439-8539-8639",
            "8140-8240-8340-8440-8540-8640",
            "8141-8241-8341-8441-8541-8641",
            "8142-8242-8342-8442-8542-8642",
            "8143-8243-8343-8443-8543-8643",
            "8144-8244-8344-8444-8544-8644",
            "8145-8245-8345-8445-8545-8645",
            "8146-8246-8346-8446-8546-8646",
            "8147-8247-8347-8447-8547-8647",
            "8148-8248-8348-8448-8548-8648",
            "8149-8249-8349-8449-8549-8649",
            "8150-8250-8350-8450-8550-8650",
        ]
    elif train == 'Comeng':
        sets = [
        "301M-1001T-302M", "303M-1002T-304M", "307M-1004T-308M", "309M-1005T-310M",
        "311M-1006T-312M", "313M-1007T-333M", "314M-1017T-334M", "316M-1033T-319M",
        "317M-1009T-318M", "320M-1107T-321M", "322M-1011T-425M", "323M-1012T-361M",
        "324M-1031T-342M", "325M-1013T-326M", "327M-1082T-349M", "328M-1014T-464M",
        "329M-1015T-366M", "330M-1025T-350M", "331M-1050T-400M", "332M-1016T-399M",
        "335M-1045T-387M", "336M-1069T-437M", "337M-1019T-438M", "338M-1092T-484M",
        "339M-1020T-340M", "341M-1021T-463M", "343M-1010T-384M", "344M-1044T-390M",
        "345M-1023T-346M", "347M-1024T-348M", "351M-1026T-352M", "353M-1027T-354M",
        "355M-1028T-356M", "357M-1029T-358M", "359M-1030T-360M", "362M-1038T-376M",
        "363M-1032T-364M", "365M-1042T-383M", "367M-1034T-368M", "369M-1035T-370M",
        "371M-1036T-372M", "373M-1037T-374M", "375M-1094T-488M", "377M-1039T-378M",
        "379M-1040T-380M", "381M-1041T-382M", "385M-1043T-386M", "389M-1063T-426M",
        "391M-1047T-392M", "393M-1048T-394M", "395M-1046T-396M", "397M-1049T-398M",
        "401M-1051T-402M", "403M-1018T-404M", "405M-1053T-406M", "407M-1054T-408M",
        "409M-1055T-410M", "411M-1056T-412M", "413M-1057T-414M", "415M-1058T-416M",
        "417M-1059T-418M", "419M-1060T-420M", "421M-1061T-422M", "423M-1062T-424M",
        "427M-1052T-487M", "428M-1064T-483M", "429M-1065T-430M", "431M-1066T-432M",
        "433M-1067T-434M", "435M-1068T-436M", "439M-1070T-440M", "441M-1071T-442M",
        "443M-1072T-444M", "445M-1073T-446M", "447M-1074T-448M", "449M-1075T-450M",
        "451M-1076T-452M", "453M-1077T-454M", "455M-1078T-456M", "457M-1079T-458M",
        "459M-1080T-460M", "461M-1081T-462M", "465M-1083T-466M", "467M-1084T-468M",
        "471M-1086T-472M", "473M-1087T-474M", "475M-1088T-476M", "477M-1089T-478M",
        "479M-1090T-480M", "481M-1091T-482M", "485M-1093T-486M", "489M-1105T-510M",
        "490M-1095T-509M", "491M-1096T-492M", "493M-1097T-494M", "495M-1098T-496M",
        "497M-1099T-498M", "499M-1100T-534M", "501M-1101T-502M", "503M-1102T-504M",
        "505M-1103T-506M", "507M-1104T-508M", "511M-1106T-512M", "513M-1008T-514M",
        "515M-1108T-516M", "517M-1117T-529M", "518M-1126T-551M", "519M-1110T-520M",
        "521M-1111T-522M", "523M-1112T-524M", "525M-1113T-526M", "527M-1114T-528M",
        "530M-1115T-552M", "531M-1116T-532M", "535M-1118T-536M", "537M-1119T-538M",
        "539M-1120T-540M", "541M-1121T-542M", "543M-1122T-544M", "545M-1123T-546M",
        "547M-1124T-548M", "549M-1125T-550M", "553M-1127T-554M", "561M-1131T-565M",
        "562M-1133T-566M", "563M-1132T-564M", "567M-1134T-568M", "569M-1156T-612M",
        "570M-1135T-661M", "571M-1136T-572M", "573M-1137T-574M", "575M-1138T-576M",
        "577M-1139T-578M", "579M-1140T-580M", "581M-1141T-584M", "582M-1145T-651M",
        "583M-1022T-589M", "585M-1143T-586M", "587M-1144T-588M", "590M-1174T-647M",
        "591M-1146T-592M", "593M-1147T-594M", "595M-1148T-596M", "597M-1149T-598M",
        "599M-1150T-600M", "601M-1151T-602M", "603M-1152T-604M", "605M-1153T-606M",
        "607M-1154T-608M", "609M-1155T-610M", "611M-1181T-662M", "613M-1157T-614M",
        "615M-1158T-616M", "617M-1159T-618M", "619M-1160T-620M", "621M-1161T-622M",
        "623M-1162T-624M", "625M-1163T-626M", "627M-1164T-648M", "628M-1176T-652M",
        "629M-1142T-630M", "631M-1166T-632M", "633M-1167T-634M", "635M-1168T-636M",
        "637M-1169T-638M", "639M-1170T-640M", "641M-1187T-674M", "642M-1171T-673M",
        "643M-1172T-644M", "645M-1173T-646M", "649M-1175T-650M", "653M-1177T-654M",
        "655M-1178T-656M", "657M-1179T-658M", "659M-1180T-660M", "663M-1182T-664M",
        "665M-1183T-666M", "667M-1184T-668M", "669M-1185T-670M", "675M-1188T-676M",
        "677M-1189T-678M", "679M-1190T-680M", "691M-1196T-692M", "693M-1197T-694M",
        "695M-1198T-696M", "697M-1199T-698M"
    ]
    elif train == 'HCMT':
        sets =[
        "9001-9101-9201-9301-9701-9801-9901",
        "9002-9102-9202-9302-9702-9802-9902",
        "9003-9103-9203-9303-9703-9803-9903",
        "9004-9104-9204-9304-9704-9804-9904",
        "9005-9105-9205-9305-9705-9805-9905",
        "9006-9106-9206-9306-9706-9806-9906",
        "9007-9107-9207-9307-9707-9807-9907",
        "9008-9108-9208-9308-9708-9808-9908",
        "9009-9109-9209-9309-9709-9809-9909",
        "9010-9110-9210-9310-9710-9810-9910",
        "9011-9111-9211-9311-9711-9811-9911",
        "9012-9112-9212-9312-9712-9812-9912",
        "9013-9113-9213-9313-9713-9813-9913",
        "9014-9114-9214-9314-9714-9814-9914",
        "9015-9115-9215-9315-9715-9815-9915",
        "9016-9116-9216-9316-9716-9816-9916",
        "9017-9117-9217-9317-9717-9817-9917",
        "9018-9118-9218-9318-9718-9818-9918",
        "9019-9119-9219-9319-9719-9819-9919",
        "9020-9120-9220-9320-9720-9820-9920",
        "9021-9121-9221-9321-9721-9821-9921",
        "9022-9122-9222-9322-9722-9822-9922",
        "9023-9123-9223-9323-9723-9823-9923",
        "9024-9124-9224-9324-9724-9824-9924",
        "9025-9125-9225-9325-9725-9825-9925",
        "9026-9126-9226-9326-9726-9826-9926",
        "9027-9127-9227-9327-9727-9827-9927",
        "9028-9128-9228-9328-9728-9828-9928",
        "9029-9129-9229-9329-9729-9829-9929",
        "9030-9130-9230-9330-9730-9830-9930",
        "9031-9131-9231-9331-9731-9831-9931",
        "9032-9132-9232-9332-9732-9832-9932",
        "9033-9133-9233-9333-9733-9833-9933",
        "9034-9134-9234-9334-9734-9834-9934",
        "9035-9135-9235-9335-9735-9835-9935",
        "9036-9136-9236-9336-9736-9836-9936",
        "9037-9137-9237-9337-9737-9837-9937",
        "9038-9138-9238-9338-9738-9838-9938",
        "9039-9139-9239-9339-9739-9839-9939",
        "9040-9140-9240-9340-9740-9840-9940",
        "9041-9141-9241-9341-9741-9841-9941",
        "9042-9142-9242-9342-9742-9842-9942",
        "9043-9143-9243-9343-9743-9843-9943",
        "9044-9144-9244-9344-9744-9844-9944",
        "9045-9145-9245-9345-9745-9845-9945",
        "9046-9146-9246-9346-9746-9846-9946",
        "9047-9147-9247-9347-9747-9847-9947",
        "9048-9148-9248-9348-9748-9848-9948",
        "9049-9149-9249-9349-9749-9849-9949",
        "9050-9150-9250-9350-9750-9850-9950",
        "9051-9151-9251-9351-9751-9851-9951",
        "9052-9152-9252-9352-9752-9852-9952",
        "9053-9153-9253-9353-9753-9853-9953",
        "9054-9154-9254-9354-9754-9854-9954",
        "9055-9155-9255-9355-9755-9855-9955",
        "9056-9156-9256-9356-9756-9856-9956",
        "9057-9157-9257-9357-9757-9857-9957",
        "9058-9158-9258-9358-9758-9858-9958",
        "9059-9159-9259-9359-9759-9859-9959",
        "9060-9160-9260-9360-9760-9860-9960",
        "9061-9161-9261-9361-9761-9861-9961",
        "9062-9162-9262-9362-9762-9862-9962",
        "9063-9163-9263-9363-9763-9863-9963",
        "9064-9164-9264-9364-9764-9864-9964",
        "9065-9165-9265-9365-9765-9865-9965",
        "9066-9166-9266-9366-9766-9866-9966",
        "9067-9167-9267-9367-9767-9867-9967",
        "9068-9168-9268-9368-9768-9868-9968",
        "9069-9169-9269-9369-9769-9869-9969",
        "9070-9170-9270-9370-9770-9870-9970"
    ]
    elif train == "Siemens Nexas":
        sets =[
    "701M-2501T-702M",
    "703M-2502T-704M",
    "705M-2503T-706M",
    "707M-2504T-708M",
    "709M-2505T-710M",
    "711M-2506T-712M",
    "713M-2507T-714M",
    "715M-2508T-716M",
    "717M-2509T-718M",
    "719M-2510T-720M",
    "721M-2511T-722M",
    "723M-2512T-724M",
    "725M-2513T-726M",
    "727M-2514T-728M",
    "729M-2515T-730M",
    "731M-2516T-732M",
    "733M-2517T-734M",
    "735M-2518T-736M",
    "737M-2519T-738M",
    "739M-2520T-740M",
    "741M-2521T-742M",
    "743M-2522T-744M",
    "745M-2523T-746M",
    "747M-2524T-748M",
    "749M-2525T-750M",
    "751M-2526T-752M",
    "753M-2527T-754M",
    "755M-2528T-756M",
    "757M-2529T-758M",
    "759M-2530T-760M",
    "761M-2531T-762M",
    "763M-2532T-764M",
    "765M-2533T-766M",
    "767M-2534T-768M",
    "769M-2535T-770M",
    "771M-2536T-772M",
    "773M-2537T-774M",
    "775M-2538T-776M",
    "777M-2539T-778M",
    "779M-2540T-780M",
    "781M-2541T-782M",
    "783M-2542T-784M",
    "785M-2543T-786M",
    "787M-2544T-788M",
    "789M-2545T-790M",
    "791M-2546T-792M",
    "793M-2547T-794M",
    "795M-2548T-796M",
    "797M-2549T-798M",
    "799M-2550T-800M",
    "801M-2551T-802M",
    "803M-2552T-804M",
    "805M-2553T-806M",
    "807M-2554T-808M",
    "809M-2555T-810M",
    "811M-2556T-812M",
    "813M-2557T-814M",
    "815M-2558T-816M",
    "817M-2559T-818M",
    "819M-2560T-820M",
    "821M-2561T-822M",
    "823M-2562T-824M",
    "825M-2563T-826M",
    "827M-2564T-828M",
    "829M-2565T-830M",
    "831M-2566T-832M",
    "833M-2567T-834M",
    "835M-2568T-836M",
    "837M-2569T-838M",
    "839M-2570T-840M",
    "841M-2571T-842M",
    "843M-2572T-844M"
]
    elif train == 'VLocity':
        sets = [
    "1100-1300-1200", "1101-1301-1201", "1102-1302-1202", "1103-1303-1203", "1104-1304-1204",
    "1105-1305-1205", "1106-1306-1206", "1107-1307-1207", "1108-1308-1208", "1109-1309-1209",
    "1110-1310-1210", "1111-1311-1211", "1112-1312-1212", "1113-1313-1213", "1114-1314-1214",
    "1115-1315-1215", "1116-1316-1216", "1117-1317-1217", "1118-1318-1218", "1119-1319-1219",
    "1120-1320-1220", "1121-1321-1221", "1122-1322-1222", "1123-1323-1223", "1124-1324-1224",
    "1125-1325-1225", "1126-1326-1226", "1127-1327-1227", "1128-1328-1228", "1130-1330-1230",
    "1131-1331-1231", "1132-1332-1232", "1133-1333-1233", "1134-1334-1234", "1135-1335-1235",
    "1136-1336-1236", "1137-1337-1237", "1138-1338-1238", "1139-1339-1239", "1140-1340-1240",
    "1141-1341-1241", "1142-1342-1242", "1143-1343-1243", "1144-1344-1244", "1145-1345-1245",
    "1146-1346-1246", "1147-1347-1247", "1148-1348-1248", "1149-1349-1249", "1150-1350-1250",
    "1151-1351-1251", "1152-1352-1252", "1153-1353-1253", "1154-1354-1254", "1155-1355-1255",
    "1156-1356-1256", "1157-1357-1257", "1158-1358-1258", "1159-1359-1259", "1160-1360-1260",
    "1161-1361-1261", "1162-1362-1262", "1163-1363-1263", "1164-1364-1264", "1165-1365-1265",
    "1166-1366-1266", "1167-1367-1267", "1168-1368-1268", "1169-1369-1269", "1170-1370-1270",
    "1171-1371-1271", "1172-1372-1272", "1173-1373-1273", "1174-1374-1274", "1175-1375-1275",
    "1176-1376-1276", "1177-1377-1277", "1178-1378-1278", "1179-1379-1279", "1180-1380-1280",
    "1181-1381-1281", "1182-1382-1282", "1183-1383-1283", "1184-1384-1284", "1185-1385-1285",
    "1186-1386-1286", "1187-1387-1287", "1188-1388-1288", "1189-1389-1289", "1190-1390-1290",
    "1191-1391-1291", "1192-1392-1292", "1193-1593-1293", "1194-1594-1294", "1195-1595-1295",
    "1196-1596-1296", "1197-1597-1297", "1198-1598-1298", "1199-1399-1299", "2100-2300-2200",
    "2101-2301-2201", "2102-2302-2202", "2103-2303-2203", "2104-2304-2204", "2105-2305-2205",
    "2106-2306-2206", "2107-2307-2207", "2108-2308-2208", "2109-2309-2209", "2110-2310-2210",
    "2111-2311-2211", "2112-2312-2212", "2113-2313-2213", "2114-2314-2214", "2115-2315-2215",
    "2116-2316-2216", "2117-2317-2217", "2118-2318-2218", "2119-2319-2219", "2120-2320-2220",
    "2121-2321-2221", "2122-2322-2222", "2123-2323-2223", "2124-2324-2224", "2125-2325-2225",
    "2126-2326-2226", "2127-2327-2227", "2128-2328-2228", "2129-2329-2229", "2130-2330-2230",
    "2131-2331-2231", "2132-2332-2232", "2134-2334-2234", "2135-2335-2235", "2136-2336-2236",
    "2137-2337-2237", "2138-2338-2238", "2139-2339-2239", "2140-2340-2240", "2141-2341-2241"
]
    elif train == 'Sprinter':
        sets = [
    '7001', '7002', '7003', '7004', '7005', '7006', '7007', '7008', '7009', '7010',
    '7011', '7012', '7013', '7014', '7015', '7016', '7017', '7018', '7019', '7020', 
    '7021', '7022'
]
    elif train == 'N Class':
        sets = [
    "N451", "N452", "N453", "N454", "N455", "N456", "N457", "N458", "N459", "N460",
    "N461", "N462", "N463", "N464", "N465", "N466", "N467", "N468", "N469", "N470",
    "N471", "N472", "N473", "N474", "N475"
]
        
    else:
        sets = ['Invalid Train Type:', f'{train}']

    # Read CSV file
    with open(f'utils/trainlogger/userdata/{user}.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        csv_data = list(reader)

   # Create a dictionary to count the occurrences of each item
    item_counts = {}
    for row in csv_data:
        if row[1] in item_counts:
            item_counts[row[1]] += 1
        else:
            item_counts[row[1]] = 1

    if summary == False:
        # Create a string with ticks for matching items
        result_string = '\n'.join([f"`{item}` {'✅️' if item in item_counts else ''} {item_counts[item]} times" if item in item_counts else f"`{item}`" for item in sets])
    else:
        result_string = ''
      
    # Calculate the percentage of sets that have been ticked
    ticked_sets = [item for item in sets if item in [row[1] for row in csv_data]]
    percent_ticked = round(len(ticked_sets) / len(sets) * 100, 2)

    # Add the percentage to the end of the string
    result_string += f"\n\n{len(ticked_sets)}/{len(sets)} ({percent_ticked}%) sets ridden" if summary == False else f"{len(ticked_sets)}/{len(sets)} `{percent_ticked}%`"
    
    return(result_string)

def stationlist(user, state):
    # Load station list for Victorian state
    if state == 'Victorian':
        with open("utils/datalists/stations.txt", "r") as file:
            sets = [line.strip() for line in file]
         # Read CSV file
        with open(f'utils/trainlogger/userdata/{user}.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            csv_data = list(reader)
            
    if state == 'New South Wales':
        with open("utils/datalists/nswstations.txt", "r") as file:
            sets = [line.strip() for line in file]
        # Read CSV file
        with open(f'utils/trainlogger/userdata/sydney-trains/{user}.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            csv_data = list(reader)
    if state == 'South Australian':
        with open("utils/datalists/adelaidestations.txt", "r") as file:
            sets = [line.strip() for line in file]
        # Read CSV file
        with open(f'utils/trainlogger/userdata/adelaide-trains/{user}.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            csv_data = list(reader)
            
    if state == 'Western Australian':
        with open("utils/datalists/perthstations.txt", "r") as file:
            sets = [line.strip() for line in file]
        # Read CSV file
        with open(f'utils/trainlogger/userdata/perth-trains/{user}.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            csv_data = list(reader)

    # Create a dictionary to count occurrences of each item
    item_counts = {}
    for row in csv_data:
        # Add count for row[5] if it exists in the row
        if row[5] in item_counts:
            item_counts[row[5]] += 1
        else:
            item_counts[row[5]] = 1

        # Add count for row[6] if it exists in the row
        if row[6] in item_counts:
            item_counts[row[6]] += 1
        else:
            item_counts[row[6]] = 1

    # Create a result string with ticks for matching items
    result_string = '\n'.join([
        f"`{item}` {'✅️' if item in item_counts else ''} {item_counts[item]} times"
        if item in item_counts else f"`{item}`"
        for item in sets
    ])
    
    # Calculate the percentage of sets that have been ticked
    ticked_sets = [item for item in sets if item in item_counts]
    percent_ticked = round(len(ticked_sets) / len(sets) * 100, 2)

    # Add the percentage to the end of the string
    result_string += f"\n\n{len(ticked_sets)}/{len(sets)} ({percent_ticked}%) stations visited"
    
    return result_string

def terminiList(user):
    termini = [
        "Alamein", "Albury", "Ararat", "Bairnsdale", "Belgrave", "Cranbourne", "Craigieburn", "East Pakenham", "Eaglehawk", "Echuca", "Epsom", "Flemington Racecourse", "Frankston", "Glen Waverley", "Hurstbridge", "Lilydale", "Maryborough", "Mernda", "Sandringham", "Seymour", "Shepparton", "Stony Point", "Sunbury", "Swan Hill", "Traralgon", "Upfield", "Waurn Ponds", "Warrnambool", "Wendouree", "Werribee", "Williamstown"
    ]
    
    with open(f'utils/trainlogger/userdata/{user}.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        csv_data = list(reader)

    item_counts = {}
    for row in csv_data:
        if row[5] in item_counts:
            item_counts[row[5]] += 1
        if row[6] in item_counts:
            item_counts[row[6]] += 1
        else:
            item_counts[row[5]] = 1
            item_counts[row[6]] = 1

    result_string = '\n'.join([f"`{item}` {'✅️' if item in item_counts else ''} {item_counts[item]} times" if item in item_counts else f"`{item}`" for item in termini])
     
    return(result_string)

def getTotalTrips(user='all', mode='all'):
    if user == 'all':
        base_paths = []
        if mode in ['all', 'train']:
            base_paths.append('utils/trainlogger/userdata/')
        if mode in ['all', 'tram']:
            base_paths.append('utils/trainlogger/userdata/tram/')
        if mode in ['all', 'sydney-trains']:
            base_paths.append('utils/trainlogger/userdata/sydney-trains/')
        if mode in ['all', 'sydney-trams']:
            base_paths.append('utils/trainlogger/userdata/sydney-trams/')
        if mode in ['all', 'bus']:
            base_paths.append('utils/trainlogger/userdata/bus/')
        if mode in ['all', 'adelaide-trains']:
            base_paths.append('utils/trainlogger/userdata/adelaide-trains/')
        if mode in ['all', 'adelaide-trams']:
            base_paths.append('utils/trainlogger/userdata/adelaide-trams/')
        if mode in ['all', 'perth-trains']:
            base_paths.append('utils/trainlogger/userdata/perth-trains/')

        file_paths = set()
        for base_path in base_paths:
            if os.path.exists(base_path):
                for root, _, files in os.walk(base_path):
                    for file in files:
                        # Normalize file name to lowercase for comparison
                        file_lower = file.lower()
                        if file_lower.endswith('.csv') and file_lower not in ['xxm9g.csv', 'comeng_17.csv']:
                            # Normalize path to avoid duplicates
                            full_path = os.path.abspath(os.path.join(root, file))
                            file_paths.add(full_path)

        total_line_count = 0
        for filename in file_paths:
            try:
                with open(filename, 'r') as csv_file:
                    csv_reader = csv.reader(csv_file)
                    line_count = sum(1 for row in csv_reader)
                    total_line_count += line_count
            except Exception as e:
                print(f"Error reading {filename}: {e}")
                continue
        return total_line_count
    else:
        if mode == 'train':
            filename = f'utils/trainlogger/userdata/{user}.csv'
        else:
            filename = f'utils/trainlogger/userdata/{mode}/{user}.csv'
        try:
            with open(filename, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                line_count = sum(1 for row in csv_reader)
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            line_count = 0
        return line_count
    
def streak(user, mode):
    """
    Returns the max and current streak for the chosen user.
    """
    if mode == 'train':
        filename = f'utils/trainlogger/userdata/{user}.csv'
    else:
        filename = f'utils/trainlogger/userdata/{mode}/{user}.csv'
    try:
        df = pd.read_csv(filename, on_bad_lines='skip')
        date_series = pd.to_datetime(df.iloc[:, 3], format='mixed', dayfirst=True, errors='coerce')
        unique_dates = sorted([d for d in date_series.unique() if pd.notna(d)])
        
        if not unique_dates:
            return 0, 0
        
        streaks = []
        currentStreak = 1
        
        for i in range(1, len(unique_dates)):
            if (unique_dates[i] - unique_dates[i-1]).days == 1:
                currentStreak += 1
            else:
                streaks.append(currentStreak)
                currentStreak = 1
        
        streaks.append(currentStreak)
        
        # heck if the most recent trip was today or yesterday
        today = pd.Timestamp.now().normalize()
        yesterday = today - pd.Timedelta(days=1)
        last_trip_date = unique_dates[-1].normalize()
        
        current_streak = streaks[-1] if last_trip_date in [today, yesterday] else 0
        
        return max(streaks), current_streak

    except Exception as e:
        print(f"Error getting streak for {user}: {e}")
        return 0, 0
    
# thing if the user has been on the train
def checkTrainRidden(trainSet, file_path):
    if not os.path.exists(file_path):
        print(f"The file {file_path} does not exist.")
        return False, []

    log_ids = []
    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if row[1] == trainSet:
                log_ids.append(row[0])
    return bool(log_ids), log_ids