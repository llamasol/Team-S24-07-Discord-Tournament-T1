import discord
import os
from dotenv import load_dotenv, find_dotenv
from discord import app_commands
from discord.utils import get


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


#Command to start check-in
@tree.command(
        name = 'checkin',
        description = 'Initiate Tournament Check-In.',
        guild = discord.Object(id=1197932384348295249))
async def checkin(interaction):
        view = CheckinButtons()
        await interaction.response.send_message('Check-In for the tournament has started! You have 15 minutes to check-in.', view = view)




#starts the bot
client.run(token)