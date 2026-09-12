import asyncio
import csv
import os
import discord
from utils.checktype import trainType
from utils.colors import getMapEmoji
from utils.locationFromNumber import GTFSgetTrainLocation, convertTrainLocationToGoogle, getTrainLocation, makeMapv2
from utils.photo import getPhotoCredits
from utils.routeName import get_route_name
from utils.search import trainData
from utils.stats.stats import log_command
from utils.stoppingpattern import getStoppingPatternFromCar
from utils.trainImage import getIcon, getImage
from utils.trainlogger.stats import checkTrainRidden
from utils.trainset import setNumber
from utils.unixtime import convert_iso_to_unix_time, convert_times

async def addmap(embed_update, mapEmbedUpdate, train, set, type, interchange_stations):
    try:
        # Generate the map asynchronously
        # After map generation, send it
        if type == "HCMT": # because ptv api lists hcmts like "9005M-9905M" for some fucking reason
            hcmtcar1 = set.split('-')
            location = getTrainLocation(hcmtcar1[0]+'M')
        else:
            location = getTrainLocation(set)
        line = ""
        print(f"Location: {location}")
        url = convertTrainLocationToGoogle(location)
        try:
            stoppingPattern = getStoppingPatternFromCar(location)
        except Exception as e:
            await embed_update.reply(content=f'An error has occurred while searching for this trains run.')
        print(f"STOPPING PATTERN: {stoppingPattern}")
        try:
            if location is not None:
                for item in location:
                    latitude = item['vehicle_position']['latitude']
                    longitude = item['vehicle_position']['longitude']
                    line = get_route_name(item['route_id'])
                    geopath=''
                    # geopath = getGeopath(item["run_ref"])
                    # print(f'geopath: {geopath}')

                await makeMapv2(latitude,longitude, train, geopath) 
        except Exception as e:
            await mapEmbedUpdate.edit(content='No trip data available.', embed=None)
            print(f'ErROR: {e}')
            return
        file_path = f"temp/{train}-map.png"
        if os.path.exists(file_path):
                file = discord.File(file_path, filename=f"{train}-map.png")
                class RunContainer(discord.ui.Container):
                    heading = discord.ui.TextDisplay(f'## {train}\'s current trip')

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

                        if currentFieldLength + len(stopEntry) > 4000:
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
                    
                    mapGallery = discord.ui.MediaGallery(discord.MediaGalleryItem(f'attachment://{train}-map.png'))
                    footer = discord.ui.TextDisplay('-# Maps © Thunderforest, Data © OpenStreetMap contributors')

                # Delete the old message
                await mapEmbedUpdate.delete()
                
                # Send a new message with the file and embed
                class RunView(discord.ui.LayoutView):
                    container = RunContainer(id=2)
                await embed_update.reply(file=file, view=RunView())
        else:
            await mapEmbedUpdate.delete()
            await embed_update.reply(content=f"Error: Map file '{file_path}' not found.")
            print(f"Error: Map file '{file_path}' not found.")
    except Exception as e:
        await embed_update.reply(f'There was an error generating the map:\n```{e}```')
        print(f'Error:\n```{e}```')  

