'''TrackPulse Vic
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


from calendar import c
from math import e
from numbers import Number
import operator
from shutil import ExecError
import shutil
import sqlite3
from tracemalloc import stop
from cycler import V
from discord.ext import commands, tasks
from discord import app_commands
import discord
import json
import requests
import asyncio
import threading
from datetime import datetime
import time
import csv
import random
from typing import Literal, Optional
import typing
from re import A
import traceback
import os
import zipfile
from pathlib import Path
import git
import pandas as pd
import builtins

# thing to make it work on all oses
import sys

from commands.NSWsearchtrain import NSWsearchTrainCommand
from commands.logger.logqldtrain import logQLDtrain
from commands.searchPhoto import searchTrainPhoto
from commands.searchtrain import searchTrainCommand
from commands.traintimleyfetcher import getchannelstocheck, seeWhereTrainsAre, trainTimleyFetcherAdd, trainTimleyFetcherList, trainTimleyFetcherRemove
from photosubmissions.manager import addSubmission, getUserID, removeSubmission, returnQueue
from utils.alias import setWebAlias
from utils.aviationAPIs.airportdata import get_airport_data
from utils.aviationAPIs.aircraftphoto import getplaneimage
from utils.game.imageadder import acceptGuesserPhoto
from utils.trainlogger.map.line_coordinates_log_train_map_pre_munnel import getTotalLines_pre_munnel
from utils.trainlogger.map.line_coordinates_log_train_map_post_munnel import getTotalLines_post_munnel
from utils.trainlogger.map.line_coordinates_log_sydney_tram_map import getTotalLines_sydney_tram
from utils.vicrailphotosapi.accepter import acceptPhoto, webAddImage
sys.stdout = sys.__stdout__ 

original_open = builtins.open

original_mkdir = os.mkdir
def custom_mkdir(path, mode=0o777):
    if isinstance(path, str):
        fixed_path = path.replace('\\', os.sep).replace('/', os.sep)
    else:
        fixed_path = str(path).replace('\\', os.sep).replace('/', os.sep)
    # print(f"Creating dir: {fixed_path}", flush=True) 
    return original_mkdir(fixed_path, mode)
os.mkdir = custom_mkdir

original_open = builtins.open
def custom_open(file, *args, **kwargs):
    if isinstance(file, str):
        fixed_path = file.replace('\\', os.sep).replace('/', os.sep)
        # print(f"Opening: {fixed_path}", flush=True)
    else:
        fixed_path = file
    try:
        return original_open(fixed_path, *args, **kwargs)
    except FileNotFoundError as e:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        alt_path = os.path.join(script_dir, fixed_path)
        print(f"Trying alt path: {alt_path}", flush=True)
        try:
            return original_open(alt_path, *args, **kwargs)
        except:
            raise e
builtins.open = custom_open

original_listdir = os.listdir
def custom_listdir(path='.'):
    if isinstance(path, str):
        fixed_path = path.replace('\\', os.sep).replace('/', os.sep)
    else:
        fixed_path = str(path).replace('\\', os.sep).replace('/', os.sep)
    print(f"Listing dir: {fixed_path}", flush=True)
    return original_listdir(fixed_path)
os.listdir = custom_listdir

# Commands imports
from commands.help import helpCommand
from commands.logexport import logExport

# Utils imports
from utils import healthcheck, trainset
from utils.directions import getDirectionName
from utils.downloader import downloader_function
from utils.favourites.viewer import *
from utils.search import *
from utils.colors import *
from utils.stationID import nameToStopID
from utils.stats.stats import *
from utils.pageScraper import *
from utils.trainImage import *
from utils.checktype import *
from utils.rareTrain import *
from utils.montagueAPI import *
from utils.map.map import *
from utils.game.lb import *

# trainlogger imports
from utils.trainlogger.achievements.check import awardAchievement, checkAchievements, checkGameAchievements, checkHangmanAchievements, getAchievementInfo
from utils.trainlogger.main import *
from utils.trainset import *
from utils.trainlogger.stats import *
from utils.trainlogger.ids import *
from utils.trainlogger.map.readlogs import logMap
from utils.trainlogger.map.mapimage import compress, legend
from utils.lines_dictionaries import *
from utils.stationcodes import *
from utils.trainlogger.achievements import *
from utils.trainlogger.graph import *

from utils.unixtime import *
from utils.pastTime import *
from utils.routeName import *
from utils.locationFromNumber import *
from utils.photo import *
from utils.mykipython import *
from utils.myki.savelogin import *
from utils.special.yearinreview import *
from utils.stoppingpattern import *
from utils.locationfromid import *
from utils.stationDisruptions import *
from utils.stats.stats import *
from utils.vlineTrickery import getVlineStopType
import threading




print("""TrackPulse Vic Copyright (C) 2024  Billy Evans
    This program comes with ABSOLUTELY NO WARRANTY.
    This is free software, and you are welcome to redistribute it
    under certain conditions""")

# Load data from text files to lists

file = open('utils\\datalists\\lines.txt','r')
lines_list = []
for line in file:
    line = line.strip()
    lines_list.append(line)
file.close()

file = open('utils\\datalists\\types.txt','r')
types_list = []
for line in file:
    line = line.strip()
    types_list.append(line)
file.close()

file = open('utils\\datalists\\nswstations.txt','r')
NSWstations_list = []
for line in file:
    line = line.strip()
    NSWstations_list.append(line)
file.close()

file = open('utils\\datalists\\nswstops.txt','r')
NSWstops_list = []
for line in file:
    line = line.strip()
    NSWstops_list.append(line)
file.close()

file = open('utils\\datalists\\adelaidestations.txt','r')
Adelaidestations_list = []
for line in file:
    line = line.strip()
    Adelaidestations_list.append(line)
file.close()

file = open('utils\\datalists\\adelaidestops.txt','r')
Adelaidestops_list = []
for line in file:
    line = line.strip()
    Adelaidestops_list.append(line)
file.close()

file = open('utils\\datalists\\adelaidelines.txt','r')
Adelaidelines_list = []
for line in file:
    line = line.strip()
    Adelaidelines_list.append(line)
file.close()

file = open('utils\\datalists\\perthlines.txt','r')
Perthlines_list = []
for line in file:
    line = line.strip()
    Perthlines_list.append(line)
file.close()

file = open('utils\\datalists\\perthstations.txt','r')
Perthstations_list = []
for line in file:
    line = line.strip()
    Perthstations_list.append(line)
file.close()

file = open('utils\\datalists\\busOps.txt','r')
busOps = []
for line in file:
    line = line.strip()
    busOps.append(line)
file.close()

file = open('utils\\datalists\\interchangestations.txt','r')
interchange_stations = []
for line in file:
    line = line.strip()
    interchange_stations.append(line)
file.close()

file = open('utils\\datalists\\autogeneratedptvlists\\metrostops.txt','r')
metro_stops = []
for line in file:
    line = line.strip()
    metro_stops.append(line)
file.close()

file = open('utils\\datalists\\autogeneratedptvlists\\tramstops.txt','r')
tram_stops = []
for line in file:
    line = line.strip()
    tram_stops.append(line)
file.close()

file = open('utils\\datalists\\busroutes.txt','r')
busroutes = []
for line in file:
    line = line.strip()
    if line not in busroutes:
        busroutes.append(line)
file.close()

file = open('utils\\datalists\\autogeneratedptvlists\\busstops.txt','r')
bus_stops = []
for line in file:
    line = line.strip()
    bus_stops.append(line)
file.close()

file = open('utils\\datalists\\autogeneratedptvlists\\vlinestops.txt','r')
vline_stops = []
for line in file:
    line = line.strip()
    vline_stops.append(line)
file.close()

file = open('utils\\datalists\\heritagestations.txt','r')
heritage_stations = []
for line in file:
    line = line.strip()
    heritage_stations.append(line)
file.close()

# Create lists of stops
metro_stations = metro_stops
metro_stations = [station.replace(' Station','') for station in metro_stations]

vline_stations = []
for stop in vline_stops:
    if stop.endswith(" Railway Station"):
        vline_stations.append(stop.replace(' Railway Station',''))

metro_tunnel_stations = ['Town Hall','Arden','Anzac','Parkville','State Library']
stations_list = metro_stations + vline_stations + metro_tunnel_stations + heritage_stations
stations_list = sorted(set(stations_list))

vline_coach_stops = []
for stop in vline_stops:
    if not stop.endswith(" Railway Station"):
        vline_coach_stops.append(stop)
ptv_list = metro_stops + vline_stops + tram_stops + bus_stops
ptv_list = sorted(set(ptv_list))

ptv_list_short = metro_stops + tram_stops + bus_stops
ptv_list_short = sorted(set(ptv_list_short))

bus_coach_stops = bus_stops + vline_coach_stops
bus_coach_stops = sorted(set(bus_coach_stops))

# Create required folders cause their not on github
required_folders = ['utils/trainlogger/userdata','temp','cache','utils/trainlogger/userdata/adelaide-trains','utils/trainlogger/userdata/adelaide-trams','utils/trainlogger/userdata/sydney-trains','utils/trainlogger/userdata/sydney-trams','utils/trainlogger/userdata/canberra-trams','utils/trainlogger/userdata/perth-trains','utils/trainlogger/userdata/bus','utils/trainlogger/userdata/tram',
                    'utils/trainlogger/achievements/data','utils/train/images','utils/game/images','utils/game/scores','photosubmissions','logins','utils/favourites/data', 'utils/trainlogger/userdata/flights', 'utils/schedule/history', 'cache']
for folder in required_folders:
    if os.path.exists(folder) and os.path.isdir(folder):
        print(f"{folder} exists")
    else:
        os.makedirs(folder)    
        print(f'Created {folder}')


#V/Line Rail Lines
vLineLines = ['Geelong','Warrnambool', 'Ballarat', 'Maryborough', 'Ararat', 'Bendigo','Echuca', 'Swan Hill','Albury', 'Seymour', 'Shepparton', 'Traralgon', 'Bairnsdale']
vline_rail_lines = [1706, 1837, 1823, 1728, 1740, 1849, 1745, 4871, 1710, 1908, 1848, 1824, 1853]


# ENV READING
config = dotenv_values(".env")

BOT_TOKEN = config['BOT_TOKEN']
STARTUP_CHANNEL_ID = int(config['STARTUP_CHANNEL_ID']) # channel id to send the startup message
RARE_SERVICE_CHANNEL_ID = int(config['RARE_SERVICE_CHANNEL_ID'])
USER_ID = config['USER_ID']

CITY_ROLE_PANEL_ENABLED = config.get('CITY_ROLE_PANEL_ENABLED', 'OFF') == 'ON'
CITY_ROLE_CHANNEL_ID = int(config.get('CITY_ROLE_CHANNEL_ID', str(STARTUP_CHANNEL_ID)))
CITY_ROLE_ID = int(config.get('CITY_ROLE_ID', '0'))
CITY_ROLE_PANEL_CUSTOM_ID = 'city_role_panel_claim_v1'
CITY_ROLE_PANEL_REMOVE_CUSTOM_ID = 'city_role_panel_remove_v1'
CITY_ROLE_DURATION_SECONDS = 21600 # six hors
CITY_ROLE_DB_PATH = str((Path(__file__).resolve().parent / 'userdata' / 'city_role_panel.db'))

bot = commands.Bot(command_prefix=commands.when_mentioned, intents=discord.Intents.default())
log_channel = bot.get_channel(STARTUP_CHANNEL_ID)

async def printlog(text):
    print(text)
    if len(str(text)) < 1000:
        log_channel = bot.get_channel(STARTUP_CHANNEL_ID)
        await log_channel.send(text)

# check if these things are on in the .env
rareCheckerOn = False
automatic_updates = False
admin_users = [1002449671224041502, 780303451980038165, 634620519500480512, 581098452327464973, 637885403101396994, 997746009318891603, int(USER_ID)]
if config['RARE_SERVICE_CHECKER'] == 'ON':
    rareCheckerOn = True
startupAchievements = False
if config['STARTUP_REFRESH_ACHIEVEMENTS'] == 'ON':
    startupAchievements = True
if config['AUTOMATIC_UPDATES'] == 'ON':
    automatic_updates = True
if config['DEVS_TO_HAVE_ADMIN_ACCESS'] == 'OFF':
    admin_users = [int(USER_ID)]
# settings
    
lineStatusOn = False

MAINTENANCE_MODE = False
maintenance_message = "```Bot currently in Maintenance Mode, bot may go offline, commands may stop working midway through and games may randomly stop, will return to normal soon, hopefully at least```"
maintenance_game_message = "```Bot currently in Maintenance Mode, this game may randomly end, will return to normal soon, hopefully at least```"

async def maintenance_func(ctx):
    if MAINTENANCE_MODE:
         await ctx.channel.send(maintenance_message)

async def maintenance_game_func(ctx):
    if MAINTENANCE_MODE:
        await ctx.channel.send(maintenance_game_message)


channel_game_status = {} # variable to store what channels are running the guessing game

global traintoedit 
traintoedit = None # var that will store the selected train in the db to edit.


# Command Groups
class CommandGroups(app_commands.Group):
    ...

trainlogs = CommandGroups(name='log')
games = CommandGroups(name='games')
search = CommandGroups(name='search')
stats = CommandGroups(name='stats')
maps = CommandGroups(name='maps')
myki = CommandGroups(name='myki')
completion = CommandGroups(name='completion')
achievements = CommandGroups(name='achievements')
favourites = CommandGroups(name='favourite')
schedule = CommandGroups(name='schedule')

async def download_csv(url, save_path):
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                file.write(response.content)
            await printlog(f"CSV downloaded successfully and saved as {save_path}")
        else:
            raise Exception(f"Failed to download CSV. Status code: {response.status_code}")
        
# web server thing for recieving submissions
from aiohttp import web

async def handle_submission(request):
    data = await request.post()
    # put the thing to add it to queue here !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    target_guild_id = 1214139268725870602
    target_channel_id = 1238821549352685568
    showcase_channel = 1322889624250486848
    target_guild = bot.get_guild(target_guild_id)
    if target_guild:
        await webAddImage(target_guild, target_channel_id, showcase_channel, data)

    
    return web.Response(text="Submission received!")

async def returnAlias(request):
    userid = request.query.get('username')
    if not userid:
        return web.json_response({'error': 'Username is required'}, status=400)
    try:
        conn = sqlite3.connect('userdata/aliases.db')
        cursor = conn.cursor()
        cursor.execute('SELECT alias FROM aliases WHERE userid = ?', (userid,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return web.json_response({'alias': result[0]})
        else:
            return web.json_response({'alias': None})
            
    except sqlite3.Error as e:
        return web.json_response({'error': f'Database error: {str(e)}'}, status=500)

async def setAlias(request):
    try:
        data = await request.json()
        discord_id = data.get("discord_id")
        name = data.get("name")

        if not discord_id or not name:
            return web.json_response({"error": "Missing discord_id or name"}, status=400)

        print(f"Received data: Discord ID = {discord_id}, Name = {name}")
        worked = setWebAlias(discord_id, name)
        if worked:
            return web.json_response({
                "message": "Data received successfully",
                "received_data": {
                    "discord_id": discord_id,
                    "name": name
                }
            }, status=200)
        else:
            return web.json_response({
                "message": "There is already another user with this alias!"
            }, status=400)

    except json.JSONDecodeError:
        return web.json_response({"error": "Invalid JSON payload"}, status=400)
    except Exception as e:
        print(f'Error setting alias: {e}')  
        return web.json_response({"error": f"Failed to process request: {str(e)}"}, status=500)

app = web.Application()
app.add_routes([web.post('/submit_photo', handle_submission)])
app.add_routes([web.get('/alias', returnAlias)])
app.add_routes([web.post('/set-alias', setAlias)])

web_runner = None
# start aiohttp server in background when bot starts
async def start_webserver():
    global web_runner
    web_runner = web.AppRunner(app)
    await web_runner.setup()
    site = web.TCPSite(web_runner, '0.0.0.0', 1237)
    await site.start()
    print('Web server on!')
    
async def stop_webserver():
    global web_runner
    if web_runner:
        await web_runner.cleanup()
        print('Web server stopped!')
        web_runner = None




@bot.event
async def on_ready():
    init_city_role_db()
    bot.add_view(CityRolePanelView())

    # download the trainset data     
    csv_url = "https://victorianrailphotos.com/api/trainsets.csv"
    save_location = "utils/trainsets.csv"
    # await printlog(f"Downloading trainset data from {csv_url} to {save_location}")
    # await download_csv(csv_url, save_location)
    
    channel = bot.get_channel(STARTUP_CHANNEL_ID)

    bot.tree.add_command(trainlogs)
    bot.tree.add_command(games)
    bot.tree.add_command(search)
    bot.tree.add_command(stats)
    bot.tree.add_command(maps)
    bot.tree.add_command(myki)
    bot.tree.add_command(completion)
    bot.tree.add_command(achievements)
    bot.tree.add_command(favourites)
    bot.tree.add_command(schedule)

    try:
        await channel.send(f"""TrackPulse Vic Copyright (C) 2024  Billy Evans
        This program comes with ABSOLUTELY NO WARRANTY.
        This is free software, and you are welcome to redistribute it
        under certain conditions""")
    except Exception as e:
        await printlog(f'Error: {e}\n make sure the bot has premission to send in the startup channel')
        return

    try:
        await ensure_city_role_panel_message()
    except Exception as e:
        await printlog(f'City role panel setup failed: {e}')

    if CITY_ROLE_PANEL_ENABLED and not city_role_expiry_loop.is_running():
        city_role_expiry_loop.start()
    
    if not trainTimleyCheckerLoop.is_running():
        trainTimleyCheckerLoop.start()  # Start the train timley checker loop
    
    try:
        if not task_loop.is_running():
            task_loop.start()
    except:
        await printlog("WARNING: Rare train checker is not enabled!")
        await channel.send(f"WARNING: Rare train checker is not enabled! <@{USER_ID}>")

    if not healthcheck_ping_loop.is_running():
        healthcheck_ping_loop.start()
    
    # Refresh all users
    if startupAchievements:
        channel_id = int(config['STARTUP_CHANNEL_ID'])  # Convert string to integer
        response_channel = bot.get_channel(channel_id)
        
        if response_channel is None:
            await printlog(f"Error: Could not find channel with ID {channel_id}")
            return
        
        response = await response_channel.send('Checking log achievements for all users...')
        
        user_files = os.listdir('utils/trainlogger/userdata')
        csv_files = [f for f in user_files if f.endswith('.csv')]
        
        for csv_file in csv_files:
            username = csv_file[:-4]  # Remove .csv extension
            await response.edit(content=f'Checking achievements for {username}...')
            await addAchievement(username, channel_id, f'<@{username}>')
        
        mode = 'guesser'
        filepath = f"utils/game/scores/{mode}.csv"
        new_achievements = []

        await response.edit(content='Finished checking log achievements for all users')
        response = await response_channel.send('Checking game achievements for all users...')

        with open(filepath, mode='r', newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                if row != ['username','id','wins','losses']:
                    username = row[1]
                    await response.edit(content=f'Checking game achievements for {username}...')
                    
                    #send achievement message
                    new = checkGameAchievements(username)
                    for achievement in new:
                        info = getAchievementInfo(achievement)
                        embed = discord.Embed(title='Achievement unlocked!', color=achievement_colour)
                        embed.add_field(name=info['name'], value=f"{info['description']}\n\n View all your achievements: </achievements view:1327085604789551134>")
                        await channel.send(f'<@{username}>',embed=embed)
                
        await response.edit(content='Finished checking game achievements for all users')

    # uptime
    global uptime
    uptime = int(time.time())
    healthcheck.pinghealthcheck() # ping to the monitoring thing
    
    # start webserver
    bot.loop.create_task(start_webserver())

    
    # restart or normal start
    file = open('restart.txt','r')
    file = file.read()

    if file == '':
        await printlog("Bot started")
    else:
        await printlog("Bot restarted")
        channel = bot.get_channel(int(file))
        await channel.send("Bot restarted")
        with open('restart.txt', 'w') as file:
            file.write('')

    # maintenance mode
    global MAINTENANCE_MODE
    file = open('maintenance.txt','r')
    file = file.read()

    if file == '':
        await printlog("Bot in normal conditions")
        MAINTENANCE_MODE = False
    else:
        await printlog("Maintenance Mode Enabled")
        MAINTENANCE_MODE = True

# achievement awarder  check achievements
async def addAchievement(username, channel, mention):
    channel = bot.get_channel(channel)
    new = checkAchievements(username)
    for achievement in new:
        info = getAchievementInfo(achievement)
        embed = discord.Embed(title='Achievement unlocked!', color=achievement_colour)
        embed.add_field(name=info['name'], value=f"{info['description']}\n\n View all your achievements: </achievements view:1327085604789551134>")
        await channel.send(mention,embed=embed)
        
# game achievement awarder  check game achievements
async def addGameAchievement(username, channel, mention, game:str='guesser'):
    await printlog(f'checking game achievements for {username}')
    channel = bot.get_channel(channel)
    print('game:', game)
    if game == 'guesser':
        new = checkGameAchievements(username)
    elif game == 'hangman':
        new = checkHangmanAchievements(username)
    print('New achievements:', new)
    for achievement in new:
        info = getAchievementInfo(achievement)
        embed = discord.Embed(title='Achievement unlocked!', color=achievement_colour)
        embed.add_field(name=info['name'], value=f"{info['description']}\n\n View all your achievements: </achievements view:1327085604789551134>")
        await channel.send(mention,embed=embed)

# in the city role assigner
def init_city_role_db():
    Path(CITY_ROLE_DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(CITY_ROLE_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS city_role_claims (
            user_id INTEGER PRIMARY KEY,
            expires_at INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def upsert_city_role_claim(user_id: int, expires_at: int):
    conn = sqlite3.connect(CITY_ROLE_DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        '''
        INSERT INTO city_role_claims (user_id, expires_at)
        VALUES (?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            expires_at = excluded.expires_at
        ''',
        (user_id, expires_at)
    )
    conn.commit()
    conn.close()


def get_active_city_role_claims():
    now = int(time.time())
    conn = sqlite3.connect(CITY_ROLE_DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT user_id, expires_at FROM city_role_claims WHERE expires_at > ? ORDER BY expires_at ASC',
        (now,)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_expired_city_role_claims():
    now = int(time.time())
    conn = sqlite3.connect(CITY_ROLE_DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT user_id FROM city_role_claims WHERE expires_at <= ?',
        (now,)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def delete_city_role_claim(user_id: int):
    conn = sqlite3.connect(CITY_ROLE_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM city_role_claims WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()


def build_city_role_panel_embed(active_claims):
    embed = discord.Embed(
        title='Who is trainspotting?',
        description='Use the button below to let others know if you are trainspotting and want to meet up with others.',
        color=discord.Color.blue(),
        timestamp=datetime.now()
    )

    if not active_claims:
        mentions_text = 'No one is trainspotting right now.'
    else:
        lines = [f'<@{user_id}>' for user_id, _ in active_claims]
        joined = '\n'.join(lines)
        if len(joined) > 1024:
            kept = []
            current = 0
            remaining = len(lines)
            for line in lines:
                add_len = len(line) + (1 if kept else 0)
                if current + add_len > 980:
                    break
                kept.append(line)
                current += add_len
                remaining -= 1
            if remaining > 0:
                kept.append(f'+ {remaining} more')
            mentions_text = '\n'.join(kept)
        else:
            mentions_text = joined

    embed.add_field(name='People trainspotting:', value=mentions_text, inline=False)
    return embed


async def get_city_role_panel_message(channel: discord.abc.Messageable):
    async for msg in channel.history(limit=200):
        if bot.user is None or msg.author.id != bot.user.id:
            continue

        has_title = any((embed.title or '').strip() == 'Who is trainspotting?' for embed in msg.embeds)
        if not has_title:
            continue

        has_button = any(
            getattr(component, 'custom_id', None) == CITY_ROLE_PANEL_CUSTOM_ID
            for row in msg.components
            for component in row.children
        )
        if has_button:
            return msg
    return None


async def refresh_city_role_panel_message(channel: discord.abc.Messageable):
    message = await get_city_role_panel_message(channel)
    if message is None:
        return

    active_claims = get_active_city_role_claims()
    guild = getattr(channel, 'guild', None)
    role = guild.get_role(CITY_ROLE_ID) if guild is not None else None
    cleaned_claims = []
    for user_id, expires_at in active_claims:
        if guild is None or role is None:
            delete_city_role_claim(user_id)
            continue

        member = guild.get_member(user_id)
        if member is None:
            try:
                member = await guild.fetch_member(user_id)
            except Exception:
                member = None

        if member is None or role not in member.roles:
            delete_city_role_claim(user_id)
            continue

        cleaned_claims.append((user_id, expires_at))

    active_claims = cleaned_claims
    embed = build_city_role_panel_embed(active_claims)
    await message.edit(embed=embed, view=CityRolePanelView())


class CityRolePanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='I am trainspotting', style=discord.ButtonStyle.success, custom_id=CITY_ROLE_PANEL_CUSTOM_ID)
    async def claim_role(self, interaction: discord.Interaction, button: discord.ui.Button):
        if CITY_ROLE_ID == 0:
            await interaction.response.send_message('Role panel role is not configured.', ephemeral=True)
            return

        role = interaction.guild.get_role(CITY_ROLE_ID)

        member = interaction.user
        if not isinstance(member, discord.Member):
            member = interaction.guild.get_member(interaction.user.id)
            if member is None:
                member = await interaction.guild.fetch_member(interaction.user.id)

        expires_at = int(time.time()) + CITY_ROLE_DURATION_SECONDS

        if role in member.roles:
            upsert_city_role_claim(member.id, expires_at)
            await interaction.response.send_message(
                f'You already marked yourself as trainspotting. Timer reset, it now expires <t:{expires_at}:R>.',
                ephemeral=True
            )
            if interaction.channel is not None:
                await refresh_city_role_panel_message(interaction.channel)
            return

        try:
            await member.add_roles(role, reason='Clicked city role panel button')
            upsert_city_role_claim(member.id, expires_at)
            await interaction.response.send_message(
                f'You have been marked as trainspotting. Your status will automatically get removed <t:{expires_at}:R>.',
                ephemeral=True
            )
            if interaction.channel is not None:
                await refresh_city_role_panel_message(interaction.channel)
        except Exception as e:
            await interaction.response.send_message(f'Failed to add role: {e}', ephemeral=True)

    @discord.ui.button(label='I am not trainspotting', style=discord.ButtonStyle.danger, custom_id=CITY_ROLE_PANEL_REMOVE_CUSTOM_ID)
    async def remove_role(self, interaction: discord.Interaction, button: discord.ui.Button):
        if CITY_ROLE_ID == 0:
            await interaction.response.send_message('Role panel role is not configured.', ephemeral=True)
            return

        role = interaction.guild.get_role(CITY_ROLE_ID)
        member = interaction.user
        if not isinstance(member, discord.Member):
            member = interaction.guild.get_member(interaction.user.id)
            if member is None:
                member = await interaction.guild.fetch_member(interaction.user.id)

        if role not in member.roles:
            delete_city_role_claim(member.id)
            await interaction.response.send_message('You already aren\'t trainspotting!', ephemeral=True)
            if interaction.channel is not None:
                await refresh_city_role_panel_message(interaction.channel)
            return

        try:
            await member.remove_roles(role, reason='Clicked city role panel remove button')
            delete_city_role_claim(member.id)
            await interaction.response.send_message(
                'Role removed. You are no longer marked as trainspotting.',
                ephemeral=True
            )
            if interaction.channel is not None:
                await refresh_city_role_panel_message(interaction.channel)
        except Exception as e:
            await interaction.response.send_message(f'Failed to remove role: {e}', ephemeral=True)


async def city_role_panel_exists(channel: discord.abc.Messageable) -> bool:
    async for msg in channel.history(limit=200):
        if bot.user is None or msg.author.id != bot.user.id:
            continue

        has_title = any((embed.title or '').strip() == 'Who is trainspotting?' for embed in msg.embeds)
        if not has_title:
            continue

        has_button = any(
            getattr(component, 'custom_id', None) == CITY_ROLE_PANEL_CUSTOM_ID
            for row in msg.components
            for component in row.children
        )
        if has_button:
            return True

    return False


async def ensure_city_role_panel_message():
    if not CITY_ROLE_PANEL_ENABLED:
        return

    channel = bot.get_channel(CITY_ROLE_CHANNEL_ID)
    if channel is None:
        await printlog(f'City role panel channel not found: {CITY_ROLE_CHANNEL_ID}')
        return

    existing_message = await get_city_role_panel_message(channel)
    if existing_message is not None:
        await refresh_city_role_panel_message(channel)
        return

    embed = build_city_role_panel_embed(get_active_city_role_claims())
    await channel.send(embed=embed, view=CityRolePanelView())


@tasks.loop(minutes=1)
async def city_role_expiry_loop():
    if not CITY_ROLE_PANEL_ENABLED:
        return

    if CITY_ROLE_ID == 0:
        return

    channel = bot.get_channel(CITY_ROLE_CHANNEL_ID)
    if channel is None:
        return

    guild = getattr(channel, 'guild', None)
    if guild is None:
        return

    role = guild.get_role(CITY_ROLE_ID)
    expired = get_expired_city_role_claims()
    if not expired:
        return

    changed = False
    for user_id, in expired:
        member = guild.get_member(user_id)
        if member is None:
            try:
                member = await guild.fetch_member(user_id)
            except Exception:
                member = None

        if member is not None and role is not None and role in member.roles:
            try:
                await member.remove_roles(role, reason='trainspotting role expired after 6 hours')
            except Exception as e:
                await printlog(f'Could not remove expired trainspotting role from {user_id}: {e}')

        delete_city_role_claim(user_id)
        changed = True

    if changed:
        await refresh_city_role_panel_message(channel)


# Rare train finder
async def check_rare_trains_in_thread():
    rare_trains = checkRareTrainsOnRoute()
    asyncio.run_coroutine_threadsafe(log_rare_trains(rare_trains), bot.loop)

async def log_rare_trains(rare_trains):
    log_channel = bot.get_channel(RARE_SERVICE_CHANNEL_ID)
    channel = bot.get_channel(RARE_SERVICE_CHANNEL_ID)

    if rare_trains:
        embed = discord.Embed(title="Trains found on lines they are not normally on!", color=rare_trains_colour)

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
        await channel.send('<@&1227171023795781694> Trains found on lines they are not normally on!\n`Due to errors in the TV api data out of our control, some data may be inaccurate.`')
    else:
        await log_channel.send("None found")

# async def check_lines_in_thread():
#     asyncio.run_coroutine_threadsafe(checklines(), bot.loop)

                 

@tasks.loop(minutes=10)
async def task_loop():
    # update status
    totalLogs = getTotalTrips()

    try:
        await printlog(f"Updating bot status, total logs = `{totalLogs}`")
    except Exception as e:
        healthcheck.pinghealthcheck(fail=True)
        
    await bot.change_presence(activity=discord.CustomActivity(name=f'{totalLogs:,} trips logged'))
    try:
        # write totalLogs to a csv with current date time in iso format
            with open('utils/trainlogger/totalLogs.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([totalLogs, datetime.now().isoformat()])
    except Exception as e:
        await printlog(f'Error writing totalLogs to CSV: {e}')
    
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


@tasks.loop(seconds=60)
async def healthcheck_ping_loop():
    healthcheck.pinghealthcheck()


global secondLoop
secondLoop = True

@tasks.loop(minutes=5)
async def trainTimleyCheckerLoop():
    # Run the train location checking in a background task so it doesn't block the bot
    async def run_checker():
        global secondLoop
        await printlog('Starting the train timley checker certified software solution!')
        channels = getchannelstocheck()
        trains = []
        
        for thing in channels:
            if thing[1] not in trains:
                trains.append(thing[1])
        print('the trains to check:', trains)
        
        tlocs = await seeWhereTrainsAre(trains)
        print(f'tlocs: {tlocs}')

        for train in tlocs:
            if train[1].startswith('No trip data available'):
                print(f'cant find run for {train[0]}')
                for channel in channels:
                    if str(train[0]) == str(channel[1]):
                        print(f"channele: {channel[0]}")
                        channelID = bot.get_channel(int(channel[0]))
                        try:
                            await channelID.send(f"{train[0]} is not currently running")
                        except:
                            try:
                                print(f'couldnt send message to {channelID}')
                            except:
                                print('couldnt send th message to the channel id which i also cant fucking say cause it is also broken ffs')
                    else:
                        print(f'{train[0]} not {channel[1]}')
            else:
                print(f'found run for {train[4]}')
                # Store the coords in the history csv
                with open(f'utils/schedule/history/{train[4]}.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([train[1], train[2], train[3], train[4], train[5], train[6], train[7], datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
                
                # Send embed only on every second loop
                if secondLoop:
                    for channel in channels:
                        if str(train[4]) == str(channel[1]):
                            embed = discord.Embed(
                                title=f'{train[4]}\'s Location',
                                description=f'{train[1]} line to {train[5]}',
                                url=train[2],
                                color=lines_dictionary_log_train_map_post_munnel[train[1]][1],
                                timestamp=datetime.now()
                            )
                            embed.set_footer(text='Maps © Thunderforest, Data © OpenStreetMap contributors')
                            
                            # Image
                            image = discord.File(f'temp/{train[0]}', filename="map.png")
                            embed.set_image(url="attachment://map.png")
                            
                            channelID = bot.get_channel(int(channel[0]))
                            try:
                                await channelID.send(embed=embed, file=image)
                            except:
                                try:
                                    print(f'Couldnt sent message to {channelID}')
                                    print(f'Couldnt sent message to {channelID.id}')
                                except:
                                    print('Couldnt sent message to the channel id which i also cant fucking say cause it is also broken ffs')
                        else:
                            print(f'{train[4]} not {channel[1]}')
                else:
                    print(f'Skipping embed for {train[4]} as secondLoop is False')

    # Start the checker as a background task
    await run_checker()
    # Toggle secondLoop after all processing is complete
    global secondLoop
    secondLoop = not secondLoop
            

# @tasks.loop(minutes=15)
# async def task_loop():
    # Create a new thread to run checkRareTrainsOnRoute
    # thread = threading.Thread(target=check_lines_in_thread)
    # thread.start()


# Help command
help_commands = ['Which /log command should I use?','/about','/achievements view','/completion sets','/completion stations','/departures','/favourite add','/favourite remove','/games station-guesser','/games station-hangman','/games station-order','/help','/line-status','/log adelaide-train','/log adelaide-tram','/log bus','/log delete','/log edit','/log export','/log import','/log perth-train','/log stats','/log sydney-train','/log sydney-tram','/log train','/log tram','/log view','/disruptions','/maps trips','/maps view','/myki calculate-fare','/search tv','/search route','/search station','/search run','/search train','/search train-photo','/search tram','/search victorianrailphotos','/stats leaderboard','/stats profile','/stats termini','/submit-photo','/wongm','/year-in-review']

async def help_autocompletion(
    interaction: discord.Interaction,
    current: str
) -> typing.List[app_commands.Choice[str]]:
    fruits = help_commands.copy()
    return [
        app_commands.Choice(name=fruit, value=fruit)
        for fruit in fruits if current.lower() in fruit.lower()
    ][:25]

@bot.tree.command(name="help", description="Lists available commands by category, or learn more about a specific command.")
@app_commands.describe(category="Choose a command category", command='Learn more about how to use a specific command.')
@app_commands.choices(category=[
    app_commands.Choice(name="General", value="general"),
    app_commands.Choice(name="Search", value="search"),
    app_commands.Choice(name="Logs", value="logs"),
    app_commands.Choice(name="Fun", value="fun"),
    app_commands.Choice(name="Myki", value="myki"),
])
@app_commands.autocomplete(command=help_autocompletion)

async def help(ctx, category: app_commands.Choice[str] = None, command:str=None):
    log_command(ctx.user.id, 'help')
    await helpCommand(ctx, category, command)
    await maintenance_func(ctx)


    
@bot.tree.command(name="disruptions", description="Show disruptions on a Metro line")
@app_commands.describe(line="What Metro line to show disruptions for?")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
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
    await ctx.response.defer()
    log_command(ctx.user.id, 'line_info')

    # Retrieve line information from API
    json_info_str = route_api_request(line, "0")
    json_info_str = json_info_str.replace("'", "\"")  # Replace single quotes with double quotes
    json_info = json.loads(json_info_str)

    routes = json_info["routes"]
    status = json_info["status"]

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

    await printlog(f"route id: {route_id}")

    # Retrieve disruption information
    disruption_description = ""
    try:
        disruptions = disruption_api_request(route_id)

        # Extracting title and description
        for general_disruption in disruptions["disruptions"]["metro_train"]:
            if general_disruption["display_on_board"]:
                disruption_description = general_disruption["description"]
                url = general_disruption['url']
                updateTime = convert_iso_to_unix_time(general_disruption['last_updated'])
                break

    except Exception as e:
        await printlog(f'here: {e}')

    # Determine the color of the embed based on the status description
    color = genColor(description)
    await printlog(f"Status color: {color}")

    # Create the embed with the retrieved information
    if disruption_description:
        embed = discord.Embed(title=f"{description} - {route_name}", color=color, url=url if url else None)
    else:
        embed = discord.Embed(title=f"{description} - {route_name}", color=color)
    embed.add_field(name="Status Description", value=description, inline=False)
    if disruption_description:
        embed.add_field(name="Disruption Info", value=f'{disruption_description}\n\nUpdated {updateTime}', inline=False)
    else:
        embed.add_field(name="Disruption Info", value=f'There are no disruptions on the {route_name} line!', inline=False)

    # Send the embed to the Discord channel
    await ctx.edit_original_response(embed=embed)
    await maintenance_func(ctx)


# Route Seach v2
@search.command(name="route", description="Show info about a tram or bus route")
@app_commands.describe(mode = "What type of transport is this route?")
@app_commands.choices(mode=[
        app_commands.Choice(name="Bus", value="2"),
        app_commands.Choice(name="Tram", value="1"),
        app_commands.Choice(name="Metro Train", value="0"),
        # app_commands.Choice(name="VLine Train", value="3"),
        # app_commands.Choice(name="Night Bus", value="4"),
])
@app_commands.describe(number = "What route number to show info about?")

async def route(ctx, mode: str, number: int):  
    log_command(ctx.user.id, 'route_search')
    try:
        json_info_str = route_api_request(number, mode)
        json_info_str = json_info_str.replace("'", "\"")  # Replace single quotes with double quotes
        json_info = json.loads(json_info_str)
        
        channel = ctx.channel
        await ctx.response.send_message(f"Results for {number}:")
        # embed = discord.Embed(title=f"Bus routes matching `{line}`:", color=bus_colour)
        counter = 0
        found_routes = False
        
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
            url = ''
            try:
                disruptions = disruption_api_request(route_id)
                # await printlog(disruptions)
                
                # Extracting title and description
                general_disruption = disruptions["disruptions"]["metro_bus"][0]
                disruptionTitle = general_disruption["title"]
                disruptionDescription = general_disruption["description"]
                url = general_disruption['url']
                updateTime = convert_iso_to_unix_time(general_disruption['last_updated'])
                
            except Exception as e:
                await printlog(e)

            
            # disruption status:

             # Check if the route number is the one you want
            if route_number == str(number):
                found_routes = True
                # Create and send the embed only for the desired route number
                if url:
                    embed = discord.Embed(title=f"Route {route_number}:", color=getColor(mode), url=url)
                else:
                    embed = discord.Embed(title=f"Route {route_number}:", color=getColor(mode))
                embed.add_field(name="Route Name", value=f"{route_number} - {route_name}", inline=False)
                embed.add_field(name="Status Description", value=description, inline=False)
                if disruptionDescription:
                    embed.add_field(name="Disruption Info",value=f'{disruptionDescription}\n\nUpdated {updateTime}', inline=False)
                    
                await channel.send(embed=embed)
          
            counter = counter + 1

        if not found_routes:
            await channel.send(f"No routes found matching number {number}")
                
    except Exception as e:
        await ctx.channel.send(f"error:\n`{e}`\nMake sure you inputted a valid route number, otherwise, the bot is broken.")

    await maintenance_func(ctx)


# train Photo search
@search.command(name="train-photo", description="Search Victorianrailphotos.com")
@app_commands.describe(number="Carriage number", search_set="Search for photos of all carriages in the set.")
async def line_info(ctx, number: str, search_set:bool=False):
    log_command(ctx.user.id, 'train-photo')
    await searchTrainPhoto(ctx, number, search_set)

# Station search station
async def station_autocompletion(
    interaction: discord.Interaction,
    current: str
) -> typing.List[app_commands.Choice[str]]:
    fruits = stations_list.copy()
    return [
        app_commands.Choice(name=fruit, value=fruit)
        for fruit in fruits if current.lower() in fruit.lower()
    ][:25]
@search.command(name='station', description='View info about and a photo of a railway station')
@app_commands.autocomplete(station=station_autocompletion)
async def stationphoto(ctx, station:str):
    async def searchstationpic():
        await ctx.response.defer()
        log_command(ctx.user.id, 'search-station')
        
        data = stationInfoAPIRequest(nameToStopID(station, '0'), 0)
        mode = 0
        if data == None: # check if its a v/line stop
            await printlog('there is no data so im trying vline')
            data = stationInfoAPIRequest(nameToStopID(station, '3'), 3)
            mode = 3
            
        suburb = data['stop']['stop_location']['suburb']
        
        amenities = data['stop']['stop_amenities']
        phone = amenities['pay_phone']
        waitingRoom = amenities['sheltered_waiting_area']
        kiosk = amenities['kiosk']
        toilet = amenities['toilet']
        car_park = amenities['car_parking']
        bike_locker = amenities['bicycle_locker']
        bike_rack = amenities['bicycle_rack']
        zone = data['stop']['stop_ticket']['zone']
        ticket_machine = data['stop']['stop_ticket']['ticket_machine']
        
        stepfree = True
        if station.title() == 'Heyington':
            stepfree = False
        
        # routes:
        routelines = ''
        for route in data['stop']['routes']:    
            routelines += f'{route["route_name"]}\n'
        
        embed= discord.Embed(title=f'{getModeEmoji(mode)} {station.title()} Station', description=suburb)
        embed.add_field(name='Services', value=f'''🚻 Toilet: {yesOrNo(toilet)}\n⌚ Waiting Room: {yesOrNo(waitingRoom)}\n☕ Kiosk: {yesOrNo(kiosk)}\n📞 Payphone: {yesOrNo(phone)}''', inline=False)
        embed.add_field(name='Parking', value=f'''🚗 Parking Spaces: {car_park} spaces\n🚲 Bike Cage: {bike_locker} spaces, Bike Racks: {bike_rack} spaces''', inline=False)
        embed.add_field(name='Ticketing', value=f'{zone}\nTicket Machine {yesOrNo(ticket_machine)}', inline=False)
        if not stepfree:
            embed.add_field(name='⚠️ Accessibility', value='This station is not step free', inline=False)
        
        photo = getStationImage(station)
        if photo != None:
            embed.set_image(url=photo)
            embed.set_footer(text=f'Photo by {getPhotoCredits(station)}')
        else:
            await printlog('no photo')
            # await ctx.edit_original_response(content=f'No photos found for {station.title()}')
            
        await ctx.edit_original_response(embed=embed)
    asyncio.create_task(searchstationpic())
    await maintenance_func(ctx)
 
# myki fare calculator   
@myki.command(name="calculate-fare", description="Calculate fare for a trip")   
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)       
@app_commands.describe(start_zone = "Start zone", end_zone = "End zone")
async def calculate_fair(ctx, start_zone:int, end_zone:int):
    async def calc():
        await ctx.response.defer()
        log_command(ctx.user.id, 'calculate-fare')
    
        start = start_zone
        end = end_zone
        if start > end:
            start = end_zone
            end = start_zone


        try:
            api_response = fareEstimate(start, end)
            json_response = json.dumps(api_response)
            data = json.loads(json_response)

            result = data['FareEstimateResult']
            
            earlyBird = result['IsEarlyBird']
            weekend = result['IsThisWeekendJourney']
            
            fairs = result['PassengerFares']
            
            embed=discord.Embed(title=f"Zone {start_zone} → {end_zone}", color=myki_colour)
            count=0
            for fair in fairs:
                type = fairs[count]['Passengemode']
                Fare2HourPeak = fairs[count]['Fare2HourPeak']
                Fare2HourOffPeak = fairs[count]['Fare2HourOffPeak']
                FareDailyPeak = fairs[count]['FareDailyPeak']
                WeekendCap = fairs[count]['WeekendCap']
                HolidayCap = fairs[count]['HolidayCap']
                Pass7Days = fairs[count]['Pass7Days']
                Pass28To69DayPerDay = fairs[count]['Pass28To69DayPerDay']
                Pass70PlusDayPerDay = fairs[count]['Pass70PlusDayPerDay']
                count +=1

                embed.add_field(name=type.title(), value=f'2 hour fare: `${Fare2HourPeak:.2f}`\nDaily cap: `${FareDailyPeak:.2f}`\nWeekend cap: `${WeekendCap:.2f}`\nHoliday cap: `${HolidayCap:.2f}`', inline=True)
                
            embed.add_field(name='Fare Info', value=f'Early Bird: {earlyBird}\nWeekend: {weekend}', inline=False)
            await ctx.edit_original_response(embed=embed)          

        except Exception as e:
            await ctx.edit_original_response(content='Invalid information. Please try again.')
            await printlog(e)
            
    asyncio.create_task(calc())
    await maintenance_func(ctx)
            

        
'''
# thing to save myki credentials to bot:
@myki.command(name='save-login', description='Save your TV account username and password to the bot, run it again to change your saved info')
@app_commands.describe(ptvusername = "PTV accpunt username", ptvpassword = "PTV account password", encryptionpassword = "A password to encrypt your PTV password")
async def login(ctx, ptvusername: str, ptvpassword: str, encryptionpassword: str):
    await ctx.response.defer(ephemeral=True)
    log_command(ctx.user.id, 'save-login')
    encryptedPassword = encryptPW(encryptionpassword, ptvpassword)
    savelogin(ptvusername, str(encryptedPassword).split("'")[1], ctx.user.id) # the split is so it dosnt include the b' part
    await ctx.edit_original_response(content=f'Saved username and password to bot.\nUsername: `{ptvusername}`\nPassword: `{ptvpassword}`\nYour password is encrypted and cannot be seen by anyone. You will need to enter your encryption password to view your mykis with the bot.\nEncryption password: `{encryptionpassword}`')
    
# disabled myki view command

@myki.command(name='view', description='View your mykis and their balances')
@app_commands.describe(encriptionpassword = "Your encryption password from the login command")
async def viewmykis(ctx, encriptionpassword: str):
    loop = asyncio.get_event_loop()
    await ctx.response.defer(ephemeral=True)
    log_command(ctx.user.id, 'view-myki')
    async def viewcards():
        # decrypt the password
        
        # get saved username and password:
        try:
            login = readlogin(ctx.user.id)
        except:
            return "You haven't logged in yet. Run </myki login:1289553446659166300> to login."

        try:
            decryptedPassword = decryptPW(encriptionpassword, login[1].encode())
        except Exception as e:
            return "Your encryption password is incorrect. Run </myki login:1289553446659166300> to reset it."
        
        # run the myki scraper
        try:
            data = getMykiInfo(login[0], decryptedPassword)
        except Exception as e:
            return f"There has been an error: `{e}`"
        
        # make embed
        embed = discord.Embed(title="Your Mykis", color=myki_colour)
        for myki, info in data.items():
            # find mobile mykis:
            prefix = "mobile myki, "
            if info[0].startswith(prefix):
                cardName = f':mobile_phone: {info[0][len(prefix):]}'
            else:
                cardName = info[0]
            
            embed.add_field(name=f'{cardName}    {info[2]}', value=f'{info[1]}')
        
        return embed

    # Create a ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        # Run the viewcards function in a separate thread
        result = await loop.run_in_executor(executor, viewcards)

        # Edit the original response based on the result
        if isinstance(result, discord.Embed):
            await ctx.edit_original_response(embed=result)
        else:
            await ctx.edit_original_response(content=result)
'''
# Wongm search
@bot.tree.command(name="wongm", description="Search Wongm's Rail Gallery")
@app_commands.describe(search="search")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def line_info(ctx, search: str):
    log_command(ctx.user.id, 'wongm-search')
    channel = ctx.channel
    await printlog(f"removing spaces in search {search}")
    spaces_removed = search.replace(' ', '%20')
    await printlog(spaces_removed)
    url = f"https://railgallery.wongm.com/page/search/?s={spaces_removed}"
    await ctx.response.send_message(url)
    
# my photo site search
@search.command(name="victorianrailphotos", description="Search for photos on victorianrailphotos.com")
@app_commands.describe(number='Carriage/Loco number', traintype='Type of train', location='Location of photo', photographer='Photographer of photo', featured='Featured photos only.')
async def victorianrailphotos(ctx, number: str = '', traintype: str = '', location: str = '', photographer: str = '', featured:bool=False):
    if featured:
        featured = 'featured'
    await ctx.response.send_message(f'[View results](https://victorianrailphotos.com/search?number={number}&type={traintype}&location={location}&photographer={photographer})')
    await maintenance_func(ctx)



# search Train search train
@search.command(name="train", description="Search for a specific Train")
@app_commands.describe(train="Carriage/Locomotive number to search for. For NSW you can also put the set number.", state="State to search in, will be found automattically if empty.", hide_run_info="Hide run info")
@app_commands.choices(state=[
        app_commands.Choice(name="Victoria", value="Victoria"),
        app_commands.Choice(name="New South Wales", value="NSW"),
])
async def train_search(ctx, train: str, state:str='auto', hide_run_info:bool=False):
    # try and auto find state
    if state == 'auto':
        Type = trainType(train) 
        if Type == f'Train type not found for {train}' or Type == None:
            print('Carriage is not victorian, checking for nsw')
            state = 'NSW'
        else:
            state = 'Victoria'
    
    if state == 'Victoria':
        # try:
        await searchTrainCommand(ctx, train, hide_run_info, metro_colour, vline_colour, ptv_grey,interchange_stations,lines_dictionary_log_train_map_post_munnel)
        # except Exception as e:
        #     await ctx.edit_original_response(content=f'An error has occored. Please try again.\n`{e}`')
        #     await printlog(f'Search Train error: {e}')
        #     return
    elif state == 'NSW':
        try:
            await NSWsearchTrainCommand(ctx,train)
        except Exception as e:
            await ctx.edit_original_response(content=f'An error has occored. Please try again.\n`{e}`')
            await printlog(f'Search Sydney Train error: {e}')
            return
    else:
        await ctx.response.send_message(f"{state} is not supported yet.")

    await maintenance_func(ctx)
        
            
# search run id   
@search.command(name="run", description="Shows the run for a specific TDN, found in the departures command")
@app_commands.describe(number="Run ID/TD Number", mode="Mode of transport to search run for")
@app_commands.choices(mode=[
        app_commands.Choice(name="Metro", value="metro"),
        app_commands.Choice(name="V/Line", value="vline"),
        app_commands.Choice(name="Tram", value="tram"),
        app_commands.Choice(name="Bus", value="bus"),
        app_commands.Choice(name="Night Bus", value="nightbus"),
        
])
async def runidsearch(ctx, number:str, mode:str='metro'):
    await ctx.response.defer()
    log_command(ctx.user.id, 'runid-search')
    async def addmap():
        try:
            line = ""
            if mode == "metro":
                if len(number) <= 4:
                    runid = "9"+TDNtoRunID(number)
                else:
                    runid = number
                runData = getTrainLocationFromID(str(runid))
                stoppingPattern = getStoppingPatternFromRunRef(runData, 0)
                await printlog('Mode is metro')
            elif mode == "tram":
                runData = getTrainLocationFromID(str(number))
                stoppingPattern = getStoppingPatternFromRunRef(runData, 1)
                await printlog('Mode is tram')
            elif mode == "bus":
                runData = getTrainLocationFromID(str(number))
                stoppingPattern = getStoppingPatternFromRunRef(runData, 2)
                await printlog('Mode is bus')
            elif mode == "vline":
                runData = getTrainLocationFromID(str(number))
                stoppingPattern = getStoppingPatternFromRunRef(runData, 3)
                await printlog('Mode is vline')
                async def strip_station_name(name):
                    return name.replace('Railway Station', '').strip()
                    
            elif mode == "nightbus":
                runData = getTrainLocationFromID(str(number))
                stoppingPattern = getStoppingPatternFromRunRef(runData, 4)
                await printlog('Mode is nightbus')

                # Filter out entries where the station name has a slash and status is 'Skipped', then strip 'Railway Station'
                stoppingPattern = [
                    (strip_station_name(station[0]), station[1], station[2]) 
                    for station in stoppingPattern 
                    if not ('/' in station[0] and station[1] == 'Skipped')
]
            await printlog(f"STOPPING PATTERN: {stoppingPattern}")
            vehicle = None
            try:
                if mode == "metro":
                    if runData is not None:
                        for item in runData:
                            # latitude = item['vehicle_position']['latitude']
                            # longitude = item['vehicle_position']['longitude']
                            try:
                                vehicle = item['vehicle_descriptor']['description']
                            except:
                                print('couldnt get vehicle')
                                vehicle = 'Unknown Train'
                            line = get_route_name(item['route_id'])
                            await printlog(f'Line: {line}')
                elif mode == "vline":
                    line = 'V/Line'
                    await printlog(f'Line: {line}')
                else: # just make the mode the type name
                    line = mode
                    await printlog(f'Line: {line}')

            except Exception as e:
                await ctx.edit_original_response(content='No trip data available.')

                await printlog(f'ErROR: {e}')
                return
            
            class RunContainer(discord.ui.Container):
                heading = discord.ui.TextDisplay(f'## Run {number} - {line} - {vehicle}' if vehicle else f'## Run {number} - {line}')

                # Add the stops to the embed.
                stopsString = ''
                fieldCounter = 0
                currentFieldLength = 0

                first_stop = True

                for stop_name, stop_time, status, schedule in stoppingPattern:
                    if status == 'Skipped':
                        # For skipped stops
                        stopEntry = f'{getMapEmoji(line, "skipped")} ~~{stop_name}~~'
                    else:
                        # Calculate delay in minutes
                        delay = (convert_times(stop_time) - convert_times(schedule)) // 60  # Convert seconds to minutes
                        delay_str = f"+{delay}m" if delay > 0 else ""

                        if first_stop:
                            if stop_name in interchange_stations:
                                emoji_type = "interchange_first"
                            else:
                                emoji_type = "terminus"
                            stopEntry = f'{getMapEmoji(line, emoji_type)} {stop_name} - {convert_iso_to_unix_time(stop_time)} {delay_str}'
                            first_stop = False
                        else:
                            # Check if it's the last stop in the list
                            if stop_name == stoppingPattern[-1][0]:  # Check if current stop name is the last one
                                if stop_name in interchange_stations:
                                    emoji_type = "interchange_last"
                                else:
                                    emoji_type = "terminus2"
                            else:
                                # Check stop_name in interchange_stations
                                if stop_name in interchange_stations:
                                    emoji_type = "interchange"
                                else:
                                    emoji_type = "stop"
                            stopEntry = f'{getMapEmoji(line, emoji_type)} {stop_name} - {convert_iso_to_unix_time(stop_time)} {delay_str}'

                    
                    # Add newline for formatting
                    stopEntry += '\n'

                    if currentFieldLength + len(stopEntry) > 3000:
                        # Add the current field and start a new one
                        if fieldCounter == 0:  # First field
                            stopsString += f'{getMapEmoji(line, "cont1")}\n'
                        else:
                            stopsString = f'{getMapEmoji(line, "cont2")}\n{stopsString}{getMapEmoji(line, "cont1")}\n'
                        runDisplaySection = discord.ui.TextDisplay(stopsString)
                        # embed.add_field(name=f"⠀", value=stopsString, inline=False)
                        stopsString = stopEntry
                        fieldCounter += 1
                        currentFieldLength = len(stopEntry)
                    else:
                        stopsString += stopEntry
                        currentFieldLength += len(stopEntry)

                # Add the last field if there's any content left
                if stopsString:
                    if fieldCounter > 0:  # Not the first field
                        stopsString = f'{getMapEmoji(line, "cont2")}\n{stopsString}'
                    runDisplay = discord.ui.TextDisplay(stopsString)
                
                # mapGallery = discord.ui.MediaGallery(discord.MediaGalleryItem(f'attachment://{train}-map.png'))
                # footer = discord.ui.TextDisplay('-# Maps © Thunderforest, Data © OpenStreetMap contributors')


            
            # Send a new message with the file and embed
            class RunView(discord.ui.LayoutView):
                container = RunContainer(id=2)
            await ctx.followup.send(view=RunView())
            
            

        except Exception as e:
            await ctx.edit_original_response(content='No trip data available.')   
            await printlog(f'ErROR: {e}') 
            await printlog(traceback.format_exc())  
            # await log_channel.send(f'Error: ```{e}```\n with finding train run ran by {ctx.user.mention}\n<@{USER_ID}>')

    # Run transportVicSearch in a separate thread
        
        
    asyncio.create_task(addmap())
            # loop = asyncio.get_event_loop()
            # task = loop.create_task(transportVicSearch_async(ctx, train.upper(), embed, embed_update))
            # await task

    await maintenance_func(ctx)
            
@search.command(name="tram", description="Search for a specific Tram")
@app_commands.describe(tram="tram")
async def tramsearch(ctx, tram: str):
    await ctx.response.defer()
    log_command(ctx.user.id, 'tram-search')
    channel = ctx.channel
    type = tramType(tram)

    await printlog(f'Set: {tram}')
    await printlog(f"Tram Type: {type}")
    if type is None:
        await ctx.edit_original_response(content="Tram not found")
    else:
        embed = discord.Embed(title=f"Info for {tram.upper()} ({type}):", color=tram_colour)
        # embed.set_thumbnail(url=getIcon(type))  # cant be bothered with image rn
        
        try:
            information = tramData(tram)
            # await printlog(information)
            if information[6] != 'n/a':
                infoData = f'**Depot:** {information[3]}\n**Operator:** {information[2]}\n**Livery:** {information[4]}\n**Status:** {information[5]}\n**Entered Service:** {information[7]}\n**Interior:** {information[6]}\n**Track Gauge:** {information[8]}\n**myki generation:** {information[9]}\n'
            else:
                infoData = f'**Depot:** {information[3]}\n**Operator:** {information[2]}\n**Livery:** {information[4]}\n**Status:** {information[5]}\n**Entered Service:** {information[7]}\n**Track Gauge:** {information[8]}\n**myki generation:** {information[9]}\n'
                
            # thing if the user has been on
            def checkTrainRidden(variable, file_path):
                if not os.path.exists(file_path):
                    print(f"The file {file_path} does not exist.")
                    return False, []

                log_ids = []
                with open(file_path, mode='r') as file:
                    csv_reader = csv.reader(file)
                    for row in csv_reader:
                        if row[1] == variable:
                            log_ids.append(row[0])
                
                return bool(log_ids), log_ids
        
            fPath = f'utils/trainlogger/userdata/tram/{ctx.user.name}.csv'
            result, log_ids = checkTrainRidden(tram, fPath)
            if result:
                log_ids_str = ', '.join([f'`{id}`' for id in log_ids])
                infoData += f'\n\nYou have been on this tram before (Log IDs: {log_ids_str})\n'
                
            embed.add_field(name='Information', value=infoData)
        except:
            if type == 'G-Class':
                embed.add_field(name='Information', value='**Status:** Testing')
            else:
                embed.add_field(name='Information', value='None available')
        try:
            import commands.searchtram as tramsearch
            output = tramsearch.tramtracker(tram)
            if output:
                current_time = datetime.now()
                date = f"{current_time.year}{current_time.month:02}{current_time.day:02}"
                tripinfo = ""
                for trip in output:
                    tripinfo += f"Trip ID: [{trip['trip_id']}](<https://anytrip.com.au/region/vic?selectedTrip=tripInstance%2F{date}%2Fau3:ac:{trip['trip_id']}%2F0>) \n"
                    route_id = trip['route_id']
                    route_id = route_id.split('-')[2].split(':')[0]
                    tripinfo += f"Route: {route_id} \n"
            embed.add_field(name="Current trip(s)", value=tripinfo,inline=False)
        except:
            await printlog(f'notrunning tram')
        if type !='G-Class':
            embed.add_field(name="Deloyments", value=f"[transportvic.me](<https://transportvic.me/tram/tracker/fleet?fleet={tram}>)", inline=False)
        imageURL, credits = getTramImage(tram.upper())
        if imageURL is not None:
            embed.set_image(url=imageURL)
            embed.set_footer(text=f'Photo by: {credits}\nMPTG (Icon), Vicsig (Other info), Myki info: r/MT discord community')
        else:
            embed.set_footer(text='MPTG (Icon), Vicsig (Other info), Myki info: r/MT discord community')

        
        # embed.add_field(name='<a:botloading2:1261102206468362381> Loading trip data', value='⠀')
        embed_update = await ctx.edit_original_response(embed=embed)

    await maintenance_func(ctx)

async def busOpsautocompletion(
    interaction: discord.Interaction,
    current: str
) -> typing.List[app_commands.Choice[str]]:
    # 1. Use set() to remove duplicates from busOps
    # 2. Use sorted() to keep the list in alphabetical order
    unique_operators = sorted(set(busOps))
    
    # 3. Return the filtered list (limited to 25 to prevent Discord API errors)
    return [
        app_commands.Choice(name=operator, value=operator)
        for operator in unique_operators if current.lower() in operator.lower()
    ][:25]

import utils.bussearch as bussearch
@search.command(name="bus", description="Search for a specific Bus")
@app_commands.describe(bus="bus number or plate")
@app_commands.autocomplete(operator=busOpsautocompletion)
async def bussearchcommand(ctx, bus: str, operator:str='Unknown'):
    await ctx.response.defer()
    bus = bus.upper()
    if operator != "Unknown":
        await printlog(f'getting operator: {operator}')
        operatorlist = {"Dysons":'D',"Kinetic":'K',"Transit Systems":'TS',"Ventura":'V',"CDC":'C',"Skybus":'SK',"McKenzies":'MK',"Martyrs":'MT',"Sunbury":'S',"Cranbourne":'CR',"Christians":'CH'}
        if operator == 'Ventura Bus Lines':
            operator = 'Ventura'
        elif operator == 'Cdc Melbourne':
            operator = 'CDC'
        elif operator == 'McKenzies Tourist Service':
            operator = 'McKenzies'
        elif operator == 'Martyrs Bus Service':
            operator = 'Martyrs'
        elif operator == 'Sunbury Bus Service':
            operator == 'Sunbury'
        elif operator == 'Cranbourne Transit':
            operator = 'Cranbourne'
        elif operator == 'Christians Bus Lines':
            operator = 'Christians'

        bus = operatorlist[operator] + bus
    
    await printlog(f'searching: {bus}')
    embed= await bussearch.search(bus, ctx)
    try:
        if embed == 'n':
            await ctx.edit_original_response(content="Please use operator prefix before number:\nDysons: `D`\nKinetic: `K`\nTransit Systems: TS\nVentura: `V`\nCDC: `C` (also include depot letter eg: W,T or O)\nSkybus: `SK`\nMcKenzies: `MK`\nChristian's: `CH`\nCranbourne: `CR`\nSunbury: `S`\nMartyr's: `MT`")
        else:
            await ctx.edit_original_response(embed=embed)

    except Exception as e:
        print(f'Error finding bus: {e}')
        await ctx.edit_original_response(content=f"can not find that bus in list")
    await maintenance_func(ctx)

@bot.tree.command(name="import-bus-tram-data", description="ADMIN ONLY Import csv data for search bus and tram")
@app_commands.describe(mode="bus or tram")
@app_commands.choices(mode=[
    app_commands.Choice(name="Bus", value="bus"),
    app_commands.Choice(name="Tram", value="tram"),
])
    
async def importbustram(ctx, mode:str, file:discord.Attachment):
    if ctx.user.id in admin_users:
        await ctx.response.defer()
        try:
            await file.save(f'temp/{file.filename}')
            if not file.filename.endswith('.csv'):
                await ctx.edit_original_response(content="Invalid file format! Make sure you're uploading a CSV file.")
                return
            if mode == 'bus':
                save_path = f'utils/bussets.csv'
            elif mode == 'tram':
                save_path = f'utils/tramsets.csv'
            shutil.copy(f'temp/{file.filename}', save_path)  
            await ctx.edit_original_response(content=f"Successfully imported data for {mode} to `{save_path}`")
            await printlog(f"Successfully imported data for {mode} to `{save_path}`")
            os.remove(f'temp/{file.filename}') 
        except Exception as e:
                await ctx.edit_original_response(content=f"Error importing data: {str(e)}")
                await printlog(f'error importing bus/tram data: {str(e)}')
    else:
        await ctx.edit_original_response("You do not have permission to use this command.")
        return
    await maintenance_func(ctx)
    
    
# add a favourite stop
async def stop_autocompletion(
    interaction: discord.Interaction,
    current: str
) -> typing.List[app_commands.Choice[str]]:
    stations = ptv_list.copy()
    suggestions = []
    
    # Add matching stations 
    for station in stations:
        if current.lower() in station.lower():
            suggestions.append(app_commands.Choice(name=station, value=station))
    return suggestions[:25]

@favourites.command(name="add", description="Add a favourite stop")
@app_commands.describe(stop="Stop name")
@app_commands.autocomplete(stop=stop_autocompletion)
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def favourite(ctx, stop: str):
    await ctx.response.defer(ephemeral=True)
    log_command(ctx.user.id, 'favourite-stop')
    
    # add the stop to the favourites
    message = save_favourites(ctx.user.id, stop)
    
    await ctx.edit_original_response(content=message)
    await maintenance_func(ctx)
    
async def stop_autocompletion(
    interaction: discord.Interaction,
    current: str
) -> typing.List[app_commands.Choice[str]]:
    # Get favourites list
    favourites = get_favourites(interaction.user.id)
    suggestions = []
    
    # Add matching favourites
    for fav in favourites:
        if current.lower() in fav.lower():
            suggestions.append(app_commands.Choice(name=f"⭐ {fav}", value=fav))
    return suggestions[:25]

@favourites.command(name="remove", description="Remove a favourite stop")
@app_commands.describe(stop="Stop name")
@app_commands.autocomplete(stop=stop_autocompletion)
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def remove(ctx, stop: str):
    await ctx.response.defer(ephemeral=True)
    log_command(ctx.user.id, 'remove-favourite-stop')
    
    # remove the stop from favourites
    message = remove_favourite(ctx.user.id, stop)
    
    await ctx.edit_original_response(content=message)
    await maintenance_func(ctx)

# Next departures for a station
async def station_autocompletion(
    interaction: discord.Interaction,
    current: str
) -> typing.List[app_commands.Choice[str]]:
    # Get favourites list
    favourites = get_favourites(interaction.user.id)
    stations = ptv_list_short.copy()
    suggestions = []
    
    # Add matching favourites first
    for fav in favourites:
        if current.lower() in fav.lower():
            suggestions.append(app_commands.Choice(name=f"⭐ {fav}", value=fav))
    
    # Add matching stations 
    for station in stations:
        if current.lower() in station.lower():
            suggestions.append(app_commands.Choice(name=station, value=station))
    return suggestions[:25]

async def time_autocompletion(
    interaction: discord.Interaction,
    current: str
) -> typing.List[app_commands.Choice[str]]:
    # Get favourites list
    times = list(pd.date_range("00:00", "23:59", freq="1min").strftime('%H:%M'))
    suggestions = []
    
    # Add matching time
    for time in times:
        if current.lower() in time.lower():
            suggestions.append(app_commands.Choice(name=time, value=time))
    return suggestions[:25]

@bot.tree.command(name="departures", description="Upcoming departures for a stop")
@app_commands.describe(stop="Station/Stop name")
@app_commands.autocomplete(stop=station_autocompletion)
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.choices(
    line=[
        app_commands.Choice(name="Alamein", value="Alamein"),
        app_commands.Choice(name="Belgrave", value="Belgrave"),
        app_commands.Choice(name="Craigieburn", value="Craigieburn"),
        app_commands.Choice(name="Cranbourne", value="Cranbourne"),
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
        app_commands.Choice(name="Flemington Racecourse", value="Flemington Racecourse"),
        app_commands.Choice(name="City Circle", value="City Circle"),
    ]
)
@app_commands.describe(time="The time you want to search the departures from (use 24hr time format)")
@app_commands.autocomplete(time=time_autocompletion)

# test
async def departures(ctx, stop: str, time:str="none", line:str='all'):
    async def nextdeps(station, time):
        channel = ctx.channel
        await ctx.response.defer()
        log_command(ctx.user.id, 'departures-search')
        station = station.strip('⭐ ')
        try:
            await printlog(f'{ctx.user.name} ran departures for {station} at time {datetime.today()} in channel {ctx.channel.mention}')
        except:
            await printlog(f'{ctx.user.name} ran departures for {station} at time {datetime.today()}')

        if station in metro_stops:
            mode = '0'
        elif station in tram_stops:
            mode = '1'
        elif station in bus_stops:
            mode ='2'
        elif station in vline_stops:
            mode = '3'
        elif station.endswith('Railway Station'):
            mode = '3'
        else:
            mode = '0' # default to metro if not found
            

        # if mode == '3':
        #     pass
        #     # await ctx.edit_original_response(content="You cannot currently search departures for V/Line services")
            # return
        if line != "all" and mode != "0":
            await ctx.edit_original_response(content="You can only specify a line for trains")
            return
        
        print(f'Finding stop id for {station}, mode {mode}')
        stop_id = nameToStopID(station, mode)
        
        if stop_id == 'None':
            print('Trying to see if its a V/Line station')
            mode = 3
            stop_id = nameToStopID(f'{station} Railway Station', mode)
            if stop_id == 'None':
                await ctx.edit_original_response(content=f"Cannot find stop {station.title()}.")
                return

        timecopy = time
        if time == "none":
            dt = datetime.fromisoformat(str(datetime.today()))
            dt = dt.astimezone()
            final_time = dt.astimezone(timezone.utc)
        else:
            try:
                # add leading 0 to time
                if len(time) == 4:
                    time = '0' + time
                date = datetime.today().strftime('%Y-%m-%d')
                date = date + ' '
                time = date + time
                dt = datetime.fromisoformat(time)
                dt = dt.astimezone()
                final_time = dt.astimezone(timezone.utc)
            except Exception as e:
                await printlog(e)
            try: # this will see if its a valid time
                await printlog(final_time)
            except UnboundLocalError:
                await ctx.edit_original_response(content=f'Invalid time: `{timecopy}`, loading current departures <a:botloading2:1261102206468362381>')
                dt = datetime.fromisoformat(str(datetime.today()))
                dt = dt.astimezone()
                final_time = dt.astimezone(timezone.utc)

        start_time = convert_iso_to_unix_time(final_time, 'short-time')

        # get departures for the stop:
        depsData = departures_api_request(stop_id, mode)
        try:
            departures = depsData['departures']
            runs = depsData['runs']
            routes = depsData['routes']
        except:
            await ctx.edit_original_response(content=f"Cannot find departures for {station.title()}")
            return
         
        
        # make embed with data
        print(f'Making embed for mode {mode}')
        # Default embed title and color
        embed_title = f"Departures from {station.title()}"
        embed_color = ptv_grey

        # Customize embed based on mode and line
        if mode == "0":
            embed_color = metro_colour
            if line == "all":
                embed_title = f"Metro trains departing {station.title()}"
            else:
                embed_title = f"Metro trains departing {station.title()} on the {line} line"
        elif mode == "1":
            embed_color = tram_colour
            embed_title = f"Trams departing {station.title()}"
        elif mode == "2":
            embed_color = bus_colour
            embed_title = f"Busses departing {station.title()}"
        elif mode == "3":
            embed_color = vline_colour
            embed_title = f"V/Line trains departing {station.title()}"

        # Add "Station" suffix if not already present
        if not station.title().endswith('Station') and mode in ["0", "3"]:
            embed_title += " Station"
            
        # Add timestamp to title
        embed_title += f" after {start_time}"
        
        # Create embed
        embed = discord.Embed(title=embed_title, timestamp=discord.utils.utcnow(), color=embed_color)


        fields = 0
        
        departures = [departure for departure in departures if get_route_name(departure['route_id']) == line or line == "all"]

        
        for departure in departures:
            # print(f'Departure: {departure}')
            lineaddon = ''
            route_id= departure['route_id'] 
            scheduled_departure_utc = departure['scheduled_departure_utc']
            if isPast(scheduled_departure_utc, final_time):
                # print(f"time in past")
                pass
            else:
                run_ref = departure['run_ref']
                at_platform = departure['at_platform']
                platform_number = departure['platform_number']
                note = departure['departure_note']
                flags = departure['flags'].split('_')
                
                # get info for the run:
                desto = runs[run_ref]['destination_name']
                try:
                    trainType = runs[run_ref]['vehicle_descriptor']['description']
                    trainNumber = runs[run_ref]['vehicle_descriptor']['id']
                except:
                    trainType = ''
                    trainNumber = ''
                    
                # get live departure time
                if mode == "0":
                    stoppingPattern=getStoppingPattern(run_ref, mode)
                    delay = 0
                    for stop in stoppingPattern:
                        if stop[0].strip() == station.title():
                            scheduled_departure_utc = stop[1] 
                            # Calculate delay in minutes
                            delay = (convert_times(stop[1]) - convert_times(stop[3])) // 60  # Convert time difference to minutes
                            if delay > 0:
                                delaystring = f'{delay} minutes late'
                            else:
                                delaystring = ''
                        else:
                            delaystring = ''
                else:
                    delaystring = ''
                
                # get the direction for busses and trams and also the route number
                if mode in ['1', '2']:
                    route_number = routes[str(route_id)]['route_number']
                    direction = getDirectionName(runs[run_ref]['direction_id'])     
                
                # train emoji
                # trainType = getEmojiForDeparture(trainType)
                
                # Convert PTV run REF to TDN
                if run_ref.startswith('9') and mode == '0':
                    TDN = RunIDtoTDN(run_ref)
                else:
                    TDN = run_ref

                #convert to timestamp
                depTime=convert_iso_to_unix_time(scheduled_departure_utc)
                #get route name:
                route_name = get_route_name(route_id)
                
                # get the train type from the number
                if mode == "0":
                    print(f'Train number: {trainNumber}')
                    trainType, trainNumber = await cleanAPITrainNumber(trainNumber)       
                    print(f'Train type: {trainType}')    
                    # replacement bus
                    if flags.__contains__('RRB-RUN'):
                        trainType = '<:Disruption:1322444175941173280> Replacement Bus'
                        trainNumber = ''
                        platform_number = 'Replacement Bus Stop'
                        lineaddon += '<:bus:1241165769241530460>'
                
                # thing for stony point
                if route_name == "Stony Point":
                    trainType = "Sprinter"
                    if station.title() == "Frankston":
                        platform_number = "3"
                    else:
                        platform_number = "1"
                
                if mode == '0':
                    embed.add_field(name=f"{getlineEmoji(route_name)}{lineaddon}\n{desto} {note if note else ''}", value=f"\nDeparting {depTime} ({convert_iso_to_unix_time(scheduled_departure_utc,'short-time')}) {delaystring}\nPlatform {platform_number}\n{trainType} {trainNumber}\nTDN: `{TDN}`")
                elif mode in ['1', '2']: 
                    embed.add_field(name=f"{route_number} to {desto}", value=f"\nDeparting {depTime} ({convert_iso_to_unix_time(scheduled_departure_utc,'short-time')})\nRun `{run_ref}`") 
                elif mode == '3':
                    embed.add_field(name=f"dsddsds", value=f"\nDeparting {depTime} ({convert_iso_to_unix_time(scheduled_departure_utc,'short-time')})\nRun `{run_ref}`")
                    
                fields = fields + 1
                if fields == 9:
                    break
        # add message for no depatures
        if fields == 0:
            embed.add_field(name="No departures found", value="There are currently no departures for this stop.")
        
        # disruptions:
        disruptions = getStationDisruptions(stop_id)
        disruptionsAmount = len(disruptions)
        if disruptionsAmount > 3:
            disruptions = disruptions[:3]  # Limit to 3 disruptions for embed size
            disruptions.insert(0,{
                'title': f'+{disruptionsAmount-3} more disruptions',
                'description': 'view more',
                'url': 'https://www.ptv.vic.gov.au/disruptions/disruptions-information/'})
        for disruption in disruptions:
            # Truncate disruption title if its ling
            title = disruption['title']
            if len(title) > 200:
                title = title[:200] + "..."
            
            embed.insert_field_at(index=0, name=f"<:Disruption:1322444175941173280> {title}", 
                                value=f"[{disruption['description']}]({disruption['url']})\n", inline=False)
        # get station image
        if mode == '0' or mode == '3':
            image = getStationImage(station)
            if image != None: 
                embed.set_thumbnail(url=image)  
                embed.set_footer(text=f"V/Line departures are unavailable | Photo by {getPhotoCredits(station)}")       
            else:
                embed.set_footer(text=f"V/Line departures are unavailable")
        
        try:
            await ctx.edit_original_response(embed=embed, content='')     
        except Exception as e:
            await ctx.edit_original_response(content=f'Error loading departures. Please try again later.\n```{e}```')
            await printlog(f'ErROR: {e}') 
            await printlog(traceback.format_exc())  
    
    asyncio.create_task(nextdeps(stop, time))
    await maintenance_func(ctx)
    
    
# ptv api search command
@search.command(name="tv", description="Search stops, routes and myki ticket outlets provided by Transport Victoria")
@app_commands.describe(search="What to search for")
@app_commands.choices(type=[
        app_commands.Choice(name="stops", value="stops"),
        app_commands.Choice(name="routes", value="routes"),
        app_commands.Choice(name="myki outlets", value="myki")
])
@app_commands.describe(maximum_responses="How many responses for each mode of transport you want")
async def search(ctx, search:str, type:str, maximum_responses:int=3):
    async def ptvsearch(search):
        await ctx.response.defer()
        log_command(ctx.user.id, 'ptv-search')
        fmtSearch = search.replace(" ", "%20")
        data = search_api_request(fmtSearch)
        if type == 'stops':
            if data['stops']:
                embed = discord.Embed(title=f"Results for {search}:")
                train_count = 0
                vline_count = 0
                tram_count = 0
                bus_count = 0
                coach_count = 0
                train_list = []
                vline_list = []
                tram_list = []
                bus_list = []
                coach_list = []
                train_embed = f""
                vline_embed = f""
                tram_embed = f""
                bus_embed = f""
                coach_embed = f""
                for stop in data['stops']:
                    stop_name = stop['stop_name']
                    stop_id = stop['stop_id']
                    stop_suburb = stop['stop_suburb']
                    route_type = stop['route_type']
                    # find emojis for the route type
                    if route_type == 3:
                        emoji = getVlineStopType(stop_name, True)
                    else:
                        emoji = getModeEmoji(route_type)
                    url = f'https://www.ptv.vic.gov.au/stop/{stop_id}'

                    if emoji == "<:train:1241164967789727744>" and train_count < maximum_responses:
                        train_count +=1
                        train_list.append(f"**{stop_name}**\n{stop_suburb}\n[View on Transport Victoria website]({url})\n")                    
                    elif emoji == "<:vline:1241165814258729092>" and vline_count < maximum_responses:
                        vline_count +=1
                        vline_list.append(f"**{stop_name}**\n{stop_suburb}\n[View on Transport Victoria website]({url})\n")
                    elif emoji == "<:tram:1241165701390012476>" and tram_count < maximum_responses:
                        tram_count +=1
                        tram_list.append(f"**{stop_name}**\n{stop_suburb}\n[View on Transport Victoria website]({url})\n")
                    elif emoji == "<:bus:1241165769241530460>" and bus_count < maximum_responses:
                        bus_count +=1
                        bus_list.append(f"**{stop_name}**\n{stop_suburb}\n[View on Transport Victoria website]({url})\n")
                    elif emoji == "<:coach:1241165858274021489>" and coach_count < maximum_responses:
                        coach_count +=1
                        coach_list.append(f"**{stop_name}**\n{stop_suburb}\n[View on Transport Victoria website]({url})\n")
                
                if train_count != 0:
                    for train in train_list:
                        train_embed = f"{train_embed}{train}"
                    embed.add_field(name="<:train:1241164967789727744> Train", value=f"{train_embed}\n\n", inline=False)

                if vline_count != 0:
                    for vline in vline_list:
                        vline_embed = f"{vline_embed}{vline}"
                    embed.add_field(name="<:vline:1241165814258729092> V/Line", value=f"{vline_embed}\n\n", inline=False)

                if tram_count != 0:
                    for tram in tram_list:
                        tram_embed = f"{tram_embed}{tram}"
                    embed.add_field(name="<:tram:1241165701390012476> Tram", value=f"{tram_embed}\n\n", inline=False)

                if bus_count != 0:
                    for bus in bus_list:
                        bus_embed = f"{bus_embed}{bus}"
                    embed.add_field(name="<:bus:1241165769241530460> Bus", value=f"{bus_embed}\n\n", inline=False)

                if coach_count != 0:
                    for coach in coach_list:
                        coach_embed = f"{coach_embed}{coach}"

                    embed.add_field(name="<:coach:1241165858274021489> Coach", value=f"{coach_embed}\n\n", inline=False)
                embed.set_footer(text="Tip: You can save a stop to your favourites with /favourites add <stop>")
                
            else:
                embed = discord.Embed(title=f"Results for {search}:")
                embed.add_field(name="No stops found", value="Try searching for something else")
                
        elif type == 'routes':
            if data['routes']:
                embed = discord.Embed(title=f"Results for {search}:")
                train_count = 0
                vline_count = 0
                tram_count = 0
                bus_count = 0
                coach_count = 0
                train_list = []
                vline_list = []
                tram_list = []
                bus_list = []
                coach_list = []
                train_embed = f""
                vline_embed = f""
                tram_embed = f""
                bus_embed = f""
                coach_embed = f""
                for route in data['routes']:
                    route_name = route['route_name']
                    route_id = route['route_id']
                    route_number = route['route_number'] + " - " if route['route_number'] else ""
                    route_service_status = route['route_service_status']['description']
                    url = f'https://www.ptv.vic.gov.au/route/{route_id}'
                    emoji = getModeEmoji(route['route_type'])

                    if emoji == "<:train:1241164967789727744>" and train_count < maximum_responses:
                        train_count +=1
                        train_list.append(f"**{route_number}{route_name}**\n{route_service_status}\n[View on Transport Victoria website]({url})\n")                    
                    elif emoji == "<:vline:1241165814258729092>":
                        if route_id in vline_rail_lines and vline_count < maximum_responses:
                            vline_count +=1
                            vline_list.append(f"**{route_number}{route_name}**\n{route_service_status}\n[View on Transport Victoria website]({url})\n")
                        if coach_count < maximum_responses:
                            coach_count +=1
                            coach_list.append(f"**{route_number}{route_name}**\n{route_service_status}\n[View on Transport Victoria website]({url})\n")
                    elif emoji == "<:tram:1241165701390012476>" and tram_count < maximum_responses:
                        tram_count +=1
                        tram_list.append(f"**{route_number}{route_name}**\n{route_service_status}\n[View on Transport Victoria website]({url})\n")
                    elif emoji == "<:bus:1241165769241530460>" and bus_count < maximum_responses:
                        bus_count +=1
                        bus_list.append(f"**{route_number}{route_name}**\n{route_service_status}\n[View on Transport Victoria website]({url})\n")
                
                if train_count != 0:
                    for train in train_list:
                        train_embed = f"{train_embed}{train}"
                    embed.add_field(name="<:train:1241164967789727744> Train", value=f"{train_embed}\n\n", inline=False)

                if vline_count != 0:
                    for vline in vline_list:
                        vline_embed = f"{vline_embed}{vline}"
                    embed.add_field(name="<:vline:1241165814258729092> V/Line", value=f"{vline_embed}\n\n", inline=False)

                if tram_count != 0:
                    for tram in tram_list:
                        tram_embed = f"{tram_embed}{tram}"
                    embed.add_field(name="<:tram:1241165701390012476> Tram", value=f"{tram_embed}\n\n", inline=False)

                if bus_count != 0:
                    for bus in bus_list:
                        bus_embed = f"{bus_embed}{bus}"
                    embed.add_field(name="<:bus:1241165769241530460> Bus", value=f"{bus_embed}\n\n", inline=False)

                if coach_count != 0:
                    for coach in coach_list:
                        coach_embed = f"{coach_embed}{coach}"
                    embed.add_field(name="<:coach:1241165858274021489> Coach", value=f"{coach_embed}\n\n", inline=False)
            else:
                embed = discord.Embed(title=f"Results for {search}:")
                embed.add_field(name="No routes found", value="Try searching for something else")
                
        elif type == 'myki':
            if data['outlets']:
                embed = discord.Embed(title=f"Results for {search}:")
                count = 0
                for outlet in data['outlets']:
                    buisness = outlet['outlet_business']
                    suburb = outlet['outlet_suburb']
                    url = generate_google_maps_link(outlet['outlet_latitude'], outlet['outlet_longitude']) 
                    embed.add_field(name=f"{buisness} - {suburb}", value=f'[View on Google Maps]({url})',inline=False)
                    count +=1
                    if count == maximum_responses:
                        break
            else:
                embed = discord.Embed(title=f"Results for {search}:")
                embed.add_field(name="No routes found", value="Try searching for something else")
                
        try:
            await ctx.edit_original_response(embed=embed)
        except Exception as e:
            await printlog('Too many characters because "maximum_responses" was set to high.')
            await ctx.edit_original_response(content='''"maximum_responses" set too high, try a lower number. If you're using the myki outlet mode, the maximum is 25.''')
            return
    asyncio.create_task(ptvsearch(search))
    await maintenance_func(ctx)
        



