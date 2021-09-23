import discord
from discord.ext import commands
from stay_alive import keep_alive

import os

# Getting the information of new members
intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix="-", intents= intents)

# -------------Get contants key--------------
TOKEN = os.getenv('TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))
CHANNEL_LOG_ID = int(os.getenv('CHANNEL_LOG_ID'))
exten = ["cogs.leveling","cogs.tracking"]

# --------------Connect Bot ---------------
@bot.event
async def on_ready():
  print('Bot đã sẵn sàng.')
  # -------Sync Extention-----
  for cog in exten:
     try:
       bot.load_extension(cog)
       print(f'{cog} was loaded!')
     except Exception as e:
       print('ERROR: '+str(e))

# -------Run Bot---------
keep_alive()
bot.run(TOKEN)