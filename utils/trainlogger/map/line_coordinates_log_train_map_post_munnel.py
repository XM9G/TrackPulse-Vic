from utils.trainlogger.map.station_coordinates_log_train_map_pre_munnel import x_offset, y_offset

line_coordinates = {
    'standard_gauge': {
        ('Albury', 'Wodonga'): [
            (6000 + x_offset, -5400 + y_offset, 6300 + x_offset, -5200 + y_offset),
        ],
        ('Wodonga', 'Chiltern'): [
            (5550 + x_offset, -5300 + y_offset, 6050 + x_offset, -5200 + y_offset),
        ],
        ('Chiltern', 'Springhurst'): [
            (5050 + x_offset, -5350 + y_offset, 5600 + x_offset, -5200 + y_offset),
        ],
        ('Springhurst', 'Wangaratta'): [
            (4450 + x_offset, -5350 + y_offset, 5099 + x_offset, -5200 + y_offset),
        ],  
        ('Wangaratta', 'Benalla'): [
            (3950 + x_offset, -5350 + y_offset, 4499 + x_offset, -5200 + y_offset),
        ],
        ('Benalla', 'Violet Town'): [
            (3449 + x_offset, -5350 + y_offset, 4000 + x_offset, -5200 + y_offset),
        ],
        ('Violet Town', 'Euroa'): [
            (3000 + x_offset, -5350 + y_offset, 3499 + x_offset, -5200 + y_offset),
        ],
        ('Euroa', 'Avenel'): [
            (2600 + x_offset, -5350 + y_offset, 3049 + x_offset, -5200 + y_offset),
        ],
        ('Avenel', 'Seymour'): [
            (1800 + x_offset, -5400 + y_offset, 2650 + x_offset, -5200 + y_offset),
            (1600 + x_offset, -5300 + y_offset, 1750 + x_offset, -5200 + y_offset),
            (1550 + x_offset, -5200 + y_offset, 1950 + x_offset, -5050 + y_offset), # seymour station icon
        ],
        
        ('Broadmeadows','Seymour'): [
            (1600 + x_offset, -5050 + y_offset, 1649 + x_offset, -2951 + y_offset),
            (1550 + x_offset, -5200 + y_offset, 1950 + x_offset, -5050 + y_offset), # seymour station icon
            (1550 + x_offset, -2950 + y_offset, 2049 + x_offset, -2801 + y_offset), # broadmeadows station icon
            ],

        ('Southern Cross', 'Broadmeadows'): [
            (200 + x_offset, -2800 + y_offset, 1650 + x_offset, -1250 + y_offset),
            (-2300 + x_offset, -1400 + y_offset, 250 + x_offset, -600 + y_offset),
            (-3050 + x_offset, -700 + y_offset, 200 + x_offset, -600 + y_offset),
            (-3500 + x_offset, -650 + y_offset, -3310 + x_offset, 200 + y_offset),
            (-3500 + x_offset, 150 + y_offset, -2850 + x_offset, 200 + y_offset),
            (-2800 + x_offset, 150 + y_offset, -2650 + x_offset, 200 + y_offset),
            (-2600 + x_offset, 100 + y_offset, -2500 + x_offset, 200 + y_offset),
            (-2450 + x_offset, 150 + y_offset, -550 + x_offset, 200 + y_offset),
            (-500 + x_offset, 150 + y_offset, 1400 + x_offset, 200 + y_offset),
            (1350 + x_offset, 150 + y_offset, 1400 + x_offset, 400 + y_offset),
            (1350 + x_offset, 450 + y_offset, 1400 + x_offset, 1250 + y_offset),
            (1200 + x_offset, 1251 + y_offset, 2349 + x_offset, 1399 + y_offset), # Southern Cross icon
            (1550 + x_offset, -2950 + y_offset, 2049 + x_offset, -2801 + y_offset), # broadmeadows station icon
        ],
    },
    'clifton_hill': {
        ('Hurstbridge', 'Wattle Glen'):[
            (5200 + x_offset, -2700 + y_offset, 5350 + x_offset, -2450 + y_offset),
        ],
        ('Wattle Glen', 'Diamond Creek'):[
            (5250 + x_offset, -2500 + y_offset, 5350 + x_offset, -2250 + y_offset),
        ],
        ('Diamond Creek', 'Eltham'):[
            (5250 + x_offset, -2300 + y_offset, 5350 + x_offset, -2050 + y_offset),
        ],
        ('Eltham', 'Montmorency'): [
            (5250 + x_offset, -2100 + y_offset, 5350 + x_offset, -1850 + y_offset),
        ],
        ('Montmorency', 'Greensborough'):[
            (5250 + x_offset, -1900 + y_offset, 5350 + x_offset, -1650 + y_offset),
        ],
        ('Greensborough', 'Watsonia'): [
            (5250 + x_offset, -1700 + y_offset, 5350 + x_offset, -1450 + y_offset),
        ],
        ('Watsonia', 'Macleod'):[
            (5250 + x_offset, -1500 + y_offset, 5350 + x_offset, -1250 + y_offset),
        ],
        ('Macleod', 'Rosanna'): [
            (5250 + x_offset, -1300 + y_offset, 5350 + x_offset, -1050 + y_offset),
        ],
        ('Rosanna', 'Heidelberg'):[
              (5250 + x_offset, -1100 + y_offset, 5350 + x_offset, -850 + y_offset),
        ],
        ('Heidelberg','Eaglemont'): [
            (5250 + x_offset, -900 + y_offset, 5350 + x_offset, -700 + y_offset),
        ],
        ('Eaglemont', 'Ivanhoe'):[
              (5250 + x_offset, -700 + y_offset, 5350 + x_offset, -450 + y_offset),
        ],
        ('Ivanhoe', 'Darebin'):[
            (5250 + x_offset, -500 + y_offset, 5400 + x_offset, -250 + y_offset),
        ],
        ('Darebin', 'Alphington'):[
            (5250 + x_offset, -300 + y_offset, 5350 + x_offset, -50 + y_offset),
        ],
        ('Alphington', 'Fairfield'):[
            (5250 + x_offset, -100 + y_offset, 5400 + x_offset, 150 + y_offset),
        ],
        ('Fairfield', 'Dennis'):[
            (5250 + x_offset, 100 + y_offset, 5350 + x_offset, 350 + y_offset),
        ],
        ('Dennis', "Westgarth"):[
            (5250 + x_offset, 300 + y_offset, 5400 + x_offset, 550 + y_offset),
        ],
        ('Westgarth', 'Clifton Hill'):[
            (5250 + x_offset, 450 + y_offset, 5400 + x_offset, 650 + y_offset),
            (4150 + x_offset, 600 + y_offset, 5300 + x_offset, 700 + y_offset),
            (4100 + x_offset, 700 + y_offset, 4250 + x_offset, 850 + y_offset), # clifton hill coords
        ],
        ('Clifton Hill', 'Victoria Park'):[
            (4100 + x_offset, 700 + y_offset, 4250 + x_offset, 1000 + y_offset),
        ],
        ('Victoria Park', 'Collingwood'):[
            (4150 + x_offset, 950 + y_offset, 4250 + x_offset, 1200 + y_offset),
        ],
        ('Collingwood', 'North Richmond'):[
              (4150 + x_offset, 1150 + y_offset, 4250 + x_offset, 1400 + y_offset),
        ],
        ('North Richmond', 'West Richmond'):[
            (4150 + x_offset, 1350 + y_offset, 4250 + x_offset, 1600 + y_offset),
        ],
        ('West Richmond','Jolimont-Mcg'):[
            (4150 + x_offset, 1550 + y_offset, 4250 + x_offset, 1800 + y_offset),
        ],
        ('Jolimont-Mcg','Flinders Street'):[
            (3600 + x_offset, 1750 + y_offset, 4250 + x_offset, 1950 + y_offset),
            (3050 + x_offset, 1900 + y_offset, 3350 + x_offset, 1950 + y_offset),
            (2750 + x_offset, 1500 + y_offset, 3050 + x_offset, 1650 + y_offset), # Town hall part
            (2900 + x_offset, 1650 + y_offset, 3049 + x_offset, 2599 + y_offset), # Flinders Street icon
            (3550 + x_offset, 1800 + y_offset, 3650 + x_offset, 2000 + y_offset),
        ],
        ('Flinders Street','Southern Cross'): [
            (2150 + x_offset, 1850 + y_offset, 2900 + x_offset, 1950 + y_offset),
            (2150 + x_offset, 1400 + y_offset, 2200 + x_offset, 1950 + y_offset),
            (2750 + x_offset, 1500 + y_offset, 3050 + x_offset, 1650 + y_offset), # Town hall part
            (2900 + x_offset, 1650 + y_offset, 3049 + x_offset, 2599 + y_offset), # Flinders Street icon
            (1200 + x_offset, 1251 + y_offset, 2349 + x_offset, 1399 + y_offset), # Southern Cross icon
        ],
        ('Southern Cross','Flagstaff'): [
            (1200 + x_offset, 1251 + y_offset, 2349 + x_offset, 1399 + y_offset), # Southern Cross icon
            (2150 + x_offset, 900 + y_offset, 2200 + x_offset, 1250 + y_offset),
            (2100 + x_offset, 850 + y_offset, 2350 + x_offset, 950 + y_offset),
            (2350 + x_offset, 650 + y_offset, 2500 + x_offset, 1150 + y_offset), # Flagstaff Coords
        ],
        ('Flagstaff','Melbourne Central'):[
            (2500 + x_offset, 900 + y_offset, 2900 + x_offset, 950 + y_offset),
            (2350 + x_offset, 650 + y_offset, 2500 + x_offset, 1150 + y_offset), # Flagstaff Coords
            (2750 + x_offset, 400 + y_offset, 3050 + x_offset, 550 + y_offset), # State Library part
            (2900 + x_offset, 550 + y_offset, 3050 + x_offset, 1150 + y_offset), # Melbourne Central Coords
        ],
        ('Melbourne Central', 'Parliament'):[
            (2750 + x_offset, 400 + y_offset, 3050 + x_offset, 550 + y_offset), # State Library part
            (2900 + x_offset, 550 + y_offset, 3050 + x_offset, 1150 + y_offset), # Melbourne Central Coords
            (3050 + x_offset, 850 + y_offset, 3250 + x_offset, 950 + y_offset),
            (3200 + x_offset, 850 + y_offset, 3250 + x_offset, 1250 + y_offset),
            (3050 + x_offset, 1250 + y_offset, 3600 + x_offset, 1400 + y_offset), # Parliament Coords
        ],
        ('Parliament','Jolimont-Mcg'):[
            (3050 + x_offset, 1250 + y_offset, 3600 + x_offset, 1400 + y_offset), # Parliament Coords
            (3200 + x_offset, 1400 + y_offset, 3250 + x_offset, 1950 + y_offset),
            (3200 + x_offset, 1850 + y_offset, 3350 + x_offset, 1950 + y_offset),
            (3400 + x_offset, 1850 + y_offset, 3500 + x_offset, 1950 + y_offset),
            (3550 + x_offset, 1700 + y_offset, 4250 + x_offset, 1950 + y_offset),
        ],

        ('Parliament','Flinders Street'):[
            (3200 + x_offset, 1400 + y_offset, 3250 + x_offset, 1950 + y_offset),
            (3000 + x_offset, 1900 + y_offset, 3250 + x_offset, 1950 + y_offset),
            (3050 + x_offset, 1250 + y_offset, 3600 + x_offset, 1400 + y_offset), # Parliament Coords
            (2750 + x_offset, 1500 + y_offset, 3050 + x_offset, 1650 + y_offset), # Town hall part
            (2900 + x_offset, 1650 + y_offset, 3049 + x_offset, 2599 + y_offset), # Flinders Street icon
        ],
        
        # begin the mernda line but it dosn't go to its initial locations
        ('Mernda', 'Hawkstowe'): [
            (4100 + x_offset, -3000 + y_offset, 4250 + x_offset, -2750 + y_offset),
        ],
        ('Hawkstowe', 'Middle Gorge'):[
            (4150 + x_offset, -2800 + y_offset, 4250 + x_offset, -2550 + y_offset),
        ],
        ('Middle Gorge','South Morang'):[
            (4150 + x_offset, -2600 + y_offset, 4250 + x_offset, -2350 + y_offset),
        ],
        ('South Morang', 'Epping'):[
            (4150 + x_offset, -2450 + y_offset, 4250 + x_offset, -2150 + y_offset),
        ],
        ('Epping','Lalor'):[
            (4150 + x_offset, -2200 + y_offset, 4250 + x_offset, -1950 + y_offset),
        ],
        ('Lalor', 'Thomastown'):[
            (4150 + x_offset, -2000 + y_offset, 4250 + x_offset, -1750 + y_offset),
        ],
        ('Thomastown','Keon Park'):[
            (4150 + x_offset, -1850 + y_offset, 4250 + x_offset, -1550 + y_offset),
        ],
        ('Keon Park','Ruthven'): [
            (4150 + x_offset, -1600 + y_offset, 4250 + x_offset, -1350 + y_offset),
        ],
        ('Ruthven', 'Reservoir'):[
            (4150 + x_offset, -1450 + y_offset, 4250 + x_offset, -1150 + y_offset),
        ],
        ('Reservoir','Regent'):[
            (4150 + x_offset, -1200 + y_offset, 4250 + x_offset, -950 + y_offset),
        ],
        ('Regent','Preston'):[
            (4150 + x_offset, -1000 + y_offset, 4250 + x_offset, -750 + y_offset),
        ],
        ('Preston','Bell'):[
            (4150 + x_offset, -850 + y_offset, 4250 + x_offset, -550 + y_offset),
        ],
        ('Bell','Thornbury'):[
            (4150 + x_offset, -600 + y_offset, 4250 + x_offset, -350 + y_offset),
        ],
        ('Thornbury','Croxton'):[
            (4150 + x_offset, -400 + y_offset, 4250 + x_offset, -150 + y_offset),
        ],
        ('Croxton','Northcote'):[
            (4150 + x_offset, -200 + y_offset, 4250 + x_offset, 50 + y_offset),
        ],
        ('Northcote','Merri'):[
            (4150 + x_offset, 0 + y_offset, 4250 + x_offset, 250 + y_offset),
        ],
        ('Merri','Rushall'):[
            (4150 + x_offset, 200 + y_offset, 4250 + x_offset, 450 + y_offset),
        ],
        ('Rushall','Clifton Hill'):[
            (4150 + x_offset, 400 + y_offset, 4250 + x_offset, 450 + y_offset),
            (4150 + x_offset, 400 + y_offset, 4200 + x_offset, 700 + y_offset),
            (4100 + x_offset, 700 + y_offset, 4250 + x_offset, 850 + y_offset), # clifton hill coords
        ],
        
        
        
        
    },
    
    'cross_city': {
        ('Sandringham', 'Hampton'): [
            (-1600 + x_offset, 3150 + y_offset, -1300 + x_offset, 3300 + y_offset),
        ],
        ('Hampton', 'Brighton Beach'): [
            (-1350 + x_offset, 3200 + y_offset, -700 + x_offset, 3300 + y_offset),
        ],
        ('Brighton Beach', 'Middle Brighton'): [
            (-750 + x_offset, 3200 + y_offset, 50 + x_offset, 3300 + y_offset),
        ],
        ('Middle Brighton', 'North Brighton'): [
            (0 + x_offset, 3200 + y_offset, 800 + x_offset, 3300 + y_offset),
        ],
        ('North Brighton', 'Gardenvale'): [
            (750 + x_offset, 3200 + y_offset, 1450 + x_offset, 3300 + y_offset),
        ],
        ('Gardenvale', 'Elsternwick'): [
            (1400 + x_offset, 3200 + y_offset, 2050 + x_offset, 3300 + y_offset),
        ],
        ('Elsternwick', 'Ripponlea'): [
            (2000 + x_offset, 3200 + y_offset, 2600 + x_offset, 3300 + y_offset),
        ],
        ('Ripponlea', 'Balaclava'): [
            (2550 + x_offset, 3200 + y_offset, 3150 + x_offset, 3300 + y_offset),
        ],
        ('Balaclava', 'Windsor'): [
            (3100 + x_offset, 3200 + y_offset, 3650 + x_offset, 3300 + y_offset),
        ],
        ('Windsor', 'Prahran'): [
            (3600 + x_offset, 3200 + y_offset, 4100 + x_offset, 3300 + y_offset),
        ],
        ('Prahran', 'South Yarra'): [
            (4050 + x_offset, 3200 + y_offset, 4900 + x_offset, 3300 + y_offset),
            (4850 + x_offset, 2900 + y_offset, 4900 + x_offset, 3250 + y_offset),
            (4800 + x_offset, 2750 + y_offset, 5050 + x_offset, 2900 + y_offset), # south yarra coords
        ],
        ('South Yarra', 'Richmond'):[
            (4600 + x_offset, 2450 + y_offset, 4900 + x_offset, 2550 + y_offset),
            (4850 + x_offset, 2450 + y_offset, 4900 + x_offset, 2800 + y_offset),
            (4800 + x_offset, 2750 + y_offset, 5050 + x_offset, 2900 + y_offset), # south yarra coords
            (4500 + x_offset, 1950 + y_offset, 4650 + x_offset, 2600 + y_offset), # richmond coords
        ],
        ('Richmond', 'Flinders Street'):[
            (4500 + x_offset, 1950 + y_offset, 4650 + x_offset, 2600 + y_offset), # richmond coords
            (3050 + x_offset, 2450 + y_offset, 4500 + x_offset, 2550 + y_offset),
            (2750 + x_offset, 1500 + y_offset, 3050 + x_offset, 1650 + y_offset), # Town hall part
            (2900 + x_offset, 1650 + y_offset, 3049 + x_offset, 2599 + y_offset), # Flinders Street icon
        ],

        #werribee line
        ('Werribee', 'Hoppers Crossing'):[
            (-4450 + x_offset, 1050 + y_offset, -3951 + x_offset, 1199 + y_offset),
        ],
        ('Hoppers Crossing', 'Williams Landing'):[
            (-4000 + x_offset, 1050 + y_offset, -3101 + x_offset, 1149 + y_offset),
        ],
        ('Williams Landing','Aircraft'): [
            (-3150 + x_offset, 1050 + y_offset, -2501 + x_offset, 1199 + y_offset),
        ],
        ('Aircraft', 'Laverton'):[
            (-2550 + x_offset, 1050 + y_offset, -2001 + x_offset, 1199 + y_offset),
        ],
        ('Laverton', 'Newport'):[ # express route
            (-2150 + x_offset, 1050 + y_offset, -2001 + x_offset, 1199 + y_offset),
            (-2000 + x_offset, 1100 + y_offset, -651 + x_offset, 1149 + y_offset),
            (-750 + x_offset, 900 + y_offset, -601 + x_offset, 1149 + y_offset),
        ],
        ('Westona', 'Laverton'):[
            (-2000 + x_offset, 1100 + y_offset, -1901 + x_offset, 1249 + y_offset),
            (-1950 + x_offset, 1200 + y_offset, -1801 + x_offset, 1299 + y_offset),
        ],
        ('Westona', 'Altona'):[
            (-1850 + x_offset, 1200 + y_offset, -1401 + x_offset, 1299 + y_offset),
        ],
        ('Altona', 'Seaholme'):[
            (-1450 + x_offset, 1200 + y_offset, -951 + x_offset, 1299 + y_offset),
        ],
        ('Seaholme','Newport'):[
            (-1000 + x_offset, 1200 + y_offset, -701 + x_offset, 1299 + y_offset),
            (-700 + x_offset, 1050 + y_offset, -651 + x_offset, 1249 + y_offset),
            (-750 + x_offset, 900 + y_offset, -601 + x_offset, 1049 + y_offset),
        ],
        ('Newport', 'Spotswood'):[
            (-750 + x_offset, 750 + y_offset, -601 + x_offset, 1049 + y_offset),
        ],
        ('Spotswood','Yarraville'):[
            (-750 + x_offset, 550 + y_offset, -651 + x_offset, 799 + y_offset),
        ],
        ('Seddon', 'Yarraville'):[
            (-750 + x_offset, 350 + y_offset, -651 + x_offset, 599 + y_offset),
        ],
        ('Seddon', 'Footscray'):[
            (-600 + x_offset, -200 + y_offset, -451 + x_offset, 149 + y_offset), # footscray station icon
            (-550 + x_offset, 100 + y_offset, -501 + x_offset, 249 + y_offset), # footscray station icon
            (-600 + x_offset, 200 + y_offset, -451 + x_offset, 349 + y_offset), # footscray station icon
            (-750 + x_offset, 250 + y_offset, -601 + x_offset, 399 + y_offset),
        ],
        ('Footscray','South Kensington'):[
            (-600 + x_offset, -200 + y_offset, -451 + x_offset, 149 + y_offset), # footscray station icon
            (-550 + x_offset, 100 + y_offset, -501 + x_offset, 249 + y_offset), # footscray station icon
            (-600 + x_offset, 200 + y_offset, -451 + x_offset, 349 + y_offset), # footscray station icon
            (-450 + x_offset, 250 + y_offset, 99 + x_offset, 349 + y_offset),
        ],
        ('South Kensington', 'North Melbourne'):[
            (50 + x_offset, 250 + y_offset, 1299 + x_offset, 349 + y_offset),
            (1200 + x_offset, 350 + y_offset, 1339 + x_offset, 499 + y_offset), # North Melbourne icon
            (1300 + x_offset, 400 + y_offset, 1649 + x_offset, 449 + y_offset), # North Melbourne icon
            (1602 + x_offset, 350 + y_offset, 2049 + x_offset, 499 + y_offset), # North Melbourne icon
        ],
        ('North Melbourne', 'Southern Cross'):[
            (1200 + x_offset, 350 + y_offset, 1339 + x_offset, 499 + y_offset), # North Melbourne icon
            (1300 + x_offset, 400 + y_offset, 1649 + x_offset, 449 + y_offset), # North Melbourne icon
            (1602 + x_offset, 350 + y_offset, 2049 + x_offset, 499 + y_offset), # North Melbourne icon
            (1250 + x_offset, 500 + y_offset, 1299 + x_offset, 1249 + y_offset),
            (1200 + x_offset, 1251 + y_offset, 2349 + x_offset, 1399 + y_offset), # Southern Cross icon
        ],
        ('Southern Cross', 'Flinders Street'):[
            (1250 + x_offset, 1400 + y_offset, 1299 + x_offset, 2549 + y_offset),
            (1250 + x_offset, 2500 + y_offset, 2899 + x_offset, 2549 + y_offset),
            (2750 + x_offset, 1500 + y_offset, 3050 + x_offset, 1650 + y_offset), # Town hall part
            (2900 + x_offset, 1650 + y_offset, 3049 + x_offset, 2599 + y_offset), # Flinders Street icon
            (1200 + x_offset, 1251 + y_offset, 2349 + x_offset, 1399 + y_offset), # Southern Cross icon
        ],
        # Williamstown Branch
        ('Newport', 'North Williamstown'):[
            (-700.0 + x_offset, 1050.0 + y_offset, -601.0 + x_offset, 1349.0 + y_offset),
            (-750 + x_offset, 900 + y_offset, -601 + x_offset, 1049 + y_offset),
        ],
        ('North Williamstown', 'Williamstown Beach'):[
            (-750.0 + x_offset, 1350.0 + y_offset, -601.0 + x_offset, 1499.0 + y_offset),
        ],
        ('Williamstown Beach', 'Williamstown'):[
            (-750.0 + x_offset, 1500.0 + y_offset, -601.0 + x_offset, 1750 + y_offset),
        ],
        
    },
    "burnley": {
    ('Lilydale', 'Mooroolbark'): [
        (6450 + x_offset, -2100 + y_offset, 6600 + x_offset, -1850 + y_offset),
    ],
    ('Mooroolbark', 'Croydon'): [
        (6500 + x_offset, -1950 + y_offset, 6600 + x_offset, -1650 + y_offset),
    ],
    ('Croydon', 'Ringwood East'): [
        (6450 + x_offset, -1750 + y_offset, 6600 + x_offset, -1450 + y_offset),
    ],
    ('Ringwood East', 'Ringwood'): [
        (6450 + x_offset, -1450 + y_offset, 6550 + x_offset, -1200 + y_offset),
        (6450 + x_offset, -1250 + y_offset, 6600 + x_offset, -1050 + y_offset),
    ],
    ('Ringwood', 'Heatherdale'): [
        (6450 + x_offset, -1200 + y_offset, 6600 + x_offset, -900 + y_offset),
    ],
    ('Heatherdale', 'Mitcham'): [
        (6450 + x_offset, -950 + y_offset, 6600 + x_offset, -700 + y_offset),
    ],
    ('Mitcham', 'Nunawading'): [
        (6450 + x_offset, -750 + y_offset, 6600 + x_offset, -500 + y_offset),
    ],
    ('Nunawading', 'Blackburn'): [
        (6450 + x_offset, -600 + y_offset, 6600 + x_offset, -300 + y_offset),
    ],
    ('Blackburn', 'Laburnum'): [
        (6500 + x_offset, -400 + y_offset, 6600 + x_offset, -100 + y_offset),
    ],
    ('Laburnum', 'Box Hill'): [
        (6500 + x_offset, -200 + y_offset, 6600 + x_offset, 100 + y_offset),
    ],
    ('Box Hill', 'Union'): [
        (6500 + x_offset, 50 + y_offset, 6600 + x_offset, 300 + y_offset),
    ],
    ('Union', 'Chatham') : [
        (6500 + x_offset, 250 + y_offset, 6600 + x_offset, 500 + y_offset),
    ],
    ('Chatham', 'Canterbury') : [
        (6500 + x_offset, 450 + y_offset, 6600 + x_offset, 700 + y_offset),
    ],
    ('Canterbury', 'East Camberwell') : [
        (6500 + x_offset, 600 + y_offset, 6600 + x_offset, 900 + y_offset),
    ],
    ('East Camberwell', 'Camberwell') : [
        (6500 + x_offset, 800 + y_offset, 6600 + x_offset, 950 + y_offset),
        (6450 + x_offset, 1150 + y_offset, 6600 + x_offset, 1300 + y_offset),
        (6500 + x_offset, 900 + y_offset, 6550 + x_offset, 1150 + y_offset),
    ],
    ('Camberwell', 'Auburn') : [
        (6400 + x_offset, 1150 + y_offset, 6600 + x_offset, 1450 + y_offset),
    ],
    ('Auburn', 'Glenferrie') : [
        (6450 + x_offset, 1350 + y_offset, 6600 + x_offset, 1650 + y_offset),
    ],
    ('Glenferrie', 'Hawthorn') : [
        (6500 + x_offset, 1600 + y_offset, 6600 + x_offset, 1850 + y_offset),
    ],
    ('Hawthorn', 'Burnley') : [
        (6200 + x_offset, 1950 + y_offset, 6550 + x_offset, 2050 + y_offset),
        (6200 + x_offset, 2000 + y_offset, 6350 + x_offset, 2100 + y_offset),
        (6500 + x_offset, 1750 + y_offset, 6600 + x_offset, 2000 + y_offset),
    ],
    ('Burnley', 'East Richmond') : [
        (5650 + x_offset, 1950 + y_offset, 6350 + x_offset, 2100 + y_offset),
    ],
    ('East Richmond', 'Richmond') : [
        (4650 + x_offset, 1950 + y_offset, 5700 + x_offset, 2050 + y_offset),
        (4500 + x_offset, 1950 + y_offset, 4650 + x_offset, 2600 + y_offset), # richmond coords
    ],
    ('Richmond','Flinders Street'):[
        (3550 + x_offset, 2000 + y_offset, 4499 + x_offset, 2049 + y_offset),
        (3050 + x_offset, 2000 + y_offset, 3499 + x_offset, 2059 + y_offset),
        (4500 + x_offset, 1950 + y_offset, 4650 + x_offset, 2600 + y_offset), # richmond coords
        (2750 + x_offset, 1500 + y_offset, 3050 + x_offset, 1650 + y_offset), # Town hall part
        (2900 + x_offset, 1650 + y_offset, 3049 + x_offset, 2599 + y_offset), # Flinders Street icon
    ],
    ('Flinders Street', 'Southern Cross'):[
        (2050 + x_offset, 1400 + y_offset, 2100 + x_offset, 2050 + y_offset),
        (2050 + x_offset, 1950 + y_offset, 2900 + x_offset, 2050 + y_offset),
        (2750 + x_offset, 1500 + y_offset, 3050 + x_offset, 1650 + y_offset), # Town hall part
        (2900 + x_offset, 1650 + y_offset, 3049 + x_offset, 2599 + y_offset), # Flinders Street icon
        (1200 + x_offset, 1251 + y_offset, 2349 + x_offset, 1399 + y_offset), # Southern Cross icon
    ],
    ('Southern Cross', 'Flagstaff'):[
        (2050 + x_offset, 800 + y_offset, 2350 + x_offset, 850 + y_offset),
        (2000 + x_offset, 800 + y_offset, 2100 + x_offset, 1250 + y_offset),
        (1200 + x_offset, 1251 + y_offset, 2349 + x_offset, 1399 + y_offset), # Southern Cross icon
        (2350 + x_offset, 650 + y_offset, 2500 + x_offset, 1150 + y_offset), # Flagstaff Coords
    ],

    ("Flagstaff", "Melbourne Central"):[
        (2500 + x_offset, 800 + y_offset, 2901 + x_offset, 852 + y_offset),
        (2350 + x_offset, 650 + y_offset, 2500 + x_offset, 1150 + y_offset), # Flagstaff Coords
        (2750 + x_offset, 400 + y_offset, 3050 + x_offset, 550 + y_offset), # State Library part
        (2900 + x_offset, 550 + y_offset, 3050 + x_offset, 1150 + y_offset), # Melbourne Central Coords
    ],
    ('Melbourne Central', 'Parliament'):[
        (3050 + x_offset, 800 + y_offset, 3400 + x_offset, 850 + y_offset),
        (3300 + x_offset, 800 + y_offset, 3400 + x_offset, 1250 + y_offset),
        (2750 + x_offset, 400 + y_offset, 3050 + x_offset, 550 + y_offset), # State Library part
        (2900 + x_offset, 550 + y_offset, 3050 + x_offset, 1150 + y_offset), # Melbourne Central Coords
        (3050 + x_offset, 1250 + y_offset, 3600 + x_offset, 1400 + y_offset), # Parliament Coords
    ],
    ('Parliament', 'Richmond'):[
        (3350 + x_offset, 2000 + y_offset, 3500 + x_offset, 2050 + y_offset),
        (3350 + x_offset, 1400 + y_offset, 3400 + x_offset, 2050 + y_offset),
        (3550 + x_offset, 2000 + y_offset, 4500 + x_offset, 2050 + y_offset),
        (3050 + x_offset, 1250 + y_offset, 3600 + x_offset, 1400 + y_offset), # Parliament Coords
        (4500 + x_offset, 1950 + y_offset, 4650 + x_offset, 2600 + y_offset), # richmond coords
    ],
    ('Flinders Street', 'Richmond'):[
        (3050 + x_offset, 2000 + y_offset, 3500 + x_offset, 2050 + y_offset),
        (3550 + x_offset, 2000 + y_offset, 4500 + x_offset, 2050 + y_offset),
        (2750 + x_offset, 1500 + y_offset, 3050 + x_offset, 1650 + y_offset), # Town hall part
        (2900 + x_offset, 1650 + y_offset, 3049 + x_offset, 2599 + y_offset), # Flinders Street icon
        (4500 + x_offset, 1950 + y_offset, 4650 + x_offset, 2600 + y_offset), # richmond coords
        
    ],

    # alamein branch
    ('Alamein', 'Ashburton'):[
        (9400 + x_offset, 950 + y_offset, 9750 + x_offset, 1150 + y_offset),
    ],
    ('Ashburton','Burwood'):[
        (8900 + x_offset, 1050 + y_offset, 9450 + x_offset, 1150 + y_offset),
    ],
    ('Burwood', 'Hartwell'):[
        (8450 + x_offset, 1050 + y_offset, 8950 + x_offset, 1150 + y_offset),
    ],
    ('Hartwell', 'Willison'):[
        (8000 + x_offset, 1050 + y_offset, 8500 + x_offset, 1150 + y_offset),
    ],
    ('Willison', 'Riversdale'):[
        (7500 + x_offset, 1050 + y_offset, 8050 + x_offset, 1150 + y_offset),
    ],
    ('Riversdale', 'Camberwell'):[
        (6500 + x_offset, 1050 + y_offset, 7550 + x_offset, 1150 + y_offset),
        (6450 + x_offset, 1050 + y_offset, 6600 + x_offset, 1300 + y_offset),
    ],

    # the beginning of the belgrave line:
    ('Belgrave', 'Tecoma'):[
        (11000 + x_offset, -1450 + y_offset, 11400 + x_offset, -1200 + y_offset),
        (11400 + x_offset, -1450 + y_offset, 11550 + x_offset, -1200 + y_offset), #belgrave coords
    ],
    ('Tecoma', 'Upwey'):[
        (10600 + x_offset, -1350 + y_offset, 11050 + x_offset, -1200 + y_offset),
    ],
    ('Upwey', 'Upper Ferntree Gully'):[
        (9900 + x_offset, -1300 + y_offset, 10650 + x_offset, -1200 + y_offset),
    ],
    ('Upper Ferntree Gully', 'Ferntree Gully'):[
        (9050 + x_offset, -1350 + y_offset, 9950 + x_offset, -1200 + y_offset),
    ],
    ('Ferntree Gully', 'Boronia'):[
        (8500 + x_offset, -1300 + y_offset, 9100 + x_offset, -1200 + y_offset),
    ],
    ('Boronia', 'Bayswater'):[
        (8000 + x_offset, -1300 + y_offset, 8550 + x_offset, -1200 + y_offset),
    ],
    ('Bayswater', 'Heathmont'):[
        (7400 + x_offset, -1300 + y_offset, 8050 + x_offset, -1200 + y_offset),
    ],
    ('Heathmont', 'Ringwood'):[
        (6450 + x_offset, -1200 + y_offset, 6600 + x_offset, -1050 + y_offset),
        (6450 + x_offset, -1300 + y_offset, 7500 + x_offset, -1200 + y_offset),
    ],
    # glen waverley branch
    ('Glen Waverley', 'Syndal'):[
        (12250 + x_offset, 1900 + y_offset, 12600 + x_offset, 2100 + y_offset),
    ],
    ('Syndal', 'Mount Waverley'):[
        (11700 + x_offset, 2000 + y_offset, 12350 + x_offset, 2100 + y_offset),
    ],
    ('Mount Waverley', 'Jordanville'):[
        (11000 + x_offset, 2000 + y_offset, 11750 + x_offset, 2100 + y_offset),
    ],
    ('Jordanville', 'Holmesglen'):[
        (10400 + x_offset, 2000 + y_offset, 11050 + x_offset, 2100 + y_offset),
    ],
    ('Holmesglen', 'East Malvern'):[
        (9750 + x_offset, 2000 + y_offset, 10450 + x_offset, 2100 + y_offset),
    ],
    ('East Malvern', 'Darling'):[
        (9200 + x_offset, 2000 + y_offset, 9800 + x_offset, 2100 + y_offset),
    ],
    ('Darling', 'Glen Iris'):[
        (8800 + x_offset, 2000 + y_offset, 9250 + x_offset, 2100 + y_offset),
    ],
    ('Glen Iris', 'Gardiner'):[
        (8350 + x_offset, 2000 + y_offset, 8850 + x_offset, 2100 + y_offset),
    ],
    ('Gardiner', 'Tooronga'):[
        (7850 + x_offset, 2000 + y_offset, 8400 + x_offset, 2100 + y_offset)
    ],
    ('Tooronga', 'Kooyong'):[
        (7350 + x_offset, 2000 + y_offset, 7900 + x_offset, 2100 + y_offset),
    ],
    ('Kooyong', 'Heyington'):[
        (6850 + x_offset, 2000 + y_offset, 7400 + x_offset, 2100 + y_offset),
    ],
    ('Heyington', 'Burnley'):[
        (6350 + x_offset, 2000 + y_offset, 6900 + x_offset, 2100 + y_offset),
        (6200 + x_offset, 1950 + y_offset, 6350 + x_offset, 2100 + y_offset),
    ],
    },
    'dandenong':{
        # Sunbury Line
        ('Sunbury', 'Diggers Rest'): [
            (-3350 + x_offset, -1850 + y_offset, -3000 + x_offset, -1700 + y_offset), # Sunbury Coords
            (-3100 + x_offset, -1700 + y_offset, -3000 + x_offset, -1550 + y_offset),
        ],
        ('Diggers Rest', 'Watergardens'): [
            (-3100 + x_offset, -1600 + y_offset, -3000 + x_offset, -1450 + y_offset),
            (-3350 + x_offset, -1450 + y_offset, -3000 + x_offset, -1300 + y_offset), # Watergardens Coords
        ],

        ('Watergardens', 'Keilor Plains'): [
            (-3100 + x_offset, -1300 + y_offset, -3000 + x_offset, -1150 + y_offset),
            (-3350 + x_offset, -1450 + y_offset, -3000 + x_offset, -1300 + y_offset), # Watergardens Coords
        ],

        ('Keilor Plains', 'St Albans'): [
            (-3100 + x_offset, -1250 + y_offset, -3000 + x_offset, -950 + y_offset),
        ],

        ('St Albans', 'Ginifer'): [
            (-3100 + x_offset, -1000 + y_offset, -3000 + x_offset, -750 + y_offset),
        ],

        ('Ginifer', 'Albion'): [
            (-3100 + x_offset, -800 + y_offset, -3000 + x_offset, -700 + y_offset),
            (-3100 + x_offset, -700 + y_offset, -3050 + x_offset, -450 + y_offset),
            (-3100 + x_offset, -500 + y_offset, -3000 + x_offset, -450 + y_offset),
        ],

        ('Albion', 'Sunshine'): [
            (-3100 + x_offset, -500 + y_offset, -3000 + x_offset, -450 + y_offset),
            (-3100 + x_offset, -500 + y_offset, -3050 + x_offset, -100 + y_offset),
            (-3100 + x_offset, -150 + y_offset, -2900 + x_offset, -100 + y_offset),
            (-2900 + x_offset, -200 + y_offset, -2750 + x_offset, -50 + y_offset), # Sunshine Coords
            (-2850 + x_offset, -80 + y_offset, -2800 + x_offset, 220 + y_offset), # Sunshine Coords
            (-2900 + x_offset, 220 + y_offset, -2750 + x_offset, 550 + y_offset), # Sunshine Coords 
        ],

        ('Sunshine', 'Tottenham'): [
            (-2750 + x_offset, -200 + y_offset, -2300 + x_offset, -100 + y_offset),
            (-2900 + x_offset, -200 + y_offset, -2750 + x_offset, -50 + y_offset), # Sunshine Coords
            (-2850 + x_offset, -80 + y_offset, -2800 + x_offset, 220 + y_offset), # Sunshine Coords
            (-2900 + x_offset, 220 + y_offset, -2750 + x_offset, 550 + y_offset), # Sunshine Coords 
        ],

        ('Tottenham', 'West Footscray'): [
            (-2350 + x_offset, -200 + y_offset, -1700 + x_offset, -100 + y_offset),
        ],

        ('West Footscray', 'Middle Footscray'): [
            (-1750 + x_offset, -200 + y_offset, -1100 + x_offset, -100 + y_offset),
        ],

        ('Middle Footscray', 'Footscray'): [
            (-1150 + x_offset, -200 + y_offset, -600 + x_offset, -100 + y_offset),
            (-600 + x_offset, -200 + y_offset, -451 + x_offset, 149 + y_offset), # footscray station icon
            (-550 + x_offset, 100 + y_offset, -501 + x_offset, 249 + y_offset), # footscray station icon
            (-600 + x_offset, 200 + y_offset, -451 + x_offset, 349 + y_offset), # footscray station icon
        ],

        #pakenham
        ('East Pakenham','Pakenham'): [
            (15700 + x_offset, 4300 + y_offset, 16000 + x_offset, 4450 + y_offset),
            (15600 + x_offset, 4300 + y_offset, 15750 + x_offset, 4650 + y_offset), # pakenham coords
        ],
        ('Pakenham','Cardinia Road'): [
            (15100 + x_offset, 4300 + y_offset, 15600 + x_offset, 4400 + y_offset),
            (15050 + x_offset, 4300 + y_offset, 15150 + x_offset, 4400 + y_offset),
            (15600 + x_offset, 4300 + y_offset, 15750 + x_offset, 4650 + y_offset), # pakenham coords
        ],
        ('Cardinia Road','Officer'): [
            (14500 + x_offset, 4300 + y_offset, 15100 + x_offset, 4400 + y_offset),
        ],
        ('Officer','Beaconsfield'): [
            (13950 + x_offset, 4300 + y_offset, 14550 + x_offset, 4400 + y_offset),
        ],
        ('Beaconsfield','Berwick'): [
            (13400 + x_offset, 4300 + y_offset, 14000 + x_offset, 4400 + y_offset),
        ],
        ('Berwick','Narre Warren'): [
            (12850 + x_offset, 4300 + y_offset, 13450 + x_offset, 4400 + y_offset),
        ],
        ('Narre Warren','Hallam'): [
            (12300 + x_offset, 4300 + y_offset, 12900 + x_offset, 4400 + y_offset),
        ],
        ('Hallam','Dandenong'): [
            (11750 + x_offset, 4300 + y_offset, 11900 + x_offset, 4650 + y_offset), # dandenong coords
            (11900 + x_offset, 4300 + y_offset, 12350 + x_offset, 4400 + y_offset),
        ],
        ('Dandenong','Yarraman'): [
            (11250 + x_offset, 4300 + y_offset, 11750 + x_offset, 4400 + y_offset),
            (11750 + x_offset, 4300 + y_offset, 11900 + x_offset, 4650 + y_offset), # dandenong coords
        ],
        ('Yarraman','Noble Park'): [
            (10700 + x_offset, 4300 + y_offset, 11300 + x_offset, 4400 + y_offset),
        ],
        ('Noble Park','Sandown Park'): [
            (10050 + x_offset, 4300 + y_offset, 10750 + x_offset, 4400 + y_offset),
        ],
        ('Sandown Park','Springvale'): [
            (9400 + x_offset, 4300 + y_offset, 10100 + x_offset, 4400 + y_offset),
        ],
        ('Springvale','Westall'): [
            (8900 + x_offset, 4300 + y_offset, 9450 + x_offset, 4400 + y_offset),
        ],
        ('Westall','Clayton'): [
            (8400 + x_offset, 4300 + y_offset, 8550 + x_offset, 4650 + y_offset), # clayton coords
            (8550 + x_offset, 4300 + y_offset, 8950 + x_offset, 4400 + y_offset),
        ],
        ('Clayton','Huntingdale'): [
            (7950 + x_offset, 4300 + y_offset, 8400 + x_offset, 4400 + y_offset),
            (8400 + x_offset, 4300 + y_offset, 8550 + x_offset, 4650 + y_offset), # clayton coords
        ],
        ('Huntingdale','Oakleigh'): [
            (7400 + x_offset, 4300 + y_offset, 8000 + x_offset, 4400 + y_offset),
        ],
        ('Oakleigh','Hughesdale'): [
            (6850 + x_offset, 4300 + y_offset, 7450 + x_offset, 4400 + y_offset),
        ],
        ('Hughesdale','Murrumbeena'): [
            (6200 + x_offset, 4300 + y_offset, 6900 + x_offset, 4400 + y_offset),
        ],
        ('Murrumbeena','Carnegie'): [
            (5600 + x_offset, 4300 + y_offset, 6250 + x_offset, 4400 + y_offset),
        ],
        ('Carnegie','Caulfield'): [
            (4900 + x_offset, 4150 + y_offset, 5450 + x_offset, 4300 + y_offset), # caulfield coords
            (5250 + x_offset, 4300 + y_offset, 5650 + x_offset, 4400 + y_offset),
        ],
        ('Caulfield','Malvern'): [
            (4900 + x_offset, 4150 + y_offset, 5450 + x_offset, 4300 + y_offset), # caulfield coords
            (4900 + x_offset, 3950 + y_offset, 5080 + x_offset, 4100 + y_offset), # malvern coords
            (5080 + x_offset, 4000 + y_offset, 5270 + x_offset, 4050 + y_offset), # malvern coords
            (5270 + x_offset, 3950 + y_offset, 5450 + x_offset, 4100 + y_offset), # malvern coords
            (5300 + x_offset, 4000 + y_offset, 5400 + x_offset, 4150 + y_offset),
        ],
        ('Malvern','Anzac'): [
            (4900 + x_offset, 3950 + y_offset, 5080 + x_offset, 4100 + y_offset), # malvern coords
            (5080 + x_offset, 4000 + y_offset, 5270 + x_offset, 4050 + y_offset), # malvern coords
            (5270 + x_offset, 3950 + y_offset, 5450 + x_offset, 4100 + y_offset), # malvern coords
            (5250 + x_offset, 2950 + y_offset, 5400 + x_offset, 4050 + y_offset),
            (3900 + x_offset, 2950 + y_offset, 4850 + x_offset, 3050 + y_offset),
        ],
        ('Anzac','Town Hall'): [
            (2750 + x_offset, 3000 + y_offset, 3950 + x_offset, 3050 + y_offset),
            (3900 + x_offset, 2950 + y_offset, 3950 + x_offset, 3050 + y_offset),
            (2750 + x_offset, 2550 + y_offset, 2850 + x_offset, 3050 + y_offset),
            (2750 + x_offset, 1600 + y_offset, 2850 + x_offset, 1800 + y_offset),
            (2750 + x_offset, 1500 + y_offset, 3050 + x_offset, 1650 + y_offset), # Town hall part
            (2900 + x_offset, 1650 + y_offset, 3049 + x_offset, 2599 + y_offset), # Flinders Street icon
        ],
        ('Town Hall','State Library'): [
            (2750 + x_offset, 1100 + y_offset, 2850 + x_offset, 1500 + y_offset),
            (2750 + x_offset, 950 + y_offset, 2850 + x_offset, 1050 + y_offset),
            (2800 + x_offset, 550 + y_offset, 2850 + x_offset, 700 + y_offset),
            (2750 + x_offset, 1500 + y_offset, 3050 + x_offset, 1650 + y_offset), # Town hall part
            (2900 + x_offset, 1650 + y_offset, 3049 + x_offset, 2599 + y_offset), # Flinders Street icon
            (2750 + x_offset, 400 + y_offset, 3050 + x_offset, 550 + y_offset), # State Library part
            (2900 + x_offset, 550 + y_offset, 3050 + x_offset, 1150 + y_offset), # Melbourne Central Coords
        ],
        ('State Library', 'Parkville'): [
            (2600 + x_offset, -250 + y_offset, 2850 + x_offset, 400 + y_offset),
            (2750 + x_offset, 400 + y_offset, 3050 + x_offset, 550 + y_offset), # State Library part
            (2900 + x_offset, 550 + y_offset, 3050 + x_offset, 1150 + y_offset), # Melbourne Central Coords
        ],
        ('Parkville', 'Arden'): [
            (2150 + x_offset, -200 + y_offset, 2650 + x_offset, -100 + y_offset),
        ],
        ('Arden', 'Footscray'): [
            (2000 + x_offset, -200 + y_offset, 2250 + x_offset, -100 + y_offset),
            (-450 + x_offset, -200 + y_offset, 1650 + x_offset, -50 + y_offset),
            (-600 + x_offset, -200 + y_offset, -451 + x_offset, 149 + y_offset), # footscray station icon
            (-550 + x_offset, 100 + y_offset, -501 + x_offset, 249 + y_offset), # footscray station icon
            (-600 + x_offset, 200 + y_offset, -451 + x_offset, 349 + y_offset), # footscray station icon
        ],
        # cranbourne branch
        ('Cranbourne','Merinda Park'): [
            (11950 + x_offset, 4950 + y_offset, 12100 + x_offset, 5200 + y_offset),
        ],
        ('Merinda Park','Lynbrook'): [
            (11950 + x_offset, 4700 + y_offset, 12100 + x_offset, 5000 + y_offset),
        ],
        ('Lynbrook','Dandenong'): [
            (12000 + x_offset, 4350 + y_offset, 12050 + x_offset, 4800 + y_offset),
            (12000 + x_offset, 4700 + y_offset, 12100 + x_offset, 4800 + y_offset),
            (11900 + x_offset, 4350 + y_offset, 12050 + x_offset, 4400 + y_offset),
            (11750 + x_offset, 4300 + y_offset, 11900 + x_offset, 4650 + y_offset), # dandenong coords
        ],
    },
    
    'frankston': {
        # frankston line
        ('Frankston', 'Kananook'):[
            (4900 + x_offset, 8350 + y_offset, 5150 + x_offset, 8650 + y_offset),
        ],
        ('Kananook', 'Seaford'):[
            (4900 + x_offset, 8150 + y_offset, 5000 + x_offset, 8400 + y_offset),
        ],
        ('Seaford', 'Carrum'):[
            (4900 + x_offset, 7950 + y_offset, 5000 + x_offset, 8200 + y_offset),
        ],
        ('Carrum', 'Bonbeach'):[
            (4900 + x_offset, 7750 + y_offset, 5000 + x_offset, 8000 + y_offset),
        ],
        ('Bonbeach', 'Chelsea'):[
            (4900 + x_offset, 7550 + y_offset, 5000 + x_offset, 7800 + y_offset),
        ],
        ('Chelsea', 'Edithvale'):[
            (4900 + x_offset, 7350 + y_offset, 5000 + x_offset, 7600 + y_offset),
        ],
        ('Edithvale', 'Aspendale'):[
            (4900 + x_offset, 7150 + y_offset, 5000 + x_offset, 7400 + y_offset),
        ],
        ('Aspendale', 'Mordialloc'):[
            (4900 + x_offset, 6950 + y_offset, 5000 + x_offset, 7200 + y_offset),
        ],
        ('Mordialloc', 'Parkdale'):[
            (4900 + x_offset, 6750 + y_offset, 5000 + x_offset, 7000 + y_offset),
        ],
        ('Parkdale', 'Mentone'):[
            (4850 + x_offset, 6550 + y_offset, 5000 + x_offset, 6800 + y_offset),
        ],
        ('Mentone', 'Cheltenham'):[
            (4900 + x_offset, 6350 + y_offset, 5000 + x_offset, 6600 + y_offset),
        ],
        ('Cheltenham', 'Southland'):[
            (4900 + x_offset, 6150 + y_offset, 5050 + x_offset, 6400 + y_offset),
        ],
        ('Southland', 'Highett'):[
            (4900 + x_offset, 5950 + y_offset, 5000 + x_offset, 6200 + y_offset),
        ],
        ('Highett', 'Moorabbin'):[
            (4900 + x_offset, 5700 + y_offset, 5000 + x_offset, 6000 + y_offset),
        ],
        ('Moorabbin', 'Patterson'):[
            (4900 + x_offset, 5550 + y_offset, 5000 + x_offset, 5800 + y_offset),
        ],
        ('Patterson', 'Bentleigh'):[
            (4900 + x_offset, 5350 + y_offset, 5000 + x_offset, 5600 + y_offset),
        ],
        ('Bentleigh', 'McKinnon'):[
            (4900 + x_offset, 5150 + y_offset, 5000 + x_offset, 5400 + y_offset),
        ],
        ('McKinnon', 'Ormond'):[
            (4900 + x_offset, 4950 + y_offset, 5000 + x_offset, 5200 + y_offset),
        ],
        ('Ormond', 'Glen Huntly'):[
            (4900 + x_offset, 4750 + y_offset, 5000 + x_offset, 5000 + y_offset),
        ],
        ('Glen Huntly', 'Caulfield'):[
            (4900 + x_offset, 4300 + y_offset, 5000 + x_offset, 4800 + y_offset),
            (4900 + x_offset, 4150 + y_offset, 5450 + x_offset, 4300 + y_offset), # caulfield coords
        ],
        ('Caulfield', 'Malvern'):[
            (4900 + x_offset, 4150 + y_offset, 5450 + x_offset, 4300 + y_offset), # caulfield coords
            (4900 + x_offset, 3950 + y_offset, 5080 + x_offset, 4100 + y_offset), # malvern coords
            (5080 + x_offset, 4000 + y_offset, 5270 + x_offset, 4050 + y_offset), # malvern coords
            (5270 + x_offset, 3950 + y_offset, 5450 + x_offset, 4100 + y_offset), # malvern coords
            (4900 + x_offset, 4000 + y_offset, 5000 + x_offset, 4150 + y_offset),
        ],
        ('Malvern', 'Armadale'):[
            (4900 + x_offset, 3950 + y_offset, 5080 + x_offset, 4100 + y_offset), # malvern coords
            (5080 + x_offset, 4000 + y_offset, 5270 + x_offset, 4050 + y_offset), # malvern coords
            (5270 + x_offset, 3950 + y_offset, 5450 + x_offset, 4100 + y_offset), # malvern coords
            (4850 + x_offset, 3800 + y_offset, 5000 + x_offset, 4050 + y_offset),
        ],
        ('Armadale', 'Toorak'):[
            (4900 + x_offset, 3550 + y_offset, 5000 + x_offset, 3850 + y_offset),
        ],
        ('Toorak', 'Hawksburn'):[
            (4900 + x_offset, 3400 + y_offset, 5000 + x_offset, 3650 + y_offset)
        ],
        ('Hawksburn', 'South Yarra'):[
            (4900 + x_offset, 2850 + y_offset, 5000 + x_offset, 3450 + y_offset),
            (4800 + x_offset, 2750 + y_offset, 5050 + x_offset, 2900 + y_offset), # south yarra coords
        ],
        ('South Yarra', 'Richmond'):[
            (4600 + x_offset, 2100 + y_offset, 5000 + x_offset, 2150 + y_offset),
            (4950 + x_offset, 2150 + y_offset, 5000 + x_offset, 2800 + y_offset),
            (4800 + x_offset, 2750 + y_offset, 5050 + x_offset, 2900 + y_offset), # south yarra coords
            (4500 + x_offset, 1950 + y_offset, 4650 + x_offset, 2600 + y_offset), # richmond coords
        ],
        ('Richmond','Flinders Street'): [
            (3050 + x_offset, 2100 + y_offset, 4550 + x_offset, 2150 + y_offset),
            (4500 + x_offset, 1950 + y_offset, 4650 + x_offset, 2600 + y_offset), # richmond coords
            (2750 + x_offset, 1500 + y_offset, 3050 + x_offset, 1650 + y_offset), # Town hall part
            (2900 + x_offset, 1650 + y_offset, 3049 + x_offset, 2599 + y_offset), # Flinders Street icon
        ],
        ('Flinders Street','Southern Cross'): [
            (1950 + x_offset, 2100 + y_offset, 2900 + x_offset, 2150 + y_offset),
            (1950 + x_offset, 1400 + y_offset, 2000 + x_offset, 2150 + y_offset),
            (2750 + x_offset, 1500 + y_offset, 3050 + x_offset, 1650 + y_offset), # Town hall part
            (2900 + x_offset, 1650 + y_offset, 3049 + x_offset, 2599 + y_offset), # Flinders Street icon
            (1200 + x_offset, 1251 + y_offset, 2349 + x_offset, 1399 + y_offset), # Southern Cross icon
        ],
        ('Southern Cross','Flagstaff'): [
            (1200 + x_offset, 1251 + y_offset, 2349 + x_offset, 1399 + y_offset), # Southern Cross icon
            (1950 + x_offset, 700 + y_offset, 2000 + x_offset, 1250 + y_offset),
            (1950 + x_offset, 700 + y_offset, 2350 + x_offset, 750 + y_offset),
            (2350 + x_offset, 650 + y_offset, 2500 + x_offset, 1150 + y_offset), # Flagstaff Coords
        ],
        ('Flagstaff','Melbourne Central'): [
            (2350 + x_offset, 650 + y_offset, 2500 + x_offset, 1150 + y_offset), # Flagstaff Coords
            (2500 + x_offset, 700 + y_offset, 2900 + x_offset, 750 + y_offset),
            (2750 + x_offset, 400 + y_offset, 3050 + x_offset, 550 + y_offset), # State Library part
            (2900 + x_offset, 550 + y_offset, 3050 + x_offset, 1150 + y_offset), # Melbourne Central Coords
        ],
        ('Melbourne Central','Parliament'): [
            (2750 + x_offset, 400 + y_offset, 3050 + x_offset, 550 + y_offset), # State Library part
            (2900 + x_offset, 550 + y_offset, 3050 + x_offset, 1150 + y_offset), # Melbourne Central Coords
            (3050 + x_offset, 700 + y_offset, 3550 + x_offset, 750 + y_offset),
            (3450 + x_offset, 700 + y_offset, 3600 + x_offset, 1250 + y_offset),
            (3050 + x_offset, 1250 + y_offset, 3600 + x_offset, 1400 + y_offset), # Parliament Coord
        ],
        ('Parliament','Richmond'): [
            (3050 + x_offset, 1250 + y_offset, 3600 + x_offset, 1400 + y_offset), # Parliament Coord
            (3500 + x_offset, 1400 + y_offset, 3550 + x_offset, 2150 + y_offset),
            (3500 + x_offset, 2100 + y_offset, 4500 + x_offset, 2150 + y_offset),
            (4500 + x_offset, 1950 + y_offset, 4650 + x_offset, 2600 + y_offset), # richmond coords
        ],

    },

    'northern': {
    # Loop
    ('North Melbourne', 'Flagstaff'):[
        (1950 + x_offset, 500 + y_offset, 2300 + x_offset, 700 + y_offset),
        (2250 + x_offset, 950 + y_offset, 2350 + x_offset, 1100 + y_offset),
        (1200 + x_offset, 350 + y_offset, 1339 + x_offset, 499 + y_offset), # North Melbourne icon
        (1300 + x_offset, 400 + y_offset, 1649 + x_offset, 449 + y_offset), # North Melbourne icon
        (1602 + x_offset, 350 + y_offset, 2049 + x_offset, 499 + y_offset), # North Melbourne icon
        (2350 + x_offset, 650 + y_offset, 2500 + x_offset, 1150 + y_offset), # Flagstaff Coords
    ],

    ("Flagstaff", "Melbourne Central"):[
        (2500 + x_offset, 1050 + y_offset, 2900 + x_offset, 1100 + y_offset),
        (2350 + x_offset, 650 + y_offset, 2500 + x_offset, 1150 + y_offset), # Flagstaff Coords
        (2750 + x_offset, 400 + y_offset, 3050 + x_offset, 550 + y_offset), # State Library part
        (2900 + x_offset, 550 + y_offset, 3050 + x_offset, 1150 + y_offset), # Melbourne Central Coords
    ],
    ('Melbourne Central', 'Parliament'):[
        (3050 + x_offset, 1000 + y_offset, 3150 + x_offset, 1250 + y_offset),
        (2750 + x_offset, 400 + y_offset, 3050 + x_offset, 550 + y_offset), # State Library part
        (2900 + x_offset, 550 + y_offset, 3050 + x_offset, 1150 + y_offset), # Melbourne Central Coords
        (3050 + x_offset, 1250 + y_offset, 3600 + x_offset, 1400 + y_offset), # Parliament Coords
    ],

    ('Parliament', 'Flinders Street'):[
        (3050 + x_offset, 1400 + y_offset, 3150 + x_offset, 1850 + y_offset),
        (2750 + x_offset, 1500 + y_offset, 3050 + x_offset, 1650 + y_offset), # Town hall part
        (2900 + x_offset, 1650 + y_offset, 3049 + x_offset, 2599 + y_offset), # Flinders Street icon
        (3050 + x_offset, 1250 + y_offset, 3600 + x_offset, 1400 + y_offset), # Parliament Coords
    ],

    ('Flinders Street', 'Southern Cross'):[
        (2250 + x_offset, 1400 + y_offset, 2300 + x_offset, 1850 + y_offset),
        (2300 + x_offset, 1800 + y_offset, 2900 + x_offset, 1850 + y_offset), 
        (2750 + x_offset, 1500 + y_offset, 3050 + x_offset, 1650 + y_offset), # Town hall part
        (2900 + x_offset, 1650 + y_offset, 3049 + x_offset, 2599 + y_offset), # Flinders Street icon
        (1200 + x_offset, 1251 + y_offset, 2349 + x_offset, 1399 + y_offset), # Southern Cross icon
    ],

    ('Southern Cross', 'North Melbourne'):[
        (1950 + x_offset, 500 + y_offset, 2300 + x_offset, 700 + y_offset),
        (2250 + x_offset, 950 + y_offset, 2300 + x_offset, 1250 + y_offset),
        (1200 + x_offset, 350 + y_offset, 1339 + x_offset, 499 + y_offset), # North Melbourne icon
        (1300 + x_offset, 400 + y_offset, 1649 + x_offset, 449 + y_offset), # North Melbourne icon
        (1602 + x_offset, 350 + y_offset, 2049 + x_offset, 499 + y_offset), # North Melbourne icon
        (1200 + x_offset, 1251 + y_offset, 2349 + x_offset, 1399 + y_offset), # Southern Cross icon
    ],

    ('North Melbourne', 'Kensington'): [
        (1950 + x_offset, -700 + y_offset, 2000 + x_offset, 350 + y_offset),
        (1950 + x_offset, -700 + y_offset, 2050 + x_offset, -650 + y_offset),
        (1200 + x_offset, 350 + y_offset, 1339 + x_offset, 499 + y_offset), # North Melbourne icon
        (1300 + x_offset, 400 + y_offset, 1649 + x_offset, 449 + y_offset), # North Melbourne icon
        (1602 + x_offset, 350 + y_offset, 2049 + x_offset, 499 + y_offset), # North Melbourne icon
    ],

    # Craigieburn Line
    ('Kensington', 'Newmarket'): [
        (1950 + x_offset, -900 + y_offset, 2050 + x_offset, -650 + y_offset),
    ],

    ('Newmarket', 'Ascot Vale'): [
        (1950 + x_offset, -1100 + y_offset, 2050 + x_offset, -850 + y_offset),
    ],

    ('Ascot Vale', 'Moonee Ponds'): [
        (1950 + x_offset, -1300 + y_offset, 2050 + x_offset, -1050 + y_offset),
    ],

    ('Moonee Ponds', 'Essendon'): [
        (1950 + x_offset, -1500 + y_offset, 2050 + x_offset, -1250 + y_offset),
    ],

    ('Essendon', 'Glenbervie'): [
        (1950 + x_offset, -1700 + y_offset, 2050 + x_offset, -1450 + y_offset),
    ],

    ('Glenbervie', 'Strathmore'): [
        (1950 + x_offset, -1900 + y_offset, 2050 + x_offset, -1650 + y_offset),
    ],

    ('Strathmore', 'Pascoe Vale'): [
        (1950 + x_offset, -2100 + y_offset, 2050 + x_offset, -1850 + y_offset),
    ],

    ('Pascoe Vale', 'Oak Park'): [
        (1950 + x_offset, -2300 + y_offset, 2050 + x_offset, -2050 + y_offset),
    ],

    ('Oak Park', 'Glenroy'): [
        (1950 + x_offset, -2500 + y_offset, 2050 + x_offset, -2250 + y_offset),
    ],

    ('Glenroy', 'Jacana'): [
        (1950 + x_offset, -2700 + y_offset, 2050 + x_offset, -2450 + y_offset),
    ],

    ('Jacana', 'Broadmeadows'): [
        (1950 + x_offset, -2800 + y_offset, 2050 + x_offset, -2650 + y_offset),
        (1550 + x_offset, -2950 + y_offset, 2049 + x_offset, -2801 + y_offset), # broadmeadows station icon
    ],

    ('Broadmeadows', 'Coolaroo'): [
        (1950 + x_offset, -3100 + y_offset, 2050 + x_offset, -2950 + y_offset),
        (1550 + x_offset, -2950 + y_offset, 2049 + x_offset, -2801 + y_offset), # broadmeadows station icon
    ],

    ('Coolaroo', 'Roxburgh Park'): [
        (1950 + x_offset, -3300 + y_offset, 2050 + x_offset, -3050 + y_offset),
    ],

    ('Roxburgh Park', 'Craigieburn'): [
        (1950 + x_offset, -3450 + y_offset, 2050 + x_offset, -3250 + y_offset),
        (1650 + x_offset, -3600 + y_offset, 2050 + x_offset, -3450 + y_offset), # craigieburn coords
    ],
    
    # upfield line
    ('Upfield', 'Gowrie'):[
        (2900 + x_offset, -3050 + y_offset, 3050 + x_offset, -2750 + y_offset),
    ],
    ('Gowrie','Fawkner'): [
        (2950 + x_offset, -2850 + y_offset, 3050 + x_offset, -2550 + y_offset),
    ],
    ('Fawkner', 'Merlynston'):[
        (2900 + x_offset, -2600 + y_offset, 3050 + x_offset, -2350 + y_offset),
    ],
    ('Merlynston','Batman'):[
        (2900 + x_offset, -2450 + y_offset, 3050 + x_offset, -2150 + y_offset),
    ],
    ('Batman', 'Coburg'):[
        (2900 + x_offset, -2200 + y_offset, 3050 + x_offset, -1950 + y_offset),
    ],
    ('Coburg', 'Moreland'):[
        (2950 + x_offset, -2000 + y_offset, 3050 + x_offset, -1750 + y_offset),
    ],
    ('Moreland','Anstey'):[
        (2900 + x_offset, -1800 + y_offset, 3050 + x_offset, -1550 + y_offset),
    ],
    ('Anstey','Brunswick'):[
        (2900 + x_offset, -1600 + y_offset, 3050 + x_offset, -1400 + y_offset),
        (2900 + x_offset, -1400 + y_offset, 3050 + x_offset, -1350 + y_offset),
    ],
    ('Brunswick',"Jewell"):[
        (2950 + x_offset, -1400 + y_offset, 3050 + x_offset, -1150 + y_offset),
    ],
    ('Jewell', 'Royal Park'):[
        (2950 + x_offset, -1200 + y_offset, 3050 + x_offset, -950 + y_offset),
    ],
    ('Royal Park', 'Flemington Bridge'):[
        (2900 + x_offset, -1000 + y_offset, 3050 + x_offset, -750 + y_offset),
    ],
    ('Flemington Bridge','Macaulay'):[
        (2900 + x_offset, -800 + y_offset, 3050 + x_offset, -550 + y_offset),
    ],
    ('Macaulay', 'North Melbourne'):[
        (2950 + x_offset, -600 + y_offset, 3050 + x_offset, -500 + y_offset),
        (1950 + x_offset, -500 + y_offset, 3000 + x_offset, -400 + y_offset),
        (1950 + x_offset, -500 + y_offset, 2000 + x_offset, 350 + y_offset),
        (1200 + x_offset, 350 + y_offset, 1339 + x_offset, 499 + y_offset), # North Melbourne icon
        (1300 + x_offset, 400 + y_offset, 1649 + x_offset, 449 + y_offset), # North Melbourne icon
        (1602 + x_offset, 350 + y_offset, 2049 + x_offset, 499 + y_offset), # North Melbourne icon
    ],
    
    
    },
        
    'flemington': {
        ('Flinders Street','Southern Cross'): [
            (2750 + x_offset, 1500 + y_offset, 3050 + x_offset, 1650 + y_offset), # Town hall part
            (2900 + x_offset, 1650 + y_offset, 3049 + x_offset, 2599 + y_offset), # Flinders Street icon
            (1200 + x_offset, 1251 + y_offset, 2349 + x_offset, 1399 + y_offset), # Southern Cross icon
            (1650 + x_offset, 2400 + y_offset, 2899 + x_offset, 2449 + y_offset),
            (1621 + x_offset, 1398 + y_offset, 1708 + x_offset, 2388 + y_offset),
            ],
        ('Southern Cross','North Melbourne'): [
            (1200 + x_offset, 1251 + y_offset, 2349 + x_offset, 1399 + y_offset), # Southern Cross icon
            (1633 + x_offset, 909 + y_offset, 1708 + x_offset, 1239 + y_offset),
            (1621 + x_offset, 747 + y_offset, 1696 + x_offset, 834 + y_offset),
            (1621 + x_offset, 492 + y_offset, 1717 + x_offset, 684 + y_offset),
            (1200 + x_offset, 350 + y_offset, 1339 + x_offset, 499 + y_offset), # North Melbourne icon
            (1300 + x_offset, 400 + y_offset, 1649 + x_offset, 449 + y_offset), # North Melbourne icon
            (1602 + x_offset, 350 + y_offset, 2049 + x_offset, 499 + y_offset), # North Melbourne icon
            
        ],
        ('North Melbourne','Showgrounds'): [
            (1621 + x_offset, 492 + y_offset, 1717 + x_offset, 684 + y_offset),
            (1612 + x_offset, -100 + y_offset, 1708 + x_offset, 345 + y_offset),
            (1633 + x_offset, -1020 + y_offset, 1717 + x_offset, 350 + y_offset),
            (1300 + x_offset, -1050 + y_offset, 1700 + x_offset, -900 + y_offset),
            (1200 + x_offset, 350 + y_offset, 1339 + x_offset, 499 + y_offset), # North Melbourne icon
            (1300 + x_offset, 400 + y_offset, 1649 + x_offset, 449 + y_offset), # North Melbourne icon
            (1602 + x_offset, 350 + y_offset, 2049 + x_offset, 499 + y_offset), # North Melbourne icon
        ],
        ('Showgrounds','Flemington Racecourse'): [
            (900 + x_offset, -1050 + y_offset, 1350 + x_offset, -900 + y_offset),
            ],
    },
    'stony_point':{
        ('Stony Point','Crib Point'): [
            (5000 + x_offset, 10150 + y_offset, 5150 + x_offset, 10400 + y_offset),
        ],
        ('Crib Point','Morradoo'): [
            (5050 + x_offset, 9900 + y_offset, 5150 + x_offset, 10200 + y_offset),
        ],
        ('Morradoo','Bittern'): [
            (5050 + x_offset, 9750 + y_offset, 5150 + x_offset, 10000 + y_offset),
        ],
        ('Bittern','Hastings'): [
            (5050 + x_offset, 9500 + y_offset, 5150 + x_offset, 9800 + y_offset),
        ],
        ('Hastings','Tyabb'): [
            (5050 + x_offset, 9350 + y_offset, 5150 + x_offset, 9600 + y_offset),
        ],
        ('Tyabb','Somerville'): [
            (5050 + x_offset, 9150 + y_offset, 5150 + x_offset, 9400 + y_offset),
        ],
        ('Somerville','Baxter'): [
            (5050 + x_offset, 8900 + y_offset, 5150 + x_offset, 9200 + y_offset),
        ],
        ('Baxter','Leawarra'): [
            (5050 + x_offset, 8750 + y_offset, 5150 + x_offset, 9000 + y_offset),
        ],
        ('Leawarra','Frankston'): [
            (4900 + x_offset, 8500 + y_offset, 5150 + x_offset, 8800 + y_offset),
        ],
        },
    
    'vline_intercity':{
        # traralgon line
        ('Traralgon','Morwell'): [
            (21750 + x_offset, 4400 + y_offset, 21900 + x_offset, 4650 + y_offset), # traralgon coords
            (21350 + x_offset, 4400 + y_offset, 21750 + x_offset, 4500 + y_offset),
        ],
        ('Morwell','Moe'): [
            (21000 + x_offset, 4350 + y_offset, 21400 + x_offset, 4500 + y_offset),
        ],
        ('Moe','Trafalgar'): [
            (20650 + x_offset, 4400 + y_offset, 21050 + x_offset, 4500 + y_offset),
        ],
        ('Trafalgar','Yarragon'): [
            (20200 + x_offset, 4400 + y_offset, 20700 + x_offset, 4500 + y_offset),
        ],  
        ('Yarragon','Warragul'): [
            (19700 + x_offset, 4400 + y_offset, 20250 + x_offset, 4500 + y_offset),
        ],
        ('Drouin','Warragul'): [
            (19300 + x_offset, 4400 + y_offset, 19750 + x_offset, 4500 + y_offset),
        ],

        ('Drouin','Longwarry'): [
            (18850 + x_offset, 4400 + y_offset, 19350 + x_offset, 4500 + y_offset),
        ],
        ('Longwarry','Bunyip'): [
            (18400 + x_offset, 4400 + y_offset, 18900 + x_offset, 4500 + y_offset),
        ],
        ('Bunyip','Garfield'): [
            (18000 + x_offset, 4350 + y_offset, 18450 + x_offset, 4500 + y_offset),
        ],
        ('Garfield','Tynong'): [
            (17600 + x_offset, 4350 + y_offset, 18050 + x_offset, 4500 + y_offset),
        ],
        ('Tynong','Nar Nar Goon'): [
            (17100 + x_offset, 4400 + y_offset, 17650 + x_offset, 4500 + y_offset),
        ],
        ('Nar Nar Goon','Pakenham'): [
            (15700 + x_offset, 4450 + y_offset, 17150 + x_offset, 4500 + y_offset),
            (17100 + x_offset, 4400 + y_offset, 17150 + x_offset, 4500 + y_offset),
            (15600 + x_offset, 4300 + y_offset, 15750 + x_offset, 4650 + y_offset), # pakenham coords
        ],

        ('Pakenham','Berwick'): [
            (13400 + x_offset, 4400 + y_offset, 13450 + x_offset, 4500 + y_offset),
            (13450 + x_offset, 4450 + y_offset, 15600 + x_offset, 4500 + y_offset),
            (15600 + x_offset, 4300 + y_offset, 15750 + x_offset, 4650 + y_offset), # pakenham coords
        ],
        ('Berwick','Dandenong'): [
            (12050 + x_offset, 4450 + y_offset, 13400 + x_offset, 4500 + y_offset),
            (13400 + x_offset, 4400 + y_offset, 13450 + x_offset, 4500 + y_offset),
            (11900 + x_offset, 4400 + y_offset, 12000 + x_offset, 4500 + y_offset),
            (11750 + x_offset, 4300 + y_offset, 11900 + x_offset, 4650 + y_offset), # dandenong coords
        ],
        ('Dandenong','Clayton'): [
            (8550 + x_offset, 4400 + y_offset, 11750 + x_offset, 4500 + y_offset),
            (11750 + x_offset, 4300 + y_offset, 11900 + x_offset, 4650 + y_offset), # dandenong coords
            (8400 + x_offset, 4300 + y_offset, 8550 + x_offset, 4650 + y_offset), # clayton coords
        ],
        ('Clayton','Caulfield'): [
            (5200 + x_offset, 4450 + y_offset, 8400 + x_offset, 4500 + y_offset),
            (5200 + x_offset, 4250 + y_offset, 5250 + x_offset, 4500 + y_offset),
            (8400 + x_offset, 4300 + y_offset, 8550 + x_offset, 4650 + y_offset), # clayton coords
            (4900 + x_offset, 4150 + y_offset, 5450 + x_offset, 4300 + y_offset), # caulfield coords
        ],
        ('Caulfield','Richmond'): [
            (5200 + x_offset, 2200 + y_offset, 5250 + x_offset, 4000 + y_offset),
            (5200 + x_offset, 4050 + y_offset, 5250 + x_offset, 4150 + y_offset),
            (4650 + x_offset, 2150 + y_offset, 4950 + x_offset, 2250 + y_offset),
            (5000 + x_offset, 2150 + y_offset, 5250 + x_offset, 2250 + y_offset),
            (4900 + x_offset, 4150 + y_offset, 5450 + x_offset, 4300 + y_offset), # caulfield coords
            (4500 + x_offset, 1950 + y_offset, 4650 + x_offset, 2600 + y_offset), # richmond coords
        ],
        ('Richmond','Flinders Street'): [
            (3050 + x_offset, 2200 + y_offset, 4550 + x_offset, 2250 + y_offset),
            (4500 + x_offset, 1950 + y_offset, 4650 + x_offset, 2600 + y_offset), # richmond coords
            (2750 + x_offset, 1500 + y_offset, 3050 + x_offset, 1650 + y_offset), # Town hall part
            (2900 + x_offset, 1650 + y_offset, 3049 + x_offset, 2599 + y_offset), # Flinders Street icon
        ],
        ('Flinders Street','Southern Cross'): [
            (1850 + x_offset, 1350 + y_offset, 1900 + x_offset, 2250 + y_offset),
            (1800 + x_offset, 2150 + y_offset, 2900 + x_offset, 2250 + y_offset),
            (2750 + x_offset, 1500 + y_offset, 3050 + x_offset, 1650 + y_offset), # Town hall part
            (2900 + x_offset, 1650 + y_offset, 3049 + x_offset, 2599 + y_offset), # Flinders Street icon
            (1200 + x_offset, 1250 + y_offset, 2349 + x_offset, 1399 + y_offset), # Southern 
        ], 
        
        # geelong line
        ('Waurn Ponds','Marshall'):[
            (-5200 + x_offset, 2750 + y_offset, -4950 + x_offset, 2900 + y_offset), # waurn ponds coords
            (-5200 + x_offset, 2600 + y_offset, -5100 + x_offset, 2750 + y_offset),
        ],
        ('Marshall','South Geelong'):[
            (-5200 + x_offset, 2400 + y_offset, -5100 + x_offset, 2650 + y_offset),
        ],
        ('South Geelong', 'Geelong'):[
            (-5200 + x_offset, 2150 + y_offset, -4950 + x_offset, 2300 + y_offset), # Geelong coords
            (-5200 + x_offset, 2150 + y_offset, -5100 + x_offset, 2450 + y_offset),
        ],
        ('Geelong','North Geelong'):[
            (-5200 + x_offset, 2000 + y_offset, -5100 + x_offset, 2150 + y_offset),
            (-5200 + x_offset, 2150 + y_offset, -4950 + x_offset, 2300 + y_offset), # Geelong coords
        ],
        ('North Geelong', 'North Shore'):[
            (-5200 + x_offset, 1800 + y_offset, -5100 + x_offset, 2050 + y_offset),
        ],
        ('North Shore','Corio'):[
            (-5200 + x_offset, 1600 + y_offset, -5100 + x_offset, 1850 + y_offset),
        ],
        ('Corio', 'Lara'):[
            (-5200 + x_offset, 1400 + y_offset, -5100 + x_offset, 1650 + y_offset),
        ],
        ('Lara', 'Little River'):[
            (-5200 + x_offset, 1200 + y_offset, -5100 + x_offset, 1450 + y_offset),
        ],
        ('Little River','Wyndham Vale'):[
            (-5200 + x_offset, 1000 + y_offset, -5100 + x_offset, 1250 + y_offset),
        ],
        ('Wyndham Vale','West Tarneit'):[
            (-5200 + x_offset, 800 + y_offset, -5100 + x_offset, 1050 + y_offset),
        ],
        ('West Tarneit','Tarneit'):[
            (-5200 + x_offset, 600 + y_offset, -5100 + x_offset, 850 + y_offset),
        ],
        ('Tarneit','Deer Park'): [
            (-5250 + x_offset, 450 + y_offset, -5100 + x_offset, 650 + y_offset),
            (-5150 + x_offset, 450 + y_offset, -4950 + x_offset, 500 + y_offset),
            (-4950 + x_offset, 200 + y_offset, -4800 + x_offset, 650 + y_offset), # deer park coords
        ],
        ('Deer Park','Sunshine'):[
            (-4800 + x_offset, 450 + y_offset, -2900 + x_offset, 500 + y_offset),
            (-2900 + x_offset, -200 + y_offset, -2750 + x_offset, -50 + y_offset), # Sunshine Coords
            (-2850 + x_offset, -80 + y_offset, -2800 + x_offset, 220 + y_offset), # Sunshine Coords
            (-2900 + x_offset, 220 + y_offset, -2750 + x_offset, 550 + y_offset), # Sunshine Coords 
        ],
        ('Sunshine','Footscray'):[
            (-2750 + x_offset, 450 + y_offset, -2600 + x_offset, 500 + y_offset),
            (-2650 + x_offset, -100 + y_offset, -2600 + x_offset, 500 + y_offset),
            (-2650 + x_offset, -50 + y_offset, -600 + x_offset, 0 + y_offset),
            (-2900 + x_offset, -200 + y_offset, -2750 + x_offset, -50 + y_offset), # Sunshine Coords
            (-2850 + x_offset, -80 + y_offset, -2800 + x_offset, 220 + y_offset), # Sunshine Coords
            (-2900 + x_offset, 220 + y_offset, -2750 + x_offset, 550 + y_offset), # Sunshine Coords  
            (-600 + x_offset, -200 + y_offset, -451 + x_offset, 149 + y_offset), # footscray station icon
            (-550 + x_offset, 100 + y_offset, -501 + x_offset, 249 + y_offset), # footscray station icon
            (-600 + x_offset, 200 + y_offset, -451 + x_offset, 349 + y_offset), # footscray station icon
        ],
        ('Footscray', 'Southern Cross'):[
            (-600 + x_offset, -200 + y_offset, -451 + x_offset, 149 + y_offset), # footscray station icon
            (-550 + x_offset, 100 + y_offset, -501 + x_offset, 249 + y_offset), # footscray station icon
            (-600 + x_offset, 200 + y_offset, -451 + x_offset, 349 + y_offset), # footscray station icon
            (-450 + x_offset, -50 + y_offset, 1600 + x_offset, 0 + y_offset),
            (1550 + x_offset, -50 + y_offset, 1600 + x_offset, 400 + y_offset),
            (1550 + x_offset, 450 + y_offset, 1600 + x_offset, 750 + y_offset),
            (1550 + x_offset, 700 + y_offset, 1900 + x_offset, 750 + y_offset),
            (1850 + x_offset, 750 + y_offset, 1900 + x_offset, 1250 + y_offset),
            (1200 + x_offset, 1250 + y_offset, 2349 + x_offset, 1399 + y_offset), # Southern 
        ], 
        # seymour line
        ('Seymour','Tallarook'):[
            (1850 + x_offset, -5050 + y_offset, 1950 + x_offset, -4900 + y_offset),
            (1550 + x_offset, -5200 + y_offset, 1950 + x_offset, -5050 + y_offset), # seymour station icon
        ],
        ('Tallarook','Broadford'):[
            (1850 + x_offset, -4950 + y_offset, 1950 + x_offset, -4700 + y_offset),
        ],
        ('Broadford','Kilmore East'):[
            (1850 + x_offset, -4750 + y_offset, 1950 + x_offset, -4500 + y_offset),
        ],
        ('Kilmore East','Wandong'):[
            (1850 + x_offset, -4550 + y_offset, 1950 + x_offset, -4300 + y_offset),
        ],
        ('Wandong','Heathcote Junction'):[
            (1850 + x_offset, -4350 + y_offset, 1950 + x_offset, -4100 + y_offset),
        ],
        ('Heathcote Junction','Wallan'):[
            (1850 + x_offset, -4150 + y_offset, 1950 + x_offset, -3900 + y_offset),
        ],
        ('Wallan','Donnybrook'):[
            (1850 + x_offset, -4000 + y_offset, 1950 + x_offset, -3700 + y_offset),
        ],
        ('Donnybrook','Craigieburn'):[
            (1650 + x_offset, -3600 + y_offset, 2050 + x_offset, -3450 + y_offset), # craigieburn coords
            (1850 + x_offset, -3750 + y_offset, 1950 + x_offset, -3600 + y_offset),
        ],
        ('Craigieburn','Broadmeadows'):[
            (1850 + x_offset, -3450 + y_offset, 1900 + x_offset, -2950 + y_offset),
            (1550 + x_offset, -2950 + y_offset, 2049 + x_offset, -2801 + y_offset), # broadmeadows station icon
            (1650 + x_offset, -3600 + y_offset, 2050 + x_offset, -3450 + y_offset), # craigieburn coords
        ],
        ('Broadmeadows','Essendon'):[
            (1850 + x_offset, -2800 + y_offset, 1950 + x_offset, -1450 + y_offset),
            (1550 + x_offset, -2950 + y_offset, 2049 + x_offset, -2801 + y_offset), # broadmeadows station icon
        ],
        ('Essendon','North Melbourne'):[
            (1850 + x_offset, -1500 + y_offset, 1950 + x_offset, 350 + y_offset),
            (1200 + x_offset, 350 + y_offset, 1339 + x_offset, 499 + y_offset), # North Melbourne icon
            (1300 + x_offset, 400 + y_offset, 1649 + x_offset, 449 + y_offset), # North Melbourne icon
            (1602 + x_offset, 350 + y_offset, 2049 + x_offset, 499 + y_offset), # North Melbourne icon
        ],
        ('North Melbourne','Southern Cross'):[
            (1850 + x_offset, 500 + y_offset, 1900 + x_offset, 1250 + y_offset),
            (1200 + x_offset, 350 + y_offset, 1339 + x_offset, 499 + y_offset), # North Melbourne icon
            (1300 + x_offset, 400 + y_offset, 1649 + x_offset, 449 + y_offset), # North Melbourne icon
            (1602 + x_offset, 350 + y_offset, 2049 + x_offset, 499 + y_offset), # North Melbourne icon
            (1200 + x_offset, 1250 + y_offset, 2349 + x_offset, 1399 + y_offset), # Southern 
        ],
        #bendigo line
        ('Eaglehawk','Bendigo'):[
            (-3350 + x_offset, -4300 + y_offset, -3050 + x_offset, -4150 + y_offset), # eaglehawk coords
            (-3350 + x_offset, -3850 + y_offset, -3100 + x_offset, -3700 + y_offset), # bendigo coords
            (-3150 + x_offset, -4150 + y_offset, -3100 + x_offset, -3900 + y_offset),
            (-3200 + x_offset, -3950 + y_offset, -3100 + x_offset, -3850 + y_offset),
        ],
        ('Epsom','Bendigo'):[
            (-2100 + x_offset, -4100 + y_offset, -1950 + x_offset, -3850 + y_offset), # epsom coords
            (-3350 + x_offset, -3850 + y_offset, -3100 + x_offset, -3700 + y_offset), # bendigo coords
            (-3200 + x_offset, -3950 + y_offset, -2100 + x_offset, -3850 + y_offset),
        ],
        ('Bendigo','Kangaroo Flat'):[
            (-3350 + x_offset, -3850 + y_offset, -3100 + x_offset, -3700 + y_offset), # bendigo coords
            (-3200 + x_offset, -3700 + y_offset, -3100 + x_offset, -3550 + y_offset),
        ],
        ('Kangaroo Flat','Castlemaine'):[
            (-3200 + x_offset, -3600 + y_offset, -3100 + x_offset, -3350 + y_offset),
            (-3450 + x_offset, -3450 + y_offset, -3100 + x_offset, -3300 + y_offset), # castlemaine coords
        ],
        ('Castlemaine','Malmsbury'):[
            (-3200 + x_offset, -3400 + y_offset, -3100 + x_offset, -3150 + y_offset),
            (-3450 + x_offset, -3450 + y_offset, -3100 + x_offset, -3300 + y_offset), # castlemaine coords
        ],
        ('Malmsbury','Kyneton'):[
            (-3200 + x_offset, -3200 + y_offset, -3100 + x_offset, -2950 + y_offset),
        ],
        ('Kyneton','Woodend'):[
            (-3200 + x_offset, -3000 + y_offset, -3100 + x_offset, -2750 + y_offset),
        ],
        ('Woodend','Macedon'):[
            (-3200 + x_offset, -2800 + y_offset, -3100 + x_offset, -2550 + y_offset),
        ],
        ('Macedon','Gisborne'):[
            (-3200 + x_offset, -2600 + y_offset, -3100 + x_offset, -2350 + y_offset),
        ],
        ('Gisborne','Riddells Creek'):[
            (-3200 + x_offset, -2400 + y_offset, -3100 + x_offset, -2150 + y_offset),
        ],
        ('Riddells Creek','Clarkefield'):[
            (-3200 + x_offset, -2200 + y_offset, -3100 + x_offset, -1950 + y_offset),
        ],
        ('Clarkefield','Sunbury'):[
            (-3200 + x_offset, -2000 + y_offset, -3100 + x_offset, -1850 + y_offset),
            (-3350 + x_offset, -1850 + y_offset, -3000 + x_offset, -1700 + y_offset), # Sunbury Coords
        ],
        ('Sunbury','Watergardens'):[
            (-3200 + x_offset, -1700 + y_offset, -3150 + x_offset, -1450 + y_offset),
            (-3350 + x_offset, -1850 + y_offset, -3000 + x_offset, -1700 + y_offset), # Sunbury Coords
            (-3350 + x_offset, -1450 + y_offset, -3000 + x_offset, -1300 + y_offset), # Watergardens Coords
        ],
        ('Watergardens','Footscray'):[
            (-3200 + x_offset, -1300 + y_offset, -3150 + x_offset, 0 + y_offset),
            (-3200 + x_offset, -50 + y_offset, -2850 + x_offset, 0 + y_offset),
            (-2800 + x_offset, -50 + y_offset, -600 + x_offset, 0 + y_offset),
            (-600 + x_offset, -200 + y_offset, -451 + x_offset, 149 + y_offset), # footscray station icon
            (-550 + x_offset, 100 + y_offset, -501 + x_offset, 249 + y_offset), # footscray station icon
            (-600 + x_offset, 200 + y_offset, -451 + x_offset, 349 + y_offset), # footscray station icon
            (-3350 + x_offset, -1450 + y_offset, -3000 + x_offset, -1300 + y_offset), # Watergardens Coords
        ],
    },
    
    'ballarat_seperate':{
        # ballarat line
        ('Wendouree','Ballarat'):[
            (-9550 + x_offset, 200 + y_offset, -9400 + x_offset, 450 + y_offset), # wendouree coords
            (-9400 + x_offset, 200 + y_offset, -9110 + x_offset, 300 + y_offset),
            (-9040 + x_offset, 200 + y_offset, -8800 + x_offset, 300 + y_offset),
            (-8900 + x_offset, 200 + y_offset, -8750 + x_offset, 500 + y_offset),
        ],
        ('Ballarat','Ballan'):[
            (-8750 + x_offset, 200 + y_offset, -8400 + x_offset, 300 + y_offset),
            (-8900 + x_offset, 200 + y_offset, -8750 + x_offset, 450 + y_offset), # ballarat coords
        ],
        ('Ballan','Bacchus Marsh'):[
            (-8450 + x_offset, 200 + y_offset, -7850 + x_offset, 300 + y_offset),
        ],
        ('Bacchus Marsh', 'Melton'):[
            (-7900 + x_offset, 200 + y_offset, -7300 + x_offset, 300 + y_offset),
        ],
        ('Melton', 'Cobblebank'):[
            (-7350 + x_offset, 200 + y_offset, -6800 + x_offset, 300 + y_offset),
        ],
        ('Cobblebank','Rockbank'):[
            (-6850 + x_offset, 200 + y_offset, -6250 + x_offset, 300 + y_offset),
        ],
        ('Rockbank', 'Caroline Springs'):[
            (-6300 + x_offset, 200 + y_offset, -5600 + x_offset, 300 + y_offset),
        ],
        ('Caroline Springs', 'Deer Park'):[
            (-5650 + x_offset, 150 + y_offset, -4950 + x_offset, 300 + y_offset),
            (-4950 + x_offset, 200 + y_offset, -4800 + x_offset, 650 + y_offset), # deer park coords
        ],
        ('Deer Park','Ardeer'):[
            (-4800 + x_offset, 200 + y_offset, -3900 + x_offset, 300 + y_offset),
            (-3950 + x_offset, 200 + y_offset, -3550 + x_offset, 300 + y_offset),
        ],
        ('Ardeer', 'Sunshine'):[
            (-3950 + x_offset, 200 + y_offset, -3550 + x_offset, 300 + y_offset),
            (-3550 + x_offset, 200 + y_offset, -2900 + x_offset, 300 + y_offset),
            (-2900 + x_offset, -200 + y_offset, -2750 + x_offset, -50 + y_offset), # Sunshine Coords
            (-2850 + x_offset, -80 + y_offset, -2800 + x_offset, 220 + y_offset), # Sunshine Coords
            (-2900 + x_offset, 220 + y_offset, -2750 + x_offset, 550 + y_offset), # Sunshine Coords 
        ],
        ('Sunshine','Footscray'):[
            (-2750 + x_offset, 200 + y_offset, -2600 + x_offset, 300 + y_offset),
            (-2650 + x_offset, -50 + y_offset, -600 + x_offset, 0 + y_offset),
            (-2650 + x_offset, -50 + y_offset, -2600 + x_offset, 300 + y_offset),
            (-2900 + x_offset, -200 + y_offset, -2750 + x_offset, -50 + y_offset), # Sunshine Coords
            (-2850 + x_offset, -80 + y_offset, -2800 + x_offset, 220 + y_offset), # Sunshine Coords
            (-2900 + x_offset, 220 + y_offset, -2750 + x_offset, 550 + y_offset), # Sunshine Coords 
            (-600 + x_offset, -200 + y_offset, -451 + x_offset, 149 + y_offset), # footscray station icon
            (-550 + x_offset, 100 + y_offset, -501 + x_offset, 249 + y_offset), # footscray station icon
            (-600 + x_offset, 200 + y_offset, -451 + x_offset, 349 + y_offset), # footscray station icon
        ],
        ('Footscray', 'Southern Cross'):[
            (-600 + x_offset, -200 + y_offset, -451 + x_offset, 149 + y_offset), # footscray station icon
            (-550 + x_offset, 100 + y_offset, -501 + x_offset, 249 + y_offset), # footscray station icon
            (-600 + x_offset, 200 + y_offset, -451 + x_offset, 349 + y_offset), # footscray station icon
            (-450 + x_offset, -50 + y_offset, 1600 + x_offset, 0 + y_offset),
            (1550 + x_offset, -50 + y_offset, 1600 + x_offset, 400 + y_offset),
            (1550 + x_offset, 450 + y_offset, 1600 + x_offset, 750 + y_offset),
            (1550 + x_offset, 700 + y_offset, 1900 + x_offset, 750 + y_offset),
            (1850 + x_offset, 750 + y_offset, 1900 + x_offset, 1250 + y_offset),
            (1200 + x_offset, 1250 + y_offset, 2349 + x_offset, 1399 + y_offset), # Southern 
        ], 
    },

    'vline_long_distance':{
        #bairsndale line
        ('Bairnsdale','Stratford'): [
            (23050 + x_offset, 4500 + y_offset, 23400 + x_offset, 4650 + y_offset),
        ],

        ('Stratford','Sale'): [
            (22650 + x_offset, 4500 + y_offset, 23100 + x_offset, 4650 + y_offset),
        ],

        ('Sale','Rosedale'): [
            (22300 + x_offset, 4500 + y_offset, 22700 + x_offset, 4600 + y_offset),
        ],

        ('Rosedale','Traralgon'): [
            (21900 + x_offset, 4500 + y_offset, 22350 + x_offset, 4600 + y_offset),
            (21750 + x_offset, 4400 + y_offset, 21900 + x_offset, 4650 + y_offset), # traralgon coords
        ],

        ('Traralgon','Morwell'): [
            (21750 + x_offset, 4400 + y_offset, 21900 + x_offset, 4650 + y_offset), # traralgon coords
            (21350 + x_offset, 4500 + y_offset, 21750 + x_offset, 4600 + y_offset),
        ],
        ('Morwell','Moe'): [
            (21000 + x_offset, 4550 + y_offset, 21400 + x_offset, 4600 + y_offset),
        ],
        ('Moe','Trafalgar'): [
            (20650 + x_offset, 4500 + y_offset, 21050 + x_offset, 4600 + y_offset),
        ],
        ('Trafalgar','Yarragon'): [
            (20200 + x_offset, 4500 + y_offset, 20700 + x_offset, 4600 + y_offset),
        ],  
        ('Yarragon','Warragul'): [
            (19700 + x_offset, 4500 + y_offset, 20250 + x_offset, 4600 + y_offset),
        ],
        ('Drouin','Warragul'): [
            (19300 + x_offset, 4500 + y_offset, 19750 + x_offset, 4600 + y_offset),
        ],

        ('Drouin','Longwarry'): [
            (18850 + x_offset, 4500 + y_offset, 19350 + x_offset, 4600 + y_offset),
        ],
        ('Longwarry','Bunyip'): [
            (18400 + x_offset, 4500 + y_offset, 18900 + x_offset, 4600 + y_offset),
        ],
        ('Bunyip','Garfield'): [
            (18000 + x_offset, 4550 + y_offset, 18450 + x_offset, 4600 + y_offset),
        ],
        ('Garfield','Tynong'): [
            (17600 + x_offset, 4550 + y_offset, 18050 + x_offset, 4600 + y_offset),
        ],
        ('Tynong','Nar Nar Goon'): [
            (17100 + x_offset, 4500 + y_offset, 17650 + x_offset, 4600 + y_offset),
        ],
        ('Nar Nar Goon','Pakenham'): [
            (15700 + x_offset, 4550 + y_offset, 17150 + x_offset, 4600 + y_offset),
            (17100 + x_offset, 4500 + y_offset, 17150 + x_offset, 4600 + y_offset),
            (15600 + x_offset, 4300 + y_offset, 15750 + x_offset, 4650 + y_offset), # pakenham coords
        ],

        ('Pakenham','Dandenong'): [
            (11850 + x_offset, 4500 + y_offset, 12000 + x_offset, 4600 + y_offset),
            (12050 + x_offset, 4500 + y_offset, 15600 + x_offset, 4600 + y_offset),
            (15600 + x_offset, 4300 + y_offset, 15750 + x_offset, 4650 + y_offset), # pakenham coords
            (11750 + x_offset, 4300 + y_offset, 11900 + x_offset, 4650 + y_offset), # dandenong coords
        ],
        ('Dandenong','Clayton'): [
            (8550 + x_offset, 4500 + y_offset, 11750 + x_offset, 4600 + y_offset),
            (11750 + x_offset, 4300 + y_offset, 11900 + x_offset, 4650 + y_offset), # dandenong coords
            (8400 + x_offset, 4300 + y_offset, 8550 + x_offset, 4650 + y_offset), # clayton coords
        ],
        ('Clayton','Caulfield'): [
            (5100 + x_offset, 4550 + y_offset, 8400 + x_offset, 4600 + y_offset),
            (5100 + x_offset, 4250 + y_offset, 5150 + x_offset, 4600 + y_offset),
            (8400 + x_offset, 4300 + y_offset, 8550 + x_offset, 4650 + y_offset), # clayton coords
            (4900 + x_offset, 4150 + y_offset, 5450 + x_offset, 4300 + y_offset), # caulfield coords
        ],
        ('Caulfield','Richmond'): [
            (5100 + x_offset, 2300 + y_offset, 5150 + x_offset, 4000 + y_offset),
            (5100 + x_offset, 4050 + y_offset, 5150 + x_offset, 4150 + y_offset),
            (4650 + x_offset, 2250 + y_offset, 4950 + x_offset, 2350 + y_offset),
            (5000 + x_offset, 2250 + y_offset, 5150 + x_offset, 2350 + y_offset),
            (4900 + x_offset, 4150 + y_offset, 5450 + x_offset, 4300 + y_offset), # caulfield coords
            (4500 + x_offset, 1950 + y_offset, 4650 + x_offset, 2600 + y_offset), # richmond coords
        ],
        ('Richmond','Flinders Street'): [
            (3050 + x_offset, 2300 + y_offset, 4550 + x_offset, 2350 + y_offset),
            (4500 + x_offset, 1950 + y_offset, 4650 + x_offset, 2600 + y_offset), # richmond coords
            (2750 + x_offset, 1500 + y_offset, 3050 + x_offset, 1650 + y_offset), # Town hall part
            (2900 + x_offset, 1650 + y_offset, 3049 + x_offset, 2599 + y_offset), # Flinders Street icon
        ],
        ('Flinders Street','Southern Cross'): [
            (1750 + x_offset, 1350 + y_offset, 1800 + x_offset, 2350 + y_offset),
            (1700 + x_offset, 2250 + y_offset, 2900 + x_offset, 2350 + y_offset),
            (2750 + x_offset, 1500 + y_offset, 3050 + x_offset, 1650 + y_offset), # Town hall part
            (2900 + x_offset, 1650 + y_offset, 3049 + x_offset, 2599 + y_offset), # Flinders Street icon
            (1200 + x_offset, 1250 + y_offset, 2349 + x_offset, 1399 + y_offset), # Southern 
        ], 

        # warrnambool line
        ('Warrnambool','Sherwood Park'): [
            (-5100 + x_offset, 4000 + y_offset, -4950 + x_offset, 4250 + y_offset),
        ],
        ('Sherwood Park','Terang'): [
            (-5100 + x_offset, 3800 + y_offset, -5000 + x_offset, 4050 + y_offset),
        ],
        ('Terang','Camperdown'): [ 
            (-5100 + x_offset, 3600 + y_offset, -5000 + x_offset, 3850 + y_offset),
        ],
        ('Camperdown','Colac'): [
            (-5100 + x_offset, 3400 + y_offset, -5000 + x_offset, 3650 + y_offset),
        ],
        ('Colac','Birregurra'): [
            (-5100 + x_offset, 3200 + y_offset, -5000 + x_offset, 3400 + y_offset),
        ],
        ('Birregurra','Winchelsea'): [
            (-5100 + x_offset, 3000 + y_offset, -5000 + x_offset, 3250 + y_offset),
        ],
        ('Winchelsea','Waurn Ponds'): [
            (-5200 + x_offset, 2750 + y_offset, -4950 + x_offset, 2900 + y_offset), # waurn ponds coords
            (-5100 + x_offset, 2900 + y_offset, -5000 + x_offset, 3050 + y_offset),
        ],
        ('Waurn Ponds','Marshall'):[
            (-5200 + x_offset, 2750 + y_offset, -4950 + x_offset, 2900 + y_offset), # waurn ponds coords
            (-5100 + x_offset, 2600 + y_offset, -5000 + x_offset, 2750 + y_offset),
        ],
        ('Marshall','South Geelong'):[
            (-5100 + x_offset, 2400 + y_offset, -5000 + x_offset, 2650 + y_offset),
        ],
        ('South Geelong', 'Geelong'):[
            (-5200 + x_offset, 2150 + y_offset, -4950 + x_offset, 2300 + y_offset), # Geelong coords
            (-5100 + x_offset, 2250 + y_offset, -5000 + x_offset, 2450 + y_offset),
        ],
        ('Geelong','North Geelong'):[
            (-5100 + x_offset, 2000 + y_offset, -5000 + x_offset, 2150 + y_offset),
            (-5200 + x_offset, 2150 + y_offset, -4950 + x_offset, 2300 + y_offset), # Geelong coords
        ],
        ('North Geelong', 'North Shore'):[
            (-5100 + x_offset, 1800 + y_offset, -5000 + x_offset, 2050 + y_offset),
        ],
        ('North Shore','Corio'):[
            (-5100 + x_offset, 1600 + y_offset, -5000 + x_offset, 1850 + y_offset),
        ],
        ('Corio', 'Lara'):[
            (-5100 + x_offset, 1400 + y_offset, -5000 + x_offset, 1650 + y_offset),
        ],
        ('Lara', 'Wyndham Vale'):[
            (-5100 + x_offset, 1000 + y_offset, -5000 + x_offset, 1450 + y_offset),
        ],
        ('Wyndham Vale','Tarneit'):[
            (-5100 + x_offset, 600 + y_offset, -5000 + x_offset, 1050 + y_offset),
        ],
        ('Tarneit','Deer Park'): [
            (-5100 + x_offset, 550 + y_offset, -5100 + x_offset, 650 + y_offset),
            (-5100 + x_offset, 550 + y_offset, -4950 + x_offset, 600 + y_offset),
            (-4950 + x_offset, 200 + y_offset, -4800 + x_offset, 650 + y_offset), # deer park coords
        ],
        ('Deer Park','Sunshine'):[
            (-4800 + x_offset, 550 + y_offset, -2900 + x_offset, 600 + y_offset),
            (-2900 + x_offset, -300 + y_offset, -2750 + x_offset, -50 + y_offset), # Sunshine Coords
            (-2850 + x_offset, -80 + y_offset, -2800 + x_offset, 220 + y_offset), # Sunshine Coords
            (-2900 + x_offset, 220 + y_offset, -2750 + x_offset, 650 + y_offset), # Sunshine Coords 
        ],
        ('Sunshine','Footscray'):[
            (-2750 + x_offset, 550 + y_offset, -2450 + x_offset, 600 + y_offset),
            (-2500 + x_offset, 50 + y_offset, -2450 + x_offset, 600 + y_offset),
            (-2500 + x_offset, 50 + y_offset, -600 + x_offset, 100 + y_offset),
            (-2900 + x_offset, -300 + y_offset, -2750 + x_offset, -50 + y_offset), # Sunshine Coords
            (-2850 + x_offset, -80 + y_offset, -2800 + x_offset, 220 + y_offset), # Sunshine Coords
            (-2900 + x_offset, 220 + y_offset, -2750 + x_offset, 650 + y_offset), # Sunshine Coords 
            (-600 + x_offset, -300 + y_offset, -451 + x_offset, 149 + y_offset), # footscray station icon
            (-550 + x_offset, 100 + y_offset, -501 + x_offset, 249 + y_offset), # footscray station icon
            (-600 + x_offset, 200 + y_offset, -451 + x_offset, 349 + y_offset), # footscray station icon
        ],
        ('Footscray', 'Southern Cross'):[
            (-600 + x_offset, -200 + y_offset, -451 + x_offset, 149 + y_offset), # footscray station icon
            (-550 + x_offset, 100 + y_offset, -501 + x_offset, 249 + y_offset), # footscray station icon
            (-600 + x_offset, 200 + y_offset, -451 + x_offset, 349 + y_offset), # footscray station icon
            (-450 + x_offset, 50 + y_offset, 1500 + x_offset, 100 + y_offset),
            (1450 + x_offset, 50 + y_offset, 1500 + x_offset, 400 + y_offset),
            (1450 + x_offset, 450 + y_offset, 1500 + x_offset, 900 + y_offset),
            (1450 + x_offset, 850 + y_offset, 1800 + x_offset, 900 + y_offset),
            (1750 + x_offset, 900 + y_offset, 1800 + x_offset, 1250 + y_offset),
            (1200 + x_offset, 1250 + y_offset, 2349 + x_offset, 1399 + y_offset), # Southern 
        ], 
        # shepparton line
        ('Shepparton','Mooroopna'):[
            (1700 + x_offset, -6100 + y_offset, 1850 + x_offset, -5850 + y_offset),
        ],
        ('Mooroopna','Murchison East'):[
            (1750 + x_offset, -5900 + y_offset, 1850 + x_offset, -5650 + y_offset),
        ],
        ('Murchison East','Nagambie'):[
            (1750 + x_offset, -5700 + y_offset, 1850 + x_offset, -5450 + y_offset),
        ],
        ('Nagambie','Seymour'):[
            (1750 + x_offset, -5500 + y_offset, 1850 + x_offset, -5450 + y_offset),
            (1750 + x_offset, -5500 + y_offset, 1800 + x_offset, -5200 + y_offset),
            (1550 + x_offset, -5200 + y_offset, 1950 + x_offset, -5050 + y_offset), # seymour station icon
        ],
        ('Seymour','Tallarook'):[
            (1750 + x_offset, -5050 + y_offset, 1850 + x_offset, -4900 + y_offset),
            (1550 + x_offset, -5200 + y_offset, 1950 + x_offset, -5050 + y_offset), # seymour station icon
        ],
        ('Tallarook','Broadford'):[
            (1750 + x_offset, -4950 + y_offset, 1850 + x_offset, -4700 + y_offset),
        ],
        ('Broadford','Kilmore East'):[
            (1750 + x_offset, -4750 + y_offset, 1850 + x_offset, -4500 + y_offset),
        ],
        ('Kilmore East','Wandong'):[
            (1750 + x_offset, -4550 + y_offset, 1850 + x_offset, -4300 + y_offset),
        ],
        ('Wandong','Heathcote Junction'):[
            (1750 + x_offset, -4350 + y_offset, 1850 + x_offset, -4100 + y_offset),
        ],
        ('Heathcote Junction','Wallan'):[
            (1750 + x_offset, -4150 + y_offset, 1850 + x_offset, -3900 + y_offset),
        ],
        ('Wallan','Donnybrook'):[
            (1750 + x_offset, -4000 + y_offset, 1850 + x_offset, -3700 + y_offset),
        ],
        ('Donnybrook','Craigieburn'):[
            (1650 + x_offset, -3600 + y_offset, 2050 + x_offset, -3450 + y_offset), # craigieburn coords
            (1750 + x_offset, -3750 + y_offset, 1850 + x_offset, -3600 + y_offset),
        ],
        ('Craigieburn','Broadmeadows'):[
            (1750 + x_offset, -3450 + y_offset, 1800 + x_offset, -2950 + y_offset),
            (1550 + x_offset, -2950 + y_offset, 2049 + x_offset, -2801 + y_offset), # broadmeadows station icon
            (1650 + x_offset, -3600 + y_offset, 2050 + x_offset, -3450 + y_offset), # craigieburn coords
        ],
        ('Broadmeadows','Essendon'):[
            (1750 + x_offset, -2800 + y_offset, 1850 + x_offset, -1450 + y_offset),
            (1550 + x_offset, -2950 + y_offset, 2049 + x_offset, -2801 + y_offset), # broadmeadows station icon
        ],
        ('Essendon','North Melbourne'):[
            (1750 + x_offset, -1500 + y_offset, 1850 + x_offset, 350 + y_offset),
            (1200 + x_offset, 350 + y_offset, 1339 + x_offset, 499 + y_offset), # North Melbourne icon
            (1300 + x_offset, 400 + y_offset, 1649 + x_offset, 449 + y_offset), # North Melbourne icon
            (1602 + x_offset, 350 + y_offset, 2049 + x_offset, 499 + y_offset), # North Melbourne icon
        ],
        ('North Melbourne','Southern Cross'):[
            (1750 + x_offset, 500 + y_offset, 1850 + x_offset, 700 + y_offset),
            (1750 + x_offset, 750 + y_offset, 1850 + x_offset, 1250 + y_offset),
            (1200 + x_offset, 350 + y_offset, 1339 + x_offset, 499 + y_offset), # North Melbourne icon
            (1300 + x_offset, 400 + y_offset, 1649 + x_offset, 449 + y_offset), # North Melbourne icon
            (1602 + x_offset, 350 + y_offset, 2049 + x_offset, 499 + y_offset), # North Melbourne icon
            (1200 + x_offset, 1250 + y_offset, 2349 + x_offset, 1399 + y_offset), # Southern 
        ],
        # swan hill line
        ('Swan Hill','Kerang'):[
            (-3350 + x_offset, -5250 + y_offset, -3200 + x_offset, -5000 + y_offset),
        ],
        ('Kerang','Pyramid'):[
            (-3300 + x_offset, -5050 + y_offset, -3200 + x_offset, -4800 + y_offset),
        ],
        ('Pyramid','Dingee'):[
            (-3300 + x_offset, -4850 + y_offset, -3200 + x_offset, -4600 + y_offset),
        ],
        ('Dingee','Raywood'):[
            (-3300 + x_offset, -4650 + y_offset, -3200 + x_offset, -4400 + y_offset),
        ],
        ('Raywood','Eaglehawk'):[
            (-3300 + x_offset, -4450 + y_offset, -3200 + x_offset, -4300 + y_offset),
            (-3350 + x_offset, -4300 + y_offset, -3050 + x_offset, -4150 + y_offset), # eaglehawk coords
        ],
        ('Eaglehawk','Bendigo'):[
            (-3350 + x_offset, -4300 + y_offset, -3050 + x_offset, -4150 + y_offset), # eaglehawk coords
            (-3350 + x_offset, -3850 + y_offset, -3100 + x_offset, -3700 + y_offset), # bendigo coords
            (-3300 + x_offset, -4150 + y_offset, -3250 + x_offset, -3850 + y_offset),
        ],
        ('Bendigo','Kangaroo Flat'):[
            (-3350 + x_offset, -3850 + y_offset, -3200 + x_offset, -3700 + y_offset), # bendigo coords
            (-3300 + x_offset, -3700 + y_offset, -3200 + x_offset, -3550 + y_offset),
        ],
        ('Kangaroo Flat','Castlemaine'):[
            (-3300 + x_offset, -3600 + y_offset, -3200 + x_offset, -3350 + y_offset),
            (-3450 + x_offset, -3450 + y_offset, -3100 + x_offset, -3300 + y_offset), # castlemaine coords
        ],
        ('Castlemaine','Malmsbury'):[
            (-3300 + x_offset, -3400 + y_offset, -3200 + x_offset, -3150 + y_offset),
            (-3450 + x_offset, -3450 + y_offset, -3100 + x_offset, -3300 + y_offset), # castlemaine coords
        ],
        ('Malmsbury','Kyneton'):[
            (-3300 + x_offset, -3200 + y_offset, -3200 + x_offset, -2950 + y_offset),
        ],
        ('Kyneton','Woodend'):[
            (-3300 + x_offset, -3000 + y_offset, -3200 + x_offset, -2750 + y_offset),
        ],
        ('Woodend','Gisborne'):[
            (-3300 + x_offset, -2800 + y_offset, -3200 + x_offset, -2750 + y_offset),
            (-3300 + x_offset, -2400 + y_offset, -3200 + x_offset, -2350 + y_offset),
            (-3300 + x_offset, -2800 + y_offset, -3250 + x_offset, -2350 + y_offset),
        ],
        ('Gisborne','Watergardens'):[
            (-3300 + x_offset, -2400 + y_offset, -3200 + x_offset, -2350 + y_offset),
            (-3350 + x_offset, -1450 + y_offset, -3000 + x_offset, -1300 + y_offset), # Watergardens Coords
            (-3300 + x_offset, -2400 + y_offset, -3250 + x_offset, -1850 + y_offset),
            (-3300 + x_offset, -1700 + y_offset, -3250 + x_offset, -1450 + y_offset),
        ],
        ('Watergardens','Footscray'):[
            (-3300 + x_offset, -1300 + y_offset, -3250 + x_offset, 100 + y_offset),
            (-3300 + x_offset, 50 + y_offset, -2850 + x_offset, 100 + y_offset),
            (-2800 + x_offset, 50 + y_offset, -2650 + x_offset, 100 + y_offset),
            (-2600 + x_offset, 50 + y_offset, -600 + x_offset, 100 + y_offset),
            (-600 + x_offset, -200 + y_offset, -451 + x_offset, 149 + y_offset), # footscray station icon
            (-550 + x_offset, 100 + y_offset, -501 + x_offset, 249 + y_offset), # footscray station icon
            (-600 + x_offset, 200 + y_offset, -451 + x_offset, 349 + y_offset), # footscray station icon
            (-3350 + x_offset, -1450 + y_offset, -3000 + x_offset, -1300 + y_offset), # Watergardens Coords
        ],
        # echuca line
        ('Echuca','Rochester'):[
            (-350 + x_offset, -4100 + y_offset, -50 + x_offset, -3950 + y_offset),
        ],
        ('Rochester','Elmore'):[
            (-800 + x_offset, -4050 + y_offset, -300 + x_offset, -3950 + y_offset),
        ],
        ('Elmore','Goornong'):[
            (-1250 + x_offset, -4050 + y_offset, -750 + x_offset, -3950 + y_offset),
        ],
        ('Goornong','Huntly'):[
            (-1700 + x_offset, -4050 + y_offset, -1200 + x_offset, -3950 + y_offset),
        ],
        ('Huntly','Epsom'):[
            (-1950 + x_offset, -4050 + y_offset, -1650 + x_offset, -3950 + y_offset),
            (-2100 + x_offset, -4100 + y_offset, -1950 + x_offset, -3850 + y_offset), # epsom coords
        ],
        ('Epsom','Bendigo'):[
            (-2100 + x_offset, -4100 + y_offset, -1950 + x_offset, -3850 + y_offset), # epsom coords
            (-3350 + x_offset, -3850 + y_offset, -3100 + x_offset, -3700 + y_offset), # bendigo coords
            (-3100 + x_offset, -4050 + y_offset, -2100 + x_offset, -4000 + y_offset),
            (-3300 + x_offset, -4050 + y_offset, -3150 + x_offset, -4000 + y_offset),
            (-3300 + x_offset, -4050 + y_offset, -3250 + x_offset, -3850 + y_offset),
        ],
        ('Woodend','Macedon'):[
            (-3300 + x_offset, -2800 + y_offset, -3200 + x_offset, -2550 + y_offset),
        ],
        ('Macedon','Gisborne'):[
            (-3300 + x_offset, -2600 + y_offset, -3200 + x_offset, -2350 + y_offset),
        ],
        ('Gisborne','Riddells Creek'):[
            (-3300 + x_offset, -2400 + y_offset, -3200 + x_offset, -2150 + y_offset),
        ],
        ('Riddells Creek','Clarkefield'):[
            (-3300 + x_offset, -2200 + y_offset, -3200 + x_offset, -1950 + y_offset),
        ],
        ('Clarkefield','Sunbury'):[
            (-3300 + x_offset, -2000 + y_offset, -3200 + x_offset, -1850 + y_offset),
            (-3350 + x_offset, -1850 + y_offset, -3000 + x_offset, -1700 + y_offset), # Sunbury Coords
        ],
        ('Sunbury','Watergardens'):[
            (-3300 + x_offset, -1700 + y_offset, -3250 + x_offset, -1450 + y_offset),
            (-3350 + x_offset, -1850 + y_offset, -3000 + x_offset, -1700 + y_offset), # Sunbury Coords
            (-3350 + x_offset, -1450 + y_offset, -3000 + x_offset, -1300 + y_offset), # Watergardens Coords
        ],
    },
    'ararat/maryborough_seperate':{
        #maryborough line
        ('Maryborough','Talbot'): [
            (-9150 + x_offset, -750 + y_offset, -9000 + x_offset, -500 + y_offset),
        ],
        ('Talbot','Clunes'): [
            (-9200 + x_offset, -550 + y_offset, -9000 + x_offset, -300 + y_offset),
        ],
        ('Clunes','Creswick'): [
            (-9100 + x_offset, -350 + y_offset, -9000 + x_offset, -100 + y_offset),
        ],
        ('Creswick','Ballarat'): [
            (-9100 + x_offset, -150 + y_offset, -9000 + x_offset, -100 + y_offset),
            (-9100 + x_offset, -150 + y_offset, -9050 + x_offset, 350 + y_offset),
            (-9100 + x_offset, 350 + y_offset, -8900 + x_offset, 400 + y_offset),
        ],
        # ararat line
        ('Ararat', 'Beaufort'):[
            (-10250 + x_offset, 300 + y_offset, -9950 + x_offset, 450 + y_offset),
        ],
        ('Beaufort','Wendouree'):[
            (-10000 + x_offset, 300 + y_offset, -9550 + x_offset, 400 + y_offset),
            (-9550 + x_offset, 200 + y_offset, -9400 + x_offset, 450 + y_offset), # wendouree coords
        ],
        ('Wendouree','Ballarat'):[
            (-9550 + x_offset, 200 + y_offset, -9400 + x_offset, 450 + y_offset), # wendouree coords
            (-9400 + x_offset, 350 + y_offset, -8900 + x_offset, 400 + y_offset),
            (-8900 + x_offset, 200 + y_offset, -8750 + x_offset, 450 + y_offset), # ballarat coords
        ],
        ('Ballarat','Ballan'):[
            (-8750 + x_offset, 300 + y_offset, -8400 + x_offset, 400 + y_offset),
            (-8900 + x_offset, 200 + y_offset, -8750 + x_offset, 450 + y_offset), # ballarat coords
        ],
        ('Ballan','Bacchus Marsh'):[
            (-8450 + x_offset, 300 + y_offset, -7850 + x_offset, 400 + y_offset),
        ],
        ('Bacchus Marsh', 'Melton'):[
            (-7900 + x_offset, 300 + y_offset, -7300 + x_offset, 400 + y_offset),
        ],
        ('Melton', 'Cobblebank'):[
            (-7350 + x_offset, 300 + y_offset, -6800 + x_offset, 400 + y_offset),
        ],
        ('Cobblebank','Rockbank'):[
            (-6850 + x_offset, 300 + y_offset, -6250 + x_offset, 400 + y_offset),
        ],
        ('Rockbank', 'Caroline Springs'):[
            (-6300 + x_offset, 300 + y_offset, -5600 + x_offset, 400 + y_offset),
        ],
        ('Caroline Springs', 'Deer Park'):[
            (-5650 + x_offset, 300 + y_offset, -4950 + x_offset, 400 + y_offset),
            (-4950 + x_offset, 200 + y_offset, -4800 + x_offset, 650 + y_offset), # deer park coords
        ],
        ('Deer Park','Ardeer'):[
            (-4800 + x_offset, 300 + y_offset, -3900 + x_offset, 400 + y_offset),
            (-3950 + x_offset, 300 + y_offset, -3550 + x_offset, 400 + y_offset),
        ],
        ('Ardeer', 'Sunshine'):[
            (-3950 + x_offset, 300 + y_offset, -3550 + x_offset, 400 + y_offset),
            (-3550 + x_offset, 300 + y_offset, -2900 + x_offset, 400 + y_offset),
            (-2900 + x_offset, -200 + y_offset, -2750 + x_offset, -50 + y_offset), # Sunshine Coords
            (-2850 + x_offset, -80 + y_offset, -2800 + x_offset, 220 + y_offset), # Sunshine Coords
            (-2900 + x_offset, 220 + y_offset, -2750 + x_offset, 550 + y_offset), # Sunshine Coords 
        ],
        ('Sunshine','Footscray'):[
            (-2750 + x_offset, 350 + y_offset, -2650 + x_offset, 400 + y_offset),
            (-2600 + x_offset, 350 + y_offset, -2450 + x_offset, 400 + y_offset),
            (-2500 + x_offset, 50 + y_offset, -2450 + x_offset, 400 + y_offset),
            (-2500 + x_offset, 50 + y_offset, -600 + x_offset, 100 + y_offset),
            (-2900 + x_offset, -200 + y_offset, -2750 + x_offset, -50 + y_offset), # Sunshine Coords
            (-2850 + x_offset, -80 + y_offset, -2800 + x_offset, 220 + y_offset), # Sunshine Coords
            (-2900 + x_offset, 220 + y_offset, -2750 + x_offset, 550 + y_offset), # Sunshine Coords 
            (-600 + x_offset, -200 + y_offset, -451 + x_offset, 149 + y_offset), # footscray station icon
            (-550 + x_offset, 100 + y_offset, -501 + x_offset, 249 + y_offset), # footscray station icon
            (-600 + x_offset, 200 + y_offset, -451 + x_offset, 349 + y_offset), # footscray station icon
        ],
        ('Footscray', 'Southern Cross'):[
            (-600 + x_offset, -200 + y_offset, -451 + x_offset, 149 + y_offset), # footscray station icon
            (-550 + x_offset, 100 + y_offset, -501 + x_offset, 249 + y_offset), # footscray station icon
            (-600 + x_offset, 200 + y_offset, -451 + x_offset, 349 + y_offset), # footscray station icon
            (-450 + x_offset, 50 + y_offset, 1500 + x_offset, 100 + y_offset),
            (1450 + x_offset, 50 + y_offset, 1500 + x_offset, 400 + y_offset),
            (1450 + x_offset, 450 + y_offset, 1500 + x_offset, 900 + y_offset),
            (1450 + x_offset, 850 + y_offset, 1800 + x_offset, 900 + y_offset),
            (1750 + x_offset, 900 + y_offset, 1800 + x_offset, 1250 + y_offset),
            (1200 + x_offset, 1250 + y_offset, 2349 + x_offset, 1399 + y_offset), # Southern 
        ],
    },
    'heritage':{
        ('Belgrave', 'Selby'):[
            (11550 + x_offset, -1450 + y_offset, 11750 + x_offset, -1350 + y_offset),
            (11400 + x_offset, -1450 + y_offset, 11550 + x_offset, -1200 + y_offset), #belgrave coords
        ],
        ('Selby', 'Menzies Creek'):[
            (11700 + x_offset, -1450 + y_offset, 12250 + x_offset, -1350 + y_offset),
        ],
        ('Menzies Creek', 'Clematis'):[
            (12200 + x_offset, -1450 + y_offset, 12850 + x_offset, -1350 + y_offset),
        ],
        ('Clematis', 'Emerald'):[
            (12800 + x_offset, -1450 + y_offset, 13300 + x_offset, -1350 + y_offset),
        ],
        ('Emerald', 'Nobelius'):[
            (13250 + x_offset, -1450 + y_offset, 13750 + x_offset, -1350 + y_offset),
        ],
        ('Nobelius', 'Nobelius Siding'):[
            (13700 + x_offset, -1450 + y_offset, 14350 + x_offset, -1350 + y_offset),
        ],
        ('Nobelius Siding', 'Lakeside'):[
            (14300 + x_offset, -1450 + y_offset, 14950 + x_offset, -1350 + y_offset), 
        ],
        ('Lakeside', 'Wright'):[
            (14900 + x_offset, -1450 + y_offset, 15350 + x_offset, -1350 + y_offset),
        ],
        ('Wright', 'Cockatoo'):[
            (15300 + x_offset, -1450 + y_offset, 15800 + x_offset, -1350 + y_offset),
        ],
        ('Cockatoo', 'Fielder'):[
            (15750 + x_offset, -1450 + y_offset, 16250 + x_offset, -1350 + y_offset),
        ],
        ('Fielder', 'Gembrook'):[
            (16200 + x_offset, -1450 + y_offset, 16450 + x_offset, -1300 + y_offset), 
        ],
        ('Healesville', 'Tunnel Hill'):[
            (6450 + x_offset, -3350 + y_offset, 6600 + x_offset, -3150 + y_offset),
        ],
        ('Bullarto', 'Passing Clouds'):[
            (-6950 + x_offset, -3000 + y_offset, -6500 + x_offset, -2800 + y_offset),
        ],
        ('Passing Clouds', 'Musk'):[
            (-7450 + x_offset, -2950 + y_offset, -6900 + x_offset, -2850 + y_offset),
        ],
        ('Musk', 'Daylesford'):[
            (-7650 + x_offset, -2950 + y_offset, -7400 + x_offset, -2800 + y_offset),
        ],
        ('Moorooduc', 'Tanti Park'):[
            (4100 + x_offset, 9000 + y_offset, 4450 + x_offset, 9150 + y_offset),
        ],
        ('Tanti Park', 'Narambi Road'):[
            (3500 + x_offset, 9000 + y_offset, 4150 + x_offset, 9100 + y_offset), 
        ],
        ('Narambi Road', 'Stopping Place 16'):[
            (2750 + x_offset, 9000 + y_offset, 3550 + x_offset, 9100 + y_offset),
        ],
        ('Stopping Place 16', 'Mornington'):[
            (2300 + x_offset, 9000 + y_offset, 2800 + x_offset, 9150 + y_offset),
        ],
        ('Castlemaine', 'Muckleford'):[
            (-3650 + x_offset, -3300 + y_offset, -3350 + x_offset, -3150 + y_offset),
            (-3450 + x_offset, -3450 + y_offset, -3100 + x_offset, -3300 + y_offset), # castlemaine coords
        ],
        ('Muckleford', 'Maldon'):[
            (-4000 + x_offset, -3300 + y_offset, -3600 + x_offset, -3150 + y_offset),
        ],
        ('Thomson', 'Winter Platform'):[
            (20950 + x_offset, 3650 + y_offset, 21100 + x_offset, 3900 + y_offset),
        ],
        ('Winter Platform', 'Cascade Bridge Halt'):[
            (20950 + x_offset, 3450 + y_offset, 21050 + x_offset, 3700 + y_offset),
        ],
        ('Cascade Bridge Halt', 'Happy Creek'):[
            (20950 + x_offset, 3250 + y_offset, 21050 + x_offset, 3500 + y_offset),
        ],
        ('Happy Creek', 'Walhalla'):[
            (20950 + x_offset, 3050 + y_offset, 21100 + x_offset, 3300 + y_offset),
        ],
        ('Drysdale', 'Suma Park'):[
            (-4450 + x_offset, 2250 + y_offset, -4200 + x_offset, 2400 + y_offset),
        ],
        ('Suma Park', "Laker's Siding"):[
            (-4250 + x_offset, 2250 + y_offset, -3600 + x_offset, 2350 + y_offset),
        ],
        ("Laker's Siding", 'Swan Bay'):[
            (-3650 + x_offset, 2250 + y_offset, -3000 + x_offset, 2350 + y_offset),
        ],
        ('Swan Bay', 'Queenscliff'):[
            (-3050 + x_offset, 2250 + y_offset, -2750 + x_offset, 2400 + y_offset),
        ],
    },
}

def getTotalLines_post_munnel():
    total_lines = 0
    for line_type in line_coordinates.values():
        for station_pair in line_type.values():
            total_lines += len(station_pair)
    return total_lines

print(getTotalLines_post_munnel())