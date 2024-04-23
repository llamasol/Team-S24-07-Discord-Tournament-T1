# Team-S24-07-Discord-Tournament-T1
 KSU Capstone Project. Project is to create a Discord bot that can perform administrative procedures for running a tournament, as well as tracking player data using game's api

# How to setup the Discord Bot

To setup the discord bot you will need a couple of things.
Before you begin, you will need a file named .env (just like that nothing else) in the same folder as the bot.py file
Within the .env file you will need to put the following things
BOT_TOKEN =
GUILD_TOKEN = 
GOOGLE_SHEETS_ID = 
GOOGLE_SHEETS_NAME = 
The bot token will be the discord bot token that you create on the discord developer dashboard. 


# How to make the discord bot token

You need to go to https://discord.com/developers/applications and create a new developer application.
 
You will be asked to name it and agree to the ToS
Once made, you will be greeted with this page
 
On the side bar, there is an option called bot, click that and it will allow you to build the bot for the application.
 
To get the bot token, you must click reset token.
This will display a token and you will copy paste that token into the .env file
It should look like BOT_TOKEN = ‘insert bot token here’

# How to get the guild token

This one is a lot simpler, you need to go to your discord client, enable discord developer mode, right click the server you want to use the bot in, then click copy server id
 
In case of the KSU League of Legends Discord Server, the ID is 752309075798392852
So it should look like GUILD_TOKEN = 752309075798392852

# How to get Sheet ID and Sheet name

The sheet id is just the ID of the google sheet that you are trying to use. To find it, all you need to do is look at the url of your google sheet. You can find the id here in the URL:
docs.google.com/spreadsheets/d/ID_IS_HERE/
Sheet name should be self-explanatory, it is just the name of the google spreadsheet

# How to setup Google API access
Google makes a good enough tutorial on how to set it up, please read up here.
https://developers.google.com/sheets/api/quickstart/python
Installation of Packages
The Required Packages for this bot to be ran on a computer are the following:
asyncio
discord
itertools
gspread
dotenv
google api
The google API package installation is found in the link on how to setup google api access. 
To install the other packages, run pip3 install <package name> and it should install the package. Do this for all the packages and you should be good to move on

# Final setup for the bot

In the src folder, there is a file called credentials, this file will need to be stored there along with in the following location on the user of the bot: ~/.config/gspread (these instructions are for linux installation.) 
From there, when you run a command that accesses the google sheet, you will need to sign into google. This is a one-time setup and should not be necessary to do once more. If everything works, the bot should be good to run. (It will bring up a browser tab to sign into google, sign in to the google account with the API key and the google account that has access to the spreadsheet)
As the bot is made with python, using any terminal to start the bot with python3 bot.py should work perfectly fine.


![image](https://github.com/llamasol/Team-S24-07-Discord-Tournament-T1/assets/156405890/e6f5d887-9355-451d-96dd-f38ec6a5aafd)

