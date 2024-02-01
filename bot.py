import discord


"""
This section defines the intents that the bot will use
as well as logging into the bot and returning to the console which bot was logged into

When you run the client via the command line, you should see the following output:
Logged in as <insert bot name>
"""
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
owner = 97355249395716096

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.author.id == owner and message.content.startswith('ping'):
        await message.channel.send('pong')
        return 'owner said ping'

#Client run command, hide token in a seperate config file that will not be uploaded to github
client.run('MTIwMTcwNjUwNTQ4MTc0ODUxMQ.GUrx0H.Q8riBO8Cv9fn9DcKf-Sb1j1KZJCcBMY-BjxNrw')