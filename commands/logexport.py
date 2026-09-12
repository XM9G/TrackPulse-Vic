import discord
import os

from utils.xmltest import convertLogsToXML

async def logExport(ctx, format:str, mode:str, hidemessage:bool=False):
    username = ctx.user.name
    userid = ctx.user.id
    if mode == 'train':
        filepath = f"utils/trainlogger/userdata/{username}.csv"
        fileid = f"utils/trainlogger/userdata/{userid}.csv"
    else:
        filepath = f"utils/trainlogger/userdata/{mode}/{username}.csv"
        fileid = f"utils/trainlogger/userdata/{mode}/{userid}.csv"
    
    if not os.path.exists(fileid):
        print(f"userid doesn't exist, using username: {filepath}")
    else:
        print(f"userid does exist, using userid: {fileid} (belonging to {username})")
        filepath = fileid
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"No {mode} logs found for {username}")
    
    if format == 'csv':
        file = discord.File(filepath)
    elif format == 'md':
        file = exportMarkdown(ctx, filepath, mode)
    elif format == 'xml':
        file = exportXML(ctx,filepath,mode)
    else:
        raise ValueError(f"Unsupported format: {format}")
        
    await ctx.response.send_message(content=f'Here is your {format} file:', file=file, ephemeral=hidemessage)

def exportMarkdown(ctx, filepath, mode):
    # Read the CSV file
    with open(filepath, 'r') as file:
        lines = file.readlines()
    
    # Create markdown table header
    markdown = "| Trip ID | Train Set | Train Type | Date | Line | From | To | Notes |\n"
    markdown += "|---------|-----------|------------|------|------|------|-----|-------|\n"
    
    # Process each line and add to markdown table
    for line in lines:
        # Split the CSV line by comma
        parts = line.strip().split(',')
        # Create table row with basic info
        row = f"| {parts[0]} | {parts[1]} | {parts[2]} | {parts[3]} | {parts[4]} | {parts[5]} | {parts[6]} |"
        
        # Add notes if they exist (8th column)
        if len(parts) >= 8 and parts[7]:
            row += f" {parts[7]} |"
        else:
            row += " |"
            
        markdown += row + "\n"
    
    # Create markdown file
    username = ctx.user.name
    markdown_filepath = f'temp/{username}-{mode}-export.md'
    
    with open(markdown_filepath, 'w') as file:
        file.write(markdown)
    
    # Send the markdown file
    file = discord.File(markdown_filepath)
    return file

def exportXML(ctx, filepath, mode):
    return(discord.File(convertLogsToXML(filepath, f'{ctx.user.name}-{mode}-export')))
    