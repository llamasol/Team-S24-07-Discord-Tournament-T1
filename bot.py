import discord
import os
from dotenv import load_dotenv, find_dotenv
from discord import app_commands

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
tree = app_commands.CommandTree(client)
owner = 97355249395716096
token = os.getenv('TOKEN')



@tree.command(
    name="ping",
    description="Ping maybe?",
    guild=discord.Object(id=1197932384348295249)
)
async def first_command(interaction):
    await interaction.response.send_message("Pong!")

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=1197932384348295249))
    print(f'Logged in as {client.user}')

#little connection test message response system
@client.event
async def on_message(message):
    if message.author == client.user and message.content.startswith('ping'):
        await message.channel.send('Why are you signed into the bot on discord...')
        return
    if message.author.id == owner and message.content.startswith('ping'):
        await message.channel.send('pong')
        print(f'owner said ping')
        return 'owner said ping'

#Checkin button class for checking in to tournaments.
class CheckinButtons(discord.ui.View):
    def __init__(self, *, timeout = 900):
        super().__init__(timeout = timeout)

    #Button to check-in.
    @discord.ui.button(
            label = "Check-In",
            style = discord.ButtonStyle.green)
    async def checkin(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        await interaction.response.edit_message(view = self)
        await interaction.followup.send('You have checked in!', ephemeral = True)

    #Button to rejoin the tournament in case someone had to leave.
    @discord.ui.button(
            label = "Leave",
            style = discord.ButtonStyle.red)
    async def leave(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        await interaction.response.edit_message(view = self)
        await interaction.followup.send('Sorry to see you go.', ephemeral = True)

#Recheck button class for volunteering to sit out of a tournament or rejoin a tournament.
class RecheckButtons(discord.ui.View):
    def __init__(self, *, timeout = 900):
        super().__init__(timeout = timeout)

    #Button to Volunteer to sit out of the tournament.
    @discord.ui.button(
            label = "Volunteer",
            style = discord.ButtonStyle.grey)
    async def volunteer(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        await interaction.response.edit_message(view = self)
        await interaction.followup.send('Thank you for volunteering!', ephemeral = True)
    
    #Button to rejoin the tournament in case someone had to leave.
    @discord.ui.button(
            label = "Rejoin",
            style = discord.ButtonStyle.blurple)
    async def rejoin(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        await interaction.response.edit_message(view = self)
        await interaction.followup.send('Welcome back to the game!', ephemeral = True)

#Checkin button command.
@tree.command(
        name = 'checkin',
        description = 'Initiate Tournament Check-In.',
        guild = discord.Object(id=1197932384348295249))
async def checkin(interaction):
        view = CheckinButtons()
        await interaction.response.send('Check-In for the tournament has started! You have 15 minutes to check-in.', view = view)

#Recheck button command.
@tree.command(
        name = 'recheck',
        description = 'Allow users to volunteer out or rejoin a match.',
        guild = discord.Object(id=1197932384348295249))
async def checkin(interaction):
        view = RecheckButtons()
        await interaction.response.send('Players needed to either volunteer or rejoin to balance teams.', view = view)

#Toxicity command.
@tree.command(
     name = 'toxicity',
     description = 'Give a player one point of toxicity.',
     guild = discord.Object(id=1197932384348295249))
async def toxicity(ctx, user: discord.Member, message: str):
     user = await client.get_user(user.id)
     await user.send(f'{message}')

#starts the bot
client.run(token)