async def searchTrainCommand(ctx, train: str, hide_run_info:bool=False, metro_colour=0x0072ce, vline_colour=0x8f1a95, ptv_grey=0x333434, interchange_stations=None,lines_dictionary_main=None):
    await ctx.response.defer()
    
    log_command(ctx.user.id, 'train-search')
    # await ctx.response.send_message(f"Searching, trip data may take longer to send...")
    channel = ctx.channel
    type = trainType(train)
    set = setNumber(train.upper())
    
    metroTrains = ['HCMT', "X'Trapolis 100", 'Alstom Comeng', 'EDI Comeng', 'Siemens Nexas', "X'Trapolis 2.0"]
    vlineTrains = ['VLocity', 'Sprinter', 'N Class']
   
    print(f'set: {set}')
    print(f"TRAINTYPE {type}")
    
    # get colour for the embed
    if type in metroTrains:
        colour = metro_colour
    elif type in vlineTrains:
        colour = vline_colour
    else:
        colour = None
    
    if type is None or set is None:
       await ctx.edit_original_response(content="Train not found")
    else:
        # try:
        #     if set.endswith('-'):
        #         set = set[:-1]
        # except:
        #     await ctx.edit_original_response(content="Train not found")
        #     return
        
        # embed = discord.Embed(title=f"{train.upper()}:", color=colour)
        # embed.add_field(name='\u200b', value=f'{setEmoji(type)}\u200b', inline=False) 
        class InfoContainer(discord.ui.Container):
            aboveheading = discord.ui.TextDisplay(f'-# Result for {train.upper()}:')
            heading = discord.ui.TextDisplay(f'# {type} `{set[:-1] if set.endswith("-") else set}`')
            # section = discord.ui.Section(accessory=discord.ui.Thumbnail(getIcon(type))).add_item(discord.ui.TextDisplay("Text in a section"))
            
            try:
            # if type in ["X'Trapolis 2.0", 'HCMT', "X'Trapolis 100", 'Alstom Comeng', 'EDI Comeng', 'Siemens Nexas','VLocity', 'Sprinter', 'N Class', 'Y Class', "T Class", "S Class (Diesel)"]:
                information = trainData(set)
                print(information)
                infoData=''
                if information[5]:
                    infoData+=f'\n- **Name:** {information[5]}\n'
                    
                if information[2]:
                    infoData+=f'- **Entered Service:** {information[2]}\n'
                    
                if information[3]:
                    infoData+=f'- **Status:** {information[3]}\n'
                
                if information[4]:
                    infoData+=f'- **Notes:** {information[4]}\n'
                if information[7]:
                    infoData+=f'- **Interior:** {information[7]}\n'
                
                if information[9]:
                    infoData+=f'- **Operator:** {information[9]}\n'
                
                if information[8]:
                    infoData+=f'- **Gauge:** {information[8]}\n'
                
                if information[1]:
                    liverydisplay = discord.ui.TextDisplay(f'**Livery:** {information[1]}')
                    
            
                fPath = f'utils/trainlogger/userdata/{ctx.user.id}.csv'
                result, log_ids = checkTrainRidden(set, fPath)
                if result:
                    log_ids_str = ', '.join([f'`{id}`' for id in log_ids])
                    infoData += f'\n\nYou have been on this train before (Log IDs: {log_ids_str})'
                    
                infofield = discord.ui.TextDisplay(f'## **Information:**\n{infoData}')
            except Exception as e:
                print(f"Error: {e}")
                infofield = discord.ui.TextDisplay(f'**Information:** None available')
                        
            # train image
            image, credits = getImage(train.upper())

            if image != None:
                galleryPic1 = discord.MediaGalleryItem(image)
                gallery = discord.ui.MediaGallery(galleryPic1)
                seperator1 = discord.ui.Separator()
                sources = discord.ui.TextDisplay(f'-# **Sources:** [{credits} (Photo)](https://victorianrailphotos.com/trains/{train.upper()}), Vicsig & Wikipedia (Other info)')
            else:
                seperator1 = discord.ui.Separator()

                sources = discord.ui.TextDisplay(f'-# **Sources:** Vicsig & Wikipedia (Other info)')
            """
            if type in metroTrains:
                embed.add_field(name='<a:botloading2:1261102206468362381> Loading trip data', value='⠀')
                """
        # send it 
        class TestView(discord.ui.LayoutView):
            container = InfoContainer(id=1, accent_color=colour)

        embed_update = await ctx.edit_original_response(view=TestView())

        if type in metroTrains or type in vlineTrains and not hide_run_info:
            # map thing
            mapEmbed = discord.Embed(title=f"Trip Information for {train.upper()}:", color=metro_colour)
            mapEmbed.add_field(name='<a:botloading2:1261102206468362381> Loading Trip Data', value='⠀')
            mapEmbedUpdate = await ctx.channel.send(file=None, embed=mapEmbed)
        
        
        # Run transportVicSearch in a separate thread
        
        if type in ['HCMT', "X'Trapolis 100", 'Alstom Comeng', 'EDI Comeng', 'Siemens Nexas'] and not hide_run_info:
            asyncio.create_task(addmap(embed_update, mapEmbedUpdate, train.upper(), set, type, interchange_stations))
            # loop = asyncio.get_event_loop()
            # task = loop.create_task(transportVicSearch_async(ctx, train.upper(), embed, embed_update))
            # await task