'''TrackPulse 𝕍𝕀ℂ
    Copyright (C) 2024  Billy Evans

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.'''


import operator
from shutil import ExecError
from tracemalloc import stop
from cycler import V
from discord.ext import commands, tasks
from discord import app_commands
import discord
import json
import requests
import re
import asyncio
import threading
import queue
from datetime import datetime
import time
import csv
import random
import pandas as pd
from typing import Literal, Optional
import typing
import enum
from re import A
from io import StringIO
import numpy as np
import io

from utils import trainset
from utils.search import *
from utils.colors import *
from utils.stats import *
from utils.pageScraper import *
from utils.trainImage import *
from utils.checktype import *
from utils.rareTrain import *
from utils.montagueAPI import *
from utils.map.map import *
from utils.game.lb import *
from utils.trainlogger.main import *
from utils.trainset import *
from utils.trainlogger.stats import *
from utils.trainlogger.ids import *
from utils.unixtime import *
from utils.pastTime import *
from utils.routeName import *
from utils.trainlogger.graph import *
from utils.locationFromNumber import *
from utils.photo import *
from utils.plane.main import *

print("""TrackPulse VIC Copyright (C) 2024  Billy Evans
    This program comes with ABSOLUTELY NO WARRANTY.
    This is free software, and you are welcome to redistribute it
    under certain conditions""")

file = open('utils\\stations.txt','r')
stations_list = []
for line in file:
    line = line.strip()
    stations_list.append(line)
file.close()

file = open('utils\\busOps.txt','r')
busOps = []
for line in file:
    line = line.strip()
    busOps.append(line)
file.close()




rareCheckerOn = False
lineStatusOn = False

# Global variable to keep track of the last sent message
last_message = None
comeng_last_message = None
last_message_metro = None
comeng_last_message_metro = None
last_message_vline = None
comeng_last_message_vline = None

# ENV READING
config = dotenv_values(".env")

BOT_TOKEN = config['BOT_TOKEN']
STARTUP_CHANNEL_ID = int(config['STARTUP_CHANNEL_ID']) # channel id to send the startup message
RARE_SERVICE_CHANNEL_ID = int(config['RARE_SERVICE_CHANNEL_ID'])
COMMAND_PREFIX = config['COMMAND_PREFIX']
USER_ID = config['USER_ID']

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=discord.Intents.all())
log_channel = bot.get_channel(STARTUP_CHANNEL_ID)

channel_game_status = {} #thing to store what channels are running the guessing game

try:    
    os.mkdir('utils/game/scores')
except FileExistsError as e:
    print(e)    

# Group commands
class CommandGroups(app_commands.Group):
    ...

trainlogs = CommandGroups(name='logs')
games = CommandGroups(name='games')
search = CommandGroups(name='search')
stats = CommandGroups(name='stats')
flight = CommandGroups(name='flight')

@bot.event
async def on_ready():
    print("Bot started")
    channel = bot.get_channel(STARTUP_CHANNEL_ID)

    bot.tree.add_command(trainlogs)
    bot.tree.add_command(games)
    bot.tree.add_command(search)
    bot.tree.add_command(stats)
    bot.tree.add_command(flight)


    await channel.send(f"""TrackPulse 𝕍𝕀ℂ Copyright (C) 2024  Billy Evans
    This program comes with ABSOLUTELY NO WARRANTY.
    This is free software, and you are welcome to redistribute it
    under certain conditions\n<@{USER_ID}> Bot is online!""")
    try:
        task_loop.start()
    except:
        print("WARNING: Rare train checker is not enabled!")
        await channel.send(f"WARNING: Rare train checker is not enabled! <@{USER_ID}>")

# Threads

# Rare train finder
def check_rare_trains_in_thread():
    rare_trains = checkRareTrainsOnRoute()
    asyncio.run_coroutine_threadsafe(log_rare_trains(rare_trains), bot.loop)

async def log_rare_trains(rare_trains):
    log_channel = bot.get_channel(RARE_SERVICE_CHANNEL_ID)
    channel = bot.get_channel(RARE_SERVICE_CHANNEL_ID)

    if rare_trains:
        embed = discord.Embed(title="Trains found on lines they are not normally on!", color=0xf23f42)

        for route in rare_trains:
            parts = route.split(' - Train ')
            route_name = parts[0]
            train_type = parts[1]
            
            # Extract the train name and train info from train_type
            train_name, train_info = train_type.split('\n') if '\n' in train_type else ('Unknown train name', 'Unknown train type')

            embed.add_field(name=route_name, value=f"{train_name}\n{train_info}", inline=True)

        try:
            await channel.send(embed=embed)
            with open('logs.txt', 'a') as file:
                file.write(f"Sent rare trains")
        except discord.HTTPException:
            await channel.send("Embed too big! There are many trains on the wrong line. Check ANYTRIP.")
            with open('logs.txt', 'a') as file:
                file.write(f"Sent rare trains but it was too long")
        await channel.send('<@&1227171023795781694> Trains found on lines they are not normally on!\n`Due to errors in the PTV api data out of our control, some data may be inaccurate.`')
    else:
        await log_channel.send("None found")

def check_lines_in_thread():
    asyncio.run_coroutine_threadsafe(checklines(), bot.loop)

