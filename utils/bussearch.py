import discord
import csv
import requests
from google.transit import gtfs_realtime_pb2
from dotenv import *
from datetime import datetime
import os

from utils.trainImage import getImage

config = dotenv_values(".env")
TRANSPORT_VIC_API_KEY = config['TRANSPORT_VIC_API_KEY']

async def search(bus, ctx):
    if bus[0] == "D":
        buss = bus[1:]
        data = getfleetsnumber(buss, "Dysons")
    elif bus[:2] == "SK":
        buss = bus[2:]
        data = getfleetsnumber(buss, "Skybus")
    elif bus[:2] == "TS":
        buss = bus[2:]
        data = getfleetsnumber(buss, "Transit Systems")
    elif bus[:2] == "MK":
        buss = bus[2:]
        data = getfleetsnumber(buss, "McKenzies")
    elif bus[:2] == "CH":
        buss = bus[2:]
        data = getfleetsnumber(buss, "Christians")
    elif bus[:2] == "CR":
        buss = bus[2:]
        data = getfleetsnumber(buss, "Cranbourne")
    elif bus[0] == "S":
        buss = bus[1:]
        data = getfleetsnumber(buss, "Sunbury")
    elif bus[:2] == "MT":
        buss = bus[2:]
        data = getfleetsnumber(buss, "Martyrs")
    elif bus[0] == "V":
        buss = bus[1:]
        data = getfleetsnumber(buss, "Ventura")
    elif bus[0] == "K":
        buss = bus[1:]
        data = getfleetsnumber(buss, "Kinetic")
    elif bus[0] == "C":
        buss = bus[1:]
        data = getfleetsnumber(buss, "CDC")
    elif len(bus) == 6:
        data = getfleets(bus)
    else:
        return "n"
    
    try:
        plate = data[1]
    except:
        return
    if data[2] == 'Dysons':
        embed=discord.Embed(title=f"{data[0]} ({data[1]})", color=discord.Color.green())
    elif data[2] == 'Ventura':
        embed=discord.Embed(title=f"{data[0]} ({data[1]})", color=discord.Color.yellow())
    elif data[2] == 'Kinetic':
        embed=discord.Embed(title=f"{data[0]} ({data[1]})", color=discord.Color.blue())
    elif data[2] == 'CDC':
        embed=discord.Embed(title=f"{data[0]} ({data[1]})", color=discord.Color.orange())
    elif data[2] == 'Transit Systems':
        embed=discord.Embed(title=f"{data[0]} ({data[1]})", color=discord.Color.dark_green())
    elif data[2] == 'Skybus':
        embed=discord.Embed(title=f"{data[0]} ({data[1]})", color=discord.Color.red())
    elif data[2] == 'McKenzies':
        embed=discord.Embed(title=f"{data[0]} ({data[1]})", color=0x47A04E)
    elif data[2] == 'Christians':
        embed=discord.Embed(title=f"{data[0]} ({data[1]})", color=0x1464cc)
    elif data[2] == 'Cranbourne':
        embed=discord.Embed(title=f"{data[0]} ({data[1]})", color=0x2a2880)
    elif data[2] == 'Sunbury':
        embed=discord.Embed(title=f"{data[0]} ({data[1]})", color=0xD9001B)
    elif data[2] == 'Martyrs':
        embed=discord.Embed(title=f"{data[0]} ({data[1]})", color=0x006cb7)
    else:
        embed=discord.Embed(title=f"{data[0]} ({data[1]})", color=discord.Color.light_gray())
    embed.add_field(name="Depot", value=data[7], inline=True)
    embed.add_field(name="Operator", value=data[2], inline=True)
    embed.add_field(name="Body", value=data[4], inline=False)
    embed.add_field(name="Chassis", value=data[3], inline=False)
    embed.add_field(name="Body Date", value=data[5], inline=False)
    embed.add_field(name="Livery", value=data[6], inline=False)
    if data[7] == "":
        embed.add_field(name="Myki generation", value="Not recorded", inline=False)
    else:
        embed.add_field(name="Myki generation", value=data[8], inline=False)
    output = bustracker(plate)
    if output:
        current_time = datetime.now()
        date = f"{current_time.year}{current_time.month:02}{current_time.day:02}"
        tripinfo = ""
        for trip in output:
            tripinfo += f"Trip ID: [{trip['trip_id']}](<https://anytrip.com.au/region/vic?selectedTrip=tripInstance%2F{date}%2Fau3:ad:{trip['trip_id']}%2F0>) \n"
            tripinfo += f"Route: {trip['route_id']} \n"
        embed.add_field(name="Current trip(s)", value=tripinfo,inline=False)
    embed.add_field(name="Deloyments", value=f"[transportvic.me](<https://transportvic.me/bus/tracker/fleet?fleet={bus}>)", inline=False)
    
    # get photo
    image, credits = getImage(plate, False, 'bus')
    if image:
        embed.set_image(url=image)
        embed.set_footer(text=f'Photo by {credits}')
    return embed
    

from staticmap import StaticMap, IconMarker
def makemap(longitude,latitude,name):
    print('started map gen')
    m = StaticMap(1024, 1024, 12, url_template='https://tile.openstreetmap.org/{z}/{x}/{y}.png')
    print('created base map')
    icon_train = IconMarker((longitude, latitude), './utils/bus.png', 25, 25)
    m.add_marker(icon_train)
    print('added marker')
    image = m.render(zoom=14)
    image.save(f'temp/{name}-map.png')
    print('saved map')

def bustracker(plate):
    stops = []
    # GTFS-R endpoint for trams
    url = "https://api.opendata.transport.vic.gov.au/opendata/public-transport/gtfs/realtime/v1/bus/vehicle-positions"
    headers = {
        "KeyId": TRANSPORT_VIC_API_KEY
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(response.content)
        with open("recentsave.txt", "w") as file:
            file.write(str(feed.entity))
        for entity in feed.entity:
            if entity.HasField("vehicle"):
                vehicle = entity.vehicle
                busplate = vehicle.vehicle.id
                route_id = vehicle.trip.route_id
                trip_id = vehicle.trip.trip_id
                if busplate == plate:
                    location = f"{vehicle.position.latitude},{vehicle.position.longitude}"
                    stops.append({
                        "trip_id": trip_id,
                        "location": location,
                        "route_id": route_id,
                    })
        return stops
                    
    else:
        print(f"Error: {response.status_code}")

def getfleets(numberplate):
    with open("utils/bussets.csv", "r", encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if row[1] == numberplate:
                return row[0],row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8] #busnumber, rego, operator, chassis, body, date, livery, depot, myki

def getfleetsnumber(fleetnumber, operator):
    with open("utils/bussets.csv", "r") as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if row[0] == fleetnumber and row[2] == operator:
                return row[0],row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]