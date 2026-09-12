from calendar import c
from math import e
from cycler import V
from discord.ext import commands
import discord
from re import A
import os
import builtins

import sys

sys.stdout = sys.__stdout__ 

original_open = builtins.open

# Utils imports
from utils.favourites.viewer import *
from utils.search import *
from utils.colors import *
from utils.stats.stats import *

# trainlogger imports
from utils.trainlogger.main import *
from utils.trainset import *
from utils.trainlogger.stats import *
from utils.trainlogger.ids import *
from utils.lines_dictionaries import *
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

print("""TrackPulse Vic Copyright (C) 2024  Billy Evans
    This program comes with ABSOLUTELY NO WARRANTY.
    This is free software, and you are welcome to redistribute it
    under certain conditions""")

# ENV READING
config = dotenv_values(".env")

BOT_TOKEN = config['BOT_TOKEN']
STARTUP_CHANNEL_ID = int(config['STARTUP_CHANNEL_ID']) # channel id to send the startup message
USER_ID = config['USER_ID']

bot = commands.Bot(command_prefix=commands.when_mentioned, intents=discord.Intents.default())
log_channel = bot.get_channel(STARTUP_CHANNEL_ID)

async def printlog(text):
    print(text)
    if len(str(text)) < 1000:
        log_channel = bot.get_channel(STARTUP_CHANNEL_ID)
        await log_channel.send(text)

admin_users = [1002449671224041502, 780303451980038165, 634620519500480512, 581098452327464973, 637885403101396994, 1065872885559861289, int(USER_ID)]
start_users = admin_users + [916060846139002940, 1166317869911511053, 746614482205278229, 997746009318891603, 1034204165326524448]
if config['DEVS_TO_HAVE_ADMIN_ACCESS'] == 'OFF':
    admin_users = [int(USER_ID)]

os.spawnl(os.P_NOWAIT, sys.executable, 'python', 'bot.py')

@bot.command()
async def megaping(ctx):
    latency = round(bot.latency * 1000)  # Convert latency to ms
    await ctx.send(f"Pong! Backup program operational! Latency: {latency} ms")
    log_command(ctx.author.id, 'ping')

@bot.command()
async def start(ctx):
    if ctx.author.id in start_users:
        log_command(ctx.author.id, 'start')
        await ctx.send(f"Starting bot")
        await printlog("Starting bot")

        os.spawnl(os.P_NOWAIT, sys.executable, 'python3', 'bot.py')

        await ctx.send(f"Started")
        await printlog("Started")

    else:
        await printlog(f'{str(ctx.author.id)} tried to start the bot.')
        await ctx.send("You are not authorized to use this command.")

@bot.command()
async def kill(ctx):
    if ctx.author.id in admin_users:
        log_command(ctx.author.id, 'kill')
        await ctx.send(f"Shutting down bot (for realsies)")
        await printlog("Shutting down bot (for realsies)")
        
        await bot.close()

    else:
        await printlog(f'{str(ctx.author.id)} tried to kill the bot.')
        await ctx.send("You are not authorized to use this command.")

# important
bot.run(BOT_TOKEN)