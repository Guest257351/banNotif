import discord
from discord.ext import commands
import logging
import traceback
import pickle
import os
from config import token, prefix, admins, devs # import settings

#setup logger
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# make developers admins
admins.extend(devs)

# allow members intent
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# initialize bot
bot = commands.Bot(command_prefix=prefix, 
                   description='A bot for notifying admins/mods when a user banned in a different server joins.', 
                   case_insensitive=True,
                   intents=intents)
notify = 963294857684713484
bannedRole = 963295496758231050


# main function
@bot.event
async def on_member_join(member):
    try:
        # check if the user is banned
        guild = await bot.fetch_guild(888271198537023509)
        ban = await guild.fetch_ban(member)
    except discord.NotFound:
        # if the user is not banned, do nothing
        return
    else:
        # if the user is banned send messages to users in notify list
        embed = discord.Embed(title='Banned user joined', description=f'{member.name} ({member.id}) joined {member.guild.name} and was banned in {guild.name} with reason: {ban.reason}', color=0xFF0000)
        channel = bot.get_channel(notify)
        if channel is not None:
            await channel.send(embed=embed)
        else:
            channel = await bot.fetch_channel(notify)
            await channel.send(embed=embed)
        await member.add_roles(member.guild.get_role(bannedRole))
                
                
# command to scan all users in the server and check if they are banned in the 2nd server
@bot.command(name='scan', help='Scan all users in the server and check if they are banned in the 2nd server.')
@commands.has_permissions(administrator=True)
async def scan(ctx):
    message = await ctx.send('Scanning and applying roles... (this may take a while)')
    guild = await bot.fetch_guild(888271198537023509)
    async with ctx.typing():
        for user in ctx.guild.members:
            try:
                # check if the user is banned
                ban = await guild.fetch_ban(user)
            except discord.NotFound:
                # if the user is not banned, do nothing
                pass
            else:
                # if the user is banned give them the banned role
                await user.add_roles(ctx.guild.get_role(bannedRole))
    await ctx.send(content='Done!')
            

# print details of the bot
@bot.event
async def on_ready():
    print('Logged in as')
    print(f'bot name: {bot.user.name}')
    print(f'bot id: {bot.user.id}')
    print(f'prefix: {prefix}')
    print(f'connected to: {len(bot.guilds)} servers')
    print(f"admins: {', '.join(str(x) for x in admins)}" if admins else 'no admins')
    print(f"devs: {', '.join(str(x) for x in devs)}" if devs else 'no devs')
    print(f"commands: {', '.join(x.name for x in bot.commands)}")
    print('------')

#run the bot
bot.run(token)