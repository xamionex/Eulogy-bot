import discord
from discord.ext import commands
import datetime
import random
import json

# set up discord related stuff
prefixvar = "$"
statusinput = input("status:")
activity = discord.Game(name=statusinput)
client = discord.Client()
bot = commands.Bot(
    command_prefix=prefixvar,
    description="This is a Bot made by Wiki and Crow.",
    help_command=None,
    activity=activity,
    status=discord.Status.online
)

# set up non-discord related stuff
eulogy_emoji = "<:eulogy_zero:967096744800296970>" # 967096744800296970 when running, 967740312543965224 when testing

coins = ["It landed on heads!", "It landed on tails!"]
jokes = [    
    "Alien Head."
]

# commands

@bot.command()
async def eulogy(ctx): # send eulogy
    await ctx.message.reply(eulogy_emoji)

@bot.command()
async def eulogycount(ctx): # count the total amount of times eulogy has been said
    # count
    counter = 0

    for channel in ctx.guild.text_channels:
        async for message in channel.history(limit=None):
            if "eulogy" in message.content.lower():
                counter += 1

    await ctx.message.reply(str(counter) + " times.")

@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None): # kick member
    if ctx.message.author.guild_permissions.kick_members:
        await member.kick(reason=reason)

        embed = discord.Embed(
            title="User Kicked",
            description="Kicked user " + str(member),
            timestamp=datetime.datetime.utcnow(),
            color=discord.Color.red()
        )

        embed.add_field(name="Reason", value=str(reason))

        await ctx.message.channel.send(embed=embed)
        await ctx.message.delete()
    else:
        await ctx.message.channel.send("You do not have permission to kick.")

@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None): # ban member
    if ctx.message.author.guild_permissions.ban_members:
        await member.ban(reason=reason)

        embed = discord.Embed(
            title="User Banned",
            description="Banned user " + str(member),
            timestamp=datetime.datetime.utcnow(),
            color=discord.Color.red()
        )

        embed.add_field(name="Reason", value=str(reason))

        await ctx.message.channel.send(embed=embed)
        await ctx.message.delete()
    else:
        await ctx.message.channel.send("You do not have permissions to ban.")

@bot.command()
async def coinflip(ctx): # flip a coin
    await ctx.message.reply(random.choice(coins))

@bot.command()
async def joke(ctx): # send a random joke out of the list
    await ctx.message.reply(random.choice(jokes))

@bot.command()
async def jokerep(ctx, *, jrep): # suggest a joke to add to the bot
    await ctx.message.channel.send(
        "Your joke was recorded. It will be added if Wiki approves it.")
    jokefile = open("jokes.txt", "a")
    jokefile.write("\n" + jrep + "\n")
    jokefile.close
    del jokefile    

@bot.command()
async def fban(ctx, member: discord.Member, *, reason=None):
    if ctx.message.author.guild_permissions.ban_members:
        embed = discord.Embed(title="user banned", description="banned user " + str(member),
            timestamp=datetime.datetime.utcnow(), color=0xf42069)
        embed = discord.Embed(
            title="User Banned",
            description="Banned user " + str(member),
            timestamp=datetime.datetime.utcnow(),
            color=discord.Color.red()
        )

        embed.add_field(name="Reason", value=str(reason))

        await ctx.message.channel.send(embed=embed)
        await ctx.message.delete()
    else:
        await ctx.message.channel.send("You do not have permissions to ban.")

@bot.command()
async def help(ctx): # creates an embed with help for each command
    embed = discord.Embed(
        title="Command Help",
        description="Help for all current commands this discord bot supports.",
        color=0xf42069
    )

    embed.add_field(
        name=f"{prefixvar}ban [member]",
        value="Bans a user.", 
        inline=False
    )

    embed.add_field(
        name=f"{prefixvar}kick [member]",
        value="Kicks a user.", 
        inline=False
    )

    embed.add_field(
        name=f"{prefixvar}coinflip",
        value="Randomly picks between heads, and tails.", 
        inline=False
    )

    embed.add_field(
        name=f"{prefixvar}joke",
        value="Randomly picks a joke from my joke database. You can recommend a joke using the jokerep command.",
        inline=False)

    embed.add_field(
        name=f"{prefixvar}jokerep [joke]",
        value="Adds a joke to the bot's database, to be used for the joke command.",
        inline=False
    )

    embed.add_field(
        name=f"{prefixvar}eulogy",
        value=eulogy_emoji,
        inline=False
    )

    embed.add_field(
        name=f"{prefixvar}eulogycount",
        value="Count how many times eulogy has been said in any way.",
        inline=False
    )

    embed.set_footer(
        text=f"Command missing? message NotAPro#9901 for help or go to bot help. Made by Wiki and Crow. (Command prefix: {prefixvar})"
    )

    await ctx.send(embed=embed)

# events
@bot.event
async def on_ready():
    print("Connected.")
    print("Awaiting commands.")

@bot.event
async def on_message(message):
    # automatic responses
    if "eulogy" in message.content.lower():
        await message.add_reaction(eulogy_emoji)
    if "cleansing pool" in message.content.lower():
        await message.reply("Watch your language.")

    await bot.process_commands(message) # fix commands not working

print("Notice! Closing this window will turn off the bot.")
bot.run('token goes here')