# Montague Bridge search
'''@bot.tree.command(name="days-since-montague-hit", description="See how many days it has been since the Montague Street bridge has been hit.")
async def train_line(ctx):
    await ctx.response.send_message(f"Checking...")
    channel = ctx.channel
    
    embed = discord.Embed(title=f"How many days since the Montague Street bridge has been hit?", color=tram_colour)
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
@app_commands.describe(rounds = "The number of rounds. Defaults to 1, max 100.", line='Select a line to only show photos from that line', ultrahard = "Ultra hard mode.")
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
])
async def game(ctx,rounds: int = 1, line:str='all', ultrahard: bool=False):
    channel = ctx.channel
    log_command(ctx.user.id, 'game-station-guesser')
    await maintenance_game_func(ctx)
    async def run_game(): 

        # Check if a game is already running in this channel
        if channel in channel_game_status and channel_game_status[channel]:
            await ctx.response.send_message("A game is already running in this channel.", ephemeral=True )
            return
        if rounds > 500:
            await ctx.response.send_message("You can only play a maximum of 500 rounds!", ephemeral=True )
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

        # Filter data by line if a specific line is selected
        if line != 'all':
            try:
                line_stations = lines_dictionary_log_train_map_post_munnel[line][0]
                filtered_data = []
                for row in data:
                    if row[1] in line_stations:  # Check if station is in the line's station list
                        filtered_data.append(row)
                data = filtered_data
            except KeyError:
                await ctx.response.send_message(f"Invalid line selected: {line}")
                return

        ignoredRounds = 0
        setLine = 'All Lines' if line == 'all' else f'{line.title()} line'

        # stuff for end of game stats
        incorrectAnswers = 0
        correctAnswers = 0
        skippedGames = 0
        participants = []
        
        # Get the photos at start and shuffle them
        try:
            available_photos = data.copy()
            random.shuffle(available_photos)
            
            if len(available_photos) < rounds:
                await ctx.response.send_message(f'Not enough photos available for {rounds} rounds. Maximum available is {len(available_photos)}.')
                channel_game_status[channel] = False
                return
            
        except IndexError:
            await ctx.response.send_message('There are currently no photos for your selected options! Try a different line.')
            channel_game_status[channel] = False
            return

        for round in range(rounds):
            roundResponse = False
            
            # Get the next photo from the shuffled list
            random_row = available_photos[round]

            # Extract data from the random row
            url = random_row[0]
            station = random_row[1] 
            difficulty = random_row[2]
            credit = random_row[3]

            if ultrahard:
                embed = discord.Embed(title=f"Guess the station! | {setLine}", color=ultrahard_colour, description=f"Mention the bot at the start of you message e.g. `@TrackPulse Vic Lilydale`. You have 30 seconds to answer.\n\n**Difficulty:** `{difficulty.upper()}`")
            else:
                embed = discord.Embed(title=f"Guess the station! | {setLine}", description=f"Mention the bot at the start of you message e.g. `@TrackPulse Vic Lilydale`. You have 30 seconds!\n\n**Difficulty:** `{difficulty}`")
                if difficulty == 'Very Easy':
                    embed.color = very_easy_colour
                elif difficulty == 'Easy':
                    embed.color = easy_colour
                elif difficulty == 'Medium':
                    embed.color = medium_colour
                elif difficulty == 'Hard':
                    embed.color = hard_colour
                elif difficulty == 'Very Hard':
                    embed.color = very_hard_colour
            
            embed.set_image(url=url)
            embed.set_footer(text=f"Photo by {credit}. | {len(data)} photos in set | Started by {ctx.user.name}")
            embed.set_author(name=f"Round {round+1}/{rounds}")

            # Send the embed message
            if round == 0:
                await ctx.response.send_message(embed=embed)
            else:
                await ctx.channel.send(embed=embed)

            # Define a check function to validate user input
            async def check(m):
                return m.channel == channel and m.author != bot.user and m.content.startswith(f'<@{bot.user.id}>')
            try:
                correct = False
                if ultrahard:
                    gameType = 'ultrahard'
                else:
                    gameType = 'guesser'
                
                
                while not correct:
                    # Wait for user's response in the same channel
                    user_response = await bot.wait_for('message', check=check, timeout=30.0)
                    if await check(user_response) == True:  # fixed cause check broke
                    
                        # Check if the user's response matches the correct station
                        if user_response.content[len(f'<@{bot.user.id}>'):].lower().replace(" ", "") == station.lower().replace(" ", ""):
                            log_command(user_response.author.id, 'game-station-guesser-correct')
                            if ultrahard:
                                await ctx.channel.send(f"{user_response.author.mention} guessed it right!")
                            else:
                                await ctx.channel.send(f"{user_response.author.mention} guessed it right! {station.title()} was the correct answer!")
                            correct = True
                            roundResponse = True
                            correctAnswers += 1
                            ignoredRounds = 0
                            await printlog(f'Ignored rounds: {ignoredRounds}')
                            if ultrahard:
                                addLb(user_response.author.id, user_response.author.name, 'ultrahard')
                            else:
                                addLb(user_response.author.id, user_response.author.name, 'guesser')
                            if user_response.author not in participants:
                                participants.append(user_response.author)

                        elif user_response.content.lower() == f'<@{bot.user.id}> skip':
                            if user_response.author.id == ctx.user.id or user_response.author.id in admin_users :
                                await ctx.channel.send(f"Round {round+1} skipped. The answer was ||{station.title()}||" if not ultrahard else f"Round {round+1} skipped.")
                                log_command(user_response.author.id, 'game-station-guesser-skip')
                                skippedGames += 1
                                roundResponse = True
                                break
                            else:
                                await ctx.channel.send(f"{user_response.author.mention} you can only skip the round if you were the one who started it.")
                                roundResponse = True
                        elif user_response.content.lower() == f'<@{bot.user.id}> stop':
                            if user_response.author.id == ctx.user.id or user_response.author.id in admin_users :
                                await ctx.channel.send(f"Game ended.")
                                log_command(user_response.author.id, 'game-station-guesser-stop')
                                embed = discord.Embed(title=f"Game Summary | {setLine}")
                                embed.add_field(name="Rounds played", value=f'{skippedGames} skipped, {rounds} total.', inline=True)
                                embed.add_field(name="Correct Guesses", value=correctAnswers, inline=True)
                                embed.add_field(name="Incorrect Guesses", value=incorrectAnswers, inline=True)
                                embed.add_field(name="Participants", value=', '.join([participant.mention for participant in participants]))
                                await ctx.channel.send(embed=embed)  
                                for user in participants:
                                    await addGameAchievement(user.name,ctx.channel.id,user.mention)  
                                channel_game_status[channel] = False
                                return
                            else:
                                await ctx.channel.send(f"{user_response.author.mention} you can only stop the game if you were the one who started it.")  
                        
                        # view the image info (admin only) 
                        elif user_response.content.lower() == f'<@{bot.user.id}> reveal' or user_response.content.lower() == f'<@{bot.user.id}> release':
                            if user_response.author.id in admin_users :
                                await ctx.channel.send(f"Station Name: `{station}`\nUrl: `{url}`")
                            else:
                                await ctx.channel.send(f"{user_response.author.mention} you can only reveal the image if you are an admin.")
                        
                        
                        else:
                            await user_response.add_reaction('❌')
                            log_command(user_response.author.id, 'game-station-guesser-incorrect')
                            roundResponse = True
                            incorrectAnswers += 1
                            if ultrahard:
                                addLoss(user_response.author.id, user_response.author.name, 'ultrahard')
                            else:
                                addLoss(user_response.author.id, user_response.author.name, 'guesser')
                            if user_response.author not in participants:
                                participants.append(user_response.author)
                          
            except asyncio.TimeoutError:
                if ultrahard:
                    await ctx.channel.send(f"Times up. Answers are not revealed in ultrahard mode.")
                else:
                    await ctx.channel.send(f"Times up. The answer was ||{station.title()}||")
            finally:
                if not roundResponse:
                    ignoredRounds += 1
                await printlog(f'Ignored rounds: {ignoredRounds}')
                if ignoredRounds >= 4 and roundResponse == False:
                    await ctx.channel.send("No responses for 4 rounds. Game ended.")
                    embed = discord.Embed(title=f"Game Summary | {setLine}")
                    embed.add_field(name="Rounds played", value=f'{skippedGames} skipped, {rounds} total.', inline=True)
                    embed.add_field(name="Correct Guesses", value=correctAnswers, inline=True)
                    embed.add_field(name="Incorrect Guesses", value=incorrectAnswers, inline=True)
                    embed.add_field(name="Participants", value=', '.join([participant.mention for participant in participants]))
                    await ctx.channel.send(embed=embed)  
                    for user in participants:
                        await addGameAchievement(user.name,ctx.channel.id,user.mention)
                    return
                        
                # Reset game status after the game ends
                channel_game_status[channel] = False
                
        embed = discord.Embed(title=f"Game Summary | {setLine}")
        embed.add_field(name="Rounds played", value=f'{skippedGames} skipped, {rounds} total.', inline=True)
        embed.add_field(name="Correct Guesses", value=correctAnswers, inline=True)
        embed.add_field(name="Incorrect Guesses", value=incorrectAnswers, inline=True)
        embed.add_field(name="Participants", value=', '.join([participant.mention for participant in participants]))
        await ctx.channel.send(embed=embed)  
        for user in participants:
            await addGameAchievement(user.name,ctx.channel.id,user.mention)

    # Run the game in a separate task
    try:
        asyncio.create_task(run_game())
    except Exception as e:
        await printlog(f'GUESSER ERROR: {e}')
        await ctx.channel.send(f'An error has occurred\n```{e}```')
        await log_channel.send(f'Error: ```{e}```\n with guesser run ran by {ctx.user.mention}\n<@{USER_ID}>')



    
@stats.command(name="leaderboard", description="Leaderboards for the games.",)
@app_commands.describe(game="What game's leaderboard to show?")
@app_commands.choices(game=[
        app_commands.Choice(name="Station Guesser", value="guesser"),
        app_commands.Choice(name="Ultrahard Station Guesser", value="ultrahard"),
        app_commands.Choice(name="Station order game", value="domino"),
        app_commands.Choice(name="Station Hangman", value="hangman"),
])
@app_commands.choices(scope=[
        app_commands.Choice(name="Global", value="global"),
        app_commands.Choice(name="Server", value="server")
])
async def lb(ctx, game:str, scope:str='global'):
    log_command(ctx.user.id, 'view-leaderboard')
    channel = ctx.channel
    try:
        guild = bot.get_guild(ctx.guild.id)
    except AttributeError:
        guild = None
        scope = 'global'
    leaders = top5(game, scope, guild if scope == 'server' else None)
    if leaders == 'no stats':
        await ctx.response.send_message('There is no data for this game yet!',ephemeral=True) # lol this would never show
        return

    # Create the embed
    embed = discord.Embed(title=f"Top 10 players for {game}" if scope == 'global' else f'Top 10 players for {game} in {guild}', color=discord.Color.gold())
    
    count = 1
    for userid, number, losses, username in leaders:
        try:
            embed.add_field(name=f'{count}.', value=f'<@{userid}> ({username})\nCorrect Guesses: {str(number)}\nIncorrect Guesses: {str(losses)}\nAccuracy: {str(round((number/(number+losses))*100, 1))}%', inline=False)
        except:
            embed.add_field(name=f'{count}.', value=f'<@{userid}> ({username})\nCorrect Guesses: {str(number)}\nIncorrect Guesses: {str(losses)}', inline=False)
        count = count + 1
        
    await ctx.response.send_message(embed=embed)
    await maintenance_func(ctx)


# Station order game made by @domino

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
@app_commands.describe(rounds = "The number of rounds. Defaults to 1.", direction = "The directions you are listing the stations in. Defaults to Up or Down.", line ='Which line to guess stations from, defaults to all lines.')
@app_commands.choices(
    direction=[
        app_commands.Choice(name="Up or Down", value='updown'),
        app_commands.Choice(name="Up", value='up'),
        app_commands.Choice(name="Down", value='down')
        ],
    )
@app_commands.choices(line=[
        app_commands.Choice(name="Alamein", value="Alamein"),
        app_commands.Choice(name="Belgrave", value="Belgrave"),
        app_commands.Choice(name="Craigieburn", value="Craigieburn"),
        app_commands.Choice(name="Cranbourne", value="Cranbourne"),
        # app_commands.Choice(name="Flemington Racecourse", value="Flemington Racecourse"),
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
])

async def testthing(ctx, rounds: int = 1, direction: str = 'updown', line:str='all'):
    channel = ctx.channel
    log_command(ctx.user.id, 'game-station-order')
    await maintenance_game_func(ctx)
    async def run_game(line):
        # Check if a game is already running in this channel
        if channel in channel_game_status and channel_game_status[channel]:
            await ctx.response.send_message("A game is already running in this channel.", ephemeral=True )
            return
        if rounds > 10:
            await ctx.response.send_message("You can only play a maximum of 10 rounds!", ephemeral=True )
            return

        channel_game_status[channel] = True

        ignoredRounds = 0
        setLine = 'All Lines' if line == 'all' else f'{line.title()} line'
        
        # stuff for end of game stats
        incorrectAnswers = 0
        correctAnswers = 0
        skippedGames = 0
        participants = []

        for round in range(rounds):
            roundResponse = False

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
            if line == 'all':
                line = None
                while line == None:
                    line = linelist[random.randint(0,len(linelist)-1)]            

            # choose random station
            if line == 'Flemington Racecourse':
                if numdirection == 5 or numdirection == -5:
                    numdirection = random.choice([-4,-3,-2,2,3,4])
            station = None
            while station == None:
                station = lines_dictionary_log_train_map_post_munnel[line][0][random.randint(0,len(lines_dictionary_log_train_map_post_munnel[line][0])-1)]
                if not 0 <= lines_dictionary_log_train_map_post_munnel[line][0].index(station)+numdirection <= len(lines_dictionary_log_train_map_post_munnel[line][0]):
                    station = None

            embed = discord.Embed(
                title=f"Which __**{numdirection if numdirection > 0 else numdirection*-1}**__ stations are __**{direction1}**__ from __**{station}**__ station on the __**{line} line**__?",
                description=f"**Answers must be in the correct order!** Answer using this format:\n<@{bot.user.id}> `station1`, `station2`{', `station3`' if numdirection >= 3 or numdirection <= -3 else ''}{', `station4`' if numdirection >= 4 or numdirection <= -4 else ''}{', `station5`' if numdirection >= 5 or numdirection <= -5 else ''}\n\n*Use <@{bot.user.id}> skip to skip to the next round.*",
                colour=lines_dictionary_log_train_map_post_munnel[line][1])
            embed.set_author(name=f"Round {round+1}/{rounds}")
            if round == 0:
                await ctx.response.send_message(embed=embed)
            else:
                await ctx.channel.send(embed=embed)

            # Define a check function to validate user input
            async def check(m): 
                return m.channel == channel and m.author != bot.user and m.content.startswith(f'<@{bot.user.id}>')
            async def funnyCheck(m):    
                return m.channel == channel and m.author != bot.user

            # get list of correct stations
            if numdirection > 0:
                correct_list = lines_dictionary_log_train_map_post_munnel[line][0][lines_dictionary_log_train_map_post_munnel[line][0].index(station)+1:lines_dictionary_log_train_map_post_munnel[line][0].index(station)+numdirection+1]
            else:
                correct_list = lines_dictionary_log_train_map_post_munnel[line][0][lines_dictionary_log_train_map_post_munnel[line][0].index(station)+numdirection:lines_dictionary_log_train_map_post_munnel[line][0].index(station)]
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

                    if await check(user_response) == True:  # fixed cause check broke    
                        # Check if the user's response matches the correct station
                        if response == correct_list1:
                            await ctx.channel.send(f"{user_response.author.mention} guessed it correctly!")
                            addLb(user_response.author.id, user_response.author.name, 'domino')
                            log_command(user_response.author.id, 'game-station-order-correct')
                            correctAnswers += 1
                            ignoredRounds = 0
                            roundResponse = True
                            correct = True 
                        elif user_response.content.lower() == f'<@{bot.user.id}> skip':
                            if user_response.author.id == ctx.user.id or user_response.author.id in admin_users :
                                await ctx.channel.send(f"Round {round+1} skipped. The answer was ||{correct_list[0]}, {correct_list[1]}{f', {correct_list[2]}' if len(correct_list) >=3 else ''}{f', {correct_list[3]}' if len(correct_list) >=4 else ''}{f', {correct_list[4]}' if len(correct_list) >=5 else ''}||")
                                log_command(user_response.author.id, 'game-station-order-skip')
                                skippedGames += 1
                                roundResponse = True
                                break
                            else:
                                await ctx.channel.send(f"{user_response.author.mention} you can only skip the round if you were the one who started it.")
                        elif user_response.content.lower() == f'<@{bot.user.id}> stop':
                            if user_response.author.id == ctx.user.id or user_response.author.id in admin_users :
                                await ctx.channel.send(f"Game ended.")
                                log_command(user_response.author.id, 'game-station-order-stop')
                                embed = discord.Embed(title=f"Game Summary | {setLine}")
                                embed.add_field(name="Rounds played", value=f'{skippedGames} skipped, {rounds} total.', inline=True)
                                embed.add_field(name="Correct Guesses", value=correctAnswers, inline=True)
                                embed.add_field(name="Incorrect Guesses", value=incorrectAnswers, inline=True)
                                embed.add_field(name="Participants", value=', '.join([participant.mention for participant in participants]))
                                await ctx.channel.send(embed=embed)  
                                for user in participants:
                                    await addGameAchievement(user.name,ctx.channel.id,user.mention)
                                channel_game_status[channel] = False
                                return
                            else:
                                await ctx.channel.send(f"{user_response.author.mention} you can only stop the game if you were the one who started it.")
                        # view the image info (admin only) 
                        elif user_response.content.lower() == f'<@{bot.user.id}> reveal' or user_response.content.lower() == f'<@{bot.user.id}> release':
                            if user_response.author.id in admin_users :
                                await ctx.channel.send(f"Stations: `{correct_list1}`")
                            else:
                                await ctx.channel.send(f"{user_response.author.mention} you can only reveal the image if you are an admin.")
                        else:
                            await user_response.add_reaction('❌')
                            log_command(user_response.author.id, 'game-station-order-incorrect')
                            roundResponse = True
                            incorrectAnswers += 1
                            addLoss(user_response.author.id, user_response.author.name, 'domino')
                            if user_response.author not in participants:
                                participants.append(user_response.author)
                
                    # checker for the funnies ( no ! needed)       
                    if await funnyCheck(user_response) == True:
                        # funny ones
                        if 'idk' in user_response.content.lower():
                            await ctx.channel.send(f"{user_response.author.mention} I don't know either.")
                        elif 'i dont know' in user_response.content.lower():
                            await ctx.channel.send(f"{user_response.author.mention} I don't know either.")
                        elif 'sorry' in user_response.content.lower():
                            await ctx.channel.send(f"{user_response.author.mention} Its ok.")
                        elif 'my bad' in user_response.content.lower():
                            await ctx.channel.send(f"{user_response.author.mention} Its ok.") 
                        elif 'oops' in user_response.content.lower():
                            await ctx.channel.send(f"{user_response.author.mention} Its ok.")
                        elif 'bruh' in user_response.content.lower():
                            await ctx.channel.send(f"{user_response.author.mention} 💀")
                        elif 'shit' in user_response.content.lower():
                            await ctx.channel.send(f"{user_response.author.mention} :(")
                        elif 'fuck' in user_response.content.lower():
                            await ctx.channel.send(f"{user_response.author.mention} :(")
                        elif 'what' in user_response.content.lower():
                            await ctx.channel.send(f"{user_response.author.mention} its a set of stations.")
                        elif 'wtf' in user_response.content.lower():
                            await ctx.channel.send(f"{user_response.author.mention} what?")
                        
            except asyncio.TimeoutError:
                await ctx.channel.send(f"Times up. The answer was ||{correct_list[0]}, {correct_list[1]}{f', {correct_list[2]}' if len(correct_list) >=3 else ''}{f', {correct_list[3]}' if len(correct_list) >=4 else ''}{f', {correct_list[4]}' if len(correct_list) >=5 else ''}||")
            finally:
                if not roundResponse:
                    ignoredRounds += 1
                await printlog(f'Ignored rounds: {ignoredRounds}')
                if ignoredRounds >= 4 and roundResponse == False:
                    await ctx.channel.send("No responses for 4 rounds. Game ended.")
                    embed = discord.Embed(title=f"Game Summary | {setLine}")
                    embed.add_field(name="Rounds played", value=f'{skippedGames} skipped, {rounds} total.', inline=True)
                    embed.add_field(name="Correct Guesses", value=correctAnswers, inline=True)
                    embed.add_field(name="Incorrect Guesses", value=incorrectAnswers, inline=True)
                    embed.add_field(name="Participants", value=', '.join([participant.mention for participant in participants]))
                    await ctx.channel.send(embed=embed)  
                    for user in participants:
                        await addGameAchievement(user.name,ctx.channel.id,user.mention)
                    return
                        
                # Reset game status after the game ends
                channel_game_status[channel] = False
                
        embed = discord.Embed(title=f"Game Summary | {setLine}")
        embed.add_field(name="Rounds played", value=f'{skippedGames} skipped, {rounds} total.', inline=True)
        embed.add_field(name="Correct Guesses", value=correctAnswers, inline=True)
        embed.add_field(name="Incorrect Guesses", value=incorrectAnswers, inline=True)
        embed.add_field(name="Participants", value=', '.join([participant.mention for participant in participants]))
        await ctx.channel.send(embed=embed)  
        for user in participants:
            await addGameAchievement(user.name,ctx.channel.id,user.mention)
            
    # Run the game in a separate task
    asyncio.create_task(run_game(line))



@games.command(name="station-hangman", description="A game where you guess the letters comprising a station name")
@app_commands.describe(rounds = "The number of rounds. Defaults to 1.")
@app_commands.describe(attempts = "The number of wrong guesses allowed. Defaults to 10.")

async def hangman(ctx, rounds: int = 1, attempts: int = 10):
    channel = ctx.channel
    log_command(ctx.user.id, 'game-station-hangman')
    await maintenance_game_func(ctx)
    async def run_game(line):
        # Check if a game is already running in this channel
        if channel in channel_game_status and channel_game_status[channel]:
            await ctx.response.send_message("A game is already running in this channel.", ephemeral=True )
            return
        if rounds > 10:
            await ctx.response.send_message("You can only play a maximum of 10 rounds!", ephemeral=True )
            return

        channel_game_status[channel] = True

        ignoredRounds = 0
        line = 'all' # change this when lines are added
        setLine = 'All Lines' if line == 'all' else f'{line.title()} line'
        
        # stuff for end of game stats
        incorrectAnswers = 0
        correctAnswers = 0
        skippedGames = 0
        participants = []

        for round in range(rounds):
            roundResponse = False
            
            # choose random line
            if line == 'all':
                line = None
                while line == None:
                    line = linelist[random.randint(0,len(linelist)-1)]            

            # choose random station
            station = ""
            while station == "":
                station = lines_dictionary_log_train_map_post_munnel[line][0][random.randint(0,len(lines_dictionary_log_train_map_post_munnel[line][0])-1)]

            guessed_list = ""
            guessed = ""
            for letter in station.replace(" ", ""):
                guessed = guessed + "- "

            failed = f""

            incorrectGuesses = 0

            embed = discord.Embed(
                title=f"Guess the station! It has {len(station)} letters",
                description=f"**Guess either letters or station names.\nNote you only have {attempts} incorrect guesses until you lose**\nAnswer using this format:\n<@{bot.user.id}> `Letter` or <@{bot.user.id}> `Station name or part of station name`\n\n*Use <@{bot.user.id}> skip to skip to the next round.*",
                colour=metro_colour)
            embed.set_author(name=f"Round {round+1}/{rounds}")
            if round == 0:
                await ctx.response.send_message(embed=embed)
            else:
                await ctx.channel.send(embed=embed)

            # Define a check function to validate user input
            async def check(m): 
                return m.channel == channel and m.author != bot.user and m.content.startswith(f'<@{bot.user.id}>')

            # the actual input part
            try:
                correct = False
                while not correct:
                    # Wait for user's response in the same channel
                    user_response = await bot.wait_for('message', check=check, timeout=30.0)

                    if await check(user_response) == True:  # fixed cause check broke    
                        # Check if the user's response matches the correct station
                        if user_response.content[len(f'<@{bot.user.id}>'):].lower().replace(" ", "") in station.lower().replace(" ", ""):
                            if not user_response.content[len(f'<@{bot.user.id}>'):].lower().replace(" ", "") in guessed_list:
                                guessed_list = guessed_list + user_response.content.replace(f'<@{bot.user.id}>', '').strip().lower().replace(" ", "")
                                await printlog(guessed_list)
                                guessed = ""
                                for letter in station.replace(" ", ""):
                                    if letter.lower() in guessed_list:
                                        guessed = guessed + letter + " "
                                    else:
                                        guessed = guessed + "- "
                                await user_response.add_reaction('✅')
                                addLb(user_response.author.id, user_response.author.name, 'hangman')
                                log_command(user_response.author.id, 'game-station-hangman-correct')
                                correctAnswers += 1
                                ignoredRounds = 0
                                roundResponse = True
                                if guessed.replace(" ", "") == station.replace(" ", ""):
                                    correct = True
                                    await ctx.channel.send("You won!")
                                await ctx.channel.send(f'# Letters: `{guessed}`\n\n**Incorrect guesses: {failed}**\n\nIncorrect guesses left: {attempts - incorrectGuesses}')
                            else:
                                await ctx.channel.send(f'Already guessed {user_response.author.mention}! Try again.')
                                log_command(user_response.author.id, 'game-station-hangman-neutral')
                                roundResponse = True
                                if user_response.author not in participants:
                                    participants.append(user_response.author)
                                await ctx.channel.send(f'# Letters: `{guessed}`\n\n**Incorrect guesses: {failed}**\n\nIncorrect guesses left: {attempts - incorrectGuesses}')
                        elif user_response.content.lower() == f'<@{bot.user.id}> skip':
                            if user_response.author.id == ctx.user.id or user_response.author.id in admin_users :
                                await ctx.channel.send(f"Round {round+1} skipped. The answer was ||{station}||")
                                log_command(user_response.author.id, 'game-station-hangman-skip')
                                skippedGames += 1
                                roundResponse = True
                                break
                            else:
                                await ctx.channel.send(f"{user_response.author.mention} you can only skip the round if you were the one who started it.")
                        elif user_response.content.lower() == f'<@{bot.user.id}> stop':
                            if user_response.author.id == ctx.user.id or user_response.author.id in admin_users :
                                await ctx.channel.send(f"Game ended.")
                                log_command(user_response.author.id, 'game-station-hangman-stop')
                                embed = discord.Embed(title=f"Game Summary | {setLine}")
                                embed.add_field(name="Rounds played", value=f'{skippedGames} skipped, {rounds} total.', inline=True)
                                embed.add_field(name="Correct Guesses", value=correctAnswers, inline=True)
                                embed.add_field(name="Incorrect Guesses", value=incorrectAnswers, inline=True)
                                embed.add_field(name="Participants", value=', '.join([participant.mention for participant in participants]))
                                await ctx.channel.send(embed=embed)  
                                for user in participants:
                                    await addGameAchievement(user.name,ctx.channel.id,user.mention, game='hangman')
                                channel_game_status[channel] = False
                                return
                            else:
                                await ctx.channel.send(f"{user_response.author.mention} you can only stop the game if you were the one who started it.")
                        # view the image info (admin only) 
                        elif user_response.content.lower() == f'<@{bot.user.id}> reveal' or user_response.content.lower() == f'<@{bot.user.id}> release':
                            if user_response.author.id in admin_users :
                                await ctx.channel.send(f"Station: `{station}`")
                            else:
                                await ctx.channel.send(f"{user_response.author.mention} you can only reveal the image if you are an admin.")
                        else:
                            if not user_response.content[1:].lower().replace(" ", "") in failed:
                                await user_response.add_reaction('❌')
                                log_command(user_response.author.id, 'game-station-hangman-incorrect')
                                roundResponse = True
                                incorrectAnswers += 1
                                incorrectGuesses += 1
                                addLoss(user_response.author.id, user_response.author.name, 'hangman')
                                if len(user_response.content[1:].lower().replace(" ", "")) == 1:
                                    if failed == "":
                                        failed = user_response.content[1:].lower().replace(" ", "")
                                    else:
                                        failed = failed + f', {user_response.content[1:].lower().replace(" ", "")}'
                                if user_response.author not in participants:
                                    participants.append(user_response.author)
                                await ctx.channel.send(f'# Letters: `{guessed}`\n\n**Incorrect guesses: {failed}**\n\nIncorrect guesses left: {attempts - incorrectGuesses}')
                                if incorrectGuesses >= attempts:
                                    await ctx.channel.send('You lost!')
                                    await ctx.channel.send(f"The answer was ||{station}||")
                                    break
                            else:
                                await ctx.channel.send(f'Already guessed {user_response.author.mention}! Try again.')
                                log_command(user_response.author.id, 'game-station-hangman-neutral')
                                roundResponse = True
                                if user_response.author not in participants:
                                    participants.append(user_response.author)
                                await ctx.channel.send(f'# Letters: `{guessed}`\n\n**Incorrect guesses: {failed}**\n\nIncorrect guesses left: {attempts - incorrectGuesses}')
                        
            except asyncio.TimeoutError:
                await ctx.channel.send(f"Times up. The answer was ||{station}||")
            finally:
                if not roundResponse:
                    ignoredRounds += 1
                await printlog(f'Ignored rounds: {ignoredRounds}')
                if ignoredRounds >= 4 and roundResponse == False:
                    await ctx.channel.send("No responses for 4 rounds. Game ended.")
                    embed = discord.Embed(title=f"Game Summary | {setLine}")
                    embed.add_field(name="Rounds played", value=f'{skippedGames} skipped, {rounds} total.', inline=True)
                    embed.add_field(name="Correct Guesses", value=correctAnswers, inline=True)
                    embed.add_field(name="Incorrect Guesses", value=incorrectAnswers, inline=True)
                    embed.add_field(name="Participants", value=', '.join([participant.mention for participant in participants]))
                    await ctx.channel.send(embed=embed)  
                    for user in participants:
                        await addGameAchievement(user.name,ctx.channel.id,user.mention, game='hangman')
                    return
                        
                # Reset game status after the game ends
                channel_game_status[channel] = False
                
        embed = discord.Embed(title=f"Game Summary | {setLine}")
        embed.add_field(name="Rounds played", value=f'{skippedGames} skipped, {rounds} total.', inline=True)
        embed.add_field(name="Correct Guesses", value=correctAnswers, inline=True)
        embed.add_field(name="Incorrect Guesses", value=incorrectAnswers, inline=True)
        embed.add_field(name="Participants", value=', '.join([participant.mention for participant in participants]))
        await ctx.channel.send(embed=embed)  
        for user in participants:
            await addGameAchievement(user.name,ctx.channel.id,user.mention, game='hangman')
            
    # Run the game in a separate task
    asyncio.create_task(run_game(line))

async def station_autocompletion(
    interaction: discord.Interaction,
    current: str
) -> typing.List[app_commands.Choice[str]]:
    fruits = stations_list.copy()
    return [
        app_commands.Choice(name=fruit, value=fruit)
        for fruit in fruits if current.lower() in fruit.lower()
    ][:25]
    
async def line_autocompletion(
    interaction: discord.Interaction,
    current: str
) -> typing.List[app_commands.Choice[str]]:
    fruits = lines_list.copy()
    return [
        app_commands.Choice(name=fruit, value=fruit)
        for fruit in fruits if current.lower() in fruit.lower()
    ][:25]
    
async def type_autocompletion(
    interaction: discord.Interaction,
    current: str
) -> typing.List[app_commands.Choice[str]]:
    fruits = types_list.copy()
    return [
        app_commands.Choice(name=fruit, value=fruit)
        for fruit in fruits if current.lower() in fruit.lower()
    ][:25]
    
#log train logger
@trainlogs.command(name="train", description="Log a train you have been on")
@app_commands.describe(number = "Carrige Number", date = "Date in DD/MM/YYYY or YYYY-MM-DD format", line = 'Train Line', start='Starting Station', end = 'Ending Station', type='Type of train (will be autofilled if a train number is entered)', notes='Any notes you want to add to the log', hidemessage='Hide the message from other users, note this will not make the log private.')
@app_commands.autocomplete(start=station_autocompletion)
@app_commands.autocomplete(end=station_autocompletion)
@app_commands.autocomplete(line=line_autocompletion)
@app_commands.autocomplete(type=type_autocompletion)

# Train logger
async def logtrain(ctx, line:str, number:str, start:str, end:str, date:str='today', type:str='auto', notes:str=None, hidemessage:bool=False):
    await maintenance_func(ctx)
    channel = ctx.channel
    await ctx.response.defer(ephemeral=hidemessage)
    log_command(ctx.user.id, 'log-train')
    await printlog(date)
    async def log(notes, ctx,line, number, start, end, date, type):
        await printlog("logging the thing")

        savedate = date.split('/')
        if date.lower() == 'today':
            current_time = time.localtime()
            savedate = time.strftime("%Y-%m-%d", current_time)
        else:
            try:
                savedate = time.strptime(date, "%d/%m/%Y")
                savedate = time.strftime("%Y-%m-%d", savedate)
            except ValueError:
                try:
                    savedate = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
                except ValueError:
                    await ctx.edit_original_response(content=f'Invalid date: `{date}`\nMake sure to use a possible date.')
                    return
            except TypeError:
                await ctx.edit_original_response(content=f'Invalid date: `{date}`\nUse the form `dd/mm/yyyy`')
                return
        
        if line == "Summer Start Metro Tunnel Service":
            log_year = int(savedate.split('-')[0])
            log_month = int(savedate.split('-')[1])
            if log_year > 2026 or log_year == 2026 and log_month >= 2:
                await ctx.edit_original_response(content='''Invalid line: The `Summer Start Metro Tunnel Service` refers to the service between Westall and West Footscray that ran between the 30th of November 2025 and the 31st of January 2026. The date you have selected, `''' + savedate + '''`, is outside that range and the line no longer in operation. Please try again and choose an operational line, the Sunbury, Pakenham and Cranbourne Lines all run via the Metro Tunnel.''')
                return

        if 'overland' in line.lower():
            await ctx.edit_original_response(content='''If you're trying to log a trip on the Overland, please use </log adelaide-train:1289843416628330506>. For a comprehensive guide of which of these log commands to use in which situation, open </help:1261177133372280957> and in the "commands" option choose "Which /log command should I use?"''')
            return
            
        # Initialize variables
        set = 'Unknown'
        type_final = 'Unknown'

        # Handle type first
        if type != 'auto':
            type_final = type
            if type == "Tait":
                set = '381M-208T-230D-317M'
            else:
                
                # check if its a known train type and find the set, but if its not known just use the number
                checkTT = trainType(number.upper())
                if checkTT == type:
                    set = setNumber(number.upper())
                    if set == None:
                        set = type
                else:
                    set = number.upper()
        else:
            # if the user puts a vlocity with he letters VL
            if number.upper().startswith('VL') or number.upper().startswith('VS') and len(number) == 6:
                print('vlocity with vl/vs')
                number = number.strip('VL').replace(' ', '') if number.upper().startswith('VL') else number.strip('VS').replace(' ', '')
            
            # checking if train number is valid
            if number != 'Unknown':
                set = setNumber(number.upper())
            if set == None:
                await ctx.edit_original_response(content=f'Invalid train number: `{number.upper()}`')
                return
            type_final = trainType(number.upper())
            
        # Strip emojis and newlines from note
        if notes:
            notes = re.sub(r'[^\x00-\x7F]+', '', notes)
            notes = notes.replace('\n', ' ')
            #add quotes so the csv dosn't break when u use a comma
            notes = f'"{notes}"'

        # Station Code Converter
        if len(start) == 3:
            printlog("converting start from station code")
            start = station_codes[start.upper()]
        if len(end) == 3:
            printlog("converting end from station code")
            end = station_codes[end.upper()]
                
            
        # Add train to the list
        print(f'adding {set} {type_final} {savedate} {line} {start.title()} {end.title()} {notes}')
        id = addTrain(ctx.user.id, ctx.user.name, set, type_final, savedate, line, start.title(), end.title(), notes)
        
        if line in vLineLines:
            embed = discord.Embed(title="Train Logged",colour=vline_map_colour)
        elif line == 'Unknown':
                embed = discord.Embed(title="Train Logged")
        else:
            try:
                embed = discord.Embed(title="Train Logged",colour=lines_dictionary_log_train_map_post_munnel[line][1])
            except:
                embed = discord.Embed(title="Train Logged")
        
        embed.add_field(name="Set", value=f'{set} ({type_final})')
        embed.add_field(name="Line", value=line)
        embed.add_field(name="Date", value=savedate)
        if getStationDistance(load_station_data("utils/trainlogger/stationDistances.csv"), start, end) != 'N/A':
            embed.add_field(name="Trip", value=f'{start.title()} to {end.title()}, {round(getStationDistance(load_station_data("utils/trainlogger/stationDistances.csv"), start, end), 1)}km')
        else:
            embed.add_field(name="Trip", value=f'{start.title()} to {end.title()}')
        if notes:
            embed.add_field(name="Notes", value=notes.strip('"'))


        # thing to find image:
        await printlog(f"Finding image for {number}")
        
        try:
            credits = None
            if not '-' in set:
                imagec = getImage(set, thumbnail=True)
                image = imagec[0]
                credits = imagec[1]

            else:
                credits = None
                hyphen_index = set.find("-")
                
                if hyphen_index != -1:
                    first_car = set[:hyphen_index]
                    await printlog(f'First car: {first_car}')
                    
                    imagec = getImage(first_car, thumbnail=True)
                    image, credits = imagec
                    
                    if image is None:
                        last_hyphen = set.rfind("-")
                        if last_hyphen != -1:
                            last_car = set[last_hyphen + 1 :]
                            await printlog(f'Last car: {last_car}')
                            
                            imagec = getImage(last_car, thumbnail=True)
                            image, credits = imagec
                            
                            if image is None:
                                await printlog(f'the loco number is: {set}')

            if image != None:
                embed.set_thumbnail(url=image)
            
        except Exception as e:
            await printlog(f"Error getting image: {e}")
            
        # extra details thing
        extraText = '\u200b'

        # tell you if you have ridden the train before
        _, count = checkTrainRidden(set, f"utils/trainlogger/userdata/{ctx.user.id}.csv")
        rides_before = max(len(count) - 1, 0)
        if rides_before > 0:
            extraText += f"You have ridden this train {rides_before} times before!"
        else:
            extraText += "This is your first time riding this train!"

        extraText += f'\nPhoto by {credits} on [victorianrailphotos.com](https://victorianrailphotos.com)' if credits is not None else ''
        embed.add_field(name="\u200b", value=extraText)

        footer = f"Log ID #{id}"
        embed.set_footer(text=footer)
        
        await ctx.edit_original_response(embed=embed)
        await addAchievement(ctx.user.name, ctx.channel.id, ctx.user.mention)

        
                        
    # Run in a separate task
    asyncio.create_task(log(notes,ctx,line, number, start, end, date, type))

    
