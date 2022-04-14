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

# load slisteners
if os.path.isfile('/saves/bannotif/listeners.p'):
    with open('/saves/bannotif/listeners.p', 'rb') as f:
        bot.listeners_ = pickle.load(f)
else:
    bot.listeners_ = []
    
# load subscribers
if os.path.isfile('/saves/bannotif/subscribers.p'):
    with open('/saves/bannotif/subscribers.p', 'rb') as f:
        bot.subscribers_ = pickle.load(f)
else:
    bot.subscribers_ = []
    

# print details of the bot and load extensions
@bot.event
async def on_ready():
    # load extensions
    extensions = ['commands', 'listeners']
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.')
            traceback.print_exc()
    # print details of the bot
    print('Logged in as')
    print(f'bot name: {bot.user.name}')
    print(f'bot id: {bot.user.id}')
    print(f'prefix: {prefix}')
    print(f'connected to: {len(bot.guilds)} servers')
    print(f"admins: {', '.join(str(x) for x in admins)}" if admins else 'no admins')
    print(f"devs: {', '.join(str(x) for x in devs)}" if devs else 'no devs')
    print(f"commands: {', '.join(x.name for x in bot.commands)}")
    print(f"loaded modules: {', '.join(x for x in extensions)}\n")
    print('------')

#run the bot
bot.run(token)