async def checklines():
        global last_message  # Referencing the global variable
        global comeng_last_message  # Referencing the global variable
        global last_message_metro  # Referencing the global variable
        global comeng_last_message_metro  # Referencing the global variable
        global last_message_vline  # Referencing the global variable
        global comeng_last_message_vline  # Referencing the global variable

        statuses = [f'{datetime.now()}']
        log_channel = bot.get_channel(int(config['STARTUP_CHANNEL_ID']))

        if lineStatusOn:
            await log_channel.send('Loading line status...')

            embed_metro = discord.Embed(title=f'<:train:1241164967789727744> Metro Trains Melbourne', color=0x008dd0)
            #embed_metro = discord.Embed(title=f'Line status - {convert_to_unix_time(datetime.now())}', color=0x008dd0)

            lines = ['Alamein','Belgrave','Craigieburn','Cranbourne','Mernda','Frankston','Glen%20Waverley','Hurstbridge','Lilydale','Pakenham','Sandringham','Stony%20Point','Sunbury','Upfield','Werribee','Williamstown',]

            for line in lines:
                json_info_str = route_api_request(line, "0")
                json_info_str = json_info_str.replace("'", "\"")  # Replace single quotes with double quotes
                json_info = json.loads(json_info_str)
                
                routes = json_info['routes']
                status = json_info['status']
                version = status['version']
                health = status['health']
                
                route = routes[0]
                route_service_status = route['route_service_status']
                description = route_service_status['description']
                timestamp = route_service_status['timestamp']
                route_type = route['route_type']
                route_id = route['route_id']
                route_name = route['route_name']
                route_number = route['route_number']
                route_gtfs_id = route['route_gtfs_id']
                geopath = route['geopath']
                
                print(f"route id: {route_id}")
                
                if description == "Service Information":
                        description = "Good Service"
                
                # disruption info
                disruptionDescription = ""
                try:
                    # print(disruption_api_request(route_id))
                    disruptions = disruption_api_request(route_id)
                    print(disruptions)
                    
                    # Extracting title and description
                    general_disruption = disruptions["disruptions"]["metro_train"][0]
                    disruptionTitle = general_disruption["title"]
                    disruptionDescription = general_disruption["description"]
                            
                except Exception as e:
                    print(e)

                color = genColor(description)
                print(f"Status color: {color}")
            
                info = f'{description}'
                embed_metro.add_field(name=f'{route_name}', value=f'{statusEmoji(description)} {info}', inline=True)
                statuses.append(description)
                # if disruptionDescription:
                #     embed_metro.add_field(name="Disruption Info",value=disruptionDescription, inline=False) h

            embed_vline = discord.Embed(title=f'<:vline:1241165814258729092> V/Line', color=0x7f3e98)
            lines = ['Geelong - Melbourne','Warrnambool - Melbourne via Apollo Bay & Geelong','Ballarat-Wendouree - Melbourne via Melton','Ararat - Melbourne via Ballarat','Maryborough - Melbourne via  Ballarat','Bendigo - Melbourne via Gisborne','Echuca-Moama - Melbourne via Bendigo or Heathcote','Swan Hill - Melbourne via Bendigo','Seymour - Melbourne via Broadmeadows','Shepparton - Melbourne via Seymour','Albury - Melbourne via Seymour','Traralgon - Melbourne via Morwell & Moe & Pakenham','Bairnsdale - Melbourne via Sale & Traralgon']
            for line in lines:
                line = line.replace(" ","%20")
                json_info_str = route_api_request(line, "3")
                json_info_str = json_info_str.replace("'", "\"")  # Replace single quotes with double quotes
                json_info = json.loads(json_info_str)
                
                routes = json_info['routes']
                status = json_info['status']
                version = status['version']
                health = status['health']
                
                route = routes[0]
                route_service_status = route['route_service_status']
                description = route_service_status['description']
                timestamp = route_service_status['timestamp']
                route_type = route['route_type']
                route_id = route['route_id']
                route_name = route['route_name']
                route_number = route['route_number']
                route_gtfs_id = route['route_gtfs_id']
                geopath = route['geopath']
                
                print(f"route id: {route_id}")

                route_name = route_name.replace("Geelong - Melbourne","Geelong")
                route_name = route_name.replace("Warrnambool - Melbourne via Apollo Bay & Geelong","Warrnambool")
                route_name = route_name.replace("Ballarat-Wendouree - Melbourne via Melton","Ballarat")
                route_name = route_name.replace("Ararat - Melbourne via Ballarat","Ararat")
                route_name = route_name.replace("Maryborough - Melbourne via  Ballarat","Maryborough")
                route_name = route_name.replace("Bendigo - Melbourne via Gisborne","Bendigo")
                route_name = route_name.replace("Echuca-Moama - Melbourne via Bendigo or Heathcote","Echuca")
                route_name = route_name.replace("Swan Hill - Melbourne via Bendigo","Swan Hill")
                route_name = route_name.replace("Seymour - Melbourne via Broadmeadows","Seymour")
                route_name = route_name.replace("Shepparton - Melbourne via Seymour","Shepparton")
                route_name = route_name.replace("Albury - Melbourne via Seymour","Albury")
                route_name = route_name.replace("Traralgon - Melbourne via Morwell & Moe & Pakenham","Traralgon")
                route_name = route_name.replace("Bairnsdale - Melbourne via Sale & Traralgon","Bairnsdale")
                
                
                # disruption info
                disruptionDescription = ""
                try:
                    # print(disruption_api_request(route_id))
                    disruptions = disruption_api_request(route_id)
                    print(disruptions)
                    
                    # Extracting title and description
                    general_disruption = disruptions["disruptions"]["regional_train"][0]
                    disruptionTitle = general_disruption["title"]
                    disruptionDescription = general_disruption["description"]

                    #Extracting the true description for V/Line Rail Distruptions
                    disruption_vline = general_disruption["disruption_type"]
                    currentness = general_disruption["disruption_status"]

                    if currentness == "Planned":
                        disruption_vline = "Good Service"
                    
                    if disruption_vline == "Service Information":
                        disruption_vline = "Good Service"

                            
                except Exception as e:
                    print(e)

                color = genColor(disruption_vline)
                print(f"Status color: {color}")
            
                info = f'{disruption_vline}'
                embed_vline.add_field(name=f'{route_name}', value=f'{statusEmoji(disruption_vline)} {info}', inline=True)
                statuses.append(disruption_vline)
                # if disruptionDescription:
                #     embed_vline.add_field(name="Disruption Info",value=disruptionDescription, inline=False) h

            try:
                if last_message:  # Check if there is a message to delete
                    print(f"Attempting to delete message ID: {last_message.id}")
                    await last_message.delete()
                    await comeng_last_message.delete()
                    await last_message_metro.delete()
                    await comeng_last_message_metro.delete()
                    await last_message_vline.delete()
                    await comeng_last_message_vline.delete()
                    print("Message deleted successfully")
            except Exception as e:
                print(f'Failed to delete the old message: {e}')

            comeng_channel = bot.get_channel(int(config['LINE_STATUS_2_CHANNEL_ID']))
            print(comeng_channel)
            send_channel = bot.get_channel(int(config['LINE_STATUS_CHANNEL_ID']))
            print(send_channel)
            
            if send_channel is None:
                print("ERROR: send_channel is None. Check the channel ID and ensure the bot has access to the channel.")
            if comeng_channel is None:
                print("ERROR: comeng_channel is None. Check the channel ID and ensure the bot has access to the channel.")
            
            try:
                last_message= await send_channel.send(f'# Line status - {convert_to_unix_time(datetime.now())}')
                comeng_last_message= await comeng_channel.send(f'# Line status - {convert_to_unix_time(datetime.now())}')    
                last_message_metro = await send_channel.send(embed=embed_metro)
                comeng_last_message_metro = await comeng_channel.send(embed=embed_metro)
                last_message_vline = await send_channel.send(embed=embed_vline)
                comeng_last_message_vline = await comeng_channel.send(embed=embed_vline)
            except Exception as e:
                print(f'ERROR: {e}')

            with open('logs.txt', 'a') as file:
                        file.write(f"LINE STATUS CHECKED AUTOMATICALLY")
                        
            # save line status to csv            
            with open('utils/line-status-data.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(statuses)
                        

@tasks.loop(minutes=10)
async def task_loop():
    if rareCheckerOn:
        log_channel = bot.get_channel(RARE_SERVICE_CHANNEL_ID)
        await log_channel.send("Checking for trains on lines they aren't meant for")
        with open('logs.txt', 'a') as file:
            file.write(f"Checking for rare trains")

        # Create a new thread to run checkRareTrainsOnRoute
        thread = threading.Thread(target=check_rare_trains_in_thread)
        thread.start()
    else:
        print("Rare checker not enabled!")

@tasks.loop(minutes=15)
async def task_loop():
    # Create a new thread to run checkRareTrainsOnRoute
    thread = threading.Thread(target=check_lines_in_thread)
    thread.start()


# Help command
@bot.tree.command(name='help', description='Run help if you want to know about a command')
async def help(ctx):
    async def helper():
        generalCmds ="""</help:1261107050545549342> - Shows this command
</stats profile:1240101357847838815> - View your profile with various stats across your logs and game wins"""
        logCmds = """</logs add-train:1254387855820849154> - Add a train in Victoria you have been on, arguments: `line` - The line the train was on, `number` - The carrige number you went on (the full set will autofill), `date` - will autofill to today if empty, `start` - station you got on at, `end` - station you got off at, `traintype` - type of train, will autofill if train number entered.
</logs add-sydney-train:1254387855820849154> - same as above but for trains in NSW
</logs add-tram:1254387855820849154> - same as above but for trams in Melbourne
</logs add-sydney-tram:1254387855820849154> - same as above but for light rail in Sydney

</logs view:1254387855820849154> - view your logs
</logs delete:1254387855820849154> - delete one of your logs, leave id blank to delete the last log from the selected mode. The id can be seen with </logs view:1254387855820849154>
</logs stats:1254387855820849154> - view various stats and graphs from your logged trips."""
        searchCmds = """</search train:1240101357847838814> - Input a carriage number to see info about it, such as it's type, next services, livery and more!
</search departures:1240101357847838814> - View the next 9 Metro and 3 V/Line departures for a station
</search metro-line:1240101357847838814> - View disruptions for a Metro Trains line
</search route:1240101357847838814> - View disruptions for a tram or bus route"""
        await ctx.response.send_message(f"# Command help\n{generalCmds}\n## Log Commands\n{logCmds}\n## Search commands\n{searchCmds}")
    asyncio.create_task(helper())

    

    
@search.command(name="metro-line", description="Show info about a Metro line")
@app_commands.describe(line="What Metro line to show info about?")
@app_commands.choices(
    line=[
        app_commands.Choice(name="Alamein", value="Alamein"),
        app_commands.Choice(name="Belgrave", value="Belgrave"),
        app_commands.Choice(name="Craigieburn", value="Craigieburn"),
        app_commands.Choice(name="Cranbourne", value="Cranbourne"),
        app_commands.Choice(name="Frankston", value="Frankston"),
        app_commands.Choice(name="Glen Waverley", value="Glen%20Waverley"),
        app_commands.Choice(name="Hurstbridge", value="Hurstbridge"),
        app_commands.Choice(name="Lilydale", value="Lilydale"),
        app_commands.Choice(name="Mernda", value="Mernda"),
        app_commands.Choice(name="Pakenham", value="Pakenham"),
        app_commands.Choice(name="Sandringham", value="Sandringham"),
        app_commands.Choice(name="Stony Point", value="Stony%20Point"),
        app_commands.Choice(name="Sunbury", value="Sunbury"),
        app_commands.Choice(name="Upfield", value="Upfield"),
        app_commands.Choice(name="Werribee", value="Werribee"),
    ]
)
async def line_info(ctx, line: str):
    """
    This function retrieves information about a Metro line and sends it as an embed to the Discord channel.

    Args:
        ctx (ApplicationContext): The context of the command.
        line (str): The name of the Metro line to retrieve information about.

    Returns:
        None
    """
    # Retrieve line information from API
    json_info_str = route_api_request(line, "0")
    json_info_str = json_info_str.replace("'", "\"")  # Replace single quotes with double quotes
    json_info = json.loads(json_info_str)

    routes = json_info["routes"]
    status = json_info["status"]
    version = status["version"]
    health = status["health"]

    route = routes[0]
    route_service_status = route["route_service_status"]
    description = route_service_status["description"]
    timestamp = route_service_status["timestamp"]
    route_type = route["route_type"]
    route_id = route["route_id"]
    route_name = route["route_name"]
    route_number = route["route_number"]
    route_gtfs_id = route["route_gtfs_id"]
    geopath = route["geopath"]

    print(f"route id: {route_id}")

    # Retrieve disruption information
    disruption_description = ""
    try:
        disruptions = disruption_api_request(route_id)
        print(disruptions)

        # Extracting title and description
        general_disruption = disruptions["disruptions"]["metro_train"][0]
        disruption_title = general_disruption["title"]
        disruption_description = general_disruption["description"]

    except Exception as e:
        print(e)

    # Determine the color of the embed based on the status description
    color = genColor(description)
    print(f"Status color: {color}")

    # Create the embed with the retrieved information
    embed = discord.Embed(title=f"Route Information - {route_name}", color=color)
    embed.add_field(name="Route Name", value=route_name, inline=False)
    embed.add_field(name="Status Description", value=description, inline=False)
    if disruption_description:
        embed.add_field(name="Disruption Info", value=disruption_description, inline=False)

    # Send the embed to the Discord channel
    await ctx.response.send_message(embed=embed)

    # Log the command usage
    with open("logs.txt", "a") as file:
        file.write(
            f"\n{datetime.datetime.now()} - user sent line info command with input {line}"
        )

# @bot.tree.command(name="vline-line", description="Show info about a V/Line line")
# @app_commands.describe(vline_line = "What V/Line line to show info about?")
# @app_commands.choices(vline_line=[
#         app_commands.Choice(name="Geelong", value="Geelong%20Melbourne"),
#         app_commands.Choice(name="Ballarat", value="Ballarat%20Melbourne"),
#         app_commands.Choice(name="Gippsland", value="Gippsland%20Melbourne"),
#         app_commands.Choice(name="Seymour", value="Seymour%20Melbourne"),

# ])

# async def vline_line_info(ctx, vline_line: str):
#     json_info_str = route_api_request(vline_line, "3")
#     json_info_str = json_info_str.replace("'", "\"")  # Replace single quotes with double quotes
#     json_info = json.loads(json_info_str)
    
#     routes = json_info['routes']
#     status = json_info['status']
#     version = status['version']
#     health = status['health']
    
#     route = routes[0]
#     route_service_status = route['route_service_status']
#     description = route_service_status['description']
#     timestamp = route_service_status['timestamp']
#     route_type = route['route_type']
#     route_id = route['route_id']
#     route_name = route['route_name']
#     route_number = route['route_number']
#     route_gtfs_id = route['route_gtfs_id']
#     geopath = route['geopath']

#     color = genColor(description)
#     print(f"Status color: {color}")
    
    
#     embed = discord.Embed(title=f"Route Information - {route_name}", color=color)
#     embed.add_field(name="Route Name", value=route_name, inline=False)
#     embed.add_field(name="Status Description", value=description, inline=False)
    
#     await ctx.response.send_message(embed=embed)

'''@search.command(name='api', description='Search the PTV api directly')
@app_commands.describe(query = "Search query", route_types='Refer to PTV api documentation for more information.') 
async def api(ctx, query: str, route_types:int=None):
    async def apisearch():
        print(f'user searching ptv api for {query}')
        file=f'temp/{ctx.user.id}-apiresponse.json'
        response = search_api_request(query)
        with open(file, "w") as file:
            file.write(format(response))

        print(f"String saved to {file}")
        await ctx.response.send_message(f'', file=discord.File(file))
    asyncio.create_task(apisearch())'''

        
@search.command(name="run", description="Show runs for a route")
@app_commands.describe(runid = "route id")
async def runs(ctx, runid: str):
    
    api_response = runs_api_request(runid)
    json_response = json.dumps(api_response)
    data = json.loads(json_response)

    # Extract relevant information from runs with vehicle data
    vehicle_data = []
    for run in data['runs']:
        if run['vehicle_position']:
            vehicle_info = {
                'run_id': run['run_id'],
                'latitude': run['vehicle_position']['latitude'],
                'longitude': run['vehicle_position']['longitude'],
                'direction': run['vehicle_position']['direction'],
                'operator': run['vehicle_descriptor']['operator'],
                'description': run['vehicle_descriptor']['description']
            }
            vehicle_data.append(vehicle_info)
    for vehicle_info in vehicle_data:
        print(vehicle_info)
    
    embed = discord.Embed(title=f"Route Information - ", color=0x0e66ad)
    for vehicle_info in vehicle_data:
        embed.add_field(name="Train type:", value=vehicle_info["description"], inline=False)    
    
    await ctx.response.send_message(embed=embed)
    with open('logs.txt', 'a') as file:
                file.write(f"\n{datetime.datetime.now()} - user sent run search command with input {runid}")
    
    
 


# # commend to show route types:
# @bot.tree.command(name="route_types", description="Show numbers for each route type")
# async def route_types(ctx):
#     embed = discord.Embed(title="Route type numbers")
#     embed.add_field(name="Metro Train", value="`0`")
#     embed.add_field(name="Tram",value="`1`")
#     embed.add_field(name="Bus",value="`2`")
#     embed.add_field(name="V/line Train",value="`3`")
#     embed.add_field(name="Night Bus",value="`4`")
#     await ctx.response.send_message(embed=embed)
    

# bus route search
'''@bot.tree.command(name="bus_route", description="Show info about a bus route")
@app_commands.describe(line = "What bus route to show info about?")


async def bus_route(ctx, line: str):
    try:
        json_info_str = route_api_request(line, "2")
        json_info_str = json_info_str.replace("'", "\"")  # Replace single quotes with double quotes
        json_info = json.loads(json_info_str)
        
        channel = ctx.channel
        await ctx.response.send_message(f"Results for {line}")
        # embed = discord.Embed(title=f"Bus routes matching `{line}`:", color=0xff8200)
        counter = 0
        for route in json_info['routes']:

            routes = json_info['routes']
            status = json_info['status']
            version = status['version']
            health = status['health']
        
        
            route = routes[counter]
            route_service_status = route['route_service_status']
            description = route_service_status['description']
            timestamp = route_service_status['timestamp']
            route_type = route['route_type']
            route_id = route['route_id']
            route_name = route['route_name']
            route_number = route['route_number']
            route_gtfs_id = route['route_gtfs_id']
            geopath = route['geopath']

            embed = discord.Embed(title=f"Bus route {route_number}:", color=0xff8200)
            embed.add_field(name="Route Name", value=f"{route_number} - {route_name}", inline=False)
            embed.add_field(name="Status Description", value=description, inline=False)

            await channel.send(embed=embed)
            print(f"sent route {route_name}")
            counter = counter + 1
    except Exception as e:
        await ctx.response.send_message(f"error:\n`{e}`\nMake sure you inputted a valid bus route number, otherwise, the bot is broken.")'''


# Route Seach v2
@search.command(name="route", description="Show info about a tram or bus route")
@app_commands.describe(rtype = "What type of transport is this route?")
@app_commands.choices(rtype=[
        app_commands.Choice(name="Tram", value="1"),
        # app_commands.Choice(name="Metro Train", value="0"),
        app_commands.Choice(name="Bus", value="2"),
        # app_commands.Choice(name="VLine Train", value="3"),
        app_commands.Choice(name="Night Bus", value="4"),
])
@app_commands.describe(number = "What route number to show info about?")

async def route(ctx, rtype: str, number: int):    
    try:
        json_info_str = route_api_request(number, rtype)
        json_info_str = json_info_str.replace("'", "\"")  # Replace single quotes with double quotes
        json_info = json.loads(json_info_str)
        
        channel = ctx.channel
        await ctx.response.send_message(f"Results for {number}:")
        # embed = discord.Embed(title=f"Bus routes matching `{line}`:", color=0xff8200)
        counter = 0
        for route in json_info['routes']:

            routes = json_info['routes']
            status = json_info['status']
            version = status['version']
            health = status['health']
        
        
            route = routes[counter]
            route_service_status = route['route_service_status']
            description = route_service_status['description']
            timestamp = route_service_status['timestamp']
            route_type = route['route_type']
            route_id = route['route_id']
            route_name = route['route_name']
            route_number = route['route_number']
            route_gtfs_id = route['route_gtfs_id']
            geopath = route['geopath']
            
             # disruption info
            disruptionDescription = ""
            try:
                disruptions = disruption_api_request(route_id)
                # print(disruptions)
                
                # Extracting title and description
                general_disruption = disruptions["disruptions"]["metro_bus"][0]
                disruptionTitle = general_disruption["title"]
                disruptionDescription = general_disruption["description"]


                
            except Exception as e:
                print(e)

            
            # disruption status:

             # Check if the route number is the one you want
            if route_number == str(number):
                # Create and send the embed only for the desired route number
                embed = discord.Embed(title=f"Route {route_number}:", color=getColor(rtype))
                embed.add_field(name="Route Name", value=f"{route_number} - {route_name}", inline=False)
                embed.add_field(name="Status Description", value=description, inline=False)
                if disruptionDescription:
                    embed.add_field(name="Disruption Info",value=disruptionDescription, inline=False)
                    
                await channel.send(embed=embed)
                with open('logs.txt', 'a') as file:
                    file.write(f"\n{datetime.datetime.now()} - user sent route search command with input {rtype}, {number}")
                                
            counter = counter + 1
                
    except Exception as e:
        await ctx.response.send_message(f"error:\n`{e}`\nMake sure you inputted a valid route number, otherwise, the bot is broken.")
        with open('logs.txt', 'a') as file:
                    file.write(f"\n{datetime.datetime.now()} - ERROR with user command - user sent route search command with input {rtype}, {number}")



# Photo search
@search.command(name="train-photo", description="Search for xm9g's railway photos")
@app_commands.describe(number="Carriage number", search_set="Search the full set instead of the train number")
async def line_info(ctx, number: str, search_set:bool):
    async def sendPhoto(photo_url):
        # Make a HEAD request to check if the photo exists
        URLresponse = requests.head(photo_url)
        print(URLresponse.status_code)
        if URLresponse.status_code == 200:
            await channel.send(photo_url)
            await channel.send(f'[Photo by {getPhotoCredits(search_query)}](<https://railway-photos.xm9g.xyz#:~:text={search_query}>)')
        else:
            mAdded = search_query+'M'
            # try with m added
            photo_url = f"https://railway-photos.xm9g.xyz/photos/{mAdded}.jpg"
            URLresponse = requests.head(photo_url)
            if URLresponse.status_code == 200:
                await channel.send(photo_url)
                for i in range(2,5):
                    photo_url = f"https://railway-photos.xm9g.xyz/photos/{mAdded}-{i}.jpg"
                    print(f"searching for other images for {mAdded}")
                    print(f"url: {photo_url}")
                    URLresponse = requests.head(photo_url)
                    if URLresponse.status_code == 200:
                        await channel.send(photo_url)
                        await channel.send(f'[Photo by {getPhotoCredits(f"{search_query}-{i}")}](<https://railway-photos.xm9g.xyz#:~:text={mAdded}>)')
                    else:
                        print("no other images found")
                        await channel.send(f"Photo not in xm9g database!")
                        break
            else:
                await channel.send(f"Photo not in xm9g database!")
                
            
            
        for i in range(2,5):
            photo_url = f"https://railway-photos.xm9g.xyz/photos/{search_query}-{i}.jpg"
            print(f"searching for other images for {search_query}")
            print(f"url: {photo_url}")
            URLresponse = requests.head(photo_url)
            if URLresponse.status_code == 200:
                await channel.send(photo_url)
                await channel.send(f'[Photo by {getPhotoCredits(f"{search_query}-{i}")}](<https://railway-photos.xm9g.xyz#:~:text={search_query}>)')
            else:
                print("no other images found")
                break
    
    # start of the thing
    channel = ctx.channel
    search_query = number.upper()
    photo_url = f"https://railway-photos.xm9g.xyz/photos/{search_query}.jpg"
    await ctx.response.send_message(f"Searching for `{search_query}`...")
    
    #get full set
    try:
        fullSet = setNumber(number).split("-")
    except:
        print(f'cannot get full set for {number}')
        search_set=False
                
    await sendPhoto(photo_url)
    
    if search_set:
        print(f'Searching full set: {fullSet}')
        if fullSet[0] != number:
            search_query=fullSet[0].upper()
            await ctx.channel.send(f'Photos for `{fullSet[0]}`')
            await sendPhoto(f"https://railway-photos.xm9g.xyz/photos/{fullSet[0]}.jpg")
        if fullSet[1] != number:
            search_query=fullSet[1].upper()
            await ctx.channel.send(f'Photos for `{fullSet[1]}`')
            await sendPhoto(f"https://railway-photos.xm9g.xyz/photos/{fullSet[1]}.jpg")
        if fullSet[2] != number:
            search_query=fullSet[2].upper()
            await ctx.channel.send(f'Photos for `{fullSet[2]}`')
            await sendPhoto(f"https://railway-photos.xm9g.xyz/photos/{fullSet[2]}.jpg")

    
    
            

# Wongm search
@search.command(name="wongm", description="Search Wongm's Rail Gallery")
@app_commands.describe(search="search")
async def line_info(ctx, search: str):
    channel = ctx.channel
    print(f"removing spaces in search {search}")
    spaces_removed = search.replace(' ', '%20')
    print(spaces_removed)
    url = f"https://railgallery.wongm.com/page/search/?s={spaces_removed}"
    await ctx.response.send_message(url)



# Train search
@search.command(name="train", description="Search for a specific Train")
@app_commands.describe(train="train")
async def train_search(ctx, train: str):
    await ctx.response.defer()
    # await ctx.response.send_message(f"Searching, trip data may take longer to send...")
    channel = ctx.channel
    type = trainType(train)
    set = setNumber(train.upper())
   
    print(f'set: {set}')
    print(f"TRAINTYPE {type}")
    if type is None:
        await channel.send("Train not found")
    else:
        embed = discord.Embed(title=f"Info for {train.upper()}:", color=0x0070c0)
        if set.endswith('-'):
            embed.add_field(name=type, value=set[:-1])
        else:
            embed.add_field(name=type, value=set)
        
        if train.upper() == "7005":  # Only old livery sprinter
            embed.set_thumbnail(url="https://xm9g.xyz/discord-bot-assets/MPTB/Sprinter-VLine.png")
        else:
            embed.set_thumbnail(url=getIcon(type))
        
        if type in ['HCMT', "X'Trapolis 100", 'Alstom Comeng', 'EDI Comeng', 'Siemens Nexas','VLocity', 'Sprinter', 'N Class']:
            information = trainData(set)
            print(information)
            infoData = f'**Livery:** {information[1]}\n**Status:** {information[3]}\n**Entered Service:** {information[2]}\n**Vicsig notes:** {information[4]}'
            if information[5]:
                infoData+=f'\n**Name:** {information[5]}'
                
            # thing if the user has been on
            def check_variable_in_csv(variable, file_path):
                if not os.path.exists(file_path):
                    print(f"The file {file_path} does not exist.")
                    return False

                with open(file_path, mode='r') as file:
                    csv_reader = csv.reader(file)
                    for row in csv_reader:
                        if row[1] == variable:
                            return True
                return False 
        
            fPath = f'utils/trainlogger/userdata/{ctx.user.name}.csv'
            trainridden = check_variable_in_csv(set, fPath)
            if trainridden:
                infoData +='\n\n✅ You have been on this train before'
                
            embed.add_field(name='Information', value=infoData)
        else:
            embed.add_field(name='Information', value='None available')
            
        
        embed.set_image(url=getImage(train.upper()))
        
        embed.add_field(name="Source:", value=f'[{getPhotoCredits(train.upper())} (Photo)](https://railway-photos.xm9g.xyz#:~:text={train.upper()}), [MPTG (Icon)](https://melbournesptgallery.weebly.com/melbourne-train-and-tram-fronts.html), [Vicsig (Other info)](https://vicsig.net)', inline=False)
        
        embed.add_field(name='<a:botloading2:1261102206468362381> Loading trip data', value='⠀')
        embed_update = await ctx.edit_original_response(embed=embed)
        
        # map thing
        mapEmbed = discord.Embed(title=f"{train}'s location")
        mapEmbed.add_field(name='<a:botloading2:1261102206468362381> Loading Map', value='⠀')
        mapEmbedUpdate = await ctx.channel.send(file=None, embed=mapEmbed)
        
        async def addmap():

                # Generate the map asynchronously
                
                
                # After map generation, send it
                if type == "HCMT": # because ptv api lists hcmts like "9005M-9905M" for some fucking reason
                    hcmtcar1 = set.split('-')
                    location = getTrainLocation(hcmtcar1[0]+'M')
                else:
                    location = getTrainLocation(set)
                url = convertTrainLocationToGoogle(location)
                try:
                    if location is not None:
                        for item in location:
                            latitude = item['vehicle_position']['latitude']
                            longitude = item['vehicle_position']['longitude']
                            geopath=''
                            # geopath = getGeopath(item["run_ref"])
                            # print(f'geopath: {geopath}')

                        await makeMapv2(latitude,longitude, train, geopath)  # Adjust this line to asynchronously generate the map
                except Exception as e:
                    await mapEmbedUpdate.delete()
                    await ctx.channel.send('No location data available.')
                    print(f'ErROR: {e}')
                    return
                file_path = f"temp/{train}-map.png"
                if os.path.exists(file_path):
                    # Delete the old message
                    await mapEmbedUpdate.delete()
                    
                    file = discord.File(file_path, filename=f"{train}-map.png")
                    
                    embed = discord.Embed(title=f"{train}'s location", url=url)
                    embed.remove_field(0)
                    embed.set_image(url=f'attachment://{train}-map.png')
                    embed.set_footer(text='Mapdata © OpenStreetMap contributors')
                
                    # Send a new message with the file and embed
                    await channel.send(file=file, embed=embed)
                else:
                    await mapEmbedUpdate.delete()
                    await ctx.channel.send(f"Error: Map file '{file_path}' not found.")
                    print(f"Error: Map file '{file_path}' not found.")
                    
        # Run transportVicSearch in a separate thread
        if type in ['HCMT', "X'Trapolis 100", 'Alstom Comeng', 'EDI Comeng', 'Siemens Nexas']:
            asyncio.create_task(addmap())
            loop = asyncio.get_event_loop()
            task = loop.create_task(transportVicSearch_async(ctx, train.upper(), embed, embed_update))
            await task
            
        else:
            embed.remove_field(3)
            await embed_update.edit(embed=embed)
            await mapEmbedUpdate.delete()
            await ctx.channel.send('Location info is only available for Metro services')
            
@search.command(name="tram", description="Search for a specific Tram")
@app_commands.describe(tram="tram")
async def tramsearch(ctx, tram: str):
    await ctx.response.send_message(f"Searching, trip data may take longer to send...")
    channel = ctx.channel
    type = tramType(tram)
    set = tram.upper()
   
    print(f'set: {set}')
    print(f"TRAINTYPE {type}")
    if type is None:
        await channel.send("Train not found")
    else:
        embed = discord.Embed(title=f"Info for {tram.upper()}:", color=0x0070c0)
        if set.endswith('-'):
            embed.add_field(name=type, value=set[:-1])
        else:
            embed.add_field(name=type, value=set)
        
        embed.set_thumbnail(url=getIcon(type))
        
        if type in ['HCMT', "X'Trapolis 100", 'Alstom Comeng', 'EDI Comeng', 'Siemens Nexas','VLocity', 'Sprinter', 'N Class']:
            information = trainData(set)
            print(information)
            infoData = f'**Livery:** {information[1]}\n**Status:** {information[3]}\n**Entered Service:** {information[2]}\n**Vicsig notes:** {information[4]}'
            if information[5]:
                infoData+=f'\n**Name:** {information[5]}'
                
            # thing if the user has been on
            def check_variable_in_csv(variable, file_path):
                if not os.path.exists(file_path):
                    print(f"The file {file_path} does not exist.")
                    return False

                with open(file_path, mode='r') as file:
                    csv_reader = csv.reader(file)
                    for row in csv_reader:
                        if row[1] == variable:
                            return True
                return False 
        
            fPath = f'utils/trainlogger/userdata/{ctx.user.name}.csv'
            trainridden = check_variable_in_csv(set, fPath)
            if trainridden:
                infoData +='\n\n✅ You have been on this train before'
                
            embed.add_field(name='Information', value=infoData)
        else:
            embed.add_field(name='Information', value='None available')
            
        
        embed.set_image(url=getTramImage(tram.upper()))
        
        embed.add_field(name="Source:", value=f'[{getPhotoCredits(tram.upper())} (Photo)](https://railway-photos.xm9g.xyz#:~:text={tram.upper()}), [MPTG (Icon)](https://melbournesptgallery.weebly.com/melbourne-train-and-tram-fronts.html), [Vicsig (Other info)](https://vicsig.net)', inline=False)
        
        embed.add_field(name='<a:botloading2:1261102206468362381> Loading trip data', value='⠀')
        embed_update = await channel.send(embed=embed)
        # if type in ['HCMT', "X'Trapolis 100", 'Alstom Comeng', 'EDI Comeng', 'Siemens Nexas']:
        loop = asyncio.get_event_loop()
        task = loop.create_task(TRAMtransportVicSearch_async(ctx, tram.upper(), embed, embed_update))
        await task
            
        # else:
        #     embed.remove_field(3)
        #     await embed_update.edit(embed=embed)
        #     await mapEmbedUpdate.delete()
        #     await ctx.channel.send('Location info is only available for Metro services')
        
        
            
async def transportVicSearch_async(ctx, train, embed, embed_update):
    runs = await asyncio.to_thread(transportVicSearch, train)  # Find runs in a separate thread
    if isinstance(runs, list):
        print("thing is a list")
        embed.remove_field(3)
        # Reverse the order of the runs list
        for i, run in enumerate(reversed(runs)):
            print(run)
            if run.startswith('#'):
                embed.add_field(name=f"Run", value=run, inline=False)
                if i>=3:
                    break
            else:
                embed.add_field(name='No runs found!', value='⠀')

        embed.add_field(name='Data Source', value=f'[View on TransportVic](https://vic.transportsg.me/metro/tracker/consist?consist={train.upper()})')
        await embed_update.edit(embed=embed)
    else:
        embed.remove_field(3)
        embed.add_field(name=f"No runs currently found for {train.upper()}", value='⠀')
        await embed_update.edit(embed=embed)
        
async def TRAMtransportVicSearch_async(ctx, tram, embed, embed_update):
    runs = await asyncio.to_thread(TRAMtransportVicSearch, tram)  # Find runs in a separate thread
    if isinstance(runs, list):
        print("thing is a list")
        embed.remove_field(3)
        for i, run in enumerate(runs):
            if run.startswith(tuple("0123456789")):
                embed.add_field(name=f"Run {i+1}", value=run, inline=False)
            else:
                embed.add_field(name='No runs found!', value='⠀')
        embed.add_field(name='Data Source', value=f'[View on TransportVic](https://vic.transportsg.me/tram/tracker/fleet?fleet={tram.upper()})')
        await embed_update.edit(embed=embed)
    else:
        embed.remove_field(3)
        embed.add_field(name=f"No runs currently found for {tram.upper()}", value='⠀')
        await embed_update.edit(embed=embed)


# Next departures for a station
async def station_autocompletion(
    interaction: discord.Interaction,
    current: str
) -> typing.List[app_commands.Choice[str]]:
    fruits = stations_list.copy()
    return [
        app_commands.Choice(name=fruit, value=fruit)
        for fruit in fruits if current.lower() in fruit.lower()
    ]
@search.command(name="departures", description="Upcoming trains departing a station")
@app_commands.describe(station="Station")
@app_commands.autocomplete(station=station_autocompletion)
# test
async def departures(ctx, station: str):
    async def nextdeps():
        channel = ctx.channel
        await ctx.response.send_message(f"Loading Departures from {station}...")
        Nstation = station.replace(' ', '%20')
        search = search_api_request(f'{Nstation.title()}%20Station')
        # find the stop id!
        def find_stop_id(data, location):
            for stop in data['stops']:
                if stop['stop_name'] == location:
                    return stop['stop_id']
            return 'None'
        
        stop_id = find_stop_id(search, f"{station.title()} Station")
        print(f'STOP ID for {station} Station: {stop_id}')
        if stop_id == 'None':
            # await ctx.channel.send("Station not found, trying for V/LINE")
            search = search_api_request(f'{Nstation.title()}%20Railway%20Station')
            stop_id = find_stop_id(search, f"{station.title()} Railway Station ")
            print(f'STOP ID for {station} Station: {stop_id}')

            
        # get departures for the stop:
        depsData = departures_api_request(stop_id, 0)
        vlineDepsData = departures_api_request(stop_id, 3)

        departures = depsData['departures']
        vdepartures = vlineDepsData['departures']
        runs = depsData['runs']
        vruns = vlineDepsData['runs']

        # make embed with data
        embed= discord.Embed(title=f"Next trains departing {station} Station")
        fields = 0
        for departure in departures:
            scheduled_departure_utc = departure['scheduled_departure_utc']
            if isPast(scheduled_departure_utc):
                # print(f"time in past")
                pass
            else:
                estimated_departure_utc = departure['estimated_departure_utc']
                run_ref = departure['run_ref']
                at_platform = departure['at_platform']
                platform_number = departure['platform_number']
                route_id= departure['route_id'] 
                note = departure['departure_note']
                
                # get info for the run:
                desto = runs[run_ref]['destination_name']
                try:
                    trainType = runs[run_ref]['vehicle_descriptor']['description']
                    trainNumber = runs[run_ref]['vehicle_descriptor']['id']
                except:
                    trainType = ''
                    trainNumber = ''

                # train info

                #convert to timestamp
                depTime=convert_iso_to_unix_time(scheduled_departure_utc)
                #get route name:
                route_name = get_route_name(route_id)                
                
                #VLINE PLATFORMS DONT WORK PLS HELP
                
                embed.add_field(name=f'{getEmojiColor(route_name)} {desto}', value=f"{note if note else ''}\nDeparting {depTime} ({convert_iso_to_unix_time(scheduled_departure_utc,'short-time')})\nPlatform {platform_number}\n{route_name} Line\n{trainType} {trainNumber}\nRun `{run_ref}`")
                fields = fields + 1
                if fields == 9:
                    break
        # the V/Line part
        fields = 0
        departureTimes = ['']
        for departure in vdepartures:
            scheduled_departure_utc = departure['scheduled_departure_utc']
            if isPast(scheduled_departure_utc):
                # print(f"time in past")
                pass
            else:
                estimated_departure_utc = departure['estimated_departure_utc']
                if estimated_departure_utc in departureTimes:
                    print(f'the deparute with that time was already added: {scheduled_departure_utc} -- {desto}')
                else:
                    departureTimes.append(estimated_departure_utc)
                    run_ref = departure['run_ref']
                    at_platform = departure['at_platform']
                    platform_number = departure['platform_number']
                    route_id= departure['route_id'] 
                    
                    # get info for the run:
                    desto = vruns[run_ref]['destination_name']
                    try:
                        trainType = runs[run_ref]['vehicle_descriptor']['description']
                    except:
                        trainType = ''

                    #convert to timestamp
                    depTime=convert_iso_to_unix_time(scheduled_departure_utc)
                    #get route name:
                    route_name = get_route_name(route_id)
                    #add to embed
                    
                    embed.add_field(name=f"<:vline:1241165814258729092> {desto.replace(' Railway Station', '')}", value=f"Departing {depTime}\n Platform {platform_number}\nLine: {route_name}\n{trainType}\n**RUNID: {run_ref}**")
                    fields = fields + 1
                    if fields == 3:
                        break
        embed.set_footer(text="V/Line departures info is in Beta")
        embed.set_thumbnail(url=getStationImage(station))
        await ctx.channel.send(embed=embed)          

    asyncio.create_task(nextdeps())

# flight search (disables cause its not 100% done)
'''@flight.command(name='departures-arrivals', description="Get the next departures for an airport.")
@app_commands.describe(icao="Airport ICAO code")
async def flightdepartures(ctx,icao:str):
    async def flightdeps():
        await ctx.response.defer()
        deps = flightDepartures(icao=icao)
        arr = flightArrivals(icao=icao)

        if not deps:
            await ctx.edit_original_response(content="No departures found in the past 5 hours.")
            return

        embed = discord.Embed(title="Flight Information", color=discord.Color.blue())

        for flight in deps:
            flight_id = flight.icao24
            departure_time = datetime.fromtimestamp(flight.firstSeen).strftime('%Y-%m-%d %H:%M:%S')
            depairport = flight.estDepartureAirport
            flight_number = flight.callsign.strip()

            embed.add_field(
                name=f"Flight {flight_number}",
                value=(
                    f"ID: {flight_id}\n"
                    f"Departure Time: {departure_time}\n"
                    f"Departure Airport: {depairport}\n"

                ),
                inline=False
            )

        await ctx.edit_original_response(embed=embed)

    asyncio.create_task(flightdeps())'''


# Montague Bridge search
'''@bot.tree.command(name="days-since-montague-hit", description="See how many days it has been since the Montague Street bridge has been hit.")
async def train_line(ctx):
    await ctx.response.send_message(f"Checking...")
    channel = ctx.channel
    
    embed = discord.Embed(title=f"How many days since the Montague Street bridge has been hit?", color=0xd8d800)
    # embed.set_image(url=getImage(train.upper()))
    
    # Create a new thread to call the function
    # days_queue = queue.Queue()
    # thread = threading.Thread(target=montagueDays, args=(days_queue,))
    # thread.start()

    # thread.join()
    # Retrieve the result from the queue
    # days = days_queue.get()
    
    api_queue = queue.Queue()
    thread = threading.Thread(target=montagueAPI, args=(api_queue,))    
    thread.start()
    thread.join()
    
    apiData = api_queue.get()
    
    # Extract individual variables from the apis data
    date = apiData["date"]
    thanks = apiData["thanks"]
    streak = apiData["streak"]
    chumps = apiData["chumps"]
    name = chumps[0]['name'] # get name from the chumps thing
    image = apiData["image"]
    thumb = apiData["thumb"]
    date_year = apiData["date_year"]
    date_week = apiData["date_week"]
    date_aus_string = apiData["date_aus_string"]
    
    embed.add_field(name=f"{convert_to_unix_time(f'{date}T00:00:00Z')} days", value='\u200b', inline=False)

    embed.add_field(name="Current Champion:", value=name)
    embed.add_field(name="Date:", value=date)
    embed.set_image(url=f'https://howmanydayssincemontaguestreetbridgehasbeenhit.com{image}')
    
    embed.set_author(name='howmanydayssincemontaguestreetbridgehasbeenhit.com', url="https://howmanydayssincemontaguestreetbridgehasbeenhit.com")
    await ctx.channel.send(embed=embed)'''
    
@games.command(name="station-guesser", description="Play a game where you guess what train station is in the photo.")
@app_commands.describe(rounds = "The number of rounds. Defaults to 1.", ultrahard = "Ultra hard mode.")
async def game(ctx, ultrahard: bool=False, rounds: int = 1):
    
    channel = ctx.channel
    async def run_game():

        # Check if a game is already running in this channel
        if channel in channel_game_status and channel_game_status[channel]:
            await ctx.response.send_message("A game is already running in this channel.", ephemeral=True )
            return
        if rounds > 25:
            await ctx.response.send_message("You can only play a maximum of 25 rounds!", ephemeral=True )
            return

        channel_game_status[channel] = True
        
        # Define the CSV file path
        if ultrahard:
            csv_file = 'utils/game/images/ultrahard.csv'
        else:
            csv_file = 'utils/game/images/guesser.csv'

        # Read the CSV file and store rows in a list
        rows = []
        with open(csv_file, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                rows.append(row)

        # Remove the header row if present
        header = rows[0]
        data = rows[1:]

        for round in range(rounds):
            # Get a random row
            random_row = random.choice(data)

            # Extract data from the random row
            url = random_row[0]
            station = random_row[1]
            difficulty = random_row[2]
            credit = random_row[3]

            if ultrahard:
                embed = discord.Embed(title=f"Guess the station!", color=0xe52727, description=f"Type ! before your answer. You have 30 seconds to answer.\n\n**Difficulty:** `{difficulty.upper()}`")
            else:
                embed = discord.Embed(title=f"Guess the station!", description=f"Type ! before your answer. You have 30 seconds to answer.\n\n**Difficulty:** `{difficulty}`")
                if difficulty == 'Very Easy':
                    embed.color = 0x89ff65
                elif difficulty == 'Easy':
                    embed.color = 0xcaff65
                elif difficulty == 'Medium':
                    embed.color = 0xffe665
                elif difficulty == 'Hard':
                    embed.color = 0xffa665
                elif difficulty == 'Very Hard':
                    embed.color = 0xff6565
            
            embed.set_image(url=url)
            embed.set_footer(text=f"Photo by {credit}. DM @xm9g to submit a photo")
            embed.set_author(name=f"Round {round+1}/{rounds}")

            # Send the embed message
            if round == 0:
                await ctx.response.send_message(embed=embed)
            else:
                await ctx.channel.send(embed=embed)

            # Define a check function to validate user input
            def check(m):
                return m.channel == channel and m.author != bot.user and m.content.startswith('!')

            try:
                correct = False
                if ultrahard:
                    gameType = 'ultrahard'
                else:
                    gameType = 'guesser'
                
                
                while not correct:
                    # Wait for user's response in the same channel
                    user_response = await bot.wait_for('message', check=check, timeout=30.0)
                    
                    # Check if the user's response matches the correct station
                    if user_response.content[1:].lower() == station.lower():
                        if ultrahard:
                            await ctx.channel.send(f"{user_response.author.mention} guessed it right!")
                        else:
                            await ctx.channel.send(f"{user_response.author.mention} guessed it right! {station.title()} was the correct answer!")
                        correct = True
                        if ultrahard:
                            addLb(user_response.author.id, user_response.author.name, 'ultrahard')
                        else:
                            addLb(user_response.author.id, user_response.author.name, 'guesser')
                            
                    elif user_response.content.lower() == '!skip':
                        if user_response.author.id in [ctx.user.id,707866373602148363,780303451980038165] :
                            await ctx.channel.send(f"Round {round+1} skipped.")
                            break
                        else:
                            await ctx.channel.send(f"{user_response.author.mention} you can only skip the round if you were the one who started it.")
                    elif user_response.content.lower() == '!stop':
                        if user_response.author.id in [ctx.user.id,707866373602148363,780303451980038165] :
                            await ctx.channel.send(f"Game ended.")
                            return
                        else:
                            await ctx.channel.send(f"{user_response.author.mention} you can only stop the game if you were the one who started it.")    
                    else:
                        await ctx.channel.send(f"Wrong guess {user_response.author.mention}! Try again.")
                        if ultrahard:
                            addLoss(user_response.author.id, user_response.author.name, 'ultrahard')
                        else:
                            addLoss(user_response.author.id, user_response.author.name, 'guesser')
            except asyncio.TimeoutError:
                if ultrahard:
                    await ctx.channel.send(f"Times up. Answers are not revealed in ultrahard mode.")
                else:
                    await ctx.channel.send(f"Times up. The answer was ||{station.title()}||")
            finally:
                # Reset game status after the game ends
                channel_game_status[channel] = False

    # Run the game in a separate task
    asyncio.create_task(run_game())
    

    
@stats.command(name="leaderboard", description="Global leaderboards for the games.",)
@app_commands.describe(game="What game's leaderboard to show?")
@app_commands.choices(game=[
        app_commands.Choice(name="Station Guesser", value="guesser"),
        app_commands.Choice(name="Ultrahard Station Guesser", value="ultrahard"),
        app_commands.Choice(name="Station order game", value="domino"),

])

async def lb(ctx, game: str='guesser'):
    channel = ctx.channel
    leaders = top5(game)
    if leaders == 'no stats':
        await ctx.response.send_message('There is no data for this game yet!',ephemeral=True)
        return
    print(leaders)
    # Create the embed
    embed = discord.Embed(title=f"Top 7 players for {game}", color=discord.Color.gold())
    
    count = 1
    for item, number, losses in leaders:
        try:
            embed.add_field(name=f'{count}: {item}', value=f'Wins: {str(number)}\nLosses: {str(losses)}\nAccuracy: {str(round((number/(number+losses))*100, 1))}%', inline=False)
        except:
            embed.add_field(name=f'{count}: {item}', value=f'Wins: {str(number)}\nLosses: {str(losses)}', inline=False)
        count = count + 1
        
    await ctx.response.send_message(embed=embed)


# Station order game made by @domino

lines_dictionary = {
    'Alamein': [['Richmond', 'East Richmond', 'Burnley', 'Hawthorn', 'Glenferrie', 'Auburn', 'Camberwell', 'Riversdale', 'Willison', 'Hartwell', 'Burwood', 'Ashburton', 'Alamein'],0x01518a],
    'Belgrave': [['Richmond', 'East Richmond', 'Burnley', 'Hawthorn', 'Glenferrie', 'Auburn', 'Camberwell', 'East Camberwell', 'Canterbury', 'Chatham', 'Union', 'Box Hill', 'Laburnum', 'Blackburn', 'Nunawading', 'Mitcham', 'Heatherdale', 'Ringwood', 'Heathmont', 'Bayswater', 'Boronia', 'Ferntree Gully', 'Upper Ferntree Gully', 'Upwey', 'Tecoma', 'Belgrave'],0x01518a],
    'Craigieburn': [['North Melbourne', 'Kensington', 'Newmarket', 'Ascot Vale', 'Moonee Ponds', 'Essendon', 'Glenbervie', 'Strathmore', 'Pascoe Vale', 'Oak Park', 'Glenroy', 'Jacana', 'Broadmeadows', 'Coolaroo', 'Roxburgh Park', 'Craigieburn'],0xfcb818],
    'Cranbourne': [['Richmond', 'South Yarra', 'Malvern', 'Caulfield', 'Carnegie', 'Murrumbeena', 'Hughesdale', 'Oakleigh', 'Huntingdale', 'Clayton', 'Westall', 'Springvale', 'Sandown Park', 'Noble Park', 'Yarraman', 'Dandenong', 'Lynbrook', 'Merinda Park', 'Cranbourne'],0x00a8e4],
    'Flemington Racecourse': [['Flemington Racecourse', 'Showgrounds', 'North Melbourne', 'Southern Cross', 'Flinders Street'],0x8a8c8f],
    'Frankston': [['Flinders Street', 'Richmond', 'South Yarra', 'Hawksburn', 'Toorak', 'Armadale', 'Malvern', 'Caulfield', 'Glen Huntly', 'Ormond', 'McKinnon', 'Bentleigh', 'Patterson', 'Moorabbin', 'Highett', 'Southland', 'Cheltenham', 'Mentone', 'Parkdale', 'Mordialloc', 'Aspendale', 'Edithvale', 'Chelsea', 'Bonbeach', 'Carrum', 'Seaford', 'Kananook', 'Frankston'],0x009645],
    'Glen Waverley': [['Richmond', 'East Richmond', 'Burnley', 'Heyington', 'Kooyong', 'Tooronga', 'Gardiner', 'Glen Iris', 'Darling', 'East Malvern', 'Holmesglen', 'Jordanville', 'Mount Waverley', 'Syndal', 'Glen Waverley'],0x01518a],
    'Hurstbridge': [['Jolimont', 'West Richmond', 'North Richmond', 'Collingwood', 'Victoria Park', 'Clifton Hill', 'Westgarth', 'Dennis', 'Fairfield', 'Alphington', 'Darebin', 'Ivanhoe', 'Eaglemont', 'Heidelberg', 'Rosanna', 'Macleod', 'Watsonia', 'Greensborough', 'Montmorency', 'Eltham', 'Diamond Creek', 'Wattle Glen', 'Hurstbridge'],0xd0202e],
    'Lilydale': [['Richmond', 'East Richmond', 'Burnley', 'Hawthorn', 'Glenferrie', 'Auburn', 'Camberwell', 'East Camberwell', 'Canterbury', 'Chatham', 'Union', 'Box Hill', 'Laburnum', 'Blackburn', 'Nunawading', 'Mitcham', 'Heatherdale', 'Ringwood', 'Ringwood East', 'Croydon', 'Mooroolbark', 'Lilydale'],0x01518a],
    'Mernda': [['Jolimont', 'West Richmond', 'North Richmond', 'Collingwood', 'Victoria Park', 'Clifton Hill', 'Rushall', 'Merri', 'Northcote', 'Croxton', 'Thornbury', 'Bell', 'Preston', 'Regent', 'Reservoir', 'Ruthven', 'Keon Park', 'Thomastown', 'Lalor', 'Epping', 'South Morang', 'Middle Gorge', 'Hawkstowe', 'Mernda'],0xd0202e],
    'Pakenham': [['Richmond', 'South Yarra', 'Malvern', 'Caulfield', 'Carnegie', 'Murrumbeena', 'Hughesdale', 'Oakleigh', 'Huntingdale', 'Clayton', 'Westall', 'Springvale', 'Sandown Park', 'Noble Park', 'Yarraman', 'Dandenong', 'Hallam', 'Narre Warren', 'Berwick', 'Beaconsfield', 'Officer', 'Cardinia Road', 'Pakenham'],0x00a8e4],
    'Sandringham': [['Flinders Street', 'Richmond', 'South Yarra', 'Prahran', 'Windsor', 'Balaclava', 'Ripponlea', 'Elsternwick', 'Gardenvale', 'North Brighton', 'Middle Brighton', 'Brighton Beach', 'Hampton', 'Sandringham'],0xf17fb1],
    'Stony Point': [['Stony Point', 'Crib Point', 'Morradoo', 'Bittern', 'Hastings', 'Tyabb', 'Somerville', 'Baxter', 'Leawarra', 'Frankston'],0x009645],
    'Sunbury': [['North Melbourne', 'Footscray', 'Middle Footscray', 'West Footscray', 'Tottenham', 'Sunshine', 'Albion', 'Ginifer', 'St Albans', 'Keilor Plains', 'Watergardens', 'Diggers Rest', 'Sunbury'],0xfcb818],
    'Upfield': [['North Melbourne', 'Macaulay', 'Flemington Bridge', 'Royal Park', 'Jewell', 'Brunswick', 'Anstey', 'Moreland', 'Coburg', 'Batman', 'Merlynston', 'Fawkner', 'Gowrie', 'Upfield'],0xfcb818],
    'Werribee': [['Flinders Street', 'Southern Cross', 'North Melbourne', 'South Kensington', 'Footscray', 'Seddon', 'Yarraville', 'Spotswood', 'Newport', 'Seaholme', 'Altona', 'Westona', 'Laverton', 'Aircraft', 'Williams Landing', 'Hoppers Crossing', 'Werribee'],0x009645],
    'Williamstown': [['Flinders Street', 'Southern Cross', 'North Melbourne', 'South Kensington', 'Footscray', 'Seddon', 'Yarraville', 'Spotswood', 'Newport', 'North Williamstown', 'Williamstown Beach', 'Williamstown'],0x009645],
    'Unknown/Other':[[None], 0x000000],
}
linelist = [
    None,
    'Alamein', #1
    'Belgrave', #2
    'Craigieburn', #3
    'Cranbourne', #4
    'Mernda', #5
    'Frankston', #6
    'Glen Waverley', #7
    'Hurstbridge', #8
    'Lilydale', #9
    None,
    'Pakenham', #11
    'Sandringham', #12
    None,
    'Sunbury', #14
    'Upfield', #15
    'Werribee', #16
    'Williamstown' #17
]

@games.command(name="station-order", description="A game where you list the stations before or after a station.")
@app_commands.describe(rounds = "The number of rounds. Defaults to 1.", direction = "The directions you are listing the stations in. Defaults to Up or Down.")
@app_commands.choices(
    direction=[
        app_commands.Choice(name="Up or Down", value='updown'),
        app_commands.Choice(name="Up", value='up'),
        app_commands.Choice(name="Down", value='down')
        ],
    )

async def testthing(ctx, direction: str = 'updown', rounds: int = 1):
    channel = ctx.channel
    async def run_game():
        # Check if a game is already running in this channel
        if channel in channel_game_status and channel_game_status[channel]:
            await ctx.response.send_message("A game is already running in this channel.", ephemeral=True )
            return
        if rounds > 25:
            await ctx.response.send_message("You can only play a maximum of 25 rounds!", ephemeral=True )
            return

        channel_game_status[channel] = True

        for round in range(rounds):
            # choose random number of stations
            numdirection = random.randint(2,5)

            # choose direction
            if direction == 'updown':
                direction1 = random.choice(['up','down'])
            else:
                direction1 = direction
            if direction1 == 'up':
                numdirection = numdirection*-1
            
            # choose random line
            line = None
            while line == None:
                line = linelist[random.randint(0,len(linelist)-1)]

            # choose random station
            if line == 'Flemington Racecourse':
                if numdirection == 5 or numdirection == -5:
                    numdirection = random.choice([-4,-3,-2,2,3,4])
            station = None
            while station == None:
                station = lines_dictionary[line][0][random.randint(0,len(lines_dictionary[line][0])-1)]
                if not 0 <= lines_dictionary[line][0].index(station)+numdirection <= len(lines_dictionary[line][0]):
                    station = None

            embed = discord.Embed(
                title=f"Which __**{numdirection if numdirection > 0 else numdirection*-1}**__ stations are __**{direction1}**__ from __**{station}**__ station on the __**{line} line**__?",
                description=f"**Answers must be in the correct order!** Answer using this format:\n!<station1>, <station2>{', <station3>' if numdirection >= 3 or numdirection <= -3 else ''}{', <station4>' if numdirection >= 4 or numdirection <= -4 else ''}{', <station5>' if numdirection >= 5 or numdirection <= -5 else ''}\n\n*Use !skip to skip to the next round.*",
                colour=lines_dictionary[line][1])
            embed.set_author(name=f"Round {round+1}/{rounds}")
            if round == 0:
                await ctx.response.send_message(embed=embed)
            else:
                await ctx.channel.send(embed=embed)

            # Define a check function to validate user input
            def check(m): return m.channel == channel and m.author != bot.user and m.content.startswith('!')

            # get list of correct stations
            if numdirection > 0:
                correct_list = lines_dictionary[line][0][lines_dictionary[line][0].index(station)+1:lines_dictionary[line][0].index(station)+numdirection+1]
            else:
                correct_list = lines_dictionary[line][0][lines_dictionary[line][0].index(station)+numdirection:lines_dictionary[line][0].index(station)]
                correct_list.reverse()
            correct_list1 = [x.lower() for x in correct_list]

            # the actual input part
            try:
                correct = False
                while not correct:
                    # Wait for user's response in the same channel
                    user_response = await bot.wait_for('message', check=check, timeout=30.0)
                    response = user_response.content[1:].lower().split(',')
                    response = [x.strip() for x in response]


                    # Check if the user's response matches the correct station
                    if response == correct_list1:
                        await ctx.channel.send(f"{user_response.author.mention} guessed it correctly!")
                        addLb(user_response.author.id, user_response.author.name, 'domino')
                        
                        correct = True 
                    elif user_response.content.lower() == '!skip':
                        if user_response.author.id in [ctx.user.id,707866373602148363,780303451980038165] :
                            await ctx.channel.send(f"Round {round+1} skipped. The answer was ||{correct_list[0]}, {correct_list[1]}{f', {correct_list[2]}' if len(correct_list) >=3 else ''}{f', {correct_list[3]}' if len(correct_list) >=4 else ''}{f', {correct_list[4]}' if len(correct_list) >=5 else ''}||")
                            break
                        else:
                            await ctx.channel.send(f"{user_response.author.mention} you can only skip the round if you were the one who started it.")
                    elif user_response.content.lower() == '!stop':
                        if user_response.author.id in [ctx.user.id,707866373602148363,780303451980038165] :
                            await ctx.channel.send(f"Game ended.")
                            return
                        else:
                            await ctx.channel.send(f"{user_response.author.mention} you can only stop the game if you were the one who started it.")
                    else:
                        await ctx.channel.send(f"Wrong guess {user_response.author.mention}! Try again.")
                        addLoss(user_response.author.id, user_response.author.name, 'domino')
                        
            except asyncio.TimeoutError:
                await ctx.channel.send(f"Times up. The answer was ||{correct_list[0]}, {correct_list[1]}{f', {correct_list[2]}' if len(correct_list) >=3 else ''}{f', {correct_list[3]}' if len(correct_list) >=4 else ''}{f', {correct_list[4]}' if len(correct_list) >=5 else ''}||")
            finally:
                # Reset game status down the game ends
                channel_game_status[channel] = False
            
    # Run the game in a separate task
    asyncio.create_task(run_game())

async def station_autocompletion(
    interaction: discord.Interaction,
    current: str
) -> typing.List[app_commands.Choice[str]]:
    fruits = stations_list.copy()
    return [
        app_commands.Choice(name=fruit, value=fruit)
        for fruit in fruits if current.lower() in fruit.lower()
    ]
@trainlogs.command(name="add-train", description="Log a train you have been on")
@app_commands.describe(number = "Carrige Number", date = "Date in DD/MM/YYYY format", line = 'Train Line', start='Starting Station', end = 'Ending Station', traintype='Type of train (will be autofilled if a train number is entered)')
@app_commands.autocomplete(start=station_autocompletion)
@app_commands.autocomplete(end=station_autocompletion)
@app_commands.choices(line=[
        app_commands.Choice(name="Alamein", value="Alamein"),
        app_commands.Choice(name="Belgrave", value="Belgrave"),
        app_commands.Choice(name="Craigieburn", value="Craigieburn"),
        app_commands.Choice(name="Cranbourne", value="Cranbourne"),
        app_commands.Choice(name="Flemington Racecourse", value="Flemington Racecourse"),
        app_commands.Choice(name="Frankston", value="Frankston"),
        app_commands.Choice(name="Glen Waverley", value="Glen Waverley"),
        app_commands.Choice(name="Hurstbridge", value="Hurstbridge"),
        app_commands.Choice(name="Lilydale", value="Lilydale"),
        app_commands.Choice(name="Mernda", value="Mernda"),
        app_commands.Choice(name="Pakenham", value="Pakenham"),
        app_commands.Choice(name="Sandringham", value="Sandringham"),
        app_commands.Choice(name="Stony Point", value="Stony Point"),
        app_commands.Choice(name="Sunbury", value="Sunbury"),
        app_commands.Choice(name="Upfield", value="Upfield"),
        app_commands.Choice(name="Werribee", value="Werribee"),
        app_commands.Choice(name="Williamstown", value="Williamstown"),
        app_commands.Choice(name="Albury", value="Albury"),
        app_commands.Choice(name="Ballarat/Maryborough/Ararat", value="Ballarat/Maryborough/Ararat"),
        app_commands.Choice(name="Bendigo/Echuca/Swan Hill", value="Bendigo/Echuca/Swan Hill"),
        app_commands.Choice(name="Geelong/Warrnambool", value="Geelong/Warrnambool"),
        app_commands.Choice(name="Seymour/Shepparton", value="Seymour/Shepparton"),
        app_commands.Choice(name="Traralgon/Bairnsdale", value="Traralgon/Bairnsdale"),
        app_commands.Choice(name="Unknown", value="Unknown")
])
@app_commands.choices(traintype=[
        app_commands.Choice(name="X'Trapolis 100", value="X'Trapolis 100"),
        app_commands.Choice(name="HCMT", value="HCMT"),
        app_commands.Choice(name="EDI Comeng", value="EDI Comeng"),
        app_commands.Choice(name="Alstom Comeng", value="Alstom Comeng"),
        app_commands.Choice(name="Siemens Nexas", value="Siemens Nexas"),
        app_commands.Choice(name="VLocity", value="VLocity"),
        app_commands.Choice(name="N Class", value="N Class"),
        app_commands.Choice(name="Sprinter", value="Sprinter"),
        app_commands.Choice(name="Other", value="Other"),
        app_commands.Choice(name="Tait", value="Tait"),
        app_commands.Choice(name="K Class", value="K Class"),
        app_commands.Choice(name="Y Class", value="Y Class"),
])

# Train logger
async def logtrain(ctx, line:str, number:str='Unknown', date:str='today', start:str='N/A', end:str='N/A', traintype:str='auto'):
    channel = ctx.channel
    print(date)
    async def log():
        print("logging the thing")

        savedate = date.split('/')
        if date.lower() == 'today':
            current_time = time.localtime()
            savedate = time.strftime("%Y-%m-%d", current_time)
        else:
            try:
                savedate = time.strptime(date, "%d/%m/%Y")
                savedate = time.strftime("%Y-%m-%d", savedate)
            except ValueError:
                await ctx.response.send_message(f'Invalid date: {date}\nMake sure to use a possible date.', ephemeral=True)
                return
            except TypeError:
                await ctx.response.send_message(f'Invalid date: {date}\nUse the form `dd/mm/yyyy`', ephemeral=True)
                return

        # checking if train number is valid
        if number != 'Unknown':
            set = setNumber(number.upper())
            if set == None:
                await ctx.response.send_message(f'Invalid train number: {number.upper()}',ephemeral=True)
                return
            type = trainType(number.upper())
        else:
            set = 'Unknown'
            type = 'Unknown'
            if traintype == 'auto':
                type = 'Unknown'
            else: type = traintype
        if traintype == "Tait":
            set = '381M-208T-230D-317M'

        # Add train to the list
        id = addTrain(ctx.user.name, set, type, savedate, line, start.title(), end.title())
        await ctx.response.send_message(f"Added {set} ({type}) on the {line} line on {savedate} from {start.title()} to {end.title()} to your file. (Log ID `#{id}`)")
        
                
    # Run in a separate task
    asyncio.create_task(log())

    
#thing to delete the stuff
@trainlogs.command(name='delete', description='Delete a logged trip. Defaults to the last logged trip.')
@app_commands.describe(id = "The ID of the log that you want to delete.", mode='What mode of log to delete?')
@app_commands.choices(mode=[
     app_commands.Choice(name="Victorian Train", value="train"),
    app_commands.Choice(name="Melbourne Tram", value="tram"),
    app_commands.Choice(name="NSW Train", value="sydney-trains"),
    app_commands.Choice(name="Sydney Light Rail", value="sydney-trams"),

])
async def deleteLog(ctx, mode:str, id:str='LAST'):
    
    async def deleteLogFunction():
        if id[0] == '#':
            idformatted = id[1:].upper()
        else:
            idformatted = id.upper()

        if idformatted != 'LAST':
            if not is_hex(idformatted):
                cmds = await bot.tree.fetch_commands()
                for cmd in cmds:
                    if cmd.name == 'train-logs':
                        cmdid = cmd.id
                        await ctx.response.send_message(f'Invalid log ID entered: `{idformatted}`. You can find the ID of a log to delete by using </train-logs view:{cmdid}>.',ephemeral=True)
                        return
                
            
        dataToDelete = universalReadRow(ctx.user.name, idformatted, mode)
        if dataToDelete in ['no data at all','no data for user']:
            await ctx.response.send_message(f'You have no logs you can delete!',ephemeral=True)
            return
        elif dataToDelete == 'invalid id did not show up':
            cmds = await bot.tree.fetch_commands()
            for cmd in cmds:
                if cmd.name == 'train-logs':
                    cmdid = cmd.id
                    await ctx.response.send_message(f'Invalid log ID entered: `{idformatted}`. You can find the ID of a log to delete by using </train-logs view:{cmdid}>.',ephemeral=True)
                    return
        else:
            idformatted1 = deleteRow(ctx.user.name, idformatted, mode)
            if idformatted == 'LAST':
                await ctx.response.send_message(f'Most recent log (`#{idformatted1}`) deleted. The data was:\n`{dataToDelete}`',ephemeral=True)
            else:
                await ctx.response.send_message(f'Log `#{idformatted}` deleted. The data was:\n`{dataToDelete}`',ephemeral=True)
            
    asyncio.create_task(deleteLogFunction())

    
  # tram logger goes here
@trainlogs.command(name="add-tram", description="Log a tram you have been on")
@app_commands.describe(number = "Tram Number", date = "Date in DD/MM/YYYY format", route = 'Tram Line', start='Starting Stop', end = 'Ending Stop')
@app_commands.autocomplete(start=station_autocompletion)
@app_commands.autocomplete(end=station_autocompletion)
@app_commands.choices(route=[
        app_commands.Choice(name="1 East Coburg - South Melbourne Beach", value="1"),
        app_commands.Choice(name="3 Melbourne University - Malvern East", value="3"),
        app_commands.Choice(name="5 Melbourne University- Malvern", value="5"),
        app_commands.Choice(name="6 Brunswick tram depot - Glen Iris", value="6"),
        app_commands.Choice(name="11 West Preston - Victoria Harbour Docklands", value="11"),
        app_commands.Choice(name="12 Victoria Gardens - St Kilda", value="12"),
        app_commands.Choice(name="16 Melbourne University - Kew", value="16"),
        app_commands.Choice(name="19 North Coburg - Flinders Street station", value="19"),
        app_commands.Choice(name="30 St Vincent's Plaza - Central Pier Docklands", value="30"),
        app_commands.Choice(name="35 City Circle", value="35"),
        app_commands.Choice(name="48 Balwyn North - Victoria Harbour Docklands", value="48"),
        app_commands.Choice(name="57 West Maribyrnong - Flinders Street station", value="57"),
        app_commands.Choice(name="58 West Coburg - Toorak", value="58"),
        app_commands.Choice(name="59 Airport West - Flinders Street station", value="59"),
        app_commands.Choice(name="64 Melbourne University - Brighton East", value="64"),
        app_commands.Choice(name="67 Melbourne University - Carnegie", value="67"),
        app_commands.Choice(name="70 Wattle Park - Waterfront City Docklands", value="70"),
        app_commands.Choice(name="72 Melbourne University - Camberwell", value="72"),
        app_commands.Choice(name="75 Vermont South Shopping Centre - Central Pier Docklands", value="75"),
        app_commands.Choice(name="78 North Richmond - Balaclava", value="78"),
        app_commands.Choice(name="82 Footscray - Moonee Ponds", value="82"),
        app_commands.Choice(name="86 Bundoora RMIT - Waterfront City Docklands", value="86"),
        app_commands.Choice(name="96 Brunswick East - St Kilda Beach", value="96"),
        app_commands.Choice(name="109 Box Hill Central - Port Melbourne", value="109")
])

async def logtram(ctx, route:str, number: str='Unknown', date:str='today', start:str='N/A', end:str='N/A'):
    channel = ctx.channel
    print(date)
    async def log():
        print("logging the thing")

        savedate = date.split('/')
        if date.lower() == 'today':
            current_time = time.localtime()
            savedate = time.strftime("%Y-%m-%d", current_time)
        else:
            try:
                savedate = time.strptime(date, "%d/%m/%Y")
                savedate = time.strftime("%Y-%m-%d", savedate)
            except ValueError:
                await ctx.response.send_message(f'Invalid date: {date}\nMake sure to use a possible date.', ephemeral=True)
                return
            except TypeError:
                await ctx.response.send_message(f'Invalid date: {date}\nUse the form `dd/mm/yyyy`', ephemeral=True)
                return

        # checking if train number is valid
        if set == None:
            await ctx.response.send_message(f'Invalid train number: {number.upper()}',ephemeral=True)
            return
        type = tramType(number.upper())
        if type == None:
            type = 'N/A'

        # Add train to the list
        id = addTram(ctx.user.name, number, type, savedate, route, start.title(), end.title())
        await ctx.response.send_message(f"Added {number} ({type}) on route {route} on {savedate} from {start.title()} to {end.title()} to your file. (Log ID `#{id}`)")
        
                
    # Run in a separate task
    asyncio.create_task(log())
    
    
    
# sydney train logger
async def NSWstation_autocompletion(
    interaction: discord.Interaction,
    current: str
) -> typing.List[app_commands.Choice[str]]:
    fruits = NSWstations_list.copy()
    return [
        app_commands.Choice(name=fruit, value=fruit)
        for fruit in fruits if current.lower() in fruit.lower()
    ]
    
@trainlogs.command(name="add-sydney-train", description="Log a Sydney/NSW train you have been on")
@app_commands.describe(number = "Carrige Number", type = 'Type of train', date = "Date in DD/MM/YYYY format", line = 'Train Line', start='Starting Station', end = 'Ending Station')
@app_commands.autocomplete(start=NSWstation_autocompletion)
@app_commands.autocomplete(end=NSWstation_autocompletion)
@app_commands.choices(line=[
        app_commands.Choice(name="T1 North Shore & Western Line", value="T1"),
        app_commands.Choice(name="T2 Inner West & Leppington Line", value="T2"),
        app_commands.Choice(name="T3 Bankstown Line", value="T3"),
        app_commands.Choice(name="T4 Eastern Suburbs & Illawarra Line", value="T4"),
        app_commands.Choice(name="T5 Cumberland Line", value="T5"),
        app_commands.Choice(name="T6 Lidcombe & Bankstown Line", value="T6"),
        app_commands.Choice(name="T7 Olympic Park Line", value="T7"),
        app_commands.Choice(name="T8 Airport & South Line", value="T8"),
        app_commands.Choice(name="T9 Northern Line", value="T9"),
        
        app_commands.Choice(name="Metro North West Line", value="Metro North West Line"),

        app_commands.Choice(name="Blue Mountains Line", value="Blue Mountains Line"),
        app_commands.Choice(name="Central Coast & Newcastle Line", value="Central Coast & Newcastle Line"),
        app_commands.Choice(name="Hunter Line", value="Hunter Line"),
        app_commands.Choice(name="South Coast Line", value="South Coast Line"),
        app_commands.Choice(name="Southern Highlands Line", value="Southern Highlands Line"),

        app_commands.Choice(name="North Coast Region", value="North Coast Region"),
        app_commands.Choice(name="North Western Region", value="North Western Region"),
        app_commands.Choice(name="Southern Region", value="Southern Region"),
        app_commands.Choice(name="Western Region", value="Western Region"),

        app_commands.Choice(name="Unknown", value="Unknown")
])
@app_commands.choices(type=[
        app_commands.Choice(name="K set", value="K set"),
        app_commands.Choice(name="Tangara - T Set", value="Tangara"),
        app_commands.Choice(name="Millennium - M Set", value="Millennium"),
        app_commands.Choice(name="OSCAR - H set", value="OSCAR"),
        app_commands.Choice(name="Waratah - A & B sets", value="Waratah"),
        
        app_commands.Choice(name="V set", value="V set"),
        app_commands.Choice(name="D set", value="D set"),
        app_commands.Choice(name="Endeavour railcar", value="Endeavour railcar"),
        app_commands.Choice(name="Hunter railcar", value="Hunter railcar"),
        app_commands.Choice(name="XPT", value="XPT"),
        app_commands.Choice(name="Xplorer", value="Xplorer"),
        
        app_commands.Choice(name="Metropolis Stock", value="Metropolis Stock"),

        app_commands.Choice(name="Unknown", value="Unknown"),
])
# SYdney train logger nsw train
async def logNSWTrain(ctx, number: str, type:str, line:str, date:str='today', start:str='N/A', end:str='N/A'):
    channel = ctx.channel
    print(date)
    async def log():
        print("logging the nsw sydney train")

        savedate = date.split('/')
        if date.lower() == 'today':
            current_time = time.localtime()
            savedate = time.strftime("%Y-%m-%d", current_time)
        else:
            try:
                savedate = time.strptime(date, "%d/%m/%Y")
                savedate = time.strftime("%Y-%m-%d", savedate)
            except ValueError:
                await ctx.response.send_message(f'Invalid date: {date}\nMake sure to use a possible date.', ephemeral=True)
                return
            except TypeError:
                await ctx.response.send_message(f'Invalid date: {date}\nUse the form `dd/mm/yyyy`', ephemeral=True)
                return

        # idk how to get nsw train set numbers i cant find a list of all sets pls help
        set = number
        if set == None:
            await ctx.response.send_message(f'Invalid train number: {number.upper()}',ephemeral=True)
            return

        # Add train to the list
        id = addSydneyTrain(ctx.user.name, set, type, savedate, line, start.title(), end.title())
        await ctx.response.send_message(f"Added {set} ({type}) on the {line} line on {savedate} from {start.title()} to {end.title()} to your file. (Log ID `#{id}`)")
        
                
    # Run in a separate task
    asyncio.create_task(log())



@trainlogs.command(name="add-sydney-tram", description="Log a Sydney Tram/Light Rail you have been on")
@app_commands.describe(number = "Carrige Number", type = 'Type of tram', date = "Date in DD/MM/YYYY format", line = 'Light Rail Line', start='Starting Stop', end = 'Ending Stop')
@app_commands.autocomplete(start=NSWstation_autocompletion)
@app_commands.autocomplete(end=NSWstation_autocompletion)
@app_commands.choices(line=[
        app_commands.Choice(name="L1 Dulwich Hill Line", value="L1"),
        app_commands.Choice(name="L2 Randwick", value="L2"),
        app_commands.Choice(name="L3 Kingsford Line", value="L3"),
])
@app_commands.choices(type=[
        app_commands.Choice(name="Urbos 3", value="Urbos 3"),
        app_commands.Choice(name="Citadis 305", value="Citadis 305"),
])
# SYdney tram logger nsw tram
async def logNSWTram(ctx, type:str, line:str, number: str='Unknown', date:str='today', start:str='N/A', end:str='N/A'):
    channel = ctx.channel
    print(date)
    async def log():
        print("logging the sydney tram")

        savedate = date.split('/')
        if date.lower() == 'today':
            current_time = time.localtime()
            savedate = time.strftime("%Y-%m-%d", current_time)
        else:
            try:
                savedate = time.strptime(date, "%d/%m/%Y")
                savedate = time.strftime("%Y-%m-%d", savedate)
            except ValueError:
                await ctx.response.send_message(f'Invalid date: {date}\nMake sure to use a possible date.', ephemeral=True)
                return
            except TypeError:
                await ctx.response.send_message(f'Invalid date: {date}\nUse the form `dd/mm/yyyy`', ephemeral=True)
                return

        # idk how to get nsw train set numbers i cant find a list of all sets pls help
        set = number
        if set == None:
            await ctx.response.send_message(f'Invalid train number: {number.upper()}',ephemeral=True)
            return

        # Add train to the list
        id = addSydneyTram(ctx.user.name, set, type, savedate, line, start.title(), end.title())
        await ctx.response.send_message(f"Added {set} ({type}) on the {line} line on {savedate} from {start.title()} to {end.title()} to your file. (Log ID `#{id}`)")
        
                
    # Run in a separate task
    asyncio.create_task(log())



async def busOpsautocompletion(
    interaction: discord.Interaction,
    current: str
) -> typing.List[app_commands.Choice[str]]:
    fruits = busOps.copy()
    return [
        app_commands.Choice(name=fruit, value=fruit)
        for fruit in fruits if current.lower() in fruit.lower()
    ]
    
@trainlogs.command(name="add-bus", description="Log a Bus you have been on")
@app_commands.describe(number = "Bus number", type = 'Type of bus', date = "Date in DD/MM/YYYY format", line = 'bus route', start='Starting Stop', end = 'Ending Stop')
@app_commands.autocomplete(operator=busOpsautocompletion)
# @app_commands.autocomplete(end=NSWstation_autocompletion)

async def logBus(ctx, line:str, operator:str='Unknown', date:str='today', start:str='N/A', end:str='N/A', type:str='Unknown', number: str='Unknown',):
    channel = ctx.channel
    print(date)
    async def log():
        print("logging the bus")

        savedate = date.split('/')
        if date.lower() == 'today':
            current_time = time.localtime()
            savedate = time.strftime("%Y-%m-%d", current_time)
        else:
            try:
                savedate = time.strptime(date, "%d/%m/%Y")
                savedate = time.strftime("%Y-%m-%d", savedate)
            except ValueError:
                await ctx.response.send_message(f'Invalid date: {date}\nMake sure to use a possible date.', ephemeral=True)
                return
            except TypeError:
                await ctx.response.send_message(f'Invalid date: {date}\nUse the form `dd/mm/yyyy`', ephemeral=True)
                return

        set = number

        # Add train to the list
        id = addBus(ctx.user.name, set, type, savedate, line, start.title(), end.title(), operator.title())
        await ctx.response.send_message(f"Added bus on route {line} on {savedate} from {start.title()} to {end.title()} with bus number {set} ({type}) Operator: {operator} to your file. (Log ID `#{id}`)")
        
                
    # Run in a separate task
    asyncio.create_task(log())
    
 # Perth Train logger
# NOT FINISHED   
'''@trainlogs.command(name="add-perth-train", description="Log a Transperth Train you have been on")
@app_commands.describe(number = "Carrige Number", type = 'Type of train', date = "Date in DD/MM/YYYY format", line = 'Light Rail Line', start='Starting Stop', end = 'Ending Stop')
@app_commands.autocomplete(start=NSWstation_autocompletion)
@app_commands.autocomplete(end=NSWstation_autocompletion)
@app_commands.choices(line=[
        app_commands.Choice(name="Fremantle line", value="Fremantle line"),
        app_commands.Choice(name="Midland line", value="Midland line"),
        app_commands.Choice(name="Armadale line", value="Armadale line"),
        app_commands.Choice(name="Joondalup line", value="Joondalup line"),
        app_commands.Choice(name="Thornlie line", value="Thornlie line"),
        app_commands.Choice(name="Mandurah line", value="Mandurah line"),
        app_commands.Choice(name="Airport line", value="Airport line"),
        app_commands.Choice(name="Morley–Ellenbrook line", value="Morley–Ellenbrook line"),
])
@app_commands.choices(type=[
        app_commands.Choice(name="A-series", value="A-series"),
        app_commands.Choice(name="B-series", value="B-series"),
        app_commands.Choice(name="C-series", value="C-series"),
])

async def logPerth(ctx, type:str, line:str, number: str='Unknown', date:str='today', start:str='N/A', end:str='N/A'):
    channel = ctx.channel
    print(date)
    async def log():
        print("logging the perth train")

        savedate = date.split('/')
        if date.lower() == 'today':
            current_time = time.localtime()
            savedate = time.strftime("%Y-%m-%d", current_time)
        else:
            try:
                savedate = time.strptime(date, "%d/%m/%Y")
                savedate = time.strftime("%Y-%m-%d", savedate)
            except ValueError:
                await ctx.response.send_message(f'Invalid date: {date}\nMake sure to use a possible date.', ephemeral=True)
                return
            except TypeError:
                await ctx.response.send_message(f'Invalid date: {date}\nUse the form `dd/mm/yyyy`', ephemeral=True)
                return

        # idk how to get nsw train set numbers i cant find a list of all sets pls help
        set = number
        if set == None:
            await ctx.response.send_message(f'Invalid train number: {number.upper()}',ephemeral=True)
            return

        # Add train to the list
        id = addPerthTrain(ctx.user.name, set, type, savedate, line, start.title(), end.title())
        await ctx.response.send_message(f"Added {set} ({type}) on the {line} line on {savedate} from {start.title()} to {end.title()} to your file. (Log ID `#{id}`)")
        
                
    # Run in a separate task
    asyncio.create_task(log())'''

# train logger reader

vLineLines = ['Geelong/Warrnambool', 'Ballarat/Maryborough/Ararat', 'Bendigo/Echuca/Swan Hill','Albury', 'Seymour/Shepparton', 'Traralgon/Bairnsdale']

@trainlogs.command(name="view", description="View logged trips for a user")
@app_commands.describe(user = "Who do you want to see the data of?", mode = 'Train or tram logs?')
@app_commands.choices(mode=[
        app_commands.Choice(name="Train VIC", value="train"),
        app_commands.Choice(name="Tram VIC", value="tram"),
        app_commands.Choice(name="Bus", value="bus"),
        app_commands.Choice(name="Train NSW", value="sydney-trains"),
        app_commands.Choice(name="Tram NSW", value="sydney-trams"),
])

async def userLogs(ctx, mode:str='train', user: discord.User=None, id:str=None):
    async def sendLogs():
        if user == None:
                userid = ctx.user
        else:
            userid = user
            
        if id != None:
            
            if mode == 'train':
                file_path = f'utils/trainlogger/userdata/{userid.name}.csv'
                
            if mode == 'tram':
                file_path = f'utils/trainlogger/userdata/tram/{userid.name}.csv'
            
            if mode == 'bus':
                file_path = f'utils/trainlogger/userdata/bus/{userid.name}.csv'  
                
            if mode == 'sydney-trains':
                file_path = f'utils/trainlogger/userdata/sydney-trains/{userid.name}.csv'  
            if mode == 'sydney-trams':
                file_path = f'utils/trainlogger/userdata/sydney-trams/{userid.name}.csv'  
                
            
            
            with open(file_path, mode='r', newline='') as file:
                
                if not id.startswith('#'):
                    cleaned_id = '#' + id
                else:
                    cleaned_id = id
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    if row[0] == cleaned_id.upper():
                        
                        # thing to find image:
                        if row[2] == 'Tait':
                            image = 'https://railway-photos.xm9g.xyz/photos/317M-6.jpg'
                        else:
                            hyphen_index = row[1].find("-")
                            if hyphen_index != -1:
                                first_car = row[1][:hyphen_index]
                                print(f'First car: {first_car}')
                                image = getImage(first_car)
                                if image == None:
                                    last_hyphen = row[1].rfind("-")
                                    if last_hyphen != -1:
                                        last_car = row[1][last_hyphen + 1 :]  # Use last_hyphen instead of hyphen_index
                                        print(f'Last car: {last_car}')
                                        image = getImage(last_car)
                                        if image == None:
                                            image = getImage(row[2])
                                            print(f'the loco number is: {row[1]}')
                                        
                            # Make the embed
                        if row[4] in vLineLines:
                            embed = discord.Embed(title=f"Log {row[0]}",colour=0x7e3e98)
                        elif row[4] == 'Unknown':
                                embed = discord.Embed(title=f"Log {row[0]}")
                        else:
                            try:
                                embed = discord.Embed(title=f"Log `{row[0]}`",colour=lines_dictionary[row[4]][1])
                            except:
                                embed = discord.Embed(title=f'Log `{id}`')
                        embed.add_field(name=f'Set', value="{} ({})".format(row[1], row[2]))
                        embed.add_field(name=f'Line', value="{}".format(row[4]))
                        embed.add_field(name=f'Date', value="{}".format(row[3]))
                        embed.add_field(name=f'Trip', value=f"{row[5]} to {row[6]}")
                        if row[5] != 'N/A' and row[6] != 'N/A':
                            embed.add_field(name='Distance:', value=f'{round(getStationDistance(load_station_data("utils/trainlogger/stationDistances.csv"), row[5], row[6]))}km')
                        try:
                            embed.set_thumbnail(url=image)
                        except:
                            print('no image')
                        await ctx.response.send_message(embed=embed)
                await ctx.response.send_message(f'Cannot find log `{id}`')
                
        else:
            # for train
            if mode == 'train':
                if user == None:
                    userid = ctx.user
                else:
                    userid = user
                
                try:
                    file = discord.File(f'utils/trainlogger/userdata/{userid.name}.csv')
                except FileNotFoundError:
                    if userid == ctx.user:
                        await ctx.response.send_message("You have no trains logged!",ephemeral=True)
                    else:
                        await ctx.response.send_message("This user has no trains logged!",ephemeral=True)
                    return
                print(userid.name)
                data = readLogs(userid.name)
                if data == 'no data':
                    if userid == ctx.user:
                        await ctx.response.send_message("You have no trains logged!",ephemeral=True)
                    else:
                        await ctx.response.send_message("This user has no trains logged!",ephemeral=True)
                    return
            
                # create thread
                try:
                    logsthread = await ctx.channel.create_thread(
                        name=f'{userid.name}\'s Train Logs',
                        auto_archive_duration=60,
                        type=discord.ChannelType.public_thread
                    )
                except Exception as e:
                    await ctx.response.send_message(f"Cannot create thread! Ensure the bot has permission to create threads and that you aren't running this in another thread or DM.\n Error: `{e}`")
                    
                # send reponse message
                pfp = ctx.user.avatar.url
                embed=discord.Embed(title='Train Logs', colour=0x7e3e98)
                embed.set_author(name=ctx.user.name, url='https://comeng.xm9g.xyz', icon_url=pfp)
                embed.add_field(name='Click here to view your logs:', value=f'<#{logsthread.id}>')
                await ctx.response.send_message(embed=embed)
                await logsthread.send(f'# <:train:1241164967789727744> {userid.name}\'s CSV file', file=file)
                await logsthread.send(f'# {userid.name}\'s Train Logs')
                formatted_data = ""
                for sublist in data:
                    if len(sublist) >= 7:  # Ensure the sublist has enough items
                        image = None
                        
                        # thing to find image:
                        hyphen_index = sublist[1].find("-")
                        if hyphen_index != -1:
                            first_car = sublist[1][:hyphen_index]
                            print(f'First car: {first_car}')
                            image = getImage(first_car)
                            if image == None:
                                last_hyphen = sublist[1].rfind("-")
                                if last_hyphen != -1:
                                    last_car = sublist[1][last_hyphen + 1 :]  # Use last_hyphen instead of hyphen_index
                                    print(f'Last car: {last_car}')
                                    image = getImage(last_car)
                                    if image == None:
                                        image = getImage(sublist[2])
                                        print(f'the loco number is: {sublist[1]}')
                                        
                        #send in thread to reduce spam!
                            # Make the embed
                        if sublist[4] in vLineLines:
                            embed = discord.Embed(title=f"Log `{sublist[0]}`",colour=0x7e3e98)
                        elif sublist[4] == 'Unknown':
                                embed = discord.Embed(title=f"Log `{sublist[0]}`")
                        else:
                            try:
                                embed = discord.Embed(title=f"Log `{sublist[0]}`",colour=lines_dictionary[sublist[4]][1])
                            except:
                                embed = discord.Embed(title=f"Log {sublist[0]}")
                        embed.add_field(name=f'Set', value="{} ({})".format(sublist[1], sublist[2]))
                        embed.add_field(name=f'Line', value="{}".format(sublist[4]))
                        embed.add_field(name=f'Date', value="{}".format(sublist[3]))
                        embed.add_field(name=f'Trip Start', value="{}".format(sublist[5]))
                        embed.add_field(name=f'Trip End', value="{}".format(sublist[6]))
                        if sublist[5] != 'N/A' and sublist[6] != 'N/A':
                            embed.add_field(name='Distance:', value=f'{round(getStationDistance(load_station_data("utils/trainlogger/stationDistances.csv"), sublist[5], sublist[6]))}km')
                        try:
                            embed.set_thumbnail(url=image)
                        except:
                            print('no image')
                        
                        await logsthread.send(embed=embed)
                        # if count == 6:
                        #     await ctx.channel.send('Max of 5 logs can be sent at a time. Use the csv option to see all logs')
                        #     return
            # for tram:
            if mode == 'tram':
                if user == None:
                    userid = ctx.user
                else:
                    userid = user
                
                try:
                    file = discord.File(f'utils/trainlogger/userdata/tram/{userid.name}.csv')
                except FileNotFoundError:
                    if userid == ctx.user:
                        await ctx.response.send_message("You have no trams logged!",ephemeral=True)
                    else:
                        await ctx.response.send_message("This user has no trams logged!",ephemeral=True)
                    return
                print(userid.name)
                data = readTramLogs(userid.name)
                if data == 'no data':
                    if userid == ctx.user:
                        await ctx.response.send_message("You have no trams logged!",ephemeral=True)
                    else:
                        await ctx.response.send_message("This user has no trams logged!",ephemeral=True)
                    return
            
                # create thread
                logsthread = await ctx.channel.create_thread(
                    name=f'{userid.name}\'s Tram Logs',
                    auto_archive_duration=60,
                    type=discord.ChannelType.public_thread
                )
                
                # send reponse message
                await ctx.response.send_message(f"Logs will be sent in <#{logsthread.id}>")
                await logsthread.send(f'# {userid.name}\'s CSV file', file=file)
                await logsthread.send(f' #<:tram:1241165701390012476> {userid.name}\'s Tram Logs')
                formatted_data = ""
                for sublist in data:
                    if len(sublist) >= 7:  # Ensure the sublist has enough items
                        image = None
                        
                        # # thing to find image:
                        # hyphen_index = sublist[1].find("-")
                        # if hyphen_index != -1:
                        #     first_car = sublist[1][:hyphen_index]
                        #     print(f'First car: {first_car}')
                        #     image = getImage(first_car)
                        #     if image == None:
                        #         last_hyphen = sublist[1].rfind("-")
                        #         if last_hyphen != -1:
                        #             last_car = sublist[1][last_hyphen + 1 :]  # Use last_hyphen instead of hyphen_index
                        #             print(f'Last car: {last_car}')
                        #             image = getImage(last_car)
                        #             if image == None:
                        #                 image = getImage(sublist[2])
                        #                 print(f'the loco number is: {sublist[1]}')
                                        
                        #send in thread to reduce spam!
                        thread = await ctx.channel.create_thread(name=f"{userid.name}'s logs")
                            # Make the embed
                        if sublist[4] in vLineLines:
                            embed = discord.Embed(title=f"Log {sublist[0]}",colour=0x7e3e98)
                        elif sublist[4] == 'Unknown':
                            embed = discord.Embed(title=f"Log {sublist[0]}")
                        else:
                            embed = discord.Embed(title=f"Log {sublist[0]}",colour=0x71bf44)
                        embed.add_field(name=f'Set', value="{} ({})".format(sublist[1], sublist[2]))
                        embed.add_field(name=f'Line', value="{}".format(sublist[4]))
                        embed.add_field(name=f'Date', value="{}".format(sublist[3]))
                        embed.add_field(name=f'Trip Start', value="{}".format(sublist[5]))
                        embed.add_field(name=f'Trip End', value="{}".format(sublist[6]))
                        # embed.set_thumbnail(url=image)

                        await logsthread.send(embed=embed)
                        time.sleep(0.5)
            
            # for sydney light rail tram:
            if mode == 'sydney-trams':
                if user == None:
                    userid = ctx.user
                else:
                    userid = user
                
                try:
                    file = discord.File(f'utils/trainlogger/userdata/sydney-trams/{userid.name}.csv')
                except FileNotFoundError:
                    if userid == ctx.user:
                        await ctx.response.send_message("You have no trams logged!",ephemeral=True)
                    else:
                        await ctx.response.send_message("This user has no trams logged!",ephemeral=True)
                    return
                print(userid.name)
                data = readSydneyLightRailLogs(userid.name)
                if data == 'no data':
                    if userid == ctx.user:
                        await ctx.response.send_message("You have no trams logged!",ephemeral=True)
                    else:
                        await ctx.response.send_message("This user has no trams logged!",ephemeral=True)
                    return
            
                # create thread
                logsthread = await ctx.channel.create_thread(
                    name=f'{userid.name}\'s Sydney Light Rail Logs',
                    auto_archive_duration=60,
                    type=discord.ChannelType.public_thread
                )
                
                # send reponse message
                await ctx.response.send_message(f"Logs will be sent in <#{logsthread.id}>")
                await logsthread.send(f'# {userid.name}\'s CSV file', file=file)
                await logsthread.send(f'# {userid.name}\'s Light Rail Logs')
                formatted_data = ""
                for sublist in data:
                    if len(sublist) >= 7:  # Ensure the sublist has enough items
                        image = None
                                        
                        #send in thread to reduce spam!
                        thread = await ctx.channel.create_thread(name=f"{userid.name}'s logs")
                            # Make the embed

                        if sublist[4] == 'Unknown':
                            embed = discord.Embed(title=f"Log {sublist[0]}")
                        else:
                            embed = discord.Embed(title=f"Log {sublist[0]}",colour=0xed2438)
                        embed.add_field(name=f'Set', value="{} ({})".format(sublist[1], sublist[2]))
                        embed.add_field(name=f'Line', value="{}".format(sublist[4]))
                        embed.add_field(name=f'Date', value="{}".format(sublist[3]))
                        embed.add_field(name=f'Trip Start', value="{}".format(sublist[5]))
                        embed.add_field(name=f'Trip End', value="{}".format(sublist[6]))

                        await logsthread.send(embed=embed)
                        time.sleep(0.5) 
            
            # for nsw train:
            if mode == 'sydney-trains':
                if user == None:
                    userid = ctx.user
                else:
                    userid = user
                
                try:
                    file = discord.File(f'utils/trainlogger/userdata/sydney-trains/{userid.name}.csv')
                except FileNotFoundError:
                    if userid == ctx.user:
                        await ctx.response.send_message("You have no trains logged!",ephemeral=True)
                    else:
                        await ctx.response.send_message("This user has no trains logged!",ephemeral=True)
                    return
                print(userid.name)
                data = readSydneyTrainLogs(userid.name)
                if data == 'no data':
                    if userid == ctx.user:
                        await ctx.response.send_message("You have no trains logged!",ephemeral=True)
                    else:
                        await ctx.response.send_message("This user has no trains logged!",ephemeral=True)
                    return
            
                # create thread
                logsthread = await ctx.channel.create_thread(
                    name=f'{userid.name}\'s NSW Train Logs',
                    auto_archive_duration=60,
                    type=discord.ChannelType.public_thread
                )
                
                # send reponse message
                await ctx.response.send_message(f"Logs will be sent in <#{logsthread.id}>")
                await logsthread.send(f'# {userid.name}\'s CSV file', file=file)
                await logsthread.send(f'# <:NSWTrains:1255084911103184906>  {userid.name}\'s NSW Train Logs')
                formatted_data = ""
                for sublist in data:
                    if len(sublist) >= 7:  # Ensure the sublist has enough items
                        image = None
                                        
                        #send in thread to reduce spam!
                        thread = await ctx.channel.create_thread(name=f"{userid.name}'s logs")
                            # Make the embed
                        if sublist[4] in vLineLines:
                            embed = discord.Embed(title=f"Log {sublist[0]}",colour=0x7e3e98)
                        elif sublist[4] == 'Unknown':
                            embed = discord.Embed(title=f"Log {sublist[0]}")
                        else:
                            embed = discord.Embed(title=f"Log {sublist[0]}",colour=0xf47913)
                        embed.add_field(name=f'Set', value="{} ({})".format(sublist[1], sublist[2]))
                        embed.add_field(name=f'Line', value="{}".format(sublist[4]))
                        embed.add_field(name=f'Date', value="{}".format(sublist[3]))
                        embed.add_field(name=f'Trip Start', value="{}".format(sublist[5]))
                        embed.add_field(name=f'Trip End', value="{}".format(sublist[6]))

                        await logsthread.send(embed=embed)
                        time.sleep(0.5)     
            
            # for bus:
            if mode == 'bus':
                if user == None:
                    userid = ctx.user
                else:
                    userid = user
                
                try:
                    file = discord.File(f'utils/trainlogger/userdata/bus/{userid.name}.csv')
                except FileNotFoundError:
                    if userid == ctx.user:
                        await ctx.response.send_message("You have no busses logged!",ephemeral=True)
                    else:
                        await ctx.response.send_message("This user has no busses logged!",ephemeral=True)
                    return
                print(userid.name)
                data = readBusLogs(userid.name)
                if data == 'no data':
                    if userid == ctx.user:
                        await ctx.response.send_message("You have no busses logged!",ephemeral=True)
                    else:
                        await ctx.response.send_message("This user has no busses logged!",ephemeral=True)
                    return
            
                # create thread
                logsthread = await ctx.channel.create_thread(
                    name=f'{userid.name}\'s Bus Logs',
                    auto_archive_duration=60,
                    type=discord.ChannelType.public_thread
                )
                
                # send reponse message
                await ctx.response.send_message(f"Logs will be sent in <#{logsthread.id}>")
                await logsthread.send(f'# {userid.name}\'s CSV file', file=file)
                await logsthread.send(f' # <:bus:1241165769241530460> {userid.name}\'s Bus Logs')
                formatted_data = ""
                for sublist in data:
                    if len(sublist) >= 7:  # Ensure the sublist has enough items
                        image = None
                                                
                        #send in thread to reduce spam!
                        thread = await ctx.channel.create_thread(name=f"{userid.name}'s bus logs")
                            # Make the embed
                        if sublist[4] == 'Unknown':
                            embed = discord.Embed(title=f"Log {sublist[0]}")
                        else:
                            embed = discord.Embed(title=f"Log {sublist[0]}",colour=0xf68a24)
                        embed.add_field(name=f'Route', value="{}".format(sublist[4]))
                        embed.add_field(name=f'Date', value="{}".format(sublist[3]))
                        embed.add_field(name=f'Trip Start', value="{}".format(sublist[5]))
                        embed.add_field(name=f'Trip End', value="{}".format(sublist[6]))
                        embed.add_field(name=f'Operator', value="{}".format(sublist[7]))
                        embed.add_field(name=f'Bus Number', value="{} ({})".format(sublist[1], sublist[2]))
                        # embed.set_thumbnail(url=image)
    
                        await logsthread.send(embed=embed)
                        time.sleep(0.5)  
    asyncio.create_task(sendLogs())

# train logger stats
@trainlogs.command(name="stats", description="View stats for a logged user's trips.")
@app_commands.describe(stat='Type of stats to view', user='Who do you want to see the data of?', format='Diffrent ways and graphs for showing the data.', mode='Train or Tram logs?')
@app_commands.choices(stat=[
    app_commands.Choice(name="Lines", value="lines"),
    app_commands.Choice(name="Stations", value="stations"),
    app_commands.Choice(name="Trips", value="pairs"),
    app_commands.Choice(name="Trip Length (VIC train only)", value="length"),
    app_commands.Choice(name="Sets", value="sets"),
    app_commands.Choice(name="Dates", value="dates"),
    app_commands.Choice(name="Types", value="types"),
    app_commands.Choice(name="Operators", value="operators"),
])
@app_commands.choices(format=[
    app_commands.Choice(name="List and Bar chart", value="l&g"),
    app_commands.Choice(name="Pie chart", value="pie"),
    app_commands.Choice(name="CSV file", value="csv"),
    app_commands.Choice(name="Daily Chart", value="daily"),
])
@app_commands.choices(mode=[
    app_commands.Choice(name="All", value="all"),
    # app_commands.Choice(name="All Trains", value="all-trains"),
    # app_commands.Choice(name="All Trams", value="all-trams"),

    app_commands.Choice(name="Train VIC", value="train"),
    app_commands.Choice(name="Tram VIC", value="tram"),
    app_commands.Choice(name="Bus", value="bus"),
    app_commands.Choice(name="Train NSW", value="sydney-trains"),
    app_commands.Choice(name="Tram NSW", value="sydney-trams"),
])
async def statTop(ctx: discord.Interaction, stat: str, format: str='l&g', global_stats:bool=False, user: discord.User = None, mode:str = 'all'):
    async def sendLogs():
        statSearch = stat
        userid = user if user else ctx.user
        
        if userid.name == 'comeng_17':
            name = 'comeng17'
        else:
            name = userid
            
        if global_stats:
            data = globalTopStats(statSearch)
        else:
            try:
                if stat == 'operators':
                    data = topOperators(userid.name)
                elif stat == 'length':
                    data = getLongestTrips(userid.name)  
                elif mode == 'train':
                    data = topStats(userid.name, statSearch)
                elif mode == 'tram':
                    data = tramTopStats(userid.name, statSearch)   
                elif mode == 'sydney-trains':
                    data = sydneyTrainTopStats(userid.name, statSearch)    
                elif mode == 'sydney-trams':
                    data = sydneyTramTopStats(userid.name, statSearch)  
                elif mode == 'bus':
                    data = busTopStats(userid.name, statSearch)  
                elif mode == 'all':
                    data = allTopStats(userid.name, statSearch) 
            except:
                await ctx.response.send_message('You have no logged trips!')
        count = 1
        message = ''
        
        # top operators thing:
        if stat == 'operators':
            try:
                pieChart(data, f'Top Operators ― {name}', ctx.user.name)
                await ctx.response.send_message(message, file=discord.File(f'temp/Graph{ctx.user.name}.png'))
            except:
                await ctx.response.send_message('User has no logs!')  
        if stat == 'length':
            try:
                lines = data.splitlines()
                chunks = []
                current_chunk = ""
                await ctx.response.send_message('Here are your longest trips:')

                for line in lines:
                    # Check if adding this line would exceed the max_length
                    if len(current_chunk) + len(line) + 1 > 1500:  # +1 for the newline character
                        chunks.append(current_chunk)
                        current_chunk = line
                    else:
                        if current_chunk:
                            current_chunk += "\n" + line
                        else:
                            current_chunk = line

                # Add the last chunk
                if current_chunk:
                    chunks.append(current_chunk)
                    
                for i, chunk in enumerate(chunks):
                    await ctx.channel.send(chunk)
                
            except Exception as e:
                await ctx.response.send_message(f"Error: `{e}`")
                
        # make temp csv
        csv_filename = f'temp/top{stat.title()}.{userid}-t{time.time()}.csv'
        with open(csv_filename, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)  # Use csv.writer on csv_file, not csvs
            for item in data:
                station, times = item.split(': ')
                writer.writerow([station, times.split()[0]])
        
        if format == 'csv':
            try:
                await ctx.response.send_message("Here is your file:", file=discord.File(csv_filename))
            except:
                ctx.response.send_message('You have no logs!')
            
        elif format == 'l&g':
            await ctx.response.send_message('Here are your stats:')
            for item in data:
                station, times = item.split(': ')
                message += f'{count}. **{station}:** `{times}`\n'
                count += 1
                if len(message) > 1900:
                    await ctx.channel.send(message)
                    message = ''
            try:
                if global_stats:
                    barChart(csv_filename, stat.title(), f'Top {stat.title()} ― Global', ctx.user.name)
                else:
                    barChart(csv_filename, stat.title(), f'Top {stat.title()} ― {name}', ctx.user.name)
                await ctx.channel.send(message, file=discord.File(f'temp/Graph{ctx.user.name}.png'))
            except:
                await ctx.channel.send('User has no logs!')
        elif format == 'pie':
            try:
                if global_stats:
                    pieChart(csv_filename, f'Top {stat.title()} ― {name}', ctx.user.name)
                else:
                    pieChart(csv_filename, f'Top {stat.title()} ― Global', ctx.user.name)

                await ctx.response.send_message(file=discord.File(f'temp/Graph{ctx.user.name}.png'))
            except:
                await ctx.response.send_message('You have no logs!')
        elif format == 'daily':
            if stat != 'dates':
                await ctx.response.send_message('Daily chart can only be used with the stat set to Top Dates')
            try:
                dayChart(csv_filename, ctx.user.name)
                await ctx.response.send_message(file=discord.File(f'temp/Graph{ctx.user.name}.png'))
            except:
                ctx.response.send_message('User has no logs!')
    await sendLogs()
   
@stats.command(name='sets', description='View which sets you have been on')
@app_commands.choices(train=[
    app_commands.Choice(name="X'Trapolis 100", value="X'Trapolis 100"),
    app_commands.Choice(name="Comeng", value="Comeng"),
    app_commands.Choice(name="Siemens Nexas", value="Siemens Nexas"),
    app_commands.Choice(name="HCMT", value="HCMT"),
    app_commands.Choice(name='VLocity', value='VLocity'),
    app_commands.Choice(name='Sprinter', value='Sprinter'),
    app_commands.Choice(name='N Class', value='N Class'),
])
async def sets(ctx, train:str):
    data =setlist(ctx.user.name, train)
    
    if len(data) <= 2000:
        await ctx.response.send_message(data)
    else:
        await ctx.response.send_message(f"{train} sets you have been on:")
        split_strings = []
        start = 0
        
        while start < len(data):
            # Find the index where the string should be split
            if start + 2000 < len(data):
                split_index = data.rfind('\n', start, start + 2000)
                if split_index == -1:
                    split_index = start + 2000
            else:
                split_index = len(data)
            
            split_strings.append(data[start:split_index])
            start = split_index + 1  # Move past the newline or split point
            
        for item in split_strings:
            await ctx.channel.send(item)

   
@bot.tree.command(name='submit-photo', description="Submit a photo to railway-photos.xm9g.xyz and the bot.")
async def submit(ctx: discord.Interaction, photo: discord.Attachment, car_number: str, date: str, location: str):
    async def submitPhoto():
        target_guild_id = 1214139268725870602
        target_channel_id = 1238821549352685568
        
        target_guild = bot.get_guild(target_guild_id)
        if target_guild:
            channel = target_guild.get_channel(target_channel_id)
            if channel:
                if photo.content_type.startswith('image/'):
                    await photo.save(f"./photo-submissions/{photo.filename}")
                    file = discord.File(f"./photo-submissions/{photo.filename}")
                    await ctx.response.send_message('Your photo has been submitted and will be reviewed shortly!\nSubmitted photos can be used in their original form with proper attribution to represent trains, trams, groupings, stations, and stops. They will be featured on the Discord bot and on https://railway-photos.xm9g.xyz.', ephemeral=True)
                    await channel.send(f'# Photo submitted by <@{ctx.user.id}>:\n- Number {car_number}\n- Date: {date}\n- Location: {location}\n<@780303451980038165> ', file=file)
                else:
                    await ctx.response.send_message("Please upload a valid image file.", ephemeral=True)
            else:
                await ctx.response.send_message("Error: Target channel not found.", ephemeral=True)
        else:
            await ctx.response.send_message("Error: Target guild not found.", ephemeral=True)

    await submitPhoto()
    
@stats.command(name='profile', description="Shows a users trip log stats, and leaderboard wins")    
async def profile(ctx, user: discord.User = None):
    async def profiles():
        if user == None:
            username = ctx.user.name
        else:
            username = user.name
        pfp = ctx.user.avatar.url
        embed = discord.Embed(title=f"Profile")
        embed.set_author(name=username, url='https://comeng.xm9g.xyz',
                     icon_url=pfp)

        
        # train logger
        try:
            lines = topStats(username, 'lines')
            stations = topStats(username, 'stations')
            sets = topStats(username, 'sets')
            trains = topStats(username, 'types')
            dates = topStats(username, 'dates')
            trips = topStats(username, 'pairs')

            #other stats stuff:
            eDate =lowestDate(username, 'train')
            LeDate =highestDate(username, 'train')
            joined = convert_iso_to_unix_time(f"{eDate}T00:00:00Z") 
            last = convert_iso_to_unix_time(f"{LeDate}T00:00:00Z")
            embed.add_field(name='<:train:1241164967789727744><:vline:1241165814258729092> Train Log Stats:', value=f'**Top Line:** {lines[0]}\n**Top Station:** {stations[0]}\n**Top Train:** {trains[0]}\n**Top Set:** {sets[0]}\n**Top Date:** {dates[0]}\n**Top Trip:** {trips[0]}\n\nUser started logging {joined}\nLast log {last}\n**Total logs:** `{logAmounts(username, "train")}`\n**Stations visited:** `{stationPercent(username)}`\n**Lines visited:** `{linePercent(username)}`\n**Distance:** `{round(getTotalTravelDistance(username))}km`')
                        
        except FileNotFoundError:
            embed.add_field(name="<:train:1241164967789727744><:vline:1241165814258729092> Train Log Stats", value=f'{username} has no logged trips!')
                   
        # Tram Logger
        try:
            lines = tramTopStats(username, 'lines')
            stations = tramTopStats(username, 'stations')
            sets = tramTopStats(username, 'sets')
            trains = tramTopStats(username, 'types')
            dates = tramTopStats(username, 'dates')
            
            #other stats stuff:
            eDate =lowestDate(username, 'tram')
            LeDate =highestDate(username, 'tram')
            joined = convert_iso_to_unix_time(f"{eDate}T00:00:00Z") 
            last = convert_iso_to_unix_time(f"{LeDate}T00:00:00Z")
            embed.add_field(name='<:tram:1241165701390012476> Tram Log Stats:', value=f'**Top Route:** {lines[0]}\n**Top Stop:** {stations[0]}\n**Top Class:** {trains[0]}\n**Top Tram Number:** {sets[0]}\n**Top Date:** {dates[0]}\n\nUser started logging {joined}\nLast log {last}\nTotal logs: {logAmounts(username, "tram")}')
  
        except FileNotFoundError:
            embed.add_field(name="<:tram:1241165701390012476> Tram Log Stats", value=f'{username} has no logged trips!')

 # sydney trains Logger
        try:
            lines = sydneyTrainTopStats(username, 'lines')
            stations = sydneyTrainTopStats(username, 'stations')
            sets = sydneyTrainTopStats(username, 'sets')
            trains = sydneyTrainTopStats(username, 'types')
            dates = sydneyTrainTopStats(username, 'dates')
             #other stats stuff:
            eDate =lowestDate(username, 'sydney-trains')
            LeDate =highestDate(username, 'sydney-trains')
            joined = convert_iso_to_unix_time(f"{eDate}T00:00:00Z") 
            last = convert_iso_to_unix_time(f"{LeDate}T00:00:00Z")
            embed.add_field(name='<:NSWTrains:1255084911103184906><:NSWMetro:1255084902748000299> Train Log Stats:', value=f'**Top Line:** {lines[0]}\n**Top Station:** {stations[0]}\n**Top Type:** {trains[0]}\n**Top Train Number:** {sets[0]}\n**Top Date:** {dates[0]}\n\nUser started logging {joined}\nLast log {last}\nTotal logs: {logAmounts(username, "sydney-trains")}')
                                  
        except FileNotFoundError:
            embed.add_field(name="<:NSWTrains:1255084911103184906><:NSWMetro:1255084902748000299> Train Log Stats", value=f'{username} has no logged trips in NSW!')

# sydney tram Logger
        try:
            lines = sydneyTramTopStats(username, 'lines')
            stations = sydneyTramTopStats(username, 'stations')
            sets = sydneyTramTopStats(username, 'sets')
            trains = sydneyTramTopStats(username, 'types')
            dates = sydneyTramTopStats(username, 'dates')
             #other stats stuff:
            eDate =lowestDate(username, 'sydney-trams')
            LeDate =highestDate(username, 'sydney-trams')
            joined = convert_iso_to_unix_time(f"{eDate}T00:00:00Z") 
            last = convert_iso_to_unix_time(f"{LeDate}T00:00:00Z")
            embed.add_field(name='<:NSWLightRail:1255084906053369856> Light Rail Log Stats:', value=f'**Top Line:** {lines[0]}\n**Top Station:** {stations[0]}\n**Top Type:** {trains[0]}\n**Top Tram Number:** {sets[0]}\n**Top Date:** {dates[0]}\n\nUser started logging {joined}\nLast log {last}\nTotal logs: {logAmounts(username, "sydney-trams")}')
                                  
        except FileNotFoundError:
            embed.add_field(name="<:NSWLightRail:1255084906053369856> Light Rail Log Stats", value=f'{username} has no logged trips in NSW!')
            
# bus Logger
        try:
            lines = busTopStats(username, 'lines')
            stations = busTopStats(username, 'stations')
            sets = busTopStats(username, 'sets')
            trains = busTopStats(username, 'types')
            dates = busTopStats(username, 'dates')
             #other stats stuff:
            eDate =lowestDate(username, 'bus')
            LeDate =highestDate(username, 'bus')
            joined = convert_iso_to_unix_time(f"{eDate}T00:00:00Z") 
            last = convert_iso_to_unix_time(f"{LeDate}T00:00:00Z")
            embed.add_field(name='<:bus:1241165769241530460><:coach:1241165858274021489><:skybus:1241165983083925514><:NSW_Bus:1264885653922123878><:Canberra_Bus:1264885650826465311> Bus Log Stats:', value=f'**Top Route:** {lines[0]}\n**Top Stop:** {stations[0]}\n**Top Type:** {trains[0]}\n**Top Bus Number:** {sets[0]}\n**Top Date:** {dates[0]}\n\nUser started logging {joined}\nLast log {last}\nTotal logs: {logAmounts(username, "bus")}')
                                  
        except FileNotFoundError:
            embed.add_field(name="<:bus:1241165769241530460><:coach:1241165858274021489><:skybus:1241165983083925514><:NSW_Bus:1264885653922123878><:Canberra_Bus:1264885650826465311> Bus Log Stats", value=f'{username} has no logged bus trips.')

        
        #games
        stats = fetchUserStats(username)
        
        if stats[0] != 'no stats':
            item, wins, losses = stats[0]
            embed.add_field(name=':question: Station Guesser', value=f'Wins: {str(wins)}\nLosses: {str(losses)}\nAccuracy: {str(round((wins/(wins+losses))*100, 1))}%')
        else:
            embed.add_field(name=':question: Station Guesser', value='No data',inline=False)
        if stats[1] != 'no stats':
            item, wins, losses = stats[1]
            embed.add_field(name=':interrobang: Ultrahard Station Guesser', value=f'Wins: {str(wins)}\nLosses: {str(losses)}\nAccuracy: {str(round((wins/(wins+losses))*100, 1))}%')
        else:
            embed.add_field(name=':interrobang: Ultrahard Station Guesser', value='No data',inline=False)
        if stats[2] != 'no stats':
            item, wins, losses = stats[2]
            embed.add_field(name=':left_right_arrow: Station Order Guesser', value=f'Wins: {str(wins)}\nLosses: {str(losses)}\nAccuracy: {str(round((wins/(wins+losses))*100, 1))}%', inline=False)
        else:
            embed.add_field(name=':left_right_arrow: Station Order Guesser', value='No data',inline=False)
        
        
        await ctx.response.send_message(embed=embed)
        
    await profiles()

# Disabled to not fuck up the data by accident
'''@bot.command()
async def ids(ctx: commands.Context) -> None:
    if ctx.author.id in [707866373602148363,780303451980038165,749835864468619376]:
        checkaddids = addids()
        if checkaddids == 'no userdata folder':
            await ctx.send('Error: No userdata folder found.')
        else:
            await ctx.send('Hexadecimal IDs have been added to all CSV files in the userdata folder.\n**Do not run this command again.**')'''


@bot.command()
@commands.guild_only()
async def sync(ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if ctx.author.id in [707866373602148363,780303451980038165]:
        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await ctx.bot.tree.sync()

            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return

        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException as e:
                print(f'Error: {e}')
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

# imptrant
bot.run(BOT_TOKEN)