#thing to delete the stuff
@trainlogs.command(name='delete', description='Delete a logged trip. Defaults to the last logged trip.')
@app_commands.describe(id = "The ID of the log that you want to delete.", mode='What mode of log to delete?')
@app_commands.choices(mode=[
    app_commands.Choice(name="Victorian Train", value="train"),
    app_commands.Choice(name="Melbourne Tram", value="tram"), 
    app_commands.Choice(name="NSW Train", value="sydney-trains"),
    app_commands.Choice(name="Sydney Light Rail", value="sydney-trams"),
    app_commands.Choice(name="Adelaide Train", value="adelaide-trains"),
    app_commands.Choice(name="Adelaide Tram", value="adelaide-trams"),
    app_commands.Choice(name="Perth Train", value="perth-trains"),
    app_commands.Choice(name="Canberra Light Rail", value="canberra-trams"),
    app_commands.Choice(name="Bus", value="bus"),
    app_commands.Choice(name="Flight", value="flights"),
])
async def deleteLog(ctx, mode:str, id:str='LAST'):
    await maintenance_func(ctx)
    class DeleteConfirmation(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=30)
            
        @discord.ui.button(label="Confirm", style=discord.ButtonStyle.danger)
        async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
            if interaction.user != ctx.user:
                await interaction.response.send_message("This isn't your log!", ephemeral=True)
                return
            
            # Delete the log
            idformatted1 = deleteRow(ctx.user.id, ctx.user.name, idformatted, mode)
            
            # Update message
            if idformatted == 'LAST':
                await interaction.response.edit_message(content=f'Most recent log (`#{idformatted1}`) deleted. The data was:\n`{dataToDelete}`', view=None)
            else:
                await interaction.response.edit_message(content=f'Log `#{idformatted}` deleted. The data was:\n`{dataToDelete}`', view=None)
                
            for child in self.children:
                child.disabled = True
                
        @discord.ui.button(label="Cancel", style=discord.ButtonStyle.gray)
        async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
            if interaction.user != ctx.user:
                await interaction.response.send_message("This isn't your log!", ephemeral=True)
                return
            
            await interaction.response.edit_message(content="Deletion cancelled.", view=None)
            for child in self.children:
                child.disabled = True

    async def deleteLogFunction():
        log_command(ctx.user.id, 'log-delete')
        
        nonlocal idformatted, dataToDelete  # Make these accessible in button callbacks
        
        if id[0] == '#':
            idformatted = id[1:].upper()
        else:
            idformatted = id.upper()

        if idformatted != 'LAST':
            if not is_hex(idformatted):
                await ctx.response.send_message(f'Invalid log ID entered: `{idformatted}`. You can find the ID of a log to delete by using </log view:1289843416628330506>.', ephemeral=True)
                return
                
        dataToDelete = universalReadRow(ctx.user.id, ctx.user.name, idformatted, mode)
        if dataToDelete in ['no data at all', 'no data for user']:
            await ctx.response.send_message(f'You have no logs you can delete!', ephemeral=True)
            return
        elif dataToDelete == 'invalid id did not show up':
            await ctx.response.send_message(f'Invalid log ID entered: `{idformatted}`. You can find the ID of a log to delete by using </log view:1289843416628330506>.', ephemeral=True)
            return
        
        else:
            # Create confirmation message with buttons
            view = DeleteConfirmation()
            if idformatted == 'LAST':
                await ctx.response.send_message(f'Are you sure you want to delete your most recent log?\nData to be deleted:\n`{dataToDelete}`', view=view, ephemeral=True)
            else:
                await ctx.response.send_message(f'Are you sure you want to delete log `#{idformatted}`?\nData to be deleted:\n`{dataToDelete}`', view=view, ephemeral=True)
            
    # Initialize variables for button callbacks
    idformatted = None  
    dataToDelete = None
    
    asyncio.create_task(deleteLogFunction())
    
