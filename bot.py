import discord
import os
from dotenv import load_dotenv, find_dotenv
from discord import app_commands
from discord.utils import get
import asyncio
import requests
from discord.ext import commands

"""
This section defines the intents that the bot will use
as well as logging into the bot and returning to the console which bot was logged into

When you run the client via the command line, you should see the following output:
Logged in as <insert bot name>
"""

load_dotenv(find_dotenv())
intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
owner = 97355249395716096
token = os.getenv('TOKEN')
riot_key="RGAPI-e09b0e22-5e18-4760-aff9-bb6d723b872a"

#Global variables to help with the bot functionality
isCheckinActive = False


#Logs the bot into discord
@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=1197932384348295249))
    print(f'Logged in as {client.user}')

#Checkin button class for checking in to tournaments.
class CheckinButtons(discord.ui.View):
    def __init__(self, *, timeout = 900):
        super().__init__(timeout = timeout)
    """
    This button is a green button that is called check in
    When this button is pulled up, it will show the text "Check-In"

    The following output when clicking the button is to be expected:
    If the user already has the player role, it means that they are already checked in.
    If the user doesn't have the player role, it will give them the player role. 
    """
    @discord.ui.button(
            label = "Check-In",
            style = discord.ButtonStyle.green)
    async def checkin(self, interaction: discord.Interaction, button: discord.ui.Button):

        player = get(interaction.guild.roles, id=1205644117657391114)
        member = interaction.user

        if player in member.roles:
            await interaction.response.edit_message(view = self)
            await interaction.followup.send('You have already checked in.', ephemeral=True)
            return "Is already checked in"
        await member.add_roles(player)
        await interaction.response.edit_message(view = self)
        await interaction.followup.send('You have checked in!', ephemeral = True)
        return "Checked in"
            

    """
    This button is the leave button. It is used for if the player checked in but has to leave
    The following output is to be expected:

    If the user has the player role, it will remove it and tell the player that it has been removed
    If the user does not have the player role, it will tell them to check in first.
    """
    @discord.ui.button(
            label = "Leave",
            style = discord.ButtonStyle.red)
    async def leave(self, interaction: discord.Interaction, button: discord.ui.Button):



        player = get(interaction.guild.roles, id=1205644117657391114)
        member = interaction.user

        if player in member.roles:
            await member.remove_roles(player)
            await interaction.response.edit_message(view = self)
            await interaction.followup.send('Sorry to see you go.', ephemeral = True)
            return "Role Removed"
        await interaction.response.edit_message(view = self)
        await interaction.followup.send('You have not checked in. Please checkin first', ephemeral = True)
        return "Did not check in yet"



class volunteerButtons(discord.ui.View):
    def __init__(self, *, timeout = 900):
        super().__init__(timeout = timeout)
    """
    This button is a green button that is called check in
    When this button is pulled up, it will show the text "Volunteer"

    The following output when clicking the button is to be expected:
    If the user already has the volunteer role, it means that they are already volunteered.
    If the user doesn't have the volunteer role, it will give them the volunteer role. 
    """
    @discord.ui.button(
            label = "Volunteer",
            style = discord.ButtonStyle.green)
    async def checkin(self, interaction: discord.Interaction, button: discord.ui.Button):

        volunteer = get(interaction.guild.roles, id=1205644141543817296)
        member = interaction.user

        if volunteer in member.roles:
            await interaction.response.edit_message(view = self)
            await interaction.followup.send('You have already volunteered to sit out, if you wish to rejoin click rejoin.', ephemeral=True)
            return "Is already checked in"
        await member.add_roles(volunteer)
        await interaction.response.edit_message(view = self)
        await interaction.followup.send('You have volunteered to sit out!', ephemeral = True)
        return "Checked in"
            

    """
    This button is the leave button. It is used for if the player who has volunteer wants to rejoin
    The following output is to be expected:

    If the user has the player role, it will remove it and tell the player that it has been removed
    If the user does not have the volunteer role, it will tell them to volunteer first.
    """
    @discord.ui.button(
            label = "Rejoin",
            style = discord.ButtonStyle.red)
    async def leave(self, interaction: discord.Interaction, button: discord.ui.Button):



        
        volunteer = get(interaction.guild.roles, id=1205644141543817296)
        member = interaction.user

        if volunteer in member.roles:
            await member.remove_roles(volunteer)
            await interaction.response.edit_message(view = self)
            await interaction.followup.send('Welcome back in!', ephemeral = True)
            return "Role Removed"
        await interaction.response.edit_message(view = self)
        await interaction.followup.send('You have not volunteered to sit out, please volunteer to sit out first.', ephemeral = True)
        return "Did not check in yet"

#Command to start check-in
@tree.command(
        name = 'checkin',
        description = 'Initiate Tournament Check-In.',
        guild = discord.Object(id=1197932384348295249)
        )
async def checkin(interaction):
        global isCheckinActive

        if isCheckinActive:
            isCheckinActive = False
            
            await volunteercheck(interaction)
            

        else:
            isCheckinActive = True
            view = CheckinButtons()
            await interaction.response.send_message('Check-In for the tournament has started! You have 10 minutes to check-in.', view = view)


            #starts a 10 minute timer to automatically start the volunteer check
            await asyncio.create_task(handleCheckin(interaction))


        


#Command to start volunteer
@tree.command(
    name='volunteercheck',
    description='initiate check for volunteers',
    guild= discord.Object(1197932384348295249)
)
async def volunteercheck(interaction):
    view = volunteerButtons()
    await interaction.response.send_message('The Volunteer check has started! You have 10 minutes to volunteer if you wish to sit out', view = view)


#Helper function to allow us to wait for the checkin timer to go through. 
async def handleCheckin(interaction):
    await asyncio.sleep(10)

    global isCheckinActive
    if isCheckinActive:
        isCheckinActive = False
        await getPreviousMessageAndDelete()
        await volunteercheck(interaction)

    
#Should get the previous message and delete it
async def getPreviousMessageAndDelete():
    channel = client.get_channel(1206780036498194443)

    async for message in channel.history():
        if message.author.id == 1201706505481748511:
            await message.delete()
            break


async def get_player_stats(summoner_id):
    api_summoner_by_name="https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"+summoner_id+"?api_key="+riot_key
    resp = requests.get(api_summoner_by_name)
    encrypted_id=resp.json()['id']
    api_rank_by_id="https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/"+encrypted_id+"?api_key="+riot_key
    resp=requests.get(api_rank_by_id)
    return resp.json()[0]['tier'], resp.json()[0]['rank']

#starts the bot
client.run(token)