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

#Button class for checking in to tournaments.
class Buttons(discord.ui.View):
    def __init__(self, *, timeout = 900):
        super().__init__(timeout = timeout)

    #Button to check-in.
    @discord.ui.button(
            label = "Check-In",
            style = discord.ButtonStyle.green)
    async def checkin(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        await interaction.response.send_message(view = self)
        await interaction.followup.send_message('You have checked in!', ephemeral = True)

    #Button to Volunteer to sit out of the tournament.
    @discord.ui.button(
            label = "Volunteer",
            style = discord.ButtonStyle.grey)
    async def volunteer(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        await interaction.response.send_message(view = self)
        await interaction.followup.send_message('Thank you for volunteering!', ephemeral = True)

    #Button to rejoin the tournament in case someone had to leave.
    @discord.ui.button(
            label = "Leave",
            style = discord.ButtonStyle.red)
    async def leave(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        await interaction.response.send_message(view = self)
        await interaction.followup.send_message('Sorry to see you go.', ephemeral = True)

    #Button to rejoin the tournament in case someone had to leave.
    @discord.ui.button(
            label = "Rejoin",
            style = discord.ButtonStyle.blurple)
    async def rejoin(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        await interaction.response.send_message(view = self)
        await interaction.followup.send_message('Welcome back to the game!', ephemeral = True)

#Button command.
@tree.command(
        name = 'checkin',
        description = 'Initiate Tournament Check-In.',
        guild = discord.Object(id=1197932384348295249))
async def checkin(interaction):
        view = Buttons()
        await interaction.response.send_message('Check-In for the tournament has started! You have 15 minutes to check-in.', view = view)

#starts the bot
client.run(token)