# log editor
@trainlogs.command(name='edit',description='Edit a logged trip')
@app_commands.choices(mode=[
    app_commands.Choice(name="Victorian Train", value="train"),
    # coming soon:
    # app_commands.Choice(name="Melbourne Tram", value="tram"),
    # app_commands.Choice(name="NSW Train", value="sydney-trains"),
    # app_commands.Choice(name="Sydney Light Rail", value="sydney-trams"),
    # app_commands.Choice(name="Adelaide Train", value="adelaide-trains"),
    # app_commands.Choice(name="Adelaide Tram", value="adelaide-traMS"),
    # app_commands.Choice(name="Perth Train", value="perth-trains"),
    # app_commands.Choice(name="Bus", value="bus"),
])
@app_commands.autocomplete(start=station_autocompletion)
@app_commands.autocomplete(end=station_autocompletion)
@app_commands.autocomplete(line=line_autocompletion)
@app_commands.autocomplete(type=type_autocompletion)
async def editrow(ctx, id:str, mode:str='train', line:str='nochange', number:str='nochange', start:str='nochange', end:str='nochange', date:str='nochange', type:str='auto', notes:str='nochange'):
    await ctx.response.defer()
    await maintenance_func(ctx)
    log_command(ctx.user.id, 'edit-row')
    
    username = ctx.user.name
    userid = ctx.user.id
    logid = id
    if logid[0] == '#':
        idformatted = logid[1:].upper()
    else:
        idformatted = logid.upper()
    
    # Find old data for the edited row
    dataToDelete = universalReadRow(userid, username, idformatted, mode)
    
    if notes != 'nochange':
            # Remove emojis using regex
            notes = re.sub(r'[^\x00-\x7F]+', '', notes)
            # Remove newlines
            notes = notes.replace('\n', ' ')
            #add quotes so the csv dosn't break when u use a comma
            notes = f'"{notes}"'
            
    # convert date from DD/MM/YYYY to YYYY-MM-DD
    if date != 'nochange':
        if date.lower() == 'today':
            current_time = time.localtime()
            savedate = time.strftime("%Y-%m-%d", current_time)
        else:
            try:
                savedate = time.strptime(date, "%d/%m/%Y")
                savedate = time.strftime("%Y-%m-%d", savedate)
            except ValueError:
                try:
                    savedate = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
                except ValueError:
                    await ctx.edit_original_response(content=f'Invalid date: `{date}`\nMake sure to use a possible date.')
                    return
            except TypeError:
                await ctx.edit_original_response(content=f'Invalid date: `{date}`\nUse the form `dd/mm/yyyy`')
                return
    else:
        savedate = 'nochange'
    
    result = editRow(userid, username, idformatted, mode,line,number,start,end,savedate,type,notes)
    
    if result == 'invalid id did not show up':
        await ctx.edit_original_response(content=f'Invalid log ID entered: `{idformatted}`')
        return
    
    
    await ctx.edit_original_response(content=f'**Successfully edited log `#{idformatted}`**\nOld data:\n`{dataToDelete}`\nNew data:\n`{result}`')

    
  # tram logger goes here
async def station_autocompletion(
    interaction: discord.Interaction,
    current: str
) -> typing.List[app_commands.Choice[str]]:
    fruits = tram_stops.copy()
    return [
        app_commands.Choice(name=fruit, value=fruit)
        for fruit in fruits if current.lower() in fruit.lower()
    ][:25]
@trainlogs.command(name="tram", description="Log a Melbourne tram you have been on")
@app_commands.describe(number = "Tram Number", date = "Date in DD/MM/YYYY format", route = 'Tram Line', start='Starting Stop', end = 'Ending Stop', hidemessage='Hide the message from other users, note this will not make the log private.')
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

async def logtram(ctx, route:str, number: str, start:str, end:str, date:str='today', notes:str=None, hidemessage:bool=False):
    await ctx.response.defer(ephemeral=hidemessage)
    await maintenance_func(ctx)
    channel = ctx.channel
    await printlog(date)
    async def log(notes):
        log_command(ctx.user.id, 'log-tram')
        await printlog("logging the thing")

        savedate = date.split('/')
        if date.lower() == 'today':
            current_time = time.localtime()
            savedate = time.strftime("%Y-%m-%d", current_time)
        else:
            try:
                savedate = time.strptime(date, "%d/%m/%Y")
                savedate = time.strftime("%Y-%m-%d", savedate)
            except ValueError:
                try:
                    savedate = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
                except ValueError:
                    await ctx.edit_original_response(content=f'Invalid date: `{date}`\nMake sure to use a possible date.')
                    return
            except TypeError:
                await ctx.edit_original_response(f'Invalid date: {date}\nUse the form `dd/mm/yyyy`')
                return

        # checking if train number is valid
        if set == None:
            await ctx.edit_original_response(f'Invalid tram number: {number.upper()}')
            return
        type = tramType(number.upper())
        if type == None or type == 'Tram type not found for UNKNOWN':
            type = 'N/A'
            
        if notes != None:
            # Remove emojis using regex
            notes = re.sub(r'[^\x00-\x7F]+', '', notes)
            # Remove newlines
            notes = notes.replace('\n', ' ')
            #add quotes so the csv dosn't break when u use a comma
            notes = f'"{notes}"'

        # Add train to the list
        id = addTram(ctx.user.id, ctx.user.name, number, type, savedate, route, start.title(), end.title(), notes)

        embed = discord.Embed(title="Tram Logged",colour=tram_colour)
        
        embed.add_field(name="Number", value=f'{number} ({type})')
        embed.add_field(name="Line", value=route)
        embed.add_field(name="Date", value=savedate)
        embed.add_field(name="Trip", value=f'{start.title()} to {end.title()}')
        if notes != None:
            embed.add_field(name="Notes", value=notes.strip('"'))

        # thing to find image:
        await printlog(f"Finding image for {number}")
        imageURL, credits = getTramImage(number.upper())
        if imageURL != None:
            embed.set_thumbnail(url=imageURL)
        credits = f' | Photo by {credits}' if credits != None else ''
        embed.set_footer(text=f"Log ID #{id}{credits}")
        await ctx.edit_original_response(embed=embed)
        
                
    # Run in a separate task
    asyncio.create_task(log(notes))
    
    
    
# sydney train logger
async def NSWstation_autocompletion(
    interaction: discord.Interaction,
    current: str
) -> typing.List[app_commands.Choice[str]]:
    fruits = NSWstations_list.copy()
    return [
        app_commands.Choice(name=fruit, value=fruit)
        for fruit in fruits if current.lower() in fruit.lower()
    ][:25]
    
@trainlogs.command(name="sydney-train", description="Log a Sydney/NSW train you have been on")
@app_commands.describe(number = "Carrige or Set Number", type = 'Type of train', date = "Date in DD/MM/YYYY format", line = 'Train Line', start='Starting Station', end = 'Ending Station', hidemessage='Hide the message from other users, note this will not make the log private.')
@app_commands.autocomplete(start=NSWstation_autocompletion)
@app_commands.autocomplete(end=NSWstation_autocompletion)

