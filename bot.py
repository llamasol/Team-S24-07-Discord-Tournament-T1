import discord
import os
from dotenv import load_dotenv, find_dotenv

"""
This section defines the intents that the bot will use
as well as logging into the bot and returning to the console which bot was logged into

When you run the client via the command line, you should see the following output:
Logged in as <insert bot name>
"""

load_dotenv(find_dotenv())
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
owner = 97355249395716096
token = os.getenv('TOKEN')


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')


#little connection test message response system
@client.event
async def on_message(message):
    if message.author == client.user and message.content.startswith('ping'):
        await message.channel.send('Why are you signed into the bot on discord...')
        return
    if message.author.id == owner and message.content.startswith('ping'):
        await message.channel.send('pong')
        return 'owner said ping'

#starts the bot
client.run(token)