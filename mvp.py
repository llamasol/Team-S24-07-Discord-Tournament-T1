import discord
from discord.ext import commands

# Create a bot instance with a command prefix
bot = commands.Bot(command_prefix='/')

# Data structure to store votes
votes = {}

@bot.event
async def on_message(message):
    # Avoid processing messages from bots to prevent recursion
    if message.author.bot:
        return

    # Process commands
    await bot.process_commands(message)

@bot.command(name='mvp')
async def vote_mvp(ctx, *, player_name):
    # Check if the user has already voted
    if ctx.author.id in votes:
        await ctx.send('You have already voted. You cannot vote again.')
        return

    # Update the vote count for the specified player
    player_name_lower = player_name.lower()
    votes[player_name_lower] = votes.get(player_name_lower, 0) + 1

    await ctx.send(f'Vote for {player_name} recorded.')

@bot.command(name='mvpresult')
async def mvp_result(ctx):
    # Sort players based on vote counts
    sorted_players = sorted(votes.items(), key=lambda x: x[1], reverse=True)

    if not sorted_players:
        await ctx.send('No votes recorded yet.')
        return

    # Display MVP and votes
    mvp_player, mvp_votes = sorted_players[0]
    await ctx.send(f'The MVP is {mvp_player} with {mvp_votes} votes.')

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot.run('YOUR_BOT_TOKEN')
