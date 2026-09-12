import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def getids(ctx, *usernames: str):
    if not usernames:
        return await ctx.send("Provide usernames.")

    results = []
    for name in usernames:
        member = discord.utils.get(ctx.guild.members, name=name.lower())
        if member:
            results.append(f"{name}: {member.id}")
        else:
            results.append(f"{name}: Not found")

    await ctx.send("\n".join(results))

# bot.run("")
# bot token there