@app_commands.choices(line=[
        app_commands.Choice(name="T1 North Shore & Western Line", value="T1"),
        app_commands.Choice(name="T2 Leppington & Inner West Line", value="T2"),
        app_commands.Choice(name="T3 Liverpool & Inner West Line", value="T3"),
        app_commands.Choice(name="T4 Eastern Suburbs & Illawarra Line", value="T4"),
        app_commands.Choice(name="T5 Cumberland Line", value="T5"),
        app_commands.Choice(name="T6 Lidcombe & Bankstown Line", value="T6"),
        app_commands.Choice(name="T7 Olympic Park Line", value="T7"),
        app_commands.Choice(name="T8 Airport & South Line", value="T8"),
        app_commands.Choice(name="T9 Northern Line", value="T9"),
        
        app_commands.Choice(name="M1 North West & Bankstown Line", value="M1"),

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
async def logNSWTrain(ctx,  line:str, number: str, start:str, end:str, type:str='auto', date:str='today', hidemessage:bool=False):
    channel = ctx.channel
    await ctx.response.defer(ephemeral=hidemessage)
    await maintenance_func(ctx)
    async def log(type):
        log_command(ctx.user.id, 'log-nsw-train')
        await printlog("logging the nsw sydney train")

        savedate = date.split('/')
        if date.lower() == 'today':
            current_time = time.localtime()
            savedate = time.strftime("%Y-%m-%d", current_time)
        else:
            try:
                savedate = time.strptime(date, "%d/%m/%Y")
                savedate = time.strftime("%Y-%m-%d", savedate)
            except ValueError:
                try:
                    savedate = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
                except ValueError:
                    await ctx.edit_original_response(content=f'Invalid date: `{date}`\nMake sure to use a possible date.')
                    return
            except TypeError:
                await ctx.response.send_message(f'Invalid date: {date}\nUse the form `dd/mm/yyyy`', ephemeral=True)
                return

        # idk how to get nsw train set numbers i cant find a list of all sets pls help
        # nvm now we have this info provided!
        set = getSydneySetNumber(number)
        if set == None:
            set = number.upper()
            
        if type == 'auto':
            type = sydneyTrainType(set)
        if set == None:
            await ctx.response.send_message(f'Invalid train number: {number.upper()}',ephemeral=True)
            return

        # Add train to the list
        id = addSydneyTrain(ctx.user.id, ctx.user.name, set, type, savedate, line, start.title(), end.title())

        embed = discord.Embed(title="Train Logged",colour=sydney_train_colour)
        
        embed.add_field(name="Number", value=f'{set} ({type})')
        embed.add_field(name="Line", value=line)
        embed.add_field(name="Date", value=savedate)
        embed.add_field(name="Trip", value=f'{start.title()} to {end.title()}')
        embed.set_footer(text=f"Log ID #{id}")

        await ctx.followup.send(embed=embed)
        
                
    # Run in a separate task
    asyncio.create_task(log(type))

# sydney train logger
async def NSWstation_autocompletion(
    interaction: discord.Interaction,
    current: str
) -> typing.List[app_commands.Choice[str]]:
    fruits = NSWstations_list.copy()
    return [
        app_commands.Choice(name=fruit, value=fruit)
        for fruit in fruits if current.lower() in fruit.lower()
    ][:25]

# Adelaide LOGGER AND overland logger
async def Adelaidestation_autocompletion(
    interaction: discord.Interaction,
    current: str
) -> typing.List[app_commands.Choice[str]]:
    fruits = Adelaidestations_list.copy()
    return [
        app_commands.Choice(name=fruit, value=fruit)
        for fruit in fruits if current.lower() in fruit.lower()
    ][:25]
    
async def Adelaideline_autocompletion(
    interaction: discord.Interaction,
    current: str
) -> typing.List[app_commands.Choice[str]]:
    fruits = Adelaidelines_list.copy()
    return [
        app_commands.Choice(name=fruit, value=fruit)
        for fruit in fruits if current.lower() in fruit.lower()
    ][:25]
    
@trainlogs.command(name="adelaide-train", description="Log an Adelaide Metro or Journey Beyond train you have been on")
@app_commands.describe(number = "Carrige Number", date = "Date in DD/MM/YYYY format", line = 'Train Line', start='Starting Station', end = 'Ending Station', hidemessage='Hide the message from other users, note this will not make the log private.')
@app_commands.autocomplete(start=Adelaidestation_autocompletion)
@app_commands.autocomplete(end=Adelaidestation_autocompletion)
@app_commands.autocomplete(line=Adelaideline_autocompletion)

# Adelaide train logger journey beyond too
async def logSATrain(ctx, line:str, number: str, start:str, end:str, date:str='today', hidemessage:bool=False):
    channel = ctx.channel
    log_command(ctx.user.id, 'log-adelaide-train')
    await printlog(date)
    await maintenance_func(ctx)
    async def log():
        await printlog("logging the adelaide train")

        savedate = date.split('/')
        if date.lower() == 'today':
            current_time = time.localtime()
            savedate = time.strftime("%Y-%m-%d", current_time)
        else:
            try:
                savedate = time.strptime(date, "%d/%m/%Y")
                savedate = time.strftime("%Y-%m-%d", savedate)
            except ValueError:
                try:
                    savedate = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
                except ValueError:
                    await ctx.edit_original_response(content=f'Invalid date: `{date}`\nMake sure to use a possible date.')
                    return
            except TypeError:
                await ctx.response.send_message(f'Invalid date: {date}\nUse the form `dd/mm/yyyy`', ephemeral=True)
                return

        # idk how to get nsw train set numbers i cant find a list of all sets pls help
        set = number
        if set == None:
            await ctx.response.send_message(f'Invalid train number: {number.upper()}',ephemeral=True)
            return
        
        if number.startswith('NR'):
            type = 'NR Class'
        elif number.startswith('4'):
            type = '4000 Class'
        elif number.startswith('3'):
            if number.startswith('31'):
                type = '3100 Class'
            else:
                type = '3000 Class'
        else:
            type = 'Unknown'
        
        # Add train to the list
        id = addAdelaideTrain(ctx.user.id, ctx.user.name, set, type, savedate, line, start.title(), end.title())

        embed = discord.Embed(title="Train Logged",colour=adelaide_metro_colour)
        
        embed.add_field(name="Number", value=f'{set} ({type})')
        embed.add_field(name="Line", value=line)
        embed.add_field(name="Date", value=savedate)
        embed.add_field(name="Trip", value=f'{start.title()} to {end.title()}')
        embed.set_footer(text=f"Log ID #{id}")

        await ctx.response.send_message(embed=embed)
        await addAchievement(ctx.user.name, ctx.channel.id, ctx.user.mention)

                
    # Run in a separate task
    asyncio.create_task(log())


# Adelaide tram logger
async def Adelaidestop_autocompletion(
    interaction: discord.Interaction,
    current: str
) -> typing.List[app_commands.Choice[str]]:
    fruits = Adelaidestops_list.copy()
    return [
        app_commands.Choice(name=fruit, value=fruit)
        for fruit in fruits if current.lower() in fruit.lower()
    ][:25]

@trainlogs.command(name="adelaide-tram", description="Log a Adelaide Tram you have been on")
@app_commands.describe(number = "Carrige Number", type = 'Type of tram', date = "Date in DD/MM/YYYY format", line = 'Tram Line', start='Starting Stop', end = 'Ending Stop', hidemessage='Hide the message from other users, note this will not make the log private.')
@app_commands.autocomplete(start=Adelaidestop_autocompletion)
@app_commands.autocomplete(end=Adelaidestop_autocompletion)

@app_commands.choices(line=[
        app_commands.Choice(name="Glenelg to Royal Adelaide Hospital Line", value="GLNELG"),
        app_commands.Choice(name="Botanic Gardens to Entertainment Centre Line", value="BTANIC"),
        app_commands.Choice(name="Glenelg to Festival Plaza Line", value="FESTVL"),
        app_commands.Choice(name="Adelaide Loop Line", value="ADLOOP"),
])
@app_commands.choices(type=[
        app_commands.Choice(name="100 Series", value="100 Series"),
        app_commands.Choice(name="200 Series", value="200 Series"),
])
# SYdney tram logger nsw tram
async def logSATram(ctx, line:str, number: str, type:str, start:str, end:str, date:str='today', hidemessage:bool=False):
    channel = ctx.channel
    await printlog(date)
    await maintenance_func(ctx)
    async def log():
        log_command(ctx.user.id, 'log-adelaide-tram')
        await printlog("logging the adelaide tram")

        savedate = date.split('/')
        if date.lower() == 'today':
            current_time = time.localtime()
            savedate = time.strftime("%Y-%m-%d", current_time)
        else:
            try:
                savedate = time.strptime(date, "%d/%m/%Y")
                savedate = time.strftime("%Y-%m-%d", savedate)
            except ValueError:
                try:
                    savedate = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
                except ValueError:
                    await ctx.edit_original_response(content=f'Invalid date: `{date}`\nMake sure to use a possible date.')
                    return
            except TypeError:
                await ctx.response.send_message(f'Invalid date: {date}\nUse the form `dd/mm/yyyy`', ephemeral=True)
                return

        # idk how to get nsw train set numbers i cant find a list of all sets pls help
        set = number
        if set == None:
            await ctx.response.send_message(f'Invalid tram number: {number.upper()}',ephemeral=True)
            return

        # Add train to the list
        id = addAdelaideTram(ctx.user.id, ctx.user.name, set, type, savedate, line, start.title(), end.title())

        embed = discord.Embed(title="Tram Logged",colour=adelaide_tram_colour)
        
        embed.add_field(name="Number", value=f'{set} ({type})')
        embed.add_field(name="Line", value=line)
        embed.add_field(name="Date", value=savedate)
        embed.add_field(name="Trip", value=f'{start.title()} to {end.title()}')
        embed.set_footer(text=f"Log ID #{id}")

        await ctx.response.send_message(embed=embed, ephemeral=hidemessage)
        
                
    # Run in a separate task
    asyncio.create_task(log())

# Perth logger
async def Perthstation_autocompletion(
    interaction: discord.Interaction,
    current: str
) -> typing.List[app_commands.Choice[str]]:
    fruits = Perthstations_list.copy()
    return [
        app_commands.Choice(name=fruit, value=fruit)
        for fruit in fruits if current.lower() in fruit.lower()
    ][:25]
    
async def Perthline_autocompletion(
    interaction: discord.Interaction,
    current: str
) -> typing.List[app_commands.Choice[str]]:
    fruits = Perthlines_list.copy()
    return [
        app_commands.Choice(name=fruit, value=fruit)
        for fruit in fruits if current.lower() in fruit.lower()
    ][:25]
    
@trainlogs.command(name="perth-train", description="Log a Perth train you have been on")
@app_commands.describe(number = "Carrige Number", date = "Date in DD/MM/YYYY format", line = 'Train Line', start='Starting Station', end = 'Ending Station', hidemessage='Hide the message from other users, note this will not make the log private.')
@app_commands.autocomplete(start=Perthstation_autocompletion)
@app_commands.autocomplete(end=Perthstation_autocompletion)
@app_commands.autocomplete(line=Perthline_autocompletion)

# Perth logger
async def logPerthTrain(ctx, number: str, line:str, start:str, end:str, date:str='today', hidemessage:bool=False):
    channel = ctx.channel
    log_command(ctx.user.id, 'log-perth-train')
    await printlog(date)
    await maintenance_func(ctx)
    async def log():
        await printlog("logging the perth train")

        savedate = date.split('/')
        if date.lower() == 'today':
            current_time = time.localtime()
            savedate = time.strftime("%Y-%m-%d", current_time)
        else:
            try:
                savedate = time.strptime(date, "%d/%m/%Y")
                savedate = time.strftime("%Y-%m-%d", savedate)
            except ValueError:
                try:
                    savedate = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
                except ValueError:
                    await ctx.edit_original_response(content=f'Invalid date: `{date}`\nMake sure to use a possible date.')
                    return
            except TypeError:
                await ctx.response.send_message(f'Invalid date: {date}\nUse the form `dd/mm/yyyy`', ephemeral=True)
                return

        set = number
        if set == None:
            await ctx.response.send_message(f'Invalid train number: {number.upper()}',ephemeral=True)
            return
        
        try:
            if 201 <= int(number) <=248:
                type = 'A-Series'
            elif 301 <= int(number) <=348:
                type = 'A-Series'
            elif 4049 <= int(number) <=4126:
                type = 'B-Series'
            elif 6049 <= int(number) <=6126:
                type = 'B-Series'
            elif 5049 <= int(number) <=5126:
                type = 'B-Series'
            elif int(str(number)[-3:]) >= 126:
                type = 'C-Series'
            else:
                type = 'Unknown'
        except:
            type = 'Unknown'
        
        # Add train to the list
        id = addPerthTrain(ctx.user.id, ctx.user.name, set, type, savedate, line, start.title(), end.title())

        embed = discord.Embed(title="Train Logged",colour=transperth_colour)
        
        embed.add_field(name="Number", value=f'{set} ({type})')
        embed.add_field(name="Line", value=line)
        embed.add_field(name="Date", value=savedate)
        embed.add_field(name="Trip", value=f'{start.title()} to {end.title()}')
        embed.set_footer(text=f"Log ID #{id}")

        await ctx.response.send_message(embed=embed, ephemeral=hidemessage)
        
                
    # Run in a separate task
    asyncio.create_task(log())

# plane logger
@trainlogs.command(name="flight", description="Log a Flight you have been on")
@app_commands.describe(flightnumber = "Flight Number", date = "Date in DD/MM/YYYY format", airline = 'Air Line', start='Starting Airport ICAO', end = 'Ending Airport ICAO', hidemessage='Hide the message from other users, note this will not make the log private.')
# @app_commands.autocomplete(start=Perthstation_autocompletion)
# @app_commands.autocomplete(end=Perthstation_autocompletion)
# @app_commands.autocomplete(line=Perthline_autocompletion)

# plane logger
async def logFlght(ctx, registration:str, type:str, start:str, end:str, airline:str, flightnumber: str='None', date:str='today', hidemessage:bool=False):
    log_command(ctx.user.id, 'log-flight')
    await ctx.response.defer(ephemeral=hidemessage)
    await printlog(date)
    await maintenance_func(ctx)
    async def log():
        await printlog("logging the fliying train")

        savedate = date.split('/')
        if date.lower() == 'today':
            current_time = time.localtime()
            savedate = time.strftime("%Y-%m-%d", current_time)
        else:
            try:
                savedate = time.strptime(date, "%d/%m/%Y")
                savedate = time.strftime("%Y-%m-%d", savedate)
            except ValueError:
                try:
                    savedate = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
                except ValueError:
                    await ctx.edit_original_response(content=f'Invalid date: `{date}`\nMake sure to use a possible date.')
                    return
            except TypeError:
                await ctx.response.send_message(f'Invalid date: {date}\nUse the form `dd/mm/yyyy`', ephemeral=True)
                return
        
        # find info for the airports
        # print('getting airport data')
        # startinfo = get_airport_data(start)
        # endinfo = get_airport_data(end)
        # print('got airport data')
        # get photo
        print('getting the pic')
        response = await getplaneimage(registration)
        print('got the pic')
        try:
            if not response.get('photos'):
                raise ValueError("No photos found for this registration")
            photo = response['photos'][0]
            imgURL = photo['thumbnail']['src']
            photographer = photo['photographer']
            url = photo['link']

        except Exception as e:
            await printlog(f'Error getting image: {e}')
            imgURL = None
            photographer = 'no one'
            url = 'https://planespotters.net'
        
        # Add train to the list
        id = addFlight(ctx.user.id, ctx.user.name, registration.upper(), type.upper(), savedate, flightnumber.upper(), start.upper(), end.upper(), airline.title())

        embed = discord.Embed(title="Flight Logged",colour=0x0070c0)
        
        embed.add_field(name="Flight", value=f'{airline} {flightnumber}')
        embed.add_field(name="Aircraft", value=f'{type} ({registration})')
        embed.add_field(name="Date", value=savedate)
        embed.add_field(name="Trip", value=f'{start.upper()} to {end.upper()}')
        embed.set_thumbnail(url=imgURL)
        embed.add_field(name="Photo", value=f'Photo by {photographer} on [planespotters.net]({url})')
        embed.set_footer(text=f"Log ID #{id}")

        await ctx.followup.send(embed=embed, ephemeral=hidemessage)
        
                
    # Run in a separate task
    asyncio.create_task(log())

async def NSWstop_autocompletion(
    interaction: discord.Interaction,
    current: str
) -> typing.List[app_commands.Choice[str]]:
    fruits = NSWstops_list.copy()
    return [
        app_commands.Choice(name=fruit, value=fruit)
        for fruit in fruits if current.lower() in fruit.lower()
    ][:25]

@trainlogs.command(name="sydney-tram", description="Log a Sydney Tram/Light Rail you have been on")
@app_commands.describe(number = "Carrige Number", type = 'Type of tram', date = "Date in DD/MM/YYYY format", line = 'Light Rail Line', start='Starting Stop', end = 'Ending Stop', hidemessage='Hide the message from other users, note this will not make the log private.')
@app_commands.autocomplete(start=NSWstop_autocompletion)
@app_commands.autocomplete(end=NSWstop_autocompletion)

@app_commands.choices(line=[
        app_commands.Choice(name="L1 Dulwich Hill Line", value="L1"),
        app_commands.Choice(name="L2 Randwick", value="L2"),
        app_commands.Choice(name="L3 Kingsford Line", value="L3"),
        app_commands.Choice(name="L4 Westmead and Carlingford Line", value="L4"),
        app_commands.Choice(name="NLR Newcastle Light Rail", value="NLR"),
])
@app_commands.choices(type=[
        app_commands.Choice(name="Urbos 3", value="Urbos 3"),
    app_commands.Choice(name="Urbos 100", value="Urbos 100"),
        app_commands.Choice(name="Citadis 305", value="Citadis 305"),
])
# SYdney tram logger nsw tram
async def logNSWTram(ctx, line:str, number: str, type:str, start:str, end:str, date:str='today', hidemessage:bool=False):
    channel = ctx.channel
    await printlog(date)
    await maintenance_func(ctx)
    async def log():
        log_command(ctx.user.id, 'log-nsw-tram')
        await printlog("logging the sydney tram")

        savedate = date.split('/')
        if date.lower() == 'today':
            current_time = time.localtime()
            savedate = time.strftime("%Y-%m-%d", current_time)
        else:
            try:
                savedate = time.strptime(date, "%d/%m/%Y")
                savedate = time.strftime("%Y-%m-%d", savedate)
            except ValueError:
                try:
                    savedate = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
                except ValueError:
                    await ctx.edit_original_response(content=f'Invalid date: `{date}`\nMake sure to use a possible date.')
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
        id = addSydneyTram(ctx.user.id, ctx.user.name, set, type, savedate, line, start.title(), end.title())

        embed = discord.Embed(title="Tram Logged",colour=sydney_tram_colour)
        
        embed.add_field(name="Number", value=f'{set} ({type})')
        embed.add_field(name="Line", value=line)
        embed.add_field(name="Date", value=savedate)
        embed.add_field(name="Trip", value=f'{start.title()} to {end.title()}')
        embed.set_footer(text=f"Log ID #{id}")

        await ctx.response.send_message(embed=embed, ephemeral=hidemessage)
        
                
    # Run in a separate task
    asyncio.create_task(log())
    
@trainlogs.command(name="canberra-tram", description="Log a Canberra Tram/Light Rail trip you have been on")
@app_commands.describe(number = "Carrige Number", type = 'Type of tram', date = "Date in DD/MM/YYYY format", line = 'Light Rail Line', start='Starting Stop', end = 'Ending Stop', hidemessage='Hide the message from other users, note this will not make the log private.')
@app_commands.choices(line=[
        app_commands.Choice(name="R1", value="R1"),
])
@app_commands.choices(type=[
        app_commands.Choice(name="Urbos 3", value="Urbos 3"),
    app_commands.Choice(name="Urbos 100", value="Urbos 100"),
])
@app_commands.choices(start=[
        app_commands.Choice(name='Alinga Street', value='Alinga Street'),
        app_commands.Choice(name='Elouera Street', value='Elouera Street'),
        app_commands.Choice(name='Ipima Street', value='Ipima Street'),
        app_commands.Choice(name='Macarthur Avenue', value='Macarthur Avenue'),
        app_commands.Choice(name='Dickson Interchange', value='Dickson Interchange'),
        app_commands.Choice(name='Swinden Street', value='Swinden Street'),
        app_commands.Choice(name='Phillip Avenue', value='Phillip Avenue'),
        app_commands.Choice(name='EPIC and Racecourse', value='EPIC and Racecourse'),
        app_commands.Choice(name='Sandford Street', value='Sandford Street'),
        app_commands.Choice(name='Well Station Drive', value='Well Station Drive'),
        app_commands.Choice(name='Nullarbor Avenue', value='Nullarbor Avenue'),
        app_commands.Choice(name='Mapleton Avenue', value='Mapleton Avenue'),
        app_commands.Choice(name='Manning Clark North', value='Manning Clark North'),
        app_commands.Choice(name='Gungahlin Place', value='Gungahlin Place'),
])
@app_commands.choices(end=[
        app_commands.Choice(name='Alinga Street', value='Alinga Street'),
        app_commands.Choice(name='Elouera Street', value='Elouera Street'),
        app_commands.Choice(name='Ipima Street', value='Ipima Street'),
        app_commands.Choice(name='Macarthur Avenue', value='Macarthur Avenue'),
        app_commands.Choice(name='Dickson Interchange', value='Dickson Interchange'),
        app_commands.Choice(name='Swinden Street', value='Swinden Street'),
        app_commands.Choice(name='Phillip Avenue', value='Phillip Avenue'),
        app_commands.Choice(name='EPIC and Racecourse', value='EPIC and Racecourse'),
        app_commands.Choice(name='Sandford Street', value='Sandford Street'),
        app_commands.Choice(name='Well Station Drive', value='Well Station Drive'),
        app_commands.Choice(name='Nullarbor Avenue', value='Nullarbor Avenue'),
        app_commands.Choice(name='Mapleton Avenue', value='Mapleton Avenue'),
        app_commands.Choice(name='Manning Clark North', value='Manning Clark North'),
        app_commands.Choice(name='Gungahlin Place', value='Gungahlin Place'),
])
# Canberra Tram Logger
async def logCanberraTram(ctx, line:str, number: str, type:str, start:str, end:str, date:str='today', hidemessage:bool=False):
    channel = ctx.channel
    await printlog(date)
    await maintenance_func(ctx)
    async def log():
        log_command(ctx.user.id, 'log-canberra-tram')
        await printlog("logging the canberra tram")

        savedate = date.split('/')
        if date.lower() == 'today':
            current_time = time.localtime()
            savedate = time.strftime("%Y-%m-%d", current_time)
        else:
            try:
                savedate = time.strptime(date, "%d/%m/%Y")
                savedate = time.strftime("%Y-%m-%d", savedate)
            except ValueError:
                try:
                    savedate = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
                except ValueError:
                    await ctx.edit_original_response(content=f'Invalid date: `{date}`\nMake sure to use a possible date.')
                    return
            except TypeError:
                await ctx.response.send_message(f'Invalid date: {date}\nUse the format `dd/mm/yyyy`', ephemeral=True)
                return
        set = number
        if set == None:
            await ctx.response.send_message(f'Invalid train number: {number.upper()}',ephemeral=True)
            return

        # Add train to the list
        id = addCanberraTram(ctx.user.id, ctx.user.name, number, type, savedate, line, start.title(), end.title())

        embed = discord.Embed(title="Tram Logged",colour=sydney_tram_colour)
        
        embed.add_field(name="Number", value=f'{number} ({type})')
        embed.add_field(name="Line", value=line)
        embed.add_field(name="Date", value=savedate)
        embed.add_field(name="Trip", value=f'{start.title()} to {end.title()}')
        embed.set_footer(text=f"Log ID #{id}")

        await ctx.response.send_message(embed=embed, ephemeral=hidemessage)
        
                
    # Run in a separate task
    asyncio.create_task(log())

async def station_autocompletion(
    interaction: discord.Interaction,
    current: str
) -> typing.List[app_commands.Choice[str]]:
    fruits = bus_coach_stops.copy()
    return [
        app_commands.Choice(name=fruit, value=fruit)
        for fruit in fruits if current.lower() in fruit.lower()
    ][:25]

async def busline_autocompletion(
    interaction: discord.Interaction,
    current: str
) -> typing.List[app_commands.Choice[str]]:
    fruits = sorted(set(busroutes))
    return [
        app_commands.Choice(name=fruit, value=fruit)
        for fruit in fruits if current.lower() in fruit.lower()
    ][:25]
    
@trainlogs.command(name="bus", description="Log a Bus you have been on")
@app_commands.describe(number = "Bus number with prefix or number plate", type = 'Type of bus', date = "Date in DD/MM/YYYY format", line = 'bus route', start='Starting Stop', end = 'Ending Stop', hidemessage='Hide the message from other users, note this will not make the log private.')
@app_commands.autocomplete(operator=busOpsautocompletion)
@app_commands.autocomplete(start=station_autocompletion)
@app_commands.autocomplete(end=station_autocompletion)
@app_commands.autocomplete(line=busline_autocompletion)

async def logBus(ctx, line:str, number: str, start:str, end:str, operator:str='Unknown', date:str='today', type:str='Unknown', notes:str=None, hidemessage:bool=False):
    channel = ctx.channel
    await ctx.response.defer(ephemeral=hidemessage)
    await printlog(date)
    await maintenance_func(ctx)
    async def log(notes,type,operator):
        log_command(ctx.user.id, 'log-bus')
        await printlog("logging the bus")

        savedate = date.split('/')
        if date.lower() == 'today':
            current_time = time.localtime()
            savedate = time.strftime("%Y-%m-%d", current_time)
        else:
            try:
                savedate = time.strptime(date, "%d/%m/%Y")
                savedate = time.strftime("%Y-%m-%d", savedate)
            except ValueError:
                try:
                    savedate = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
                except ValueError:
                    await ctx.edit_original_response(content=f'Invalid date: `{date}`\nMake sure to use a possible date.')
                    return
            except TypeError:
                await ctx.edit_original_response(content=f'Invalid date: {date}\nUse the form `dd/mm/yyyy`', ephemeral=True)
                return
        set = number.upper()
        # format notes so it dosnt break anything
        if notes:
            notes = re.sub(r'[^\x00-\x7F]+', '', notes)
            notes = notes.replace('\n', ' ')
            # notes = f'"{notes}"'
        try:
            await printlog("trying new version")
            if set[0] == "D":
                numbertest = set[1:]
                operator = "Dysons"
            elif set[:2] == "SK":
                numbertest = set[2:]
                operator == "Skybus"
            elif set[:2] == "MK":
                numbertest = set[2:]
                operator = "McKenzies"
            elif set[:2] == "TS":
                numbertest = set[2:]
                operator = "Transit Systems"
            elif set[:2] == "CH":
                numbertest = set[2:]
                operator = "Christians"
            elif set[:2] == "CR":
                numbertest = set[2:]
                operator = "Cranbourne"
            elif set[:2] == "MT":
                numbertest = set[2:]
                operator = "Martyrs"
            elif set[0] == "S":
                numbertest = set[1:]
                operator = "Sunbury"
            elif set[0] == "V":
                numbertest = set[1:]
                operator = "Ventura"
            elif set[0] == "K":
                numbertest = set[1:]
                operator = "Kinetic"
            elif set[0] == "C":
                numbertest = set[1:]
                operator = "CDC"
            elif len(set) == 6:
                operator = "platenumber"
            if operator != "platenumber":
                with open('utils/bussets.csv','r') as bussetsFile:
                    reader = csv.reader(bussetsFile)
                    for row in reader:
                        if row[0] == numbertest and row[2] == operator:
                            type = f'{row[4]} on {row[3]}'
                            plate = row[1]
                            await printlog(f"type: {type}\nplate:{plate}")
            elif operator == "platenumber":
                with open('utils/bussets.csv','r') as bussetsFile:
                    reader = csv.reader(bussetsFile)
                    for row in reader:
                        if row[1] == set:
                            type = f'{row[4]} on {row[3]}'
                            plate = row[1]
                            numbertest = row[0]
                            operator = row[2]
                            await printlog(f"type: {type}\nplate:{plate}")
        except:
            await printlog("reverting to old version")
            try:
                if operator == 'Ventura Bus Lines':
                    operator = 'Ventura'
                elif operator == 'Cdc Melbourne':
                    operator = 'CDC'
                elif operator == 'McKenzies Tourist Service':
                    operator = 'McKenzies'
                elif operator == 'Martyrs Bus Service':
                    operator = 'Martyrs'
                elif operator == 'Sunbury Bus Service':
                    operator == 'Sunbury'
                elif operator == 'Cranbourne Transit':
                    operator = 'Cranbourne'
                elif operator == 'Christians Bus Lines':
                    operator = 'Christians'
                with open('utils/bussets.csv','r') as bussetsFile:
                    reader = csv.reader(bussetsFile)
                    for row in reader:
                        if row[0] == set and row[2] == operator:
                            type = f'{row[4]} on {row[3]}'
                            plate = row[1]
                            await printlog(f"type: {type}\nplate:{plate}")
            except:
                pass



        # Add bus to the list
        try:
            id = addBus(ctx.user.id, ctx.user.name, numbertest, type, savedate, line, start.title(), end.title(), operator.title(), notes)
        except:
            id = addBus(ctx.user.id, ctx.user.name, set, type, savedate, line, start.title(), end.title(), operator.title(), notes)

        embed = discord.Embed(title="Bus Logged",colour=bus_colour)

        embed.add_field(name="Route", value=line)
        if operator == "platenumber":
            operator = "Unknown"
        embed.add_field(name="Operator", value=operator)
        try:
            embed.add_field(name="Number", value=f'{numbertest}')
        except:
            embed.add_field(name="Number", value=f'{set}')
        try:
            embed.add_field(name="Number Plate", value=f'{plate}')
        except:
            pass
        embed.add_field(name="Type", value=f'{type}')
        embed.add_field(name="Date", value=savedate)
        embed.add_field(name="Trip", value=f'{start.title()} to {end.title()}')
        if notes != None:
            embed.add_field(name="Notes", value=notes)
        try:
            image, credits = getImage(plate, False, 'bus')
            if image:
                embed.set_thumbnail(url=image)
                embed.set_footer(text=f'Log ID #{id} | Photo by {credits}')
            else:
                embed.set_footer(text=f"Log ID #{id}")
        except:
            embed.set_footer(text=f"Log ID #{id}")

        await ctx.edit_original_response(embed=embed)
        
                
    # Run in a separate task
    asyncio.create_task(log(notes,type,operator))

@trainlogs.command(name='busedit',description='Edit a logged trip')
@app_commands.choices(mode=[
    app_commands.Choice(name="Bus", value="bus"),
])
@app_commands.autocomplete(operator=busOpsautocompletion)
@app_commands.autocomplete(start=station_autocompletion)
@app_commands.autocomplete(end=station_autocompletion)
@app_commands.describe(date = "Date in DD/MM/YYYY format")
async def editrow(ctx, id:str, mode:str='bus', line:str='nochange', number:str='nochange', start:str='nochange', end:str='nochange', date:str='nochange', type:str='auto', operator:str='nochange', notes:str='nochange'):
    await ctx.response.defer()
    await maintenance_func(ctx)
    log_command(ctx.user.id, 'edit-row')
    
    username = ctx.user.name
    userid = ctx.user.id
    logid = id
    if logid[0] == '#':
        idformatted = logid[1:].upper()
    else:
        idformatted = logid.upper()
    
    # Find old data for the edited row
    dataToDelete = universalReadRow(userid, username, idformatted, mode)
    
    if notes != 'nochange':
            # Remove emojis using regex
            notes = re.sub(r'[^\x00-\x7F]+', '', notes)
            # Remove newlines
            notes = notes.replace('\n', ' ')
            #add quotes so the csv dosn't break when u use a comma
            notes = f'"{notes}"'
            
    # convert date from DD/MM/YYYY to YYYY-MM-DD
    if date != 'nochange':
        if date.lower() == 'today':
            current_time = time.localtime()
            savedate = time.strftime("%Y-%m-%d", current_time)
        else:
            try:
                savedate = time.strptime(date, "%d/%m/%Y")
                savedate = time.strftime("%Y-%m-%d", savedate)
            except ValueError:
                try:
                    savedate = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
                except ValueError:
                    await ctx.edit_original_response(content=f'Invalid date: `{date}`\nMake sure to use a possible date.')
                    return
            except TypeError:
                await ctx.edit_original_response(content=f'Invalid date: `{date}`\nUse the form `dd/mm/yyyy`')
                return
    else:
        savedate = 'nochange'

    try:
        await printlog("trying new version")
        if number[0] == "D":
            numbertest = number[1:]
            operator = "Dysons"
        elif number[0] == "V":
            numbertest = number[1:]
            operator = "Ventura"
        elif number[0] == "K":
            numbertest = number[1:]
            operator = "Kinetic"
        elif number[0] == "C":
            numbertest = number[1:]
            operator = "CDC"
        elif number[0] == "S":
            numbertest = number[1:]
            operator = "Skybus"
        elif number[:2] == "TS":
            numbertest = number[2:]
            operator = "Transit Systems"
        elif number[:2] == "MK":
            numbertest = number[2:]
            operator = "McKenzies"
        elif len(number) == 6:
            operator = "platenumber"
        if operator != "platenumber":
            with open('utils/bussets.csv','r') as bussetsFile:
                reader = csv.reader(bussetsFile)
                for row in reader:
                    if row[0] == numbertest and row[2] == operator:
                        type = f'{row[4]} on {row[3]}'
                        plate = row[1]
                        await printlog(f"type: {type}\nplate:{plate}")
        elif operator == "platenumber":
            with open('utils/bussets.csv','r') as bussetsFile:
                reader = csv.reader(bussetsFile)
                for row in reader:
                    if row[1] == set:
                        type = f'{row[4]} on {row[3]}'
                        plate = row[1]
                        numbertest = row[0]
                        operator = row[2]
                        await printlog(f"type: {type}\nplate:{plate}")
    except:
        await printlog("reverting to old version")
        try:
            if operator == 'Ventura Bus Lines':
                operator = 'Ventura'
            elif operator == 'Cdc Melbourne':
                operator = 'CDC'
            elif operator == 'McKenzies Tourist Service':
                operator = 'McKenzies'
            with open('utils/bussets.csv','r') as bussetsFile:
                reader = csv.reader(bussetsFile)
                for row in reader:
                    if row[0] == number and row[2] == operator:
                        type = f'{row[4]} on {row[3]}'
                        plate = row[1]
                        await printlog(f"type: {type}\nplate:{plate}")
        except:
            pass
    try:
        result = editRowBus(userid, username, idformatted, mode,line,numbertest,start,end,savedate,type,operator,notes)
    except:
        result = editRowBus(userid, username, idformatted, mode,line,number,start,end,savedate,type,operator,notes)
    
    if result == 'invalid id did not show up':
        await ctx.edit_original_response(content=f'Invalid log ID entered: `{idformatted}`')
        return
    
    
    await ctx.edit_original_response(content=f'**Successfully edited log `#{idformatted}`**\nOld data:\n`{dataToDelete}`\nNew data:\n`{result}`')

# train logger reader log view
vLineLines = ['Geelong','Warrnambool', 'Ballarat', 'Maryborough', 'Ararat', 'Bendigo','Echuca', 'Swan Hill','Albury', 'Seymour', 'Shepparton', 'Traralgon', 'Bairnsdale']

@trainlogs.command(name="view", description="View logged trips for a user")
@app_commands.describe(user = "Who do you want to see the data of?", mode = 'Train or tram logs?',id='Leave blank to show all logs')
@app_commands.choices(mode=[
        app_commands.Choice(name="Victorian Trains", value="train"),
        app_commands.Choice(name="Melbourne Trams", value="tram"),
        app_commands.Choice(name="Bus", value="bus"),
        app_commands.Choice(name="NSW Trains", value="sydney-trains"),
        app_commands.Choice(name="Sydney Light Rail", value="sydney-trams"),
        app_commands.Choice(name="Adelaide Trains & Journey Beyond", value="adelaide-trains"),
        app_commands.Choice(name="Adelaide Trams", value="adelaide-trams"),
        app_commands.Choice(name="Perth Trains", value="perth-trains"),
        app_commands.Choice(name="Canberra Light Rail", value="canberra-trams"),
        app_commands.Choice(name="Flights", value="flights"),

])
# @app_commands.choices(send=[
#         app_commands.Choice(name="Web (Victorian Train only)", value="web"),
#         app_commands.Choice(name="Thread", value="thread"),
# ])

async def userLogs(ctx, mode:str='train', user: discord.User=None, id:str=None):
    await maintenance_func(ctx)
    async def sendLogs():
        log_command(ctx.user.id, 'view-log')
        
        # if mode == 'train' and id == None and send == 'web':
        #     await ctx.response.send_message('[Click here to view your logs online](https://trackpulsevic.xm9g.net/logs/viewer)', ephemeral=False)
        #     return
        
        if user == None:
                userid = ctx.user
        else:
            userid = user
            
        if userid != ctx.user and ctx.user.id not in admin_users:
            await ctx.response.send_message('You cannot view other users logs.', ephemeral=True)
            return
            
        # for signle log viewing
        if id != None:
            await ctx.response.defer()
            
            if mode == 'train':
                file_path = f'utils/trainlogger/userdata/{userid.name}.csv'
                fileid = f'utils/trainlogger/userdata/{userid.id}.csv'
            else:
                file_path = f'utils/trainlogger/userdata/{mode}/{userid.name}.csv'
                fileid = f'utils/trainlogger/userdata/{mode}/{userid.id}.csv'
            
            if not os.path.exists(fileid):
                print(f"userid doesn't exist, using username: {file_path}")
            else:
                print(f"userid does exist, using userid: {fileid} (belonging to {userid.name})")
                file_path = fileid
                
            
            if mode != 'bus':
                with open(file_path, mode='r', newline='') as file:
                    
                    if not id.startswith('#'):
                        cleaned_id = '#' + id
                    else:
                        cleaned_id = id
                    csv_reader = csv.reader(file)
                    for row in csv_reader:
                        if row[0] == cleaned_id.upper():
                            
                            # thing to find image:
                            image, credits = None, None

                            train_number = row[1]

                            if "-" not in train_number:
                                image, credits = getImage(train_number)
                            else:
                                hyphen_index = train_number.find("-")
                                if hyphen_index != -1:
                                    first_car = train_number[:hyphen_index]
                                    await printlog(f'First car: {first_car}')
                                    
                                    image, credits = getImage(first_car)
                                    
                                    if image is None:
                                        last_hyphen = train_number.rfind("-")
                                        if last_hyphen != -1:
                                            last_car = train_number[last_hyphen + 1 :]
                                            await printlog(f'Last car: {last_car}')
                                            
                                            image, credits = getImage(last_car)
                                            
                                            if image is None:
                                                image, credits = getImage(row[2])
                                                await printlog(f'the loco number is: {train_number}')
                                            
                            # Make the embed
                            if row[4] in vLineLines:
                                embed = discord.Embed(title=f"Log {row[0]}",colour=vline_map_colour)
                            elif row[4] == 'Unknown':
                                    embed = discord.Embed(title=f"Log {row[0]}")
                            else:
                                try:
                                    embed = discord.Embed(title=f"Log `{row[0]}`",colour=lines_dictionary_log_train_map_post_munnel[row[4]][1])
                                except:
                                    embed = discord.Embed(title=f'Log `{id}`')
                            embed.add_field(name=f'Set', value="{} ({})".format(row[1], row[2]))
                            embed.add_field(name=f'Line', value="{}".format(row[4]))
                            embed.add_field(name=f'Date', value="{}".format(row[3]))
                            embed.add_field(name=f'Trip', value=f"{row[5]} to {row[6]}")
                            if row[5] != 'N/A' and row[6] != 'N/A':
                                if getStationDistance(load_station_data("utils/trainlogger/stationDistances.csv"), row[5], row[6]) != 'N/A':
                                    embed.add_field(name='Distance:', value=f'{round(getStationDistance(load_station_data("utils/trainlogger/stationDistances.csv"), row[5], row[6]))}km')
                            try:
                                if row[7]:
                                    embed.add_field(name='Notes:', value=row[7].strip('"'))
                                    
                            except:
                                pass
                            try:
                                embed.set_thumbnail(url=image)
                                embed.set_footer(text=f'Photo by {credits}')
                            except:
                                await printlog('no image')
                            await ctx.followup.send(embed=embed)
                            return
                    # if there is no row with the id:
                    await ctx.followup.send(f'Cannot find log `{id}`')
            elif mode == 'bus':
                with open(file_path,'r') as buslogs:
                    reader = csv.reader(buslogs)
                    if not id.startswith('#'):
                        cleaned_id = '#' + id
                    else:
                        cleaned_id = id
                    for row in reader:
                        if row[0] == cleaned_id.upper():
                            # get plate
                            plate = None
                            with open('utils/bussets.csv','r') as bussets:
                                reader = csv.reader(bussets)
                                for busrow in reader:
                                    if busrow[0] == row[1] and row[7] == busrow[2]:
                                        plate = busrow[1]
                                        print(plate)
                                        break
                            #make embed
                            embed = discord.Embed(title=f"Log {row[0]}",colour=bus_colour)
                            embed.add_field(name='Route',value=row[4])
                            embed.add_field(name='Operator',value=row[7])
                            embed.add_field(name='Number',value=row[1])
                            if plate:
                                embed.add_field(name='Number Plate',value=plate)
                                image, credits = getImage(plate, False, 'bus')
                                if image:
                                    embed.set_thumbnail(url=image)
                                    embed.set_footer(text=f'Photo by {credits}')
                            embed.add_field(name='Type',value=row[2])
                            embed.add_field(name='Date',value=row[3])
                            embed.add_field(name='Trip',value=f"{row[5]} to {row[6]}")
                            if row[8]:
                                embed.add_field(name='Notes',value=row[8])
                await ctx.followup.send(embed=embed)

                
        else:
            # for train
            if mode == 'train':
                if user == None:
                    userid = ctx.user
                else:
                    userid = user
                
                try:
                    try:
                        file = discord.File(f'utils/trainlogger/userdata/{userid.id}.csv')
                    except:
                        file = discord.File(f'utils/trainlogger/userdata/{userid.name}.csv')
                except FileNotFoundError:
                    if userid == ctx.user:
                        await ctx.response.send_message("You have no trains logged!",ephemeral=True)
                    else:
                        await ctx.response.send_message("This user has no trains logged!",ephemeral=True)
                    return
                await printlog(userid.name)
                data = readLogs(userid.id, userid.name)
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
                pfp = userid.avatar.url
                embed=discord.Embed(title='Train Logs', colour=vline_colour)
                embed.set_author(name=userid.name, url='https://victorianrailphotos.com', icon_url=pfp)
                embed.add_field(name='Click here to view your logs:', value=f'<#{logsthread.id}>')
                embed.add_field(name='Click here to view your own logs on the website:', value=f'[Trackpulse Vic Website](https://discord.com/oauth2/authorize?client_id=1214144664513417218&redirect_uri=https%3A%2F%2Ftrackpulsevic.xm9g.net%2Flogs%2Fviewer&response_type=code&scope=identify)')
                await ctx.response.send_message(embed=embed)
                await logsthread.send(f'# <:train:1241164967789727744> {userid.name}\'s CSV file', file=file)
                await logsthread.send(f'# {userid.name}\'s Train Logs')
                formatted_data = ""
                for sublist in data:
                    if len(sublist) >= 7:  # Ensure the sublist has enough items
                        image = None
                        
                        # thing to find image:
                        image, credits = None, None

                        train_number = sublist[1]

                        if "-" not in train_number:
                            image, credits = getImage(train_number)
                        else:
                            hyphen_index = train_number.find("-")
                            if hyphen_index != -1:
                                first_car = train_number[:hyphen_index]
                                await printlog(f'First car: {first_car}')
                                
                                image, credits = getImage(first_car)
                                
                                if image is None:
                                    last_hyphen = train_number.rfind("-")
                                    if last_hyphen != -1:
                                        last_car = train_number[last_hyphen + 1 :]
                                        await printlog(f'Last car: {last_car}')
                                        
                                        image, credits = getImage(last_car)
                                        
                                        if image is None:
                                            image, credits = getImage(sublist[2])
                                            await printlog(f'the loco number is: {train_number}')

                                        
                        #send in thread to reduce spam!
                            # Make the embed
                        if sublist[4] in vLineLines:
                            embed = discord.Embed(title=f"Log `{sublist[0]}`",colour=vline_colour)
                        elif sublist[4] == 'Unknown':
                                embed = discord.Embed(title=f"Log `{sublist[0]}`")
                        else:
                            try:
                                embed = discord.Embed(title=f"Log `{sublist[0]}`",colour=lines_dictionary_log_train_map_post_munnel[sublist[4]][1])
                            except:
                                embed = discord.Embed(title=f"Log {sublist[0]}")
                        embed.add_field(name=f'Set', value="{} ({})".format(sublist[1], sublist[2]))
                        embed.add_field(name=f'Line', value="{}".format(sublist[4]))
                        embed.add_field(name=f'Date', value="{}".format(sublist[3]))
                        embed.add_field(name=f'Trip Start', value="{}".format(sublist[5]))
                        embed.add_field(name=f'Trip End', value="{}".format(sublist[6]))
                        if sublist[5] != 'N/A' and sublist[6] != 'N/A':
                            if getStationDistance(load_station_data("utils/trainlogger/stationDistances.csv"), sublist[5], sublist[6]) != 'N/A':
                                embed.add_field(name='Distance:', value=f'{round(getStationDistance(load_station_data("utils/trainlogger/stationDistances.csv"), sublist[5], sublist[6]))}km')
                        if sublist[7]:
                            embed.add_field(name='Notes:', value=sublist[7].strip('"'))
                        try:
                            embed.set_thumbnail(url=image)
                        except:
                            await printlog('no image')
                        
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
                    try:
                        file = discord.File(f'utils/trainlogger/userdata/tram/{userid.id}.csv')
                    except:
                        file = discord.File(f'utils/trainlogger/userdata/tram/{userid.name}.csv')
                except FileNotFoundError:
                    if userid == ctx.user:
                        await ctx.follow("You have no trams logged!",ephemeral=True)
                    else:
                        await ctx.response.send_message("This user has no trams logged!",ephemeral=True)
                    return
                await printlog(userid.name)
                data = readTramLogs(userid.id, userid.name)
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
                await logsthread.send(f' # <:tram:1241165701390012476> {userid.name}\'s Tram Logs')
                formatted_data = ""
                for sublist in data:
                    if len(sublist) >= 7:  # Ensure the sublist has enough items
                        image = None
                                                                
                        #send in thread to reduce spam!
                        thread = await ctx.channel.create_thread(name=f"{userid.name}'s logs")
                            # Make the embed
                        if sublist[4] in vLineLines:
                            embed = discord.Embed(title=f"Log {sublist[0]}",colour=vline_colour)
                        elif sublist[4] == 'Unknown':
                            embed = discord.Embed(title=f"Log {sublist[0]}")
                        else:
                            embed = discord.Embed(title=f"Log {sublist[0]}",colour=tram_colour)
                        embed.add_field(name=f'Set', value="{} ({})".format(sublist[1], sublist[2]))
                        embed.add_field(name=f'Line', value="{}".format(sublist[4]))
                        embed.add_field(name=f'Date', value="{}".format(sublist[3]))
                        embed.add_field(name=f'Trip Start', value="{}".format(sublist[5]))
                        embed.add_field(name=f'Trip End', value="{}".format(sublist[6]))
                        if len(sublist) >= 8:
                            embed.add_field(name='Notes:', value=sublist[7].strip('"'))
                        # embed.set_thumbnail(url=image)

                        try:
                            embed.set_thumbnail(url=image)
                        except:
                            await printlog('no image')

                        await logsthread.send(embed=embed)
                        time.sleep(1)
            
            # for sydney light rail tram:
            if mode == 'sydney-trams':
                if user == None:
                    userid = ctx.user
                else:
                    userid = user
                
                try:
                    try:
                        file = discord.File(f'utils/trainlogger/userdata/sydney-trams/{userid.id}.csv')
                    except:
                        file = discord.File(f'utils/trainlogger/userdata/sydney-trams/{userid.name}.csv')
                except FileNotFoundError:
                    if userid == ctx.user:
                        await ctx.response.send_message("You have no trams logged!",ephemeral=True)
                    else:
                        await ctx.response.send_message("This user has no trams logged!",ephemeral=True)
                    return
                await printlog(userid.name)
                data = readSydneyLightRailLogs(userid.id, userid.name)
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
                            embed = discord.Embed(title=f"Log {sublist[0]}",colour=sydney_tram_colour)
                        embed.add_field(name=f'Set', value="{} ({})".format(sublist[1], sublist[2]))
                        embed.add_field(name=f'Line', value="{}".format(sublist[4]))
                        embed.add_field(name=f'Date', value="{}".format(sublist[3]))
                        embed.add_field(name=f'Trip Start', value="{}".format(sublist[5]))
                        embed.add_field(name=f'Trip End', value="{}".format(sublist[6]))

                        await logsthread.send(embed=embed)
                        time.sleep(1) 
            
            # for nsw train:
            if mode == 'sydney-trains':
                if user == None:
                    userid = ctx.user
                else:
                    userid = user
                
                try:
                    try:
                        file = discord.File(f'utils/trainlogger/userdata/sydney-trains/{userid.id}.csv')
                    except:
                        file = discord.File(f'utils/trainlogger/userdata/sydney-trains/{userid.name}.csv')
                except FileNotFoundError:
                    if userid == ctx.user:
                        await ctx.response.send_message("You have no trains logged!",ephemeral=True)
                    else:
                        await ctx.response.send_message("This user has no trains logged!",ephemeral=True)
                    return
                await printlog(userid.name)
                data = readSydneyTrainLogs(userid.id, userid.name)
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
                            embed = discord.Embed(title=f"Log {sublist[0]}",colour=vline_colour)
                        elif sublist[4] == 'Unknown':
                            embed = discord.Embed(title=f"Log {sublist[0]}")
                        else:
                            embed = discord.Embed(title=f"Log {sublist[0]}",colour=sydney_train_colour)
                        embed.add_field(name=f'Set', value="{} ({})".format(sublist[1], sublist[2]))
                        embed.add_field(name=f'Line', value="{}".format(sublist[4]))
                        embed.add_field(name=f'Date', value="{}".format(sublist[3]))
                        embed.add_field(name=f'Trip Start', value="{}".format(sublist[5]))
                        embed.add_field(name=f'Trip End', value="{}".format(sublist[6]))

                        await logsthread.send(embed=embed)
                        time.sleep(1)     
            # for adelaide:
            if mode == 'adelaide-trains':
                if user == None:
                    userid = ctx.user
                else:
                    userid = user
                
                try:
                    try:
                        file = discord.File(f'utils/trainlogger/userdata/adelaide-trains/{userid.id}.csv')
                    except:
                        file = discord.File(f'utils/trainlogger/userdata/adelaide-trains/{userid.name}.csv')
                except FileNotFoundError:
                    if userid == ctx.user:
                        await ctx.response.send_message("You have no Adelaide trains logged!",ephemeral=True)
                    else:
                        await ctx.response.send_message("This user has no Adelaide trains logged!",ephemeral=True)
                    return
                await printlog(userid.name)
                data = readPerthLogs(userid.name)
                if data == 'no data':
                    if userid == ctx.user:
                        await ctx.response.send_message("You have no Adelaide trains logged!",ephemeral=True)
                    else:
                        await ctx.response.send_message("This user has no Adelaide trains logged!",ephemeral=True)
                    return
            
                # create thread
                logsthread = await ctx.channel.create_thread(
                    name=f'{userid.name}\'s Adelaide Train Logs',
                    auto_archive_duration=60,
                    type=discord.ChannelType.public_thread
                )
                
                # send reponse message
                await ctx.response.send_message(f"Logs will be sent in <#{logsthread.id}>")
                await logsthread.send(f'# {userid.name}\'s CSV file', file=file)
                await logsthread.send(f' # <:Adelaide_train_:1300008231510347807><:journeybeyond:1300021503093510155> {userid.name}\'s Adelaide Train Logs')
                formatted_data = ""
                for sublist in data:
                    if len(sublist) >= 7:  # Ensure the sublist has enough items
                        image = None
                                                
                        #send in thread to reduce spam!
                        thread = await ctx.channel.create_thread(name=f"{userid.name}'s Adelaide Train logs")
                            # Make the embed
                        if sublist[4] == 'Unknown':
                            embed = discord.Embed(title=f"Log {sublist[0]}")
                        else:
                            embed = discord.Embed(title=f"Log {sublist[0]}",colour=adelaide_metro_colour)
                        embed.add_field(name=f'Line', value="{}".format(sublist[4]))
                        embed.add_field(name=f'Date', value="{}".format(sublist[3]))
                        embed.add_field(name=f'Trip Start', value="{}".format(sublist[5]))
                        embed.add_field(name=f'Trip End', value="{}".format(sublist[6]))
                        embed.add_field(name=f'Number', value="{} ({})".format(sublist[1], sublist[2]))
    
                        await logsthread.send(embed=embed)
                        time.sleep(0.7)

            # for adelaide tram:
            if mode == 'adelaide-trams':
                if user == None:
                    userid = ctx.user
                else:
                    userid = user
                
                try:
                    try:
                        file = discord.File(f'utils/trainlogger/userdata/adelaide-trams/{userid.id}.csv')
                    except:
                        file = discord.File(f'utils/trainlogger/userdata/adelaide-trams/{userid.name}.csv')
                except FileNotFoundError:
                    if userid == ctx.user:
                        await ctx.response.send_message("You have no trams logged!",ephemeral=True)
                    else:
                        await ctx.response.send_message("This user has no trams logged!",ephemeral=True)
                    return
                await printlog(userid.name)
                data = readAdelaideTramLogs(userid.id, userid.name)
                if data == 'no data':
                    if userid == ctx.user:
                        await ctx.response.send_message("You have no trams logged!",ephemeral=True)
                    else:
                        await ctx.response.send_message("This user has no trams logged!",ephemeral=True)
                    return
            
                # create thread
                logsthread = await ctx.channel.create_thread(
                    name=f'{userid.name}\'s Adelaide Tram Logs',
                    auto_archive_duration=60,
                    type=discord.ChannelType.public_thread
                )
                
                # send reponse message
                await ctx.response.send_message(f"Logs will be sent in <#{logsthread.id}>")
                await logsthread.send(f'# {userid.name}\'s CSV file', file=file)
                await logsthread.send(f'# {userid.name}\'s Tram Logs')
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
                            embed = discord.Embed(title=f"Log {sublist[0]}",colour=adelaide_tram_colour)
                        embed.add_field(name=f'Set', value="{} ({})".format(sublist[1], sublist[2]))
                        embed.add_field(name=f'Line', value="{}".format(sublist[4]))
                        embed.add_field(name=f'Date', value="{}".format(sublist[3]))
                        embed.add_field(name=f'Trip Start', value="{}".format(sublist[5]))
                        embed.add_field(name=f'Trip End', value="{}".format(sublist[6]))

                        await logsthread.send(embed=embed)
                        time.sleep(2) 

            # for perth:
            if mode == 'perth-trains':
                if user == None:
                    userid = ctx.user
                else:
                    userid = user
                
                try:
                    try:
                        file = discord.File(f'utils/trainlogger/userdata/pertth-trains/{userid.id}.csv')
                    except:
                        file = discord.File(f'utils/trainlogger/userdata/perth-trains/{userid.name}.csv')
                except FileNotFoundError:
                    if userid == ctx.user:
                        await ctx.response.send_message("You have no Perth trains logged!",ephemeral=True)
                    else:
                        await ctx.response.send_message("This user has no Perth trains logged!",ephemeral=True)
                    return
                await printlog(userid.name)
                data = readAdelaideLogs(userid.id, userid.name)
                if data == 'no data':
                    if userid == ctx.user:
                        await ctx.response.send_message("You have no Perth trains logged!",ephemeral=True)
                    else:
                        await ctx.response.send_message("This user has no Perth trains logged!",ephemeral=True)
                    return
            
                # create thread
                logsthread = await ctx.channel.create_thread(
                    name=f'{userid.name}\'s Perth Train Logs',
                    auto_archive_duration=60,
                    type=discord.ChannelType.public_thread
                )
                
                # send reponse message
                await ctx.response.send_message(f"Logs will be sent in <#{logsthread.id}>")
                await logsthread.send(f'# {userid.name}\'s CSV file', file=file)
                await logsthread.send(f'# <:transperthtrain:1335396329798631477><:TransWA:1335397360255373392> {userid.name}\'s Perth Train Logs')
                formatted_data = ""
                for sublist in data:
                    if len(sublist) >= 7:  # Ensure the sublist has enough items
                        image = None
                                                
                        #send in thread to reduce spam!
                        thread = await ctx.channel.create_thread(name=f"{userid.name}'s Perth Train logs")
                            # Make the embed
                        if sublist[4] == 'Unknown':
                            embed = discord.Embed(title=f"Log {sublist[0]}")
                        else:
                            embed = discord.Embed(title=f"Log {sublist[0]}",colour=transperth_colour)
                        embed.add_field(name=f'Line', value="{}".format(sublist[4]))
                        embed.add_field(name=f'Date', value="{}".format(sublist[3]))
                        embed.add_field(name=f'Trip Start', value="{}".format(sublist[5]))
                        embed.add_field(name=f'Trip End', value="{}".format(sublist[6]))
                        embed.add_field(name=f'Number', value="{} ({})".format(sublist[1], sublist[2]))
                        # embed.set_thumbnail(url=image)
    
                        await logsthread.send(embed=embed)
                        time.sleep(2)  
            # for bus:
            if mode == 'bus':
                if user == None:
                    userid = ctx.user
                else:
                    userid = user
                
                try:
                    try:
                        file = discord.File(f'utils/trainlogger/userdata/bus/{userid.id}.csv')
                    except:
                        file = discord.File(f'utils/trainlogger/userdata/bus/{userid.name}.csv')
                except FileNotFoundError:
                    if userid == ctx.user:
                        await ctx.response.send_message("You have no busses logged!",ephemeral=True)
                    else:
                        await ctx.response.send_message("This user has no busses logged!",ephemeral=True)
                    return
                await printlog(userid.name)
                data = readBusLogs(userid.id, userid.name)
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
                            embed = discord.Embed(title=f"Log {sublist[0]}",colour=bus_colour)
                        with open('utils/bussets.csv','r') as bussets:
                            reader = csv.reader(bussets)
                            for row in reader:
                                if row[0] == sublist[1] and row[2] == sublist[7]:
                                    plate = row[1]
                        embed.add_field(name=f'Route', value="{}".format(sublist[4]))
                        embed.add_field(name=f'Operator', value="{}".format(sublist[7]))
                        embed.add_field(name=f'Bus Number', value="{}".format(sublist[1]))
                        try:
                            embed.add_field(name=f'Bus Plate', value=plate)
                        except:
                            pass
                        embed.add_field(name=f'Type', value="{}".format( sublist[2]))
                        embed.add_field(name=f'Date', value="{}".format(sublist[3]))
                        embed.add_field(name=f'Trip', value="{} to {}".format(sublist[5],sublist[6]))
                        if len(sublist) > 8:
                            embed.add_field(name='Notes:', value=sublist[8].strip('"'))
                        try:
                            image, credits = getImage(plate, False, 'bus')
                            if image:
                                embed.set_thumbnail(url=image)
                                embed.set_footer(text=f'Photo by {credits}')
                        except:
                            pass
        
                        await logsthread.send(embed=embed)
                        time.sleep(2) 
            # for plane:
            if mode == 'flights':
                if user == None:
                    userid = ctx.user
                else:
                    userid = user
                
                try:
                    try:
                        file = discord.File(f'utils/trainlogger/userdata/flights/{userid.id}.csv')
                    except:
                        file = discord.File(f'utils/trainlogger/userdata/flights/{userid.name}.csv')
                except FileNotFoundError:
                    if userid == ctx.user:
                        await ctx.response.send_message("You have no flights logged!",ephemeral=True)
                    else:
                        await ctx.response.send_message("This user has no flights logged!",ephemeral=True)
                    return
                await printlog(userid.name)
                data = readFlightlogs(userid.id, userid.name)
                if data == 'no data':
                    if userid == ctx.user:
                        await ctx.response.send_message("You have no flights logged!",ephemeral=True)
                    else:
                        await ctx.response.send_message("This user has no flights logged!",ephemeral=True)
                    return
            
                # create thread
                logsthread = await ctx.channel.create_thread(
                    name=f'{userid.name}\'s Flight Logs',
                    auto_archive_duration=60,
                    type=discord.ChannelType.public_thread
                )
                
                # send reponse message
                await ctx.response.send_message(f"Logs will be sent in <#{logsthread.id}>")
                await logsthread.send(f'# {userid.name}\'s CSV file', file=file)
                await logsthread.send(f' # {userid.name}\'s Flight Logs')
                formatted_data = ""
                for sublist in data:
                    if len(sublist) >= 7:  # Ensure the sublist has enough items
                        image = None
                        
                        # get image
                        try:
                            response = getplaneimage(sublist[1])
                            photo = response['photos'][0]
                            imgURL = photo['thumbnail']['src']
                            photographer = photo['photographer']
                            url = photo['link']
                        except Exception as e:
                            await printlog(f'Error getting image: {e}')
                            imgURL = None
                            photographer = 'no one'
                            url = 'https://planespotters.net'
                                                
                        #send in thread to reduce spam!
                        thread = await ctx.channel.create_thread(name=f"{userid.name}'s flight logs")
                            # Make the embed
                        if sublist[4] == 'Unknown':
                            embed = discord.Embed(title=f"Log {sublist[0]}")
                        else:
                            embed = discord.Embed(title=f"Log {sublist[0]}",colour=bus_colour)
                        embed.add_field(name=f'Flight', value=f"{sublist[7]} {sublist[4]}")
                        embed.add_field(name=f'Date', value="{}".format(sublist[3]))
                        embed.add_field(name=f'Trip Start', value="{}".format(sublist[5]))
                        embed.add_field(name=f'Trip End', value="{}".format(sublist[6]))
                        embed.add_field(name=f'Registration', value="{}".format(sublist[1]))
                        if len(sublist) > 8:
                            embed.add_field(name='Notes:', value=sublist[8].strip('"'))
                        embed.set_thumbnail(url=imgURL)
                        embed.add_field(name='Photo', value=f'Photo by {photographer} on [planespotters.net]({url})')
    
                        await logsthread.send(embed=embed)
                        time.sleep(2)  
            # for canberra tram:
            if mode == 'canberra-trams':
                if user == None:
                    userid = ctx.user
                else:
                    userid = user
                
                try:
                    try:
                        file = discord.File(f'utils/trainlogger/userdata/canberra-trams/{userid.id}.csv')
                    except:
                        file = discord.File(f'utils/trainlogger/userdata/canberra-trams/{userid.name}.csv')
                except FileNotFoundError:
                    if userid == ctx.user:
                        await ctx.response.send_message("You have no trips logged!",ephemeral=True)
                    else:
                        await ctx.response.send_message("This user has no trips logged!",ephemeral=True)
                    return
                await printlog(userid.name)
                data = universalReadLogs(userid.id, userid.name, mode='canberra-trams')
                if data == 'no data':
                    if userid == ctx.user:
                        await ctx.response.send_message("You have no trips logged!",ephemeral=True)
                    else:
                        await ctx.response.send_message("This user has no trips logged!",ephemeral=True)
                    return
            
                # create thread
                logsthread = await ctx.channel.create_thread(
                    name=f'{userid.name}\'s Canberra Light Rail Logs',
                    auto_archive_duration=60,
                    type=discord.ChannelType.public_thread
                )
                
                # send reponse message
                await ctx.response.send_message(f"Logs will be sent in <#{logsthread.id}>")
                await logsthread.send(f'# {userid.name}\'s CSV file', file=file)
                await logsthread.send(f' # {userid.name}\'s Canberra Light Rail Logs')
                formatted_data = ""
                for sublist in data:
                    if len(sublist) >= 7:  # Ensure the sublist has enough items                                         
                        #send in thread to reduce spam!
                            # Make the embed
                        embed = discord.Embed(title=f"Log {sublist[0]}",colour=sydney_tram_colour)
                        embed.add_field(name=f'Tram', value=f"{sublist[2]} {sublist[1]}")
                        embed.add_field(name=f'Date', value="{}".format(sublist[3]))
                        embed.add_field(name=f'Line', value="{}".format(sublist[4]))
                        embed.add_field(name=f'Trip Start', value="{}".format(sublist[5]))
                        embed.add_field(name=f'Trip End', value="{}".format(sublist[6]))
                        await logsthread.send(embed=embed)
                        time.sleep(2)   
    asyncio.create_task(sendLogs())

# log export
@trainlogs.command(name='export', description='Export your logs in various formats')
@app_commands.choices(format=[
    app_commands.Choice(name="CSV file (Excel)", value="csv"),
    app_commands.Choice(name="Markdown file", value="md"),
    app_commands.Choice(name="XML file", value="xml"),
    app_commands.Choice(name='HTML file',value='html')
])
@app_commands.choices(mode=[
    app_commands.Choice(name="Victorian Trains", value="train"),
    app_commands.Choice(name="Melbourne Trams", value="tram"),
    app_commands.Choice(name="Bus", value="bus"),
    app_commands.Choice(name="New South Wales Trains", value="sydney-trains"),
    app_commands.Choice(name="Sydney Light Rail", value="sydney-trams"),
    app_commands.Choice(name="Adelaide Trains", value="adelaide-trains"),
    app_commands.Choice(name="Adelaide Trams", value="adelaide-trams"),
    app_commands.Choice(name="Perth Trains", value="perth-trains"),
])
async def export(ctx, format:str, mode:str, hidemessage:bool=False):
    await maintenance_func(ctx)
    try:
        await logExport(ctx, format, mode, hidemessage)
    except FileNotFoundError as e:
        await ctx.response.send_message(f'You have no logs for that mode!')
    except Exception as e:
        await ctx.response.send_message(f"Error: `{e}`")
        
# log import
@trainlogs.command(name='import', description='Import your logs from a CSV file')
@app_commands.choices(mode=[
    app_commands.Choice(name="Victorian Trains", value="train"),
    app_commands.Choice(name="Melbourne Trams", value="tram"), 
    app_commands.Choice(name="Bus", value="bus"),
    app_commands.Choice(name="New South Wales Trains", value="sydney-trains"),
    app_commands.Choice(name="Sydney Light Rail", value="sydney-trams"),
    app_commands.Choice(name="Adelaide Trains", value="adelaide-trains"),
    app_commands.Choice(name="Adelaide Trams", value="adelaide-trams"),
    app_commands.Choice(name="Perth Trains", value="perth-trains"),
])
async def importlogs(ctx, mode:str, file:discord.Attachment):
    await ctx.response.defer(ephemeral=True)
    await maintenance_func(ctx)
    log_command(ctx.user.id, 'import-log')

    class ImportConfirmation(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=30)
            
        @discord.ui.button(label="Confirm Import", style=discord.ButtonStyle.danger)
        async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
            if interaction.user != ctx.user:
                await interaction.response.send_message("This isn't your command!", ephemeral=True)
                return
            
            try:
                # Download the file
                await file.save(f'temp/{file.filename}')
                if not file.filename.endswith('.csv'):
                    await interaction.response.edit_message(content="Invalid file format! Make sure you're uploading a CSV file.", view=None)
                    return
                
                # Validate CSV format
                with open(f'temp/{file.filename}', 'r') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if len(row) < 7:  # Basic validation - ensure minimum columns
                            await interaction.response.edit_message(content="Invalid CSV format! Make sure you're uploading a valid log file.", view=None)
                            return
                
                # Copy to user's log file
                if mode == 'train':
                    save_path = f'utils/trainlogger/userdata/{ctx.user.id}.csv'
                else:
                    save_path = f'utils/trainlogger/userdata/{mode}/{ctx.user.id}.csv'
                    
                shutil.copy(f'temp/{file.filename}', save_path)
                
                await interaction.response.edit_message(content=f"Successfully imported logs for {mode} from `{file.filename}`", view=None)
                
            except Exception as e:
                await interaction.response.edit_message(content=f"Error importing logs: {str(e)}", view=None)
            finally:
                # Cleanup temp file
                try:
                    os.remove(f'temp/{file.filename}') 
                except:
                    pass
                
        @discord.ui.button(label="Cancel", style=discord.ButtonStyle.gray)
        async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
            if interaction.user != ctx.user:
                await interaction.response.send_message("This isn't your import!", ephemeral=True)
                return
            
            await interaction.response.edit_message(content="Import cancelled.", view=None)

    # Create confirmation message with buttons
    view = ImportConfirmation()
    await ctx.edit_original_response(
        content=f"Are you sure you want to import logs for **{mode}** from `{file.filename}`?\n⚠️ This will overwrite any existing logs you have for this mode.", 
        view=view
    )

# train log stats
@trainlogs.command(name="stats", description="View stats for a logged user's trips.")
@app_commands.describe(stat='Type of stats to view', user='Who do you want to see the data of?', format='Diffrent ways and graphs for showing the data.', mode='Train or Tram logs?', year='Filter by year', global_stats='View global stats?')
@app_commands.choices(stat=[
    app_commands.Choice(name="Lines", value="lines"),
    app_commands.Choice(name="Stations", value="stations"),
    app_commands.Choice(name="Trips", value="pairs"),
    app_commands.Choice(name="Trip Length (Vic train only)", value="length"),
    app_commands.Choice(name='Distance over time (Vic train only)', value='distanceovertime'),
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

    app_commands.Choice(name="Victorian Trains", value="train"),
    app_commands.Choice(name="Melbourne Trams", value="tram"),
    app_commands.Choice(name="Bus", value="bus"),
    app_commands.Choice(name="New South Wales Trains", value="sydney-trains"),
    app_commands.Choice(name="Sydney Light Rail", value="sydney-trams"),
    app_commands.Choice(name="Adelaide Trains", value="adelaide-trains"),
    app_commands.Choice(name="Adelaide Trams", value="adelaide-trams"),
    app_commands.Choice(name="Perth Trains", value="perth-trains"),
    app_commands.Choice(name="Canberra Light Rail", value="canberra-trams"),
    app_commands.Choice(name="Flights", value="flights"),

])
async def statTop(ctx: discord.Interaction, stat: str, mode:str, format: str='l&g', global_stats:bool=False, user: discord.User = None, year:int=0):
    async def sendLogs():
        await ctx.response.defer()
        await maintenance_func(ctx)
        log_command(ctx.user.id, 'log-stats')
        statSearch = stat
        userid = user if user else ctx.user
        if user != None:
            if user != ctx.user and ctx.user.id not in admin_users:
                print(f'user {user} is not the same as {ctx.user}')
                await ctx.followup.send('You can only view your own stats!')
                return
        if global_stats:
            if stat == 'distanceovertime':
                data = distanceOverTime(userid.id, year, True)
            data = globalTopStats(statSearch)
        else:
            try:
                if stat == 'operators':
                    data = topOperators(userid.id)
                elif stat == 'length':
                    data = getLongestTrips(userid.id)  
                elif stat == 'distanceovertime':
                    data = distanceOverTime(userid.id, year)
                elif mode == 'all':
                    data = allTopStats(userid.id, statSearch, year)
                else:
                    data = topStats(userid.id, statSearch, year, mode)
                
            except:
                await ctx.followup.send('You have no logged trips!')
        count = 1
        message = ''
        
        # top operators thing:
        if stat == 'operators':
            try:
                pieChart(data, f'Top Operators ― {userid}', ctx.user.name)
                await ctx.followup.send(message, file=discord.File(f'temp/Graph{ctx.user.name}.png'))
            except:
                await ctx.followup.send('User has no logs!')  
                
        # length
        if stat == 'length':
            try:
                # create thread
                try:
                    logsthread = await ctx.channel.create_thread(
                        name=f"{userid.name}'s longest trips in Victoria",
                        auto_archive_duration=60,
                        type=discord.ChannelType.public_thread
                    )
                except Exception as e:
                    await ctx.followup.send(f"Cannot create thread! Ensure the bot has permission to create threads and that you aren't running this in another thread or DM.\n Error: `{e}`")

                # send reponse message
                pfp = userid.avatar.url
                embed=discord.Embed(title=f"{userid.name}'s longest trips in Victoria", colour=metro_colour)
                embed.set_author(name=userid.name, url='https://victorianrailphotos.com', icon_url=pfp)
                embed.add_field(name='Click here to view your data:', value=f'<#{logsthread.id}>')
                await ctx.followup.send(embed=embed)
                
                lines = data.splitlines()
                chunks = []
                current_chunk = ""
                await logsthread.send('Here are your longest trips in Victoria:')

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
                    await logsthread.send(chunk)
                    time.sleep(0.7)
                
            except Exception as e:
                await ctx.followup.send(f"Error: `{e}`")
                await log_channel.send(f'Error: ```{e}```\n with trip length run ran by {ctx.user.mention}\n<@{USER_ID}>')
            finally:
                return
        
        # distance over time
        if stat == 'distanceovertime':
            distanceChart(data, userid)
            await ctx.followup.send(file=discord.File(f'temp/Graph{ctx.user.id}.png'))
                
        # make temp csv
        csv_filename = f'temp/top{stat.title()}.{userid}-t{time.time()}.csv'
        with open(csv_filename, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            for item in data:
                station, times = item.split(': ')
                writer.writerow([station, times.split()[0]])
        
        if format == 'csv':
            try:
                await ctx.followup.send("Here is your file:", file=discord.File(csv_filename))
            except:
                await ctx.followup.send('You have no logs!')
            
        elif format == 'l&g':
            # create thread
            try:
                logsthread = await ctx.channel.create_thread(
                    name=stat.title(),
                    auto_archive_duration=60,
                    type=discord.ChannelType.public_thread
                )
            except Exception as e:
                await ctx.followup.send(f"Cannot create thread! Ensure the bot has permission to create threads and that you aren't running this in another thread or DM.\n Error: `{e}`")
        
            # gen the graph
            try:
                if global_stats:
                    barChart(csv_filename, stat.title(), f'Top {stat.title()} ― Global', ctx.user.name, True)
                else:
                    barChart(csv_filename, stat.title(), f'Top {stat.title()} in {year} ― {userid}' if year !=0 else f'Top {stat.title()} ― {userid}', ctx.user.name, True)
            except Exception as e:
                await ctx.followup.send(f"Error generating graph: `{e}`")
                return
            # send reponse message
            pfp = userid.avatar.url
            embed=discord.Embed(title=stat.title(), colour=metro_colour)
            embed.set_author(name=userid.name, url='https://victorianrailphotos.com', icon_url=pfp)
            embed.add_field(name='Click here to view your full stats:', value=f'<#{logsthread.id}>')
            embed.set_image(url='attachment://graph.png')
            await ctx.followup.send(embed=embed, file=discord.File(f'temp/Graph{ctx.user.name}.png', filename="graph.png"))
            for item in data:
                station, times = item.split(': ')
                message += f'{count}. **{station}:** `{times}`\n'
                count += 1
                if len(message) > 1900:
                    await logsthread.send(message)
                    message = ''
            try:
                if global_stats:
                    barChart(csv_filename, stat.title(), f'Top {stat.title()} ― Global', ctx.user.name, False)
                else:
                    barChart(csv_filename, stat.title(), f'Top {stat.title()} in {year} ― {userid}' if year !=0 else f'Top {stat.title()} ― {userid}', ctx.user.name, False)
                await logsthread.send(message, file=discord.File(f'temp/Graph{ctx.user.name}.png'))
            except FileNotFoundError:
                await logsthread.send(f'User has no logs! {e}')
            except Exception as e:
                await ctx.followup.send(f"Error: `{e}`")
                
        elif format == 'pie':
            try:
                if global_stats:
                    pieChart(csv_filename, f'Top {stat.title()} ― {userid}', ctx.user.name)
                else:
                    pieChart(csv_filename, f'Top {stat.title()} ― Global', ctx.user.name)

                await ctx.followup.send(file=discord.File(f'temp/Graph{ctx.user.name}.png'))
            except FileNotFoundError:
                await ctx.followup.send('You have no logs!')
            except Exception as e:
                await ctx.followup.send(f"Error: `{e}`")
                
        elif format == 'daily':
            if stat != 'dates':
                await ctx.followup.send('Daily chart can only be used with the stat set to Top Dates')
            try:
                dayChart(csv_filename, ctx.user.name)
                await ctx.followup.send(file=discord.File(f'temp/Graph{ctx.user.name}.png'))
            except FileNotFoundError:
                ctx.followup.send('User has no logs!')
            except Exception as e:
                await ctx.followup.send(f"Error: `{e}`")
    await sendLogs()

@stats.command(name='termini', description='View which line termini you have been to')
async def termini(ctx):
    await ctx.response.defer()
    await maintenance_func(ctx)
    log_command(ctx.user.id, 'log-termini')
    try:
        data =terminiList(ctx.user.id)
    except:
        data = 'No logs found'
    
    
    if len(data) <= 2000:
        embed = discord.Embed(title=f'Line termini {ctx.user.name} has visited', colour=metro_colour, description=data)
        await ctx.edit_original_response(embed=embed)
        return
    else:
        await ctx.response.send_message(f"Termini you have visited:")
        split_strings = []
        start = 0
        
        while start < len(data):
            if start + 2000 < len(data):
                split_index = data.rfind('\n', start, start + 2000)
                if split_index == -1:
                    split_index = start + 2000
            else:
                split_index = len(data)
            
            split_strings.append(data[start:split_index])
            start = split_index + 1
            
        for item in split_strings:
            await ctx.channel.send(item)

@completion.command(name='sets', description='View which sets you have been on')
@app_commands.choices(train=[
    app_commands.Choice(name="Summary", value="summary"),
    app_commands.Choice(name="X'Trapolis 100", value="X'Trapolis 100"),
    app_commands.Choice(name="X'Trapolis 2.0", value="X'Trapolis 2.0"),
    app_commands.Choice(name="Comeng", value="Comeng"),
    app_commands.Choice(name="Siemens Nexas", value="Siemens Nexas"),
    app_commands.Choice(name="HCMT", value="HCMT"),
    app_commands.Choice(name='VLocity', value='VLocity'),
    app_commands.Choice(name='Sprinter', value='Sprinter'),
    app_commands.Choice(name='N Class', value='N Class'),
])
async def sets(ctx, train:str):
    await maintenance_func(ctx)
    userid = ctx.user
    trainTypes = ["X'Trapolis 100", "X'Trapolis 2.0", "Comeng", 'Siemens Nexas', 'HCMT', 'VLocity', 'Sprinter', 'N Class']
    await ctx.response.defer()
    log_command(ctx.user.id, 'log-sets')
    
    # summary:
    if train == 'summary':
        embed = discord.Embed(title=f'{userid.name}\'s set completion summary', colour=metro_colour)
        for train in trainTypes:
            try:
                data = setlist(ctx.user.id, train, summary=True)
                embed.add_field(name=f'{getTrainTypeEmoji(train)} {train}', value=data, inline=True)
            except:
                await ctx.edit_original_response(content='No logs found!')
                return
        embed.set_footer(text='Choose a train type to see which sets you have been on.')
        await ctx.edit_original_response(embed=embed)
        return
    # specific train
    try:
        data = setlist(ctx.user.id, train)
    except:
        await ctx.edit_original_response(content='No logs found!')
    
    # create thread
    try:
        logsthread = await ctx.channel.create_thread(
            name=f'{train} sets {userid.name} has been on',
            auto_archive_duration=60,
            type=discord.ChannelType.public_thread
        )
    except Exception as e:
        await ctx.response.send_message(f"Cannot create thread! Ensure the bot has permission to create threads and that you aren't running this in another thread or DM.\n Error: `{e}`")
        
    # send reponse message
    pfp = userid.avatar.url
    embed=discord.Embed(title=f'{train} sets {userid.name} has been on', colour=metro_colour)
    embed.set_author(name=userid.name, url='https://victorianrailphotos.com', icon_url=pfp)
    embed.add_field(name='Click here to view your data:', value=f'<#{logsthread.id}>')
    await ctx.edit_original_response(embed=embed)

    if len(data) <= 2000:
        await logsthread.send(data)
    else:
        await logsthread.send(f"{train} sets you have been on:")
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
            start = split_index + 1
            
        for item in split_strings:
            await logsthread.send(item)

@completion.command(name='lines', description='View which stations on lines you have been on')
@app_commands.choices(line=[
    app_commands.Choice(name="Summary", value="Summary"),
    app_commands.Choice(name="Hurstbridge", value="Hurstbridge"),
    app_commands.Choice(name="Mernda",value="Mernda"),
    app_commands.Choice(name="Craigieburn",value="Craigieburn"),
    app_commands.Choice(name="Sunbury",value="Sunbury"),
    app_commands.Choice(name="Upfield",value="Upfield"),
    app_commands.Choice(name="Cranbourne",value="Cranbourne"),
    app_commands.Choice(name="Pakenham",value="Pakenham"),
    app_commands.Choice(name="Frankston",value="Frankston"),
    app_commands.Choice(name="Stony Point",value="Stony Point"),
    app_commands.Choice(name="Werribee",value="Werribee"),
    app_commands.Choice(name="Williamstown",value="Williamstown"),
    app_commands.Choice(name="Sandringham",value="Sandringham"),
    app_commands.Choice(name="Alamein",value="Alamein"),
    app_commands.Choice(name="Belgrave",value="Belgrave"),
    app_commands.Choice(name="Glen Waverley",value="Glen Waverley"),
    app_commands.Choice(name="Lilydale",value="Lilydale"),
    app_commands.Choice(name="Flemington Racecourse",value="Flemington Racecourse"),
    app_commands.Choice(name="Metro Tunnel",value="Metro Tunnel"),
    app_commands.Choice(name="City Loop",value="City Loop")
])
async def sets(ctx, line:str):
    await maintenance_func(ctx)
    userid = ctx.user
    trainLines = ["Hurstbridge", "Mernda", "Craigieburn", "Sunbury", "Upfield", "Cranbourne", "Pakenham", "Frankston", "Stony Point", "Werribee", "Williamstown", "Sandringham", "Alamein", "Lilydale", "Glen Waverley", "Belgrave", "Metro Tunnel", "City Loop", "Flemington Racecourse", "All"]
    await ctx.response.defer()
    log_command(ctx.user.id, 'completion-lines')

    if line == 'Summary':
        embed = discord.Embed(title=f'{userid.name}\'s line completion summary', colour=metro_colour)
        for line in trainLines:
            try:
                data = completionList(ctx.user.id, line, summary=True)
                embed.add_field(name=f'{line}', value=data, inline=True)
            except Exception as e:
                await ctx.edit_original_response(content=f'No logs found! {e}')
                return
        embed.set_footer(text="Choose a line to see which stations you've been to")
        await ctx.edit_original_response(embed=embed)
        return
    
    try:
        data = completionList(ctx.user.id, line)
    except Exception as e:
        await ctx.edit_original_response(content=f'No logs found! {e}')

    try:
        logsthread = await ctx.channel.create_thread(
            name=f'{line} stations {userid.name} has been to',
            auto_archive_duration=60,
            type=discord.ChannelType.public_thread
        )
    except Exception as e:
        await ctx.response.send_message(f"Cannot create thread! Ensure the bot has permission to create threads and that you aren't running this in another thread or DM.\n Error: `{e}`")

    pfp = userid.avatar.url
    embed=discord.Embed(title=f'{line} stations {userid.name} has been to', colour=metro_colour)
    embed.set_author(name=userid.name, url='https://victorianrailphotos.com', icon_url=pfp)
    embed.add_field(name='Click here to view your data:', value=f'<#{logsthread.id}>')
    await ctx.edit_original_response(embed=embed)

    if len(data) <= 2000:
        await logsthread.send(data)
    else:
        await logsthread.send(f"{line} stations you have been to:")
        split_strings = []
        start = 0

        while start < len(data):
            if start + 2000 < len(data):
                split_index = data.rfind('\n', start, start + 2000)
                if split_index == -1:
                    split_index = start + 2000
            else:
                split_index = len(data)

            split_strings.append(data[start:split_index])
            start = split_index + 1
        
        for item in split_strings:
            await logsthread.send(item)

@completion.command(name='stations', description='View which you have visited')
@app_commands.choices(state=[
    app_commands.Choice(name="Victoria", value="Victorian"),
    app_commands.Choice(name="New South Wales", value="New South Wales"),
    app_commands.Choice(name="South Australia", value="South Australian"),
    app_commands.Choice(name="Western Australia", value="Western Australian"),
])
async def sets(ctx, state:str):
    await maintenance_func(ctx)
    userid = ctx.user
    await ctx.response.defer()
    log_command(ctx.user.id, 'log-stations')
    try:
        data =stationlist(ctx.user.id, state)
    except Exception as e:
        await ctx.edit_original_response(content='No logs found')
        await printlog(f'ERROR: {e}')
        
    # create thread
    try:
        logsthread = await ctx.channel.create_thread(
            name=f'{state} stations {userid.name} has been to',
            auto_archive_duration=60,
            type=discord.ChannelType.public_thread
        )
    except Exception as e:
        await ctx.response.send_message(f"Cannot create thread! Ensure the bot has permission to create threads and that you aren't running this in another thread or DM.\n Error: `{e}`")
        
    # send reponse message
    pfp = userid.avatar.url
    embed=discord.Embed(title=f'{state} stations {userid.name} has been to', colour=metro_colour)
    embed.set_author(name=userid.name, url='https://victorianrailphotos.com', icon_url=pfp)
    embed.add_field(name='Click here to view your data:', value=f'<#{logsthread.id}>')
    await ctx.edit_original_response(embed=embed)
    
    if len(data) <= 2000:
        await logsthread.send(data)
    else:
        await logsthread.send(f"{state} stations you have been to:")
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
            await logsthread.send(item)

@bot.tree.command(name='submit-photo', description="This command has been retired.")
@app_commands.choices(photofor=[
    app_commands.Choice(name="Railway Photo & Bot train search", value="website"),
    app_commands.Choice(name="Bot/Website Station Photo Guessing Game", value="guesser"),
    
])
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def submit(ctx: discord.Interaction, photo: discord.Attachment, date: str, location: str, photofor:str, number: str=''):
    await ctx.response.defer(ephemeral=True)
    await maintenance_func(ctx)
    log_command(ctx.user.id, 'submit-photo-retired')
    async def submitPhoto():
        await ctx.followup.send('This command has been retired. Please submit photos via the VictorianRailPhotos website: https://victorianrailphotos.com/upload')
    await submitPhoto()
    
@bot.tree.command(name='alias', description='Set or update an alias for your photos to be displayed on VictorianRailPhotos')
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def alias(ctx: discord.Interaction, name: str):
    await ctx.response.defer()
    await maintenance_func(ctx)
    worked = setWebAlias(ctx.user.id, name)
    if worked:
        await ctx.followup.send(f'Set alias to `{name}`')
    else:
        await ctx.followup.send('There was an error changing your alias, please try again later.')
    

@bot.tree.command(name='accept', description="ADMIN ONLY Accept a photo submission from the queue")
@app_commands.choices(mode=[
    app_commands.Choice(name='train', value='train'),
    app_commands.Choice(name='tram', value='tram'),
    app_commands.Choice(name='bus', value='bus'),
])

async def accept(ctx, id: int, mode:str, traintype:str, featured:bool=False, note:str=None, number:str=None, location:str=None, date:str=None, reason:str=None):
    await ctx.response.defer()
    await maintenance_func(ctx)
    if ctx.user.id in admin_users:            
        try:
            userid = await getUserID(id)
        except TypeError:
            await ctx.followup.send('i cant find that id')
            return

        # see if thers an alias
        conn = sqlite3.connect('userdata/aliases.db')
        cursor = conn.cursor()
        # If userid is an email, skip alias lookup
        if isinstance(userid, str) and '@' in userid:
            userName = userid[:-12]
        else:
            cursor.execute('SELECT alias FROM aliases WHERE userid = ?', (int(userid),))
            result = cursor.fetchone()
            if result:
                userName = result[0]
            else:
                userName = bot.get_user(int(userid)).name
        conn.close()

        apiResponse = await acceptPhoto(id, userName, traintype, featured, note, number, location, date, mode.lower())

        print(apiResponse)
        if 'error' in apiResponse.lower():
            await ctx.followup.send(apiResponse)
            return
        
        user_id, msgid = await removeSubmission(id)

        # If user_id is an email, don't send DM
        if isinstance(user_id, str) and '@' in user_id:
            m = f'Did not send a message as that user is not from Discord.'
        else:
            user = bot.get_user(int(user_id))
            m = f'sent message confirming to user ID: {user.mention}'
            try:
                if reason is None:
                    await user.send(f"Your photo with id {id} has been accepted and removed from the queue. You can see it shortly in the bot and on the website/game.\nView photo in the TrackPulse server: https://discord.com/channels/1214139268725870602/1322889624250486848/{msgid}")
                else:
                    await user.send(f"Your photo with id {id} has been accepted and removed from the queue. You can see it shortly in the bot and on the website/game.\nView photo in the TrackPulse server: https://discord.com/channels/1214139268725870602/1322889624250486848/{msgid}. Note that {reason}.")
            except:
                m = (f"Could not send message to user ID: {user.id}. They may have DMs disabled.")
        await ctx.followup.send(f"Submission with queue number {id} has been accepted and removed from the queue. {m}")
    else:
        await ctx.followup.send("You do not have permission to use this command.")

@bot.tree.command(name='accept-guesser', description="ADMIN ONLY Accept a photo submission for the station photo guessing game")
@app_commands.describe(station="only put in the name of the station, not 'station' or anything else")
@app_commands.choices(mode=[
    app_commands.Choice(name="Normal", value="guesser"),
    app_commands.Choice(name="Ultra hard", value="ultrahard"),
])
    
async def accept_guesser(ctx, id: int, station:str, difficulty:str, mode:str='guesser'):
    if ctx.user.id in admin_users:
        await ctx.response.defer()
        try:
            try:
                userid = await getUserID(id)
                userid = bot.get_user(int(userid))
            except TypeError:
                raise Exception('Could not find user ID for that submission')
            await acceptGuesserPhoto(id, station, difficulty, mode, userid.name)
        except Exception as e:
            await ctx.followup.send(f'Couldnt add guesser image: `{e}`')
            return
        await removeSubmission(id) # remove from queue
        await ctx.followup.send(f"Submission with queue number {id} has been accepted and added to the guessing game.")
    else:
        await ctx.response.send_message("You do not have permission to use this command.")
        return
    await maintenance_func(ctx)
    
@bot.command(name='reject', description="Reject a photo submission from the queue")
async def reject(ctx, id: int, *, reason: str):
    if ctx.author.id in admin_users:
        userid, msgid = await removeSubmission(id)
        if '@' in userid:
            await ctx.send(f'Submission with queue number `{id}` has been rejected and removed from the queue. Did not send a message as that user is not from Discord.')
            return
        else:
            user = bot.get_user(int(userid))
            
            m = f'Sent message confirming to user ID: {user.mention}'
            try:
                await user.send(f"Your photo with id `{id}` has been rejected and removed from the queue.\nReason: {reason}")
            except:
                m = (f"Could not send message to user ID: {userid}. They may have DMs disabled.")
            await ctx.send(f"Submission with queue number `{id}` has been rejected and removed from the queue. {m}")
    await maintenance_func(ctx)
    
@bot.tree.command(name='queue', description="View the current photo submission queue")
async def queue(ctx: discord.Interaction):
    await ctx.response.defer()
    await maintenance_func(ctx)
    if ctx.user.id in admin_users:
        data = await returnQueue()
        embed = discord.Embed(title='Photo Submission Queue (top 25)')
    else:
        data = await returnQueue(ctx.user.id)
        embed = discord.Embed(title='Your photo Submission Queue (top 25)', description=f'Total items: {len(data)}')
        
    count = 0
    for item in data:
        userMention = bot.get_user(int(item[3]))
        embed.add_field(name=item[1], value=f'Photo ID: **{item[0]}**, Train {item[7]}, Location: {item[5]}\nSubmitted by {userMention.mention}', inline=False)
        count += 1
        if count == 25:
            break
    await ctx.edit_original_response(embed=embed)
    
@stats.command(name='profile', description="Shows a users trip log stats, and leaderboard wins")    
async def profile(ctx, user: discord.User = None):
    await maintenance_func(ctx)
    log_command(ctx.user.id, 'view-profile')
    try:
        await ctx.response.defer()
        async def profiles():
            if user == None:
                username = ctx.user.name
                userid =ctx.user.id
                pfp = ctx.user.avatar.url
            else:
                username = user.name
                userid =user.id
                pfp = user.avatar.url

            pages = []
            current_page = 0

            # Victoria Trains and Trams
            embed1 = discord.Embed(title=f"Profile | Victoria - Page 1/5")
            embed1.set_author(name=username, url='https://xm9g.net', icon_url=pfp)
            try:
                # Victoria Trains
                lines = topStats(userid, 'lines', 0, 'train')
                stations = topStats(userid, 'stations', 0, 'train')
                sets = topStats(userid, 'sets', 0, 'train')
                trains = topStats(userid, 'types', 0, 'train')
                dates = topStats(userid, 'dates', 0, 'train')
                trips = topStats(userid, 'pairs', 0, 'train')

                #other stats stuff:
                eDate =lowestDate(userid, 'train')
                LeDate =highestDate(userid, 'train')
                joined = convert_iso_to_unix_time(f"{eDate}T00:00:00Z") 
                last = convert_iso_to_unix_time(f"{LeDate}T00:00:00Z")
                embed1.add_field(
        name='<:train:1241164967789727744><:vline:1241165814258729092> Train Log Stats:',
        value=f'**Top Line:** {lines[1] if len(lines) > 1 and lines[0].startswith("Unknown") else lines[0]}\n'
            f'**Top Station:** {stations[1] if len(stations) > 1 and stations[0].startswith("Unknown") else stations[0]}\n'
            f'**Top Train:** {trains[1] if len(trains) > 1 and trains[0].startswith("Unknown") else trains[0]}\n'
            f'**Top Set:** {sets[1] if len(sets) > 1 and sets[0].startswith("Unknown") else sets[0]}\n'
            f'**Top Date:** {dates[1] if len(dates) > 1 and dates[0].startswith("Unknown") else dates[0]}\n'
            f'**Top Trip:** {trips[1] if len(trips) > 1 and trips[0].startswith("Unknown") else trips[0]}\n\n'
            f'User started logging {joined}\n'
            f'Last log {last}\n'
            f'**Longest Streak:** `{streak(userid, "train")[0]}` (current: `{streak(userid, "train")[1]}`)\n'
            f'**Total logs:** `{logAmounts(userid, "train")}`\n'
            f'**Stations visited:** `{stationPercent(userid)}`\n'
            f'**Lines visited:** `{linePercent(userid)}`\n'
            f'**Distance:** `{round(getTotalTravelDistance(userid))}km`'
    )       
            except FileNotFoundError:
                embed1.add_field(name="<:train:1241164967789727744><:vline:1241165814258729092> Train Log Stats", value=f'{username} has no logged trips!')

            # Victoria Trams
            try:
                lines = topStats(userid, 'lines', 0, 'tram')
                stations = topStats(userid, 'stations', 0, 'tram')
                sets = topStats(userid, 'sets', 0, 'tram')
                trains = topStats(userid, 'types', 0, 'tram')
                dates = topStats(userid, 'dates', 0, 'tram')
                trips = topStats(userid, 'pairs', 0, 'tram')

                #other stats stuff:
                eDate =lowestDate(userid, 'tram')
                LeDate =highestDate(userid, 'tram')
                joined = convert_iso_to_unix_time(f"{eDate}T00:00:00Z") 
                last = convert_iso_to_unix_time(f"{LeDate}T00:00:00Z")
                embed1.add_field(
        name='<:tram:1241165701390012476> Tram Log Stats:',
        value=f'**Top Route:** {lines[1] if len(lines) > 1 and lines[0].startswith("Unknown") else lines[0]}\n'
            f'**Top Stop:** {stations[1] if len(stations) > 1 and stations[0].startswith("Unknown") else stations[0]}\n'
            f'**Top Class:** {trains[1] if len(trains) > 1 and trains[0].startswith("Unknown") else trains[0]}\n'
            f'**Top Tram Number:** {sets[1] if len(sets) > 1 and sets[0].startswith("Unknown") else sets[0]}\n'
            f'**Top Date:** {dates[1] if len(dates) > 1 and dates[0].startswith("Unknown") else dates[0]}\n\n'
            f'**Longest Streak:** `{streak(userid, "tram")[0]}` (current: `{streak(userid, "tram")[1]}`)\n'
            f'User started logging {joined}\n'
            f'Last log {last}\n'
            f'Total logs: {logAmounts(userid, "tram")}'
    )
            except FileNotFoundError:
                embed1.add_field(name="<:tram:1241165701390012476> Tram Log Stats", value=f'{username} has no logged trips!')
            pages.append(embed1)

            # NSW Trains and Light Rail
            embed2 = discord.Embed(title=f"Profile | NSW - Page 2/5")
            embed2.set_author(name=username, url='https://xm9g.net', icon_url=pfp)
            # NSW Trains
            try:
                lines = topStats(userid, 'lines', 0, 'sydney-trains')
                stations = topStats(userid, 'stations', 0, 'sydney-trains')
                sets = topStats(userid, 'sets', 0, 'sydney-trains')
                trains = topStats(userid, 'types', 0, 'sydney-trains')
                dates = topStats(userid, 'dates', 0, 'sydney-trains')
                trips = topStats(userid, 'pairs', 0, 'sydney-trains')
                
                #other stats stuff:
                eDate =lowestDate(userid, 'sydney-trains')
                LeDate =highestDate(userid, 'sydney-trains')
                joined = convert_iso_to_unix_time(f"{eDate}T00:00:00Z") 
                last = convert_iso_to_unix_time(f"{LeDate}T00:00:00Z")
                embed2.add_field(
        name='<:NSWTrains:1255084911103184906><:NSWMetro:1255084902748000299> Train Log Stats:',
        value=f'**Top Line:** {lines[1] if len(lines) > 1 and lines[0].startswith("Unknown") else lines[0]}\n'
            f'**Top Station:** {stations[1] if len(stations) > 1 and stations[0].startswith("Unknown") else stations[0]}\n'
            f'**Top Type:** {trains[1] if len(trains) > 1 and trains[0].startswith("Unknown") else trains[0]}\n'
            f'**Top Train Number:** {sets[1] if len(sets) > 1 and sets[0].startswith("Unknown") else sets[0]}\n'
            f'**Top Trip:** {trips[1] if len(trips) > 1 and trips[0].startswith("Unknown") else trips[0]}\n'
            f'**Top Date:** {dates[1] if len(dates) > 1 and dates[0].startswith("Unknown") else dates[0]}\n\n'
            f'**Longest Streak:** `{streak(userid, "sydney-trains")[0]}` (current: `{streak(userid, "sydney-trains")[1]}`)\n'
            f'User started logging {joined}\n'
            f'Last log {last}\n'
            f'Total logs: {logAmounts(userid, "sydney-trains")}'
    )
            except FileNotFoundError:
                embed2.add_field(name="<:NSWTrains:1255084911103184906><:NSWMetro:1255084902748000299> Train Log Stats", value=f'{username} has no logged trips in NSW!')

            # NSW Light Rail
            try:
                lines = topStats(userid, 'lines', 0, 'sydney-trams')
                stations = topStats(userid, 'stations', 0, 'sydney-trams')
                sets = topStats(userid, 'sets', 0, 'sydney-trams')
                trains = topStats(userid, 'types', 0, 'sydney-trams')
                dates = topStats(userid, 'dates', 0, 'sydney-trams')
                trips = topStats(userid, 'pairs', 0, 'sydney-trams')
                
                #other stats stuff:
                eDate =lowestDate(userid, 'sydney-trams')
                LeDate =highestDate(userid, 'sydney-trams')
                joined = convert_iso_to_unix_time(f"{eDate}T00:00:00Z") 
                last = convert_iso_to_unix_time(f"{LeDate}T00:00:00Z")
                embed2.add_field(
        name='<:NSWLightRail:1255084906053369856> Light Rail Log Stats:',
        value=f'**Top Line:** {lines[1] if len(lines) > 1 and lines[0].startswith("Unknown") else lines[0]}\n'
            f'**Top Stop:** {stations[1] if len(stations) > 1 and stations[0].startswith("Unknown") else stations[0]}\n'
            f'**Top Type:** {trains[1] if len(trains) > 1 and trains[0].startswith("Unknown") else trains[0]}\n'
            f'**Top Tram Number:** {sets[1] if len(sets) > 1 and sets[0].startswith("Unknown") else sets[0]}\n'
            f'**Top Trip:** {trips[1] if len(trips) > 1 and trips[0].startswith("Unknown") else trips[0]}\n'
            f'**Top Date:** {dates[1] if len(dates) > 1 and dates[0].startswith("Unknown") else dates[0]}\n\n'
            f'**Longest Streak:** `{streak(userid, "sydney-trams")[0]}` (current: `{streak(userid, "sydney-trams")[1]}`)\n'
            f'User started logging {joined}\n'
            f'Last log {last}\n'
            f'Total logs: {logAmounts(userid, "sydney-trams")}'
    )
            except FileNotFoundError:
                embed2.add_field(name="<:NSWLightRail:1255084906053369856> Light Rail Log Stats", value=f'{username} has no logged trips in NSW!')
            pages.append(embed2)

            # Adelaide Trains and Trams
            embed3 = discord.Embed(title=f"Profile | Adelaide - Page 3/5")
            embed3.set_author(name=username, url='https://xm9g.net', icon_url=pfp)
            # Adelaide Trains
            try:
                lines = topStats(userid, 'lines', 0, 'adelaide-trains')
                stations = topStats(userid, 'stations', 0, 'adelaide-trains')
                sets = topStats(userid, 'sets', 0, 'adelaide-trains')
                trains = topStats(userid, 'types', 0, 'adelaide-trains')
                dates = topStats(userid, 'dates', 0, 'adelaide-trains')
                trips = topStats(userid, 'pairs', 0, 'adelaide-trains')

                #other stats stuff:
                eDate =lowestDate(userid, 'adelaide-trains')
                LeDate =highestDate(userid, 'adelaide-trains')
                joined = convert_iso_to_unix_time(f"{eDate}T00:00:00Z") 
                last = convert_iso_to_unix_time(f"{LeDate}T00:00:00Z")
                embed3.add_field(
        name='<:Adelaide_train_:1300008231510347807><:journeybeyond:1300021503093510155> Adelaide Train Log Stats:',
        value=f'**Top Line:** {lines[1] if len(lines) > 1 and lines[0].startswith("Unknown") else lines[0]}\n'
            f'**Top Station:** {stations[1] if len(stations) > 1 and stations[0].startswith("Unknown") else stations[0]}\n'
            f'**Top Type:** {trains[1] if len(trains) > 1 and trains[0].startswith("Unknown") else trains[0]}\n'
            f'**Top Number:** {sets[1] if len(sets) > 1 and sets[0].startswith("Unknown") else sets[0]}\n'
            f'**Top Trip:** {trips[1] if len(trips) > 1 and trips[0].startswith("Unknown") else trips[0]}\n'
            f'**Top Date:** {dates[1] if len(dates) > 1 and dates[0].startswith("Unknown") else dates[0]}\n\n'
            f'**Longest Streak:** `{streak(userid, "adelaide-trains")[0]}` (current: `{streak(userid, "adelaide-trains")[1]}`)\n'
            f'User started logging {joined}\n'
            f'Last log {last}\n'
            f'Total logs: {logAmounts(userid, "adelaide-trains")}'
    )
            except FileNotFoundError:
                embed3.add_field(name="<:Adelaide_train_:1300008231510347807><:journeybeyond:1300021503093510155> Adelaide Train Log Stats:", value=f'{username} has no logged trips in Adelaide!')

            # Adelaide Trams
            try:
                lines = topStats(userid, 'lines', 0, 'adelaide-trams')
                stations = topStats(userid, 'stations', 0, 'adelaide-trams')
                sets = topStats(userid, 'sets', 0, 'adelaide-trams')
                trains = topStats(userid, 'types', 0, 'adelaide-trams')
                dates = topStats(userid, 'dates', 0, 'adelaide-trams')
                trips = topStats(userid, 'pairs', 0, 'adelaide-trams')
                
                #other stats stuff:
                eDate =lowestDate(userid, 'adelaide-trams')
                LeDate =highestDate(userid, 'adelaide-trams')
                joined = convert_iso_to_unix_time(f"{eDate}T00:00:00Z") 
                last = convert_iso_to_unix_time(f"{LeDate}T00:00:00Z")
                embed3.add_field(
        name='<:adelaidetram:1357271311021379644> Adelaide Tram Log Stats:',
        value=f'**Top Route:** {lines[1] if len(lines) > 1 and lines[0].startswith("Unknown") else lines[0]}\n'
            f'**Top Stop:** {stations[1] if len(stations) > 1 and stations[0].startswith("Unknown") else stations[0]}\n'
            f'**Top Type:** {trains[1] if len(trains) > 1 and trains[0].startswith("Unknown") else trains[0]}\n'
            f'**Top Tram Number:** {sets[1] if len(sets) > 1 and sets[0].startswith("Unknown") else sets[0]}\n'
            f'**Top Trip:** {trips[1] if len(trips) > 1 and trips[0].startswith("Unknown") else trips[0]}\n'
            f'**Top Date:** {dates[1] if len(dates) > 1 and dates[0].startswith("Unknown") else dates[0]}\n\n'
            f'**Longest Streak:** `{streak(userid, "adelaide-trams")[0]}` (current: `{streak(userid, "adelaide-trams")[1]}`)\n'
            f'User started logging {joined}\n'
            f'Last log {last}\n'
            f'Total logs: {logAmounts(userid, "adelaide-trams")}'
    )
            except FileNotFoundError:
                embed3.add_field(name="<:adelaidetram:1357271311021379644> Adelaide Tram Log Stats", value=f'{username} has no logged trips in Adelaide!')
            pages.append(embed3)

            # Perth, Canberra, Buses, Flights20
            embed4 = discord.Embed(title=f"Profile | Other States & Modes - Page 4/5")
            embed4.set_author(name=username, url='https://xm9g.net', icon_url=pfp)
            # Perth Trains
            try:
                lines = topStats(userid, 'lines', 0, 'perth-trains')
                stations = topStats(userid, 'stations', 0, 'perth-trains')
                sets = topStats(userid, 'sets', 0, 'perth-trains')
                trains = topStats(userid, 'types', 0, 'perth-trains')
                dates = topStats(userid, 'dates', 0, 'perth-trains')
                trips = topStats(userid, 'pairs', 0, 'perth-trains')

                #other stats stuff:
                eDate =lowestDate(userid, 'perth-trains')
                LeDate =highestDate(userid, 'perth-trains')
                joined = convert_iso_to_unix_time(f"{eDate}T00:00:00Z") 
                last = convert_iso_to_unix_time(f"{LeDate}T00:00:00Z")
                embed4.add_field(
        name='<:transperthtrain:1335396329798631477><:TransWA:1335397360255373392> Perth Train Log Stats:',
        value=f'**Top Line:** {lines[1] if len(lines) > 1 and lines[0].startswith("Unknown") else lines[0]}\n'
            f'**Top Station:** {stations[1] if len(stations) > 1 and stations[0].startswith("Unknown") else stations[0]}\n'
            f'**Top Type:** {trains[1] if len(trains) > 1 and trains[0].startswith("Unknown") else trains[0]}\n'
            f'**Top Number:** {sets[1] if len(sets) > 1 and sets[0].startswith("Unknown") else sets[0]}\n'
            f'**Top Trip:** {trips[1] if len(trips) > 1 and trips[0].startswith("Unknown") else trips[0]}\n'
            f'**Top Date:** {dates[1] if len(dates) > 1 and dates[0].startswith("Unknown") else dates[0]}\n\n'
            f'**Longest Streak:** `{streak(userid, "perth-trains")[0]}` (current: `{streak(userid, "perth-trains")[1]}`)\n'
            f'User started logging {joined}\n'
            f'Last log {last}\n'
            f'Total logs: {logAmounts(userid, "perth-trains")}'
    )
            except FileNotFoundError:
                embed4.add_field(name="<:transperthtrain:1335396329798631477><:TransWA:1335397360255373392> Perth Train Log Stats", value=f'{username} has no logged trips in Perth!')

            # Canberra Light Rail
            try:
                lines = topStats(userid, 'lines', 0, 'canberra-trams')
                stations = topStats(userid, 'stations', 0, 'canberra-trams')
                sets = topStats(userid, 'sets', 0, 'canberra-trams')
                trains = topStats(userid, 'types', 0, 'canberra-trams')
                dates = topStats(userid, 'dates', 0, 'canberra-trams')
                trips = topStats(userid, 'pairs', 0, 'canberra-trams')

                #other stats stuff:
                eDate =lowestDate(userid, 'canberra-trams')
                LeDate =highestDate(userid, 'canberra-trams')
                joined = convert_iso_to_unix_time(f"{eDate}T00:00:00Z") 
                last = convert_iso_to_unix_time(f"{LeDate}T00:00:00Z")
                embed4.add_field(
        name='<:canberraLightRail:1422730624426573854> Canberra Light Rail Log Stats:',
        value=f'**Top Line:** {lines[1] if len(lines) > 1 and lines[0].startswith("Unknown") else lines[0]}\n'
            f'**Top Station:** {stations[1] if len(stations) > 1 and stations[0].startswith("Unknown") else stations[0]}\n'
            f'**Top Type:** {trains[1] if len(trains) > 1 and trains[0].startswith("Unknown") else trains[0]}\n'
            f'**Top Number:** {sets[1] if len(sets) > 1 and sets[0].startswith("Unknown") else sets[0]}\n'
            f'**Top Trip:** {trips[1] if len(trips) > 1 and trips[0].startswith("Unknown") else trips[0]}\n'
            f'**Top Date:** {dates[1] if len(dates) > 1 and dates[0].startswith("Unknown") else dates[0]}\n\n'
            f'**Longest Streak:** `{streak(userid, "canberra-trams")[0]}` (current: `{streak(userid, "canberra-trams")[1]}`)\n'
            f'User started logging {joined}\n'
            f'Last log {last}\n'
            f'Total logs: {logAmounts(userid, "canberra-trams")}'
    )
            except FileNotFoundError:
                embed4.add_field(name="<:canberraLightRail:1422730624426573854> Canberra Light Rail Log Stats", value=f'{username} has no logged trips in Canberra!')

            # Buses
            try:
                lines = topStats(userid, 'lines', 0, 'bus')
                stations = topStats(userid, 'stations', 0, 'bus')
                sets = topStats(userid, 'sets', 0, 'bus')
                trains = topStats(userid, 'types', 0, 'bus')
                dates = topStats(userid, 'dates', 0, 'bus')
                trips = topStats(userid, 'pairs', 0, 'bus')
                
                #other stats stuff:
                eDate =lowestDate(userid, 'bus')
                LeDate =highestDate(userid, 'bus')
                joined = convert_iso_to_unix_time(f"{eDate}T00:00:00Z") 
                last = convert_iso_to_unix_time(f"{LeDate}T00:00:00Z")
                embed4.add_field(
        name='<:bus:1241165769241530460><:coach:1241165858274021489><:skybus:1241165983083925514><:NSW_Bus:1264885653922123878><:transperthbus:1335396307510235217><:Canberra_Bus:1264885650826465311> Bus Log Stats:',
        value=f'**Top Route:** {lines[1] if len(lines) > 1 and lines[0].startswith("Unknown") else lines[0]}\n'
            f'**Top Stop:** {stations[1] if len(stations) > 1 and stations[0].startswith("Unknown") else stations[0]}\n'
            f'**Top Type:** {trains[1] if len(trains) > 1 and trains[0].startswith("Unknown") else trains[0]}\n'
            f'**Top Bus Number:** {sets[1] if len(sets) > 1 and sets[0].startswith("Unknown") else sets[0]}\n'
            f'**Top Trip:** {trips[1] if len(trips) > 1 and trips[0].startswith("Unknown") else trips[0]}\n'
            f'**Top Date:** {dates[1] if len(dates) > 1 and dates[0].startswith("Unknown") else dates[0]}\n\n'
            f'**Longest Streak:** `{streak(userid, "bus")[0]}` (current: `{streak(userid, "bus")[1]}`)\n'
            f'User started logging {joined}\n'
            f'Last log {last}\n'
            f'Total logs: {logAmounts(userid, "bus")}'
    )
            except FileNotFoundError:
                embed4.add_field(name="<:bus:1241165769241530460><:coach:1241165858274021489><:skybus:1241165983083925514><:NSW_Bus:1264885653922123878><:transperthbus:1335396307510235217><:Canberra_Bus:1264885650826465311> Bus Log Stats", value=f'{username} has no logged bus trips!')

            # Flights
            try:
                lines = topStats(userid, 'lines', 0, 'flights')
                stations = topStats(userid, 'stations', 0, 'flights')
                sets = topStats(userid, 'sets', 0, 'flights')
                trains = topStats(userid, 'types', 0, 'flights')
                dates = topStats(userid, 'dates', 0, 'flights')
                trips = topStats(userid, 'pairs', 0, 'flights')
                
                #other stats stuff:
                eDate =lowestDate(userid, 'flights')
                LeDate =highestDate(userid, 'flights')
                joined = convert_iso_to_unix_time(f"{eDate}T00:00:00Z") 
                last = convert_iso_to_unix_time(f"{LeDate}T00:00:00Z")
                embed4.add_field(
        name='✈️ Flight Log Stats:',
        value=f'**Top Route:** {lines[1] if len(lines) > 1 and lines[0].startswith("Unknown") else lines[0]}\n'
            f'**Top Airport:** {stations[1] if len(stations) > 1 and stations[0].startswith("Unknown") else stations[0]}\n'
            f'**Top Type:** {trains[1] if len(trains) > 1 and trains[0].startswith("Unknown") else trains[0]}\n'
            f'**Top Registration:** {sets[1] if len(sets) > 1 and sets[0].startswith("Unknown") else sets[0]}\n'
            f'**Top Trip:** {trips[1] if len(trips) > 1 and trips[0].startswith("Unknown") else trips[0]}\n'
            f'**Top Date:** {dates[1] if len(dates) > 1 and dates[0].startswith("Unknown") else dates[0]}\n\n'
            f'**Longest Streak:** `{streak(userid, "flights")[0]}` (current: `{streak(userid, "flights")[1]}`)\n'
            f'User started logging {joined}\n'
            f'Last log {last}\n'
            f'Total logs: {logAmounts(userid, "flights")}'
    )
            except FileNotFoundError:
                embed4.add_field(name="✈️ Flight Log Stats", value=f'{username} has no logged plane trips!')
            pages.append(embed4)

            # Page 5: Game Stats
            embed5 = discord.Embed(title=f"Profile | Game Stats - Page 5/5")
            embed5.set_author(name=username, url='https://xm9g.net', icon_url=pfp)
            
            #games
            stats = fetchUserStats(username)
            
            if stats[0] != 'no stats':
                item, wins, losses = stats[0]
                embed5.add_field(name=':question: Station Guesser', value=f'Wins: {str(wins)}\nLosses: {str(losses)}\nAccuracy: {str(round((wins/(wins+losses))*100, 1))}%')
            else:
                embed5.add_field(name=':question: Station Guesser', value='No data',inline=False)
            if stats[1] != 'no stats':
                item, wins, losses = stats[1]
                embed5.add_field(name=':interrobang: Ultrahard Station Guesser', value=f'Wins: {str(wins)}\nLosses: {str(losses)}\nAccuracy: {str(round((wins/(wins+losses))*100, 1))}%')
            else:
                embed5.add_field(name=':interrobang: Ultrahard Station Guesser', value='No data',inline=False)
            if stats[2] != 'no stats':
                item, wins, losses = stats[2]
                embed5.add_field(name=':left_right_arrow: Station Order Guesser', value=f'Wins: {str(wins)}\nLosses: {str(losses)}\nAccuracy: {str(round((wins/(wins+losses))*100, 1))}%', inline=False)
            else:
                embed5.add_field(name=':left_right_arrow: Station Order Guesser', value='No data',inline=False)
            if stats[3] != 'no stats':
                item, wins, losses = stats[3]
                embed5.add_field(name=':grey_question: Station Hangman', value=f'Wins: {str(wins)}\nLosses: {str(losses)}\nAccuracy: {str(round((wins/(wins+losses))*100, 1))}%', inline=False)
            else:
               embed5.add_field(name=':grey_question: Station Hangman', value='No data',inline=False)
            
            # other stats
            try:
                embed5.set_footer(text=f"favourite command: {getFavoriteCommand(userid)[0]}")
            except FileNotFoundError:
                await printlog('user has no commands used')
            
            pages.append(embed5)

            class ProfileView(discord.ui.View):
                def __init__(self, pages, current_page=0):
                    super().__init__(timeout=300)
                    self.pages = pages
                    self.current_page = current_page

                @discord.ui.button(label="Previous", style=discord.ButtonStyle.gray)
                async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                    if interaction.user != ctx.user:
                        await interaction.response.send_message("This isn't your profile!", ephemeral=True)
                        return
                    if self.current_page > 0:
                        self.current_page -= 1
                        await interaction.response.edit_message(embed=self.pages[self.current_page], view=self)
                    else:
                        await interaction.response.defer()

                @discord.ui.button(label="Next", style=discord.ButtonStyle.gray)
                async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                    if interaction.user != ctx.user:
                        await interaction.response.send_message("This isn't your profile!", ephemeral=True)
                        return
                    if self.current_page < len(self.pages) - 1:
                        self.current_page += 1
                        await interaction.response.edit_message(embed=self.pages[self.current_page], view=self)
                    else:
                        await interaction.response.defer()

            if pages:
                view = ProfileView(pages, current_page)
                await ctx.edit_original_response(embed=pages[0], view=view)
            else:
                await ctx.edit_original_response(content="No profile data available.")
            
        await profiles()
        
    except Exception as e:
        import traceback
        await printlog(f"{traceback.format_exc()}")
        await ctx.edit_original_response(content = f"Error: `{e}`")

# map view command
@maps.command(name='view', description='View the maps the bot uses')
@app_commands.choices(mode=[
        app_commands.Choice(name="Victorian Trains", value="time_based_variants/log_train_map_post_munnel.png"),
        app_commands.Choice(name="Victorian Trains before the Metro Tunnel Big Switch", value="time_based_variants/log_train_map_pre_munnel.png"),
        app_commands.Choice(name="Sydney Trains", value="log_sydney-train_map.png"),
        app_commands.Choice(name="NSW Intercity Trains", value="log__sydney-train__map.png"),
        app_commands.Choice(name="NSW Regional and Interstate Trains", value="log___sydney-train___map.png"),
        app_commands.Choice(name="NSW Light Rail", value="log_sydney-tram_map.png"),
])
async def viewMaps(ctx, mode: str, no_compression: bool = False):
    await ctx.response.defer()
    await maintenance_func(ctx)
    log_command(ctx.user.id,'map-view')
    try:
        editmode = mode.removeprefix("time_based_variants/") + str(no_compression)
        try:
            file=discord.File(f'cache/{editmode}.png', filename='map.png')
        except:
            uncompressed = Image.open(f'utils/trainlogger/map/{mode}')
            legended = legend(uncompressed,f'utils/trainlogger/map/legends/{mode}')
            if no_compression:
                legended.save(f'cache/{editmode}.png')
            else:
                compressed = compress(legended)
                compressed.save(f'cache/{editmode}.png')
            file=discord.File(f'cache/{editmode}.png', filename='map.png')
        if mode == "time_based_variants/log_train_map_pre_munnel.png":
            embed = discord.Embed(title=f"Former map of the network covered by </log train:1289843416628330506>", color=0xb8b8b8, description="This is a map that is used by a seperate command to show where you have been on the railway network. This is the map that was used before the Metro Tunnel Big Switch on February 1st 2026.")
            user = await bot.fetch_user(1002449671224041502)
            pfp = user.avatar.url
            embed.set_author(name="Map by Comeng17", icon_url=pfp)
            await printlog(f"Retrieved /log train map for {ctx.user.name} in {ctx.channel.mention}")
        elif mode == "time_based_variants/log_train_map_post_munnel.png":
            embed = discord.Embed(title=f"Map of the network covered by </log train:1289843416628330506>", color=0xb8b8b8, description="This is a map that is used by a seperate command to show where you have been on the railway network.")
            user = await bot.fetch_user(1002449671224041502)
            pfp = user.avatar.url
            embed.set_author(name="Map by Comeng17", icon_url=pfp)
            await printlog(f"Retrieved future /log train map for {ctx.user.name} in {ctx.channel.mention}")
        elif mode == "log_sydney-train_map.png":
            embed = discord.Embed(title=f"Map of the network covered by </log sydney-train:1289843416628330506> (Sydney Metropolitan Network only)", color=0xb8b8b8, description="This is a map that is used by a seperate command to show where you have been on the railway network.")
            user = await bot.fetch_user(829535993643794482)
            pfp = user.avatar.url
            embed.set_author(name="Map by aperturethefloof", icon_url=pfp)
            await printlog(f"Retrieved Sydney Trains map for {ctx.user.name} in {ctx.channel.mention}")
        elif mode == "log__sydney-train__map.png":
            embed = discord.Embed(title=f"Map of the network covered by </log sydney-train:1289843416628330506> (NSW Intercity Network only)", color=0xb8b8b8, description="This is a map that is used by a seperate command to show where you have been on the railway network.")
            user = await bot.fetch_user(829535993643794482)
            pfp = user.avatar.url
            embed.set_author(name="Map by aperturethefloof", icon_url=pfp)
            await printlog(f"Retrieved NSW Intercity map for {ctx.user.name} in {ctx.channel.mention}")
        elif mode == "log___sydney-train___map.png":
            embed = discord.Embed(title=f"Map of the network covered by </log sydney-train:1289843416628330506> (NSW Regional and Interstate Network only)", color=0xb8b8b8, description="This is a map that is used by a seperate command to show where you have been on the railway network.")
            user = await bot.fetch_user(829535993643794482)
            pfp = user.avatar.url
            embed.set_author(name="Map by aperturethefloof", icon_url=pfp)
            await printlog(f"Retrieved NSW Regional map for {ctx.user.name} in {ctx.channel.mention}")
        elif mode == "log_sydney-tram_map.png":
            embed = discord.Embed(title=f"Map of the network covered by </log sydney-tram:1289843416628330506>", color=0xb8b8b8, description="This is a map that is used by a seperate command to show where you have been on the railway network.")
            user = await bot.fetch_user(829535993643794482)
            pfp = user.avatar.url
            embed.set_author(name="Map by aperturethefloof", icon_url=pfp)
            await printlog(f"Retrieved NSW Light Rail for {ctx.user.name} in {ctx.channel.mention}")
        embed.set_image(url="attachment://map.png")
        embed.set_footer(text="If you're interested in helping make these maps (especially the interstate ones) contact Xm9G or Comeng17")
        if no_compression:
            await ctx.followup.send(file=file)
        else:
            await ctx.followup.send(embed=embed, file=file)
    except Exception as e:
        await printlog(e)

# map trip command maps trips 
@maps.command(name='trips', description="View a map of all the trips you've logged")
@app_commands.choices(mode=[
        app_commands.Choice(name="Victorian Trains", value="time_based_variants/log_train_map_post_munnel.png"),
        app_commands.Choice(name="Victorian Trains before the Metro Tunnel Big Switch", value="time_based_variants/log_train_map_pre_munnel.png"),
        # app_commands.Choice(name="NSW Light Rail", value="log_sydney-tram_map.png"),
])
@app_commands.autocomplete(line=line_autocompletion)
@app_commands.choices(train=[
        app_commands.Choice(name="All", value="all"),
        app_commands.Choice(name="EDI Comeng", value="EDI Comeng"),
        app_commands.Choice(name="Alstom Comeng", value="Alstom Comeng"),
        app_commands.Choice(name="X'Trapolis 100", value="X'Trapolis 100"),
        app_commands.Choice(name="X'Trapolis 2.0", value="X'Trapolis 2.0"),
        app_commands.Choice(name="HCMT", value="HCMT"),
        app_commands.Choice(name="Siemens", value="Siemens Nexas"),
        app_commands.Choice(name="VLocity", value="VLocity"),
        app_commands.Choice(name="N Class", value="N Class"),
        app_commands.Choice(name="Sprinter", value="Sprinter"),
        app_commands.Choice(name="Other", value="Other"),
])
async def mapstrips(ctx,mode: str="time_based_variants/log_train_map_post_munnel.png",line: str='All', train:str='all', year: int=0, user: discord.Member=None,global_stats:bool=False,no_compression:bool=False):
    await ctx.response.defer()
    await maintenance_func(ctx)
    log_command(ctx.user.id, 'maps-trips')
    await printlog(f"Making trip map for {str(ctx.user.id)}")

    async def generate_map():
        if user == None:
            username = ctx.user.name
            target_user = ctx.user.id
        else:
            username = user.name
            target_user = user.id

        if mode == "time_based_variants/log_train_map_pre_munnel.png":
            modeName = 'vic'
            try:
                percent_amount = await asyncio.to_thread(logMap, target_user, lines_dictionary_log_train_map_pre_munnel, mode, line, year, 'vic', train, global_stats, no_compression)
            except FileNotFoundError:
                await ctx.followup.send(f'{"You have" if user == None else username + " has"} no logs!')
                return
            except Exception as e:
                await ctx.followup.send(f'An error occurred while generating the map:\n```{e}```')
                print(f'Error generating map for {username}:\n```{str(e)}\n\n{traceback.format_exc()}```\n<@{USER_ID}>')
                return
            
            # get the percentage of area covered
            percentageCovered = (percent_amount/getTotalLines_pre_munnel()*100)
            
            # Send the map once generated
            try:
                # make nameextras string
                nameextras = ''
                if global_stats == False:
                    nameextras = f'@{username}'
                else:
                    nameextras = f'All'
                if train != 'all' and year != 0:
                    nameextras += f' for {train} trains in {year}'
                elif train != 'all':
                    nameextras += f' for ' + train.strip("\'")
                elif year != 0:
                    nameextras += f' in {year}'
                if line != 'All':
                    nameextras += f' on the {line} line'
                nameextras += f' | {round(percentageCovered, 2)} percent of segments travelled'
                
                if global_stats == True:
                    file = discord.File(f'cache/{modeName}-{year}-{train}-{line}-{str(no_compression)}.png', filename='map.png')
                else:
                    file = discord.File(f'cache/{target_user}-{modeName}-{year}-{train}-{line}-{str(no_compression)}.png', filename='map.png')
                line_str = '' if line == 'All' else f' on the {line} Line'
                year_str = '' if year == 0 else f' in {str(year)}'
                cleanednamextras = nameextras.replace(' ', '%20').replace('|', '%7C')
                imageURL = f"https://trackpulsevic.xm9g.net/logs/map?img={target_user}-{modeName}-{year}-{train.replace(' ', '%20')}-{line.replace(' ', '%20')}-{str(no_compression)}&name={username}%27s%20Victorian%20train%20map{cleanednamextras}"
                embed = discord.Embed(title=f"Pre Big Switch Map of logs with </log train:1289843416628330506> for {nameextras}", 
                                    color=0xb8b8b8, 
                                    description=f"[Click here to view in your browser]({imageURL})")
                embed.set_image(url="attachment://map.png")
                user_pic = await bot.fetch_user(1002449671224041502)
                pfp = user_pic.avatar.url
                embed.set_author(name="Map by Comeng17", icon_url=pfp)
                embed.set_footer(text="If you're interested in helping make these maps (especially the interstate ones) contact Xm9G or Comeng17")
                if no_compression:
                    await ctx.followup.send(file=file)
                else:
                    await ctx.followup.send(embed=embed, file=file)
            except Exception as e:
                await ctx.followup.send(f'Error sending map:\n```{e}```')
        
        if mode == "time_based_variants/log_train_map_post_munnel.png":
            modeName = 'vic-metrotunnel'
            try:
                percent_amount = await asyncio.to_thread(logMap, target_user, lines_dictionary_log_train_map_post_munnel, mode, line, year, 'vic-metrotunnel', train, global_stats, no_compression)
            except FileNotFoundError:
                await ctx.followup.send(f'{"You have" if user == None else username + " has"} no logs!')
                return
            except Exception as e:
                await ctx.followup.send(f'An error occurred while generating the map:\n```{e}```')
                print(f'Error generating map for {username}:\n```{str(e)}\n\n{traceback.format_exc()}```\n<@{USER_ID}>')
                return

            # get the percentage of area covered
            percentageCovered = (percent_amount/getTotalLines_post_munnel()*100)

            # Send the map once generated
            try:
                # make nameextras string
                nameextras = ''
                if global_stats == False:
                    nameextras = f'@{username}'
                else:
                    nameextras = f'All'
                if train != 'all' and year != 0:
                    nameextras += f' for {train} trains in {year}'
                elif train != 'all':
                    nameextras += f' for ' + train.strip("\'")
                elif year != 0:
                    nameextras += f' in {year}'
                if line != 'All':
                    nameextras += f' on the {line} line'
                nameextras += f' | {round(percentageCovered, 2)} percent of segments travelled'

                if global_stats == True:
                    file = discord.File(f'cache/{modeName}-{year}-{train}-{line}-{str(no_compression)}.png', filename='map.png')
                else:
                    file = discord.File(f'cache/{target_user}-{modeName}-{year}-{train}-{line}-{str(no_compression)}.png', filename='map.png')
                line_str = '' if line == 'All' else f' on the {line} Line'
                year_str = '' if year == 0 else f' in {str(year)}'
                imageURL = f'https://trackpulsevic.xm9g.net/logs/map?img={target_user}-{modeName}&name={username}-{str(no_compression)}\'s%20Victorian%20train%20map%20post%20Metro%20Tunnel'
                embed = discord.Embed(title=f"Map of logs with </log train:1289843416628330506> for {nameextras}", 
                                    color=0xb8b8b8, 
                                    description=f"[Click here to view in your browser]({imageURL})")
                embed.set_image(url="attachment://map.png")
                user_pic = await bot.fetch_user(1002449671224041502)
                pfp = user_pic.avatar.url
                embed.set_author(name="Map by Comeng17", icon_url=pfp)
                embed.set_footer(text="If you're interested in helping make these maps (especially the interstate ones) contact Xm9G or Comeng17")
                if no_compression:
                    await ctx.followup.send(file=file)
                else:
                    await ctx.followup.send(embed=embed, file=file)
            except Exception as e:
                await ctx.followup.send(f'Error sending map:\n```{e}```')
        
        if mode == "log_sydney-tram_map.png":
            modeName = 'sydney-tram'
            try:
                await asyncio.to_thread(logMap, target_user, lines_dictionary_log_sydney_tram_map, mode, line, year, 'sydney-tram')
            except FileNotFoundError:
                await ctx.followup.send(f'{"You have" if user == None else username + " has"} no logs!')
                return
            except Exception as e:
                await ctx.followup.send(f'Error:\n```{e}```')
                return
            # Send the map once generated
            try:
                if global_stats == True:
                    file = discord.File(f'cache/{modeName}-{year}-{train}-{line}.png', filename='map.png')
                else:
                    file = discord.File(f'cache/{target_user}-{modeName}-{year}-{train}-{line}.png', filename='map.png')
                line_str = '' if line == 'All' else f' on the {line} Line'
                year_str = '' if year == 0 else f' in {str(year)}'
                imageURL = f'https://trackpulsevic.xm9g.net/logs/map?img={target_user}-{modeName}&name={username}\'s%20Sydney%20tram%20map'
                embed = discord.Embed(title=f"Map of logs with </log sydney-tram:1289843416628330506> for @{username}{year_str}{line_str}", 
                                    color=0xb8b8b8, 
                                    description=f"THIS MAP IS NOT FINISHED [Click here to view in your browser]({imageURL})")
                embed.set_image(url="attachment://map.png")
                user_pic = await bot.fetch_user(829535993643794482)
                pfp = user_pic.avatar.url
                embed.set_author(name="Map by aperturethefloof", icon_url=pfp)
                embed.set_footer(text="If you're interested in helping make these maps (especially the interstate ones) contact Xm9G or Comeng17")
                if no_compression:
                    await ctx.followup.send(file=file)
                else:
                    await ctx.followup.send(embed=embed, file=file)
            except Exception as e:
                await ctx.followup.send(f'Error sending map:\n```{e}```')

# Start the async map generation
    async def safe_generate_map():
        import os
        import traceback
        
        # get memory usage before starting the map generation
        baseline_rss_kb = 0
        try:
            with open('/proc/self/status', 'r') as f:
                for line in f:
                    if line.startswith('VmRSS:'):
                        baseline_rss_kb = int(line.split()[1])
                        break
        except:
            pass

        map_task = asyncio.ensure_future(generate_map())
        
        try:
            while not map_task.done():
                await asyncio.sleep(1.0)
                
                # 2. Get the Current RAM
                current_rss_kb = 0
                try:
                    with open('/proc/self/status', 'r') as f:
                        for line in f:
                            if line.startswith('VmRSS:'):
                                current_rss_kb = int(line.split()[1])
                                break
                except:
                    continue 
                
                # how much mapstrips is using compared to before it started
                command_usage_kb = current_rss_kb - baseline_rss_kb
                
                # 4GB limit
                if command_usage_kb > (4 * 1024 * 1024): 
                    map_task.cancel()
                    
                    print(f"MEMORY ERROR (EXCEEDED) in map generation")
                    
                    error_msg = ("Map Generation ERROR: Memory Limit Reached. Please try again in a few minutes. "
                                 "If you see me again, please know the developers are actively trying to fix this issue. "
                                 "Apologies for any inconvenience.")
                    
                    try:
                        await ctx.edit_original_response(content=error_msg)
                    except:
                        try:
                            await ctx.followup.send(error_msg)
                        except:
                            pass
                    return
            
            await map_task
            
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f'CRITICAL ERROR in map generation: {e}\n{traceback.format_exc()}')

    await safe_generate_map()

@bot.command(name='testfind')
async def testfind(ctx):
    info = await seeWhereTrainsAre(['271M', '115M'])
    print(info)
    for train in info:
        embed = discord.Embed(title=f'{train[4]}\'s Location')
        embed.add_field(name='Line', value=f'{train[1]} line to {train[5]}')
        embed.add_field(name='URL', value=train[2])
        await ctx.send(embed=embed)
    

# achievement commands
@bot.command()
async def refreshachievements(ctx):
    log_command(ctx.author.id, 'refresh-achievements')
    response = await ctx.send('Checking for new Achievements...')
    await addAchievement(ctx.author.name,ctx.channel.id, ctx.author.mention)
    new = checkGameAchievements(ctx.author.name)
    for achievement in new:
        info = getAchievementInfo(achievement)
        embed = discord.Embed(title='Achievement unlocked!', color=achievement_colour)
        embed.add_field(name=info['name'], value=f"{info['description']}\n\n View all your achievements: </achievements view:1327085604789551134>")
        await ctx.send(f'<@{ctx.author.id}>',embed=embed)

@bot.command()
async def award(ctx, user: discord.User, achievement:int):
    if ctx.author.id in admin_users:
        log_command(ctx.author.id, 'award-achievement')
        await ctx.send(f'Awarding achievement id `{achievement}` to {user.mention}...')
        awardAchievement(user.name, achievement)
        info = getAchievementInfo(str(achievement))
        embed = discord.Embed(title='Achievement unlocked!', color=achievement_colour)
        embed.add_field(name=info['name'], value=f"{info['description']}\n\n View all your achievements: </achievements view:1327085604789551134>")
        await user.send(f'<@{user.id}>',embed=embed)   
    else:
        print('User is not an admin, he cannot give achievements') 

    
@achievements.command(name='view', description='View your achievements.')
@app_commands.describe(user="Who's achievements to show?")
async def viewAchievements(ctx, user: discord.User = None):
    await ctx.response.defer()
    await maintenance_func(ctx)
    log_command(ctx.user.id, 'view-achievements')

    if user is None:
        user = ctx.user

    # Get user's achievements
    user_achievements = {}  # Change to dict to store dates
    filepath = f'utils/trainlogger/achievements/data/{user.name}.csv'
    if os.path.exists(filepath):
        with open(filepath, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                # Process achievements in pairs (id, date)
                for i in range(0, len(row), 2):
                    if i+1 < len(row):
                        achievement_id = row[i]
                        achievement_date = row[i+1]
                        user_achievements[achievement_id] = achievement_date

    # Get all achievements from master list with dates
    all_achievements = []
    with open('utils/trainlogger/achievements/achievements.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row:  # Skip empty rows
                achievement_id = row[0]
                name = row[1] 
                description = row[2]
                has_achievement = achievement_id in user_achievements
                date = user_achievements.get(achievement_id, None) if has_achievement else None
                all_achievements.append((achievement_id, name, description, has_achievement, date))

    # Get all achievements from master list
    all_achievements = []
    with open('utils/trainlogger/achievements/achievements.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row:  # Skip empty rows
                achievement_id = row[0]
                name = row[1]
                description = row[2]
                has_achievement = achievement_id in user_achievements
                all_achievements.append((achievement_id, name, description, has_achievement))

    # Calculate percentage
    total_achievements = len(all_achievements)
    achieved = sum(1 for _, _, _, has_achievement in all_achievements if has_achievement)
    percentage = (achieved / total_achievements) * 100 if total_achievements > 0 else 0

    # Split achievements into pages of 10
    pages = [all_achievements[i:i + 10] for i in range(0, len(all_achievements), 10)]
    current_page = 0

    async def get_page_embed(page_num):
        embed = discord.Embed(title=f"{user.name}'s Achievements", description=f"**Progress:** {achieved}/{total_achievements} ({percentage:.1f}%)", color=achievement_colour)
        embed.set_footer(text=f"Page {page_num + 1}/{len(pages)}")
        
        for achievement in pages[page_num]:
            achievement_id, name, description, has_achievement = achievement
            emoji = "✅" if has_achievement else "🔒"
            value = description
            if has_achievement:
                date = user_achievements.get(achievement_id)
                if date != 'unknown':
                    value += f"\nDate earned: {date}"
            embed.add_field(name=f"{emoji} {name}", value=value, inline=False)
        
        return embed
       # Create buttons
    class NavButtons(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=180)

        @discord.ui.button(label="Previous", style=discord.ButtonStyle.gray)
        async def previous_button(self, interaction: discord.Interaction, _):
            nonlocal current_page
            if current_page > 0:
                current_page -= 1
                await interaction.response.edit_message(embed=await get_page_embed(current_page), view=self)
            else:
                await interaction.response.defer()

        @discord.ui.button(label="Next", style=discord.ButtonStyle.gray)
        async def next_button(self, interaction: discord.Interaction, _):
            nonlocal current_page
            if current_page < len(pages) - 1:
                current_page += 1
                await interaction.response.edit_message(embed=await get_page_embed(current_page), view=self)
            else:
                await interaction.response.defer()
      # Send initial embed with buttons
    await ctx.edit_original_response(embed=await get_page_embed(0), view=NavButtons())
   
    
@bot.tree.command(name="line-status", description="View your line status for all lines.")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.choices(operator=[
    app_commands.Choice(name="Metro", value="metro"),
    app_commands.Choice(name="V/Line", value="vline"),
])
async def checklines(ctx, operator: str):
    # Defer the response to avoid timeout
    await ctx.response.defer()
    await maintenance_func(ctx)
    log_command(ctx.user.id, 'line-status')

    # Run the async function in the background
    asyncio.create_task(run_in_thread(ctx, operator))

async def run_in_thread(ctx, operator):
    statuses = [f'{datetime.now()}']
    log_channel = bot.get_channel(int(config['STARTUP_CHANNEL_ID']))

    # Process metro lines
    if operator == 'metro':
        embed_metro = discord.Embed(title=f'<:train:1241164967789727744> Metro Line Status', color=metro_colour, timestamp=discord.utils.utcnow())
        lines = ['Alamein', 'Belgrave', 'Craigieburn', 'Cranbourne', 'Mernda', 'Frankston', 'Glen%20Waverley', 'Hurstbridge', 'Lilydale', 'Pakenham', 'Sandringham', 'Stony%20Point', 'Sunbury', 'Upfield', 'Werribee', 'Williamstown']
        
        # Process each line in a separate background thread to avoid blocking
        for line in lines:
            json_info_str = await asyncio.to_thread(route_api_request, line, "0")
            json_info = json.loads(json_info_str.replace("'", '"'))
            
            # Process JSON data
            routes = json_info['routes']
            status = json_info['status']
            route = routes[0]
            route_service_status = route['route_service_status']
            description = route_service_status['description']
            route_id = route['route_id']
            route_name = route['route_name']
            
            if description == "Service Information":
                description = "Good Service"
            
            disruptionDescription = ""
            try:
                disruptions = await asyncio.to_thread(disruption_api_request, route_id)
                general_disruption = disruptions["disruptions"]["metro_train"][0]
                disruptionDescription = general_disruption["description"]
            except Exception as e: 
                await printlog(e)

            color = genColor(description)
            info = f'{description}'
            embed_metro.add_field(name=f'{route_name}', value=f'{statusEmoji(description)} {info}', inline=True)
            statuses.append(description)

    # Process V/Line lines
    # Made by Comeng17
    elif operator == 'vline':
        embed_vline = discord.Embed(title=f'<:vline:1241165814258729092> V/Line Line Status', color=vline_colour, timestamp=discord.utils.utcnow())
        lines = ['Geelong - Melbourne', 'Warrnambool - Melbourne via Apollo Bay & Geelong', 'Ballarat-Wendouree - Melbourne via Melton', 'Ararat - Melbourne via Ballarat', 'Maryborough - Melbourne via  Ballarat', 'Bendigo - Melbourne via Gisborne', 'Echuca-Moama - Melbourne via Bendigo or Heathcote', 'Swan Hill - Melbourne via Bendigo', 'Seymour - Melbourne via Broadmeadows', 'Shepparton - Melbourne via Seymour', 'Albury - Melbourne via Seymour', 'Traralgon - Melbourne via Morwell & Moe & Pakenham', 'Bairnsdale - Melbourne via Sale & Traralgon']
        
        for line in lines:
            line = line.replace(" ", "%20")
            json_info_str = await asyncio.to_thread(route_api_request, line, "3")
            json_info = json.loads(json_info_str.replace("'", '"'))
            
            routes = json_info['routes']
            route = routes[0]
            route_service_status = route['route_service_status']
            description = route_service_status['description']
            route_id = route['route_id']
            route_name = route['route_name']
            
            # Simplify route name
            route_name = route_name.split(' - ')[0]  # This is a simple approach; adjust if names change
            
            disruptionDescription = ""
            try:
                disruptions = await asyncio.to_thread(disruption_api_request, route_id)
                general_disruption = disruptions["disruptions"]["regional_train"][0]
                disruptionDescription = general_disruption["description"]
                disruption_vline = general_disruption["disruption_type"]
                currentness = general_disruption["disruption_status"]
                if currentness == "Planned" or disruption_vline == "Service Information":
                    disruption_vline = "Good Service"
            except Exception as e:
                await printlog(e)

            color = genColor(disruption_vline)
            info = f'{disruption_vline}'
            embed_vline.add_field(name=f'{route_name}', value=f'{statusEmoji(disruption_vline)} {info}', inline=True)
            statuses.append(disruption_vline)

    try:
        # Send the response after data is processed
        await ctx.edit_original_response(embed=embed_metro if operator == 'metro' else embed_vline)
    except Exception as e:
        await printlog(f'ERROR: {e}')

    with open('logs.txt', 'a') as file:
        file.write(f"LINE STATUS CHECKED MANUALLY\n")
        
    with open('utils/line-status-data.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(statuses)
        
@schedule.command(name="add", description="Add a train to make its run be send in a channel every 10 minutes.")
@app_commands.describe(train="A carriage number on the train to send, eg 860M", channel="The channel to send the run to")
async def add_schedule(ctx, train: str, channel: discord.TextChannel):
    await maintenance_func(ctx)
    if ctx.user.guild_permissions.administrator:
        log_command(ctx.user.id, 'add-schedule')
        await ctx.response.defer()
        await trainTimleyFetcherAdd(ctx, train, channel, 10)
    else:
        await ctx.response.send_message("Only administrators can add schedules.", ephemeral=True)
        return
    
@schedule.command(name="remove", description="Remove a train to make its run not be send in the channel.")
@app_commands.describe(train="The carriage number of the train to stop sending, eg 860M", channel="The channel to stop sending the run to.")
async def add_schedule(ctx, train: str, channel: discord.TextChannel):
    if ctx.user.guild_permissions.administrator:
        log_command(ctx.user.id, 'remove-schedule')
        await ctx.response.defer()
        await maintenance_func(ctx)
        await trainTimleyFetcherRemove(ctx, train, channel)
    else:
        await ctx.response.send_message("Only administrators can remove schedules.", ephemeral=True)
        return
    
@schedule.command(name="list", description="List all trains that are being sent in a channel.")
async def list_schedule(ctx, channel: discord.TextChannel):
    log_command(ctx.user.id, 'view-schedule-list')
    await ctx.response.defer()
    await maintenance_func(ctx)
    await trainTimleyFetcherList(ctx, channel)

#about/credits
@bot.tree.command(name="about", description="View information about the bot.")
async def about(ctx):
    await ctx.response.defer()
    await maintenance_func(ctx)
    log_command(ctx.user.id, 'about')
    embed = discord.Embed(title="About", description=f"TrackPulse Vic is a Discord bot designed for users to log their train, tram or bus trips across Victoria, New South Wales, South Australia and Western Australia, allowing you to keep track of what transport you have taken and when. It also includes other features such as real-time tracking for Metro Trains Melbourne, upcoming departures for Melbourne stations and the ability to search for information on specific trains, and also fun games for you to play with your friends.\nOnline Since <t:{uptime}:R>", color=discord.Color.blue())
    embed.add_field(name="Developed by", value="[Comeng17](https://github.com/Comeng17)", inline=True)
    embed.add_field(name="Created by", value="[Billy Evans](https://xm9g.net/)", inline=True)
    embed.add_field(name="Contributions by",value=f'[domino6658](https://github.com/domino6658)\n[AshKmo](https://github.com/AshKmo)\n[Richy](https://github.com/Richy023)\n[minirobinbin](https://github.com/minirobinbin)\n[NebulaFire](https://github.com/NebulaInferno)\nCaroline Springs (hosting)\nAperture (NSW train info)\n',inline=True)
    embed.add_field(name='Photos sourced from',value="[Victorian Rail Photos](https://victorianrailphotos.com/)")
    embed.add_field(name="Data Sources", value="[Transport Victoria](https://www.ptv.vic.gov.au/)\n", inline=True)
    embed.add_field(name='Website', value='https://trackpulsevic.xm9g.net')
    embed.add_field(name='Discord Server', value='https://discord.gg/nfAqAnceQ5')
    embed.add_field(name='Report issues', value='[Report a bug on github](https://github.com/TrackPulse-Vic/TrackPulse-Vic/issues)')
    embed.set_footer(text=f"{getTotalTrips()} trips logged with TrackPulse Vic", icon_url="https://xm9g.net/discord-bot-assets/logo.png")
    await ctx.edit_original_response(embed=embed)


# year in review
@bot.tree.command(name="year-in-review", description="View your year in review for a specific year.")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def yearinreview(ctx, year: int=2025):
    async def yir():
        await ctx.response.defer()
        await maintenance_func(ctx)
        log_command(ctx.user.id, 'year-in-review')
        current_year = datetime.now().year
        unix_time = int(time.time())
        if current_year == year:
            if unix_time < 1764507600:
                await ctx.edit_original_response(content=f"Your {current_year} year in review will be available <t:1764507600:R>.")
                return
                # pass
        try:
        
            embed = discord.Embed(title=f":bar_chart: {ctx.user.name}'s Victorian Trains Year in Review: {year}", color=discord.Color.blue())
            data = year_in_review(f'utils/trainlogger/userdata/{ctx.user.id}.csv', year)
            
            (lilydale_value, ringwood_value), count = data.get("top_pair")
            embed.add_field(name=f"In {year} {ctx.user.name} went on {str(data['total_trips'])} train trips :chart_with_upwards_trend:", value=f"\n**First Trip:** {data['first_trip'][5]} to {data['first_trip'][6]} on {data['first_trip'][3]} :calendar_spiral: \n**Last Trip:** {data['last_trip'][5]} to {data['last_trip'][6]} on {data['last_trip'][3]} :calendar_spiral: \n\n:star: **Favourite Trip:** {lilydale_value} to {ringwood_value} - {count} times\n:metro: {vline_metroprecent(ctx.user.name, year)}", inline=False)
            
            top_lines = data['top_5_lines']
            formatted_lines = "\n".join([f"{i + 1}. {line[0]}: {line[1]} trips" for i, line in enumerate(top_lines)])
            embed.add_field(name=f"{ctx.user.name}'s Top Lines :railway_track:", value=formatted_lines or "No lines found.", inline=False)
            
            top_stations = data['top_5_stations']
            formatted_stations = "\n".join([f"{i + 1}. {line[0]}: {line[1]} visits" for i, line in enumerate(top_stations)])
            embed.add_field(name=f"{ctx.user.name}'s Top Stations :station:", value=formatted_stations or "No Stations found.", inline=False)
            
            top_stations = data['top_5_trains']
            formatted_stations = "\n".join([f"{i + 1}. {line[0]}: {line[1]} trips" for i, line in enumerate(top_stations)])
            embed.add_field(name=f"{ctx.user.name}'s Top Train types :train:", value=formatted_stations or "No Trains found.", inline=False)
            
            top_stations = data['top_number']
            formatted_stations = "\n".join([f"{i + 1}. {line[0]}: {line[1]} trips" for i, line in enumerate(top_stations)])
            embed.add_field(name=f"{ctx.user.name}'s Top Trains :bullettrain_side:", value=formatted_stations or "No Trains found.", inline=False)
            
            # v/line vs metro percent
            
            embed.set_thumbnail(url=ctx.user.avatar.url)
            embed.set_footer(text="Trains Logged with TrackPulse Vic", icon_url="https://xm9g.net/discord-bot-assets/logo.png")

            await ctx.edit_original_response(embed=embed)
            
        except Exception as e:
            await ctx.edit_original_response(embed=discord.Embed(title="Error", description=f"An error occurred while fetching data: {e}"))
        
    asyncio.create_task(yir())

@bot.command()
@commands.guild_only()
async def sync(ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if ctx.author.id in admin_users:

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
                await printlog(f'Error: {e}')
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

# sends a message to a specific channel
@bot.command()
async def send(ctx, user: discord.Member, *, message: str):
    if ctx.author.id in admin_users:
        log_command(ctx.author.id, 'send')
        try:
            await user.send(message)
            await ctx.send(f"Sent message to {user.mention}.")
        except discord.errors.Forbidden:
            await ctx.send("Couldn't send a message to that user.")
    else:
        await ctx.send("You are not authorized to use this command.")
        
# export train data
@bot.command()
async def exporthistory(ctx, train:str):
    if ctx.author.id in admin_users:
        filepath = f'utils/schedule/history/{train}.csv'
        if not os.path.exists(filepath):
            await ctx.send(f"No history found for train {train}.")
            return
    
        log_command(ctx.author.id, 'export-history')
        await ctx.send(file=discord.File(filepath, filename=f"{train}.csv"))
    else:
        await ctx.send("Currently only admins can export train history, in the future this data may become available to all users.")

@bot.command(name='backup')
async def backup(ctx):
    if ctx.guild is not None:
        await ctx.send("This command can only be used in DMs.")
        return

    if ctx.author.id not in admin_users:
        await ctx.send("You are not authorized to use this command.")
        return

    log_command(ctx.author.id, 'backup')
    await ctx.send("Preparing backup archive...")

    root_path = Path(__file__).resolve().parent
    userdata_path = root_path / 'utils' / 'trainlogger' / 'userdata'
    leaderboard_path = root_path / 'utils' / 'game' / 'scores'
    temp_path = root_path / 'temp'
    temp_path.mkdir(parents=True, exist_ok=True)

    backup_name = f"trackpulse-backup-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"
    max_discord_file_size = 8 * 1024 * 1024
    target_archive_size = int(7.5 * 1024 * 1024)

    files_to_backup = []
    for source_path in [userdata_path, leaderboard_path]:
        if source_path.exists():
            for file_path in source_path.rglob('*'):
                if file_path.is_file():
                    if source_path == userdata_path and 'maps' in file_path.relative_to(userdata_path).parts:
                        continue
                    files_to_backup.append(file_path)

    if not files_to_backup:
        await ctx.send("No backup data was found.")
        return

    files_to_backup.sort(key=lambda p: str(p))

    archive_groups = []
    current_group = []
    current_estimated_size = 0

    for file_path in files_to_backup:
        file_size = file_path.stat().st_size
        # Include a small buffer per file for zip metadata overhead.
        estimated_entry_size = file_size + 2048

        if current_group and (current_estimated_size + estimated_entry_size) > target_archive_size:
            archive_groups.append(current_group)
            current_group = []
            current_estimated_size = 0

        current_group.append(file_path)
        current_estimated_size += estimated_entry_size

    if current_group:
        archive_groups.append(current_group)

    created_archives = []

    try:
        total_parts = len(archive_groups)
        for index, group in enumerate(archive_groups, start=1):
            archive_filename = f"{backup_name}-part{index:02d}-of-{total_parts:02d}.zip"
            archive_path = temp_path / archive_filename

            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as archive:
                for file_path in group:
                    archive.write(file_path, file_path.relative_to(root_path))

            created_archives.append(archive_path)
            archive_size = archive_path.stat().st_size
            if archive_size > max_discord_file_size:
                await ctx.send(
                    f"Backup failed: {archive_filename} is {archive_size / (1024 * 1024):.2f} MB, "
                    "which is above Discord's 8 MB upload limit."
                )
                return

        await ctx.send(f"Backup ready. Sending {len(created_archives)} archive file(s).")
        for archive_path in created_archives:
            await ctx.send(file=discord.File(str(archive_path), filename=archive_path.name))
    except Exception as e:
        await printlog(f"Backup creation failed: {e}")
        await ctx.send(f"Failed to generate backup: {e}")
    finally:
        for archive_path in created_archives:
            if archive_path.exists():
                try:
                    archive_path.unlink()
                except Exception:
                    pass

# analytics viewer
@bot.command()
async def analytics(ctx,mode: str=None, user: discord.Member=None):
    if ctx.author.id in admin_users:
        log_command(ctx.author.id,'analytics')
        
        if mode == "commands":
            # Dictionary to store total command counts across all users
            total_commands = {}
            folder_path = 'utils/stats/data'
            
            # Process each user's CSV file
            for filename in os.listdir(folder_path):
                if filename.endswith('.csv'):
                    with open(os.path.join(folder_path, filename), 'r') as f:
                        next(f) # Skip header
                        for line in f:
                            command, count = line.strip().split(',')
                            total_commands[command] = total_commands.get(command, 0) + int(count)
            
            # Sort commands by count
            sorted_commands = sorted(total_commands.items(), key=lambda x: x[1], reverse=True)
            
            # Format output
            output = "Top commands across all users:\n"
            for command, count in sorted_commands:
                output += f"{command}: {count}\n"
                
            # Split into chunks if too long
            if len(output) > 2000:
                chunks = [output[i:i+1990] for i in range(0, len(output), 1990)]
                for chunk in chunks:
                    await ctx.send(chunk)
            else:
                await ctx.send(output)
        elif mode == 'servers':
            pass
            # guild_list = []
            # total_users = 0
            
            # # Get all guilds
            # for guild in bot.guilds:
            #     member_count = len(guild.members)
            #     total_users += member_count
            #     guild_list.append(f"{guild.name}: {member_count} members")
            
            # # Format output
            # output = f"Bot is in {len(bot.guilds)} servers with {total_users} total users:\n"
            # output += "\n".join(guild_list)
            
            # # Split into chunks if too long
            # if len(output) > 2000:
            #     chunks = [output[i:i+1990] for i in range(0, len(output), 1990)]
            #     for chunk in chunks:
            #         await ctx.send(f"```{chunk}```")
            # else:
            #     await ctx.send(f"```{output}```")
            
        elif user == None:
            all_files = []
            folder_path = 'utils/stats/data'

            command_counts = []
            for filename in os.listdir(folder_path):
                if filename.endswith('.csv'):
                    # Read command counts for this user
                    total_commands = 0
                    with open(os.path.join(folder_path, filename), 'r') as f:
                        next(f) # Skip header
                        for line in f:
                            count = int(line.strip().split(',')[1])
                            total_commands += count
                    
                    command_counts.append((f'<@{filename.strip(".csv")}>', total_commands))
            
            # Sort by number of commands
            command_counts.sort(key=lambda x: x[1], reverse=True)
            
            output = f"{len(command_counts)} users:\n"
            current_chunk = ""
            chunks = []
            
            for user, count in command_counts:
                line = f'{user} - {count} commands\n'
                if len(current_chunk) + len(line) > 1900: 
                    chunks.append(current_chunk)
                    current_chunk = line
                else:
                    current_chunk += line
            
            if current_chunk:
                chunks.append(current_chunk)

            messages = []
            for _ in chunks:
                msg = await ctx.send('...')
                messages.append(msg)

            for i, chunk in enumerate(chunks):
                prefix = output if i == 0 else ""  
                await messages[i].edit(content=prefix + chunk)
            
        else:
            try:
                file = discord.File(f'utils/stats/data/{user.id}.csv')
                await ctx.send(file=file)
            except FileNotFoundError:
                await ctx.send(content=f'No analytics data found for {user.mention}')

# commands to edit the train info database
@bot.tree.command(name="select-train-for-editing", description="Select a line in the train info database to edit.")
async def select_train(ctx, train: str):
    await ctx.response.defer()
    if ctx.user.id in admin_users:
        log_command(ctx.user.id, 'select-train-for-editing')
        with open('utils/trainsets.csv', 'r', newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    collumheadings = next(reader)
                    found = False
                    for row in reader:
                        if row[0].lower() == train.lower():
                            found = True
                            break
                    if found:
                        await ctx.edit_original_response(content=f"Found the train in the db,\nplease say the new values for each collum in the same format as the above, or say 'cancel' to cancel the edit.\n{collumheadings}\nCopy and pase the message below to make editing easier:")
                        await ctx.channel.send(f"{','.join(row)}")
                        def check(m):
                            return m.author == ctx.user and m.channel == ctx.channel
                        try:
                            msg = await bot.wait_for("message", check=check, timeout=60)
                            if msg.content.lower() == 'cancel':
                                await ctx.channel.send("Edit cancelled.")
                                return
                            new_values = msg.content.split(',')
                            if len(new_values) != len(collumheadings):
                                await ctx.channel.send(f"Incorrect number of values provided. Expected {len(collumheadings)}, got {len(new_values)}.\n**Most likely this is due to there being a comma in the text somewhere, e.g. the date. Please remove this.**")
                                return
                            
                            rows = []
                            with open('utils/trainsets.csv', 'r', newline='', encoding='utf-8') as csvfile:
                                reader = csv.reader(csvfile)
                                collumheadings = next(reader)
                                for row in reader:
                                    rows.append(row)
                            
                            # Find the row to edit and update it
                            for row in rows:
                                if row[0].lower() == train.lower():
                                    for i, value in enumerate(new_values):
                                        row[i] = value.strip()
                                    break
                            
                            # Write the updated data back to the CSV
                            with open('D:\\Billy\\Douments\\Self made programs\\railway-photos-1\\trainsets.csv', 'w', newline='', encoding='utf-8') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(collumheadings)
                                writer.writerows(rows)
                                
                            # push the file to github
                            await ctx.channel.send("Pushing changes to GitHub...")
                            repo_dir = "D:\\Billy\\Douments\\Self made programs\\railway-photos-1"
                            repo = git.Repo(repo_dir)
                            await ctx.channel.send("Pulling from git...")
                            await printlog("Pulling from git...")
                            try:
                                directory = repo_dir
                                directory = git.cmd.Git(directory)
                                try:
                                    directory.stash('save')  # Stash local changes
                                except Exception as e:
                                    await printlog(f"Potential Error during stash save: ```{e}```")
                                try:
                                    directory.pull()
                                except Exception as e:
                                    await ctx.channel.send(f"Error during git pull: {e}")
                                    await printlog(f"Error during git pull: {e}")
                                    return
                                try:
                                    directory.stash('pop')  # Restore stashed changes
                                except Exception as e:
                                    await printlog(f"Potential Error during stash pop: ```{e}```")
                            except Exception as e:
                                await ctx.channel.send(f"Error initializing git: {e}")
                                await printlog(f"Error initializing git: {e}")
                                return

                            try:
                                repo.git.add('trainsets.csv')
                                repo.git.commit('-m', f'Updated train info for {train} via bot by {ctx.user.name}')
                            except Exception as e:
                                await ctx.channel.send(f"Error committing changes: {e}")
                                await printlog(f"Error committing changes: {e}")
                                return

                            try:
                                repo.git.push('origin', 'main')
                            except Exception as e:
                                await ctx.channel.send(f"Error pushing changes to GitHub: {e}")
                                await printlog(f"Error pushing changes to GitHub: {e}")
                                return
                            
                            await ctx.channel.send("Train info updated successfully!")
                            await printlog(f"Train info for {train} updated successfully by {ctx.user.name}")
                        except asyncio.TimeoutError:
                            await ctx.channel.send("response timed out. edit cancelled.")
                    else:
                        await ctx.edit_original_response(content=f"Train `{train}` not found in the database. Please check the train number and try again.")
    else:
        await ctx.edit_original_response(content="Only TrackPulse Vic admins can edit the train database. If you think this is a mistake, please joing the TrackPulse Vic server.\nhttps://discord.gg/nfAqAnceQ5")
        await printlog(f'{str(ctx.user.id)} tried to edit the train info database.')

# ping command
@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)  # Convert latency to ms
    await ctx.send(f"Pong! Latency: {latency} ms")
    log_command(ctx.author.id, 'ping')
    
@bot.command()
async def syncdb(ctx, ):
    if ctx.author.id in admin_users:
        log_command(ctx.author.id, 'sync-db')
        # Download trainsets.csv
        csv_url ='https://victorianrailphotos.com/api/trainsets.csv'
        save_location = "utils/trainsets.csv"
        await ctx.send(f"Downloading trainset data from {csv_url} to {save_location}")
        await printlog(f"Downloading trainset data from {csv_url} to `{save_location}`")
        try:
            await download_csv(csv_url, save_location)
            await ctx.send(f"Success downloading trainsets.csv!")
        except Exception as e:
            await ctx.send(f"Error downloading trainsets.csv: `{e}`")

        # Download tramsets.csv
        tram_url = "https://victorianrailphotos.com/api/tramsets.csv"
        tram_save_location = "utils/tramsets.csv"
        await ctx.send(f"Downloading tramset data from {tram_url} to {tram_save_location}")
        await printlog(f"Downloading tramset data from {tram_url} to `{tram_save_location}`")
        try:
            await download_csv(tram_url, tram_save_location)
            await ctx.send(f"Success downloading tramsets.csv!")
        except Exception as e:
            await ctx.send(f"Error downloading tramsets.csv: `{e}`")

        # Download bussets.csv
        bus_url = "https://victorianrailphotos.com/api/bussets.csv"
        bus_save_location = "utils/bussets.csv"
        await ctx.send(f"Downloading busset data from {bus_url} to {bus_save_location}")
        await printlog(f"Downloading busset data from {bus_url} to `{bus_save_location}`")
        try:
            await download_csv(bus_url, bus_save_location)
            await ctx.send(f"Success downloading bussets.csv!")
        except Exception as e:
            await ctx.send(f"Error downloading bussets.csv: `{e}`")
    else:
        await printlog(f'{str(ctx.author.id)} tried to sync the database.')
        await ctx.send("You are not authorized to use this command.")

@bot.command()
async def synclists(ctx):
    if ctx.author.id in admin_users:
        log_command(ctx.author.id, 'sync-lists')
        await printlog("Downloading stop name data from TV")
        await ctx.send("Downloading stop name data from TV")
        try:
            downloader_function(0)
            await ctx.send("Metro stop data downloaded")
            downloader_function(1)
            await ctx.send("Tram stop data downloaded")
            downloader_function(2)
            await ctx.send("Bus stop data downloaded")
            downloader_function(3)
            await ctx.send("V/Line stop data downloaded")
            await ctx.send("Success!")
        except Exception as e:
            await ctx.send(f"Error: `{e}`")

    else:
        await printlog(f'{str(ctx.author.id)} tried to update stop data.')
        await ctx.send("You are not authorized to use this command.")

@bot.command()
async def restart(ctx):
    if ctx.author.id in admin_users:
        log_command(ctx.author.id, 'restart')
        await ctx.send(f"Restarting bot")
        await printlog("Restarting bot")
        
        with open('restart.txt', 'w') as file:
            file.write(str(ctx.channel.id))
        await bot.close()
        await stop_webserver()
        os.system('python bot.py')

    else:
        await printlog(f'{str(ctx.author.id)} tried to restart the bot.')
        await ctx.send("You are not authorized to use this command.")

@bot.command()
async def maintenancemode(ctx):
    if ctx.author.id in admin_users:
        log_command(ctx.author.id, 'maintenance')
        await ctx.send(f"Toggling Maintenance Mode")
        await printlog("Toggling Maintenance Mode")
        global MAINTENANCE_MODE
        MAINTENANCE_MODE = not(MAINTENANCE_MODE)
        if MAINTENANCE_MODE:
            with open('maintenance.txt', 'w') as file:
                file.write(":3")
            await ctx.send(f"Maintenance Mode On")
            await printlog("Maintenance Mode On")
        else:
            with open('maintenance.txt', 'w') as file:
                file.write("")
            await ctx.send(f"Maintenance Mode Off")
            await printlog("Maintenance Mode Off")

    else:
        await printlog(f'{str(ctx.author.id)} tried to toggle maintenance mode.')
        await ctx.send("You are not authorized to use this command.")

@bot.command()
async def maintenancequery(ctx):
    log_command(ctx.author.id, 'maintenance')
    if MAINTENANCE_MODE:
        await ctx.send(f"Maintenance Mode On")
        await printlog("Maintenance Mode On")
    else:
        await ctx.send(f"Maintenance Mode Off")
        await printlog("Maintenance Mode Off")


@bot.command()
async def shutdown(ctx):
    if ctx.author.id in admin_users:
        log_command(ctx.author.id, 'shutdown')
        await ctx.send(f"Shutting down bot")
        await printlog("Shutting down bot")
        
        await bot.close()
        await stop_webserver()

    else:
        await printlog(f'{str(ctx.author.id)} tried to shutdown the bot.')
        await ctx.send("You are not authorized to use this command.")

@bot.command()
async def update(ctx):
    if automatic_updates == True:
        if ctx.author.id in admin_users:
            log_command(ctx.author.id, 'update')
            await ctx.send("Updating bot...")
            await printlog("Pulling from git...")
        
            try:
                directory = Path(__file__).parents[0]
                directory = git.cmd.Git(directory)
                try:
                    directory.stash('save')  # Stash local changes
                except Exception as e:
                    await printlog(f"Potential Error: ```{e}```")
                directory.pull()
                try:
                    directory.stash('pop')  # Restore stashed changes
                except Exception as e:
                    await printlog(f"Potential Error: ```{e}```")

                await ctx.send("The bot has successfully been updated, restart to apply changes.")
                await printlog('Successfully updated bot')
            except Exception as e:
                await ctx.send(f"Update Failed. Error:\n```{e}```")
                await printlog(f"Update Failed. Error:\n```{e}```")

        else:
            await printlog(f'{str(ctx.author.id)} tried to update the bot.')
            await ctx.send("You are not authorized to use this command.")
    else:
        await ctx.send("Remote updates are not enabled")

@bot.command()
async def deletecache(ctx):
    if ctx.author.id in admin_users:
        log_command(ctx.author.id, 'deletecache')
        await ctx.send(f"Deleting Cache")
        await printlog("Deleting Cache")
        folder_path = "cache"
        for filename in os.listdir(folder_path): 
            file_path = os.path.join(folder_path, filename)  
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)  
                elif os.path.isdir(file_path):  
                    os.rmdir(file_path)  
            except Exception as e:  
                print(f"Error deleting {file_path}: {e}")
        await ctx.send("The cache has successfully been deleted")
        await printlog('Deletion Done')
    else:
        await printlog(f'{str(ctx.author.id)} tried to delete the cache.')
        await ctx.send("You are not authorized to use this command.")
        
# thing to notify of errors:
# @bot.event
# async def on_command_error(ctx, error):
#     log_channel = bot.get_channel(STARTUP_CHANNEL_ID)
#     if not isinstance(error, commands.CommandNotFound):
#         await log_channel.send(f"{str(error)}\n<@780303451980038165>")
#         await ctx.channel.send(f"An error occurred: {str(error)}")
        
#     await log_channel.send(f"{str(error)}")

# important
bot.run(BOT_TOKEN)
