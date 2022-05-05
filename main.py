import math
import re
import discord
from discord.ext import commands
import datetime
import random
import json
import io
import threading
import time

# set up intents
intents = discord.Intents.default()
intents.members = True
intents.messages = True

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
    status=discord.Status.online,
    intents=intents
)

# set up non-discord related stuff
eulogy_emoji = "<:eulogy_zero:967096744800296970>" # 967096744800296970 when running, 967740312543965224 when testing

coins = ["It landed on heads!", "It landed on tails!"]

jokes = [
    "Alien Head.",
    "Ion Surge.",
    "Suppressive Fire."
]

# load in save
with io.open('save.json', mode='r', encoding='utf-8') as file:
    data = file.read()
    data.replace('\n', '')
    data.replace('\t', '')

save = json.loads(data)

# commands

@bot.command()
async def eulogy(ctx): # send eulogy
    await ctx.message.reply(eulogy_emoji)

@bot.command()
async def eulogycount(ctx): # count the total amount of times eulogy has been said
    # count
    counter = 0

    for channel in ctx.guild.text_channels: # go through every channel
        async for message in channel.history(limit=None): # go through every message
            if "eulog" in message.content.lower():
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
async def echo(self, ctx, *, message):
    await ctx.message.delete()
    await ctx.send(message)


@bot.command()
async def echoembed(self, ctx, *, message):
    embed = discord.Embed(
            title=message,
            timestamp=datetime.datetime.utcnow(),
            color=discord.Color.red()
    )

    await ctx.message.delete()
    await ctx.message.channel.send(embed=embed)


@bot.command()
async def joke(ctx): # send a random joke out of the list
    await ctx.message.reply(random.choice(jokes))

@bot.command()
async def jokerep(ctx, *, jrep): # suggest a joke to add to the bot
    await ctx.message.channel.send(
        "Your joke was recorded. It will be added if Wiki or Crow approves of it.")
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

    embed.add_field(
        name=f"{prefixvar}lunarcoins",
        value="Show your lunar coins. Lunar coins drop as you send messages.",
        inline=False
    )

    embed.add_field(
        name=f"{prefixvar}eulogies",
        value="Show your eulogies. Eulogies can be purchased using lunar coins.",
        inline=False
    )

    embed.add_field(
        name=f"{prefixvar}bazaar",
        value="Show the different types of lunar pods.",
        inline=False
    )

    embed.add_field(
        name=f"{prefixvar}lunarpod [type]",
        value="Open a lunar pod using lunar coins to get eulogies.",
        inline=False
    )

    embed.add_field(
        name=f"{prefixvar}leaderboard",
        value="Show the eulogy leaderboard.",
        inline=False
    )

    embed.set_footer(
        text=f"Command missing? message NotAPro#9901 for help or go to bot help. Made by Wiki and Crow. (Command prefix: {prefixvar})"
    )

    await ctx.send(embed=embed)

# lunar coin commands
@bot.command()
async def lunarcoins(ctx):
    try:
        await ctx.message.reply("You have " + str(save[ctx.message.author.name]["coins"]) + " lunar coins!")
    except:
        save[ctx.message.author.name]["coins"] = 0
        save[ctx.message.author.name]["id"] = ctx.message.author.id
        await ctx.message.reply("You have " + str(save[ctx.message.author.name]["coins"]) + " lunar coins!")

@bot.command()
async def eulogies(ctx):
    try:
        await ctx.message.reply("You have " + str(save[ctx.message.author.name]["eulogies"]) + " eulogies!")
    except:
        save[ctx.message.author.name]["eulogies"] = 0
        save[ctx.message.author.name]["id"] = ctx.message.author.id
        await ctx.message.reply("You have " + str(save[ctx.message.author.name]["eulogies"]) + " eulogies!")

@bot.command()
async def lunarpod(ctx, type=None):
    if not type in ["1", "2", "3", "4", "5", "6"] or type == None:
        await ctx.message.reply("Use `$lunarpod [type]` to open a lunar pod. Use `$bazaar` to see types of lunar pods.")
        return

    if save[ctx.message.author.name]["coins"] <= 0:
        await ctx.message.reply("You do not have sufficient lunar coins. Use `$bazaar` to see prices.")
        return

    eulogies_dropped = 0
    
    if type == "1":
        if save[ctx.message.author.name]["coins"] < math.ceil((1 + (save[ctx.message.author.name]["coins"] / 100))):
            ctx.message.reply("You do not have sufficient lunar coins. Use `$bazaar` to see prices.")
            return

        save[ctx.message.author.name]["coins"] -= math.ceil((1 + (save[ctx.message.author.name]["coins"] / 100)))

        if random.randint(1, 20) == 20:
            eulogies_dropped += 1
    elif type == "2":
        if save[ctx.message.author.name]["coins"] < math.ceil((3 + ((save[ctx.message.author.name]["coins"] / 100) * 5))):
            await ctx.message.reply("You do not have sufficient lunar coins. Use `$bazaar` to see prices.")
            return

        save[ctx.message.author.name]["coins"] -= math.ceil((3 + ((save[ctx.message.author.name]["coins"] / 100) * 5)))

        if random.randint(1, 100) <= 15:
            eulogies_dropped += 1
    elif type == "3":
        if save[ctx.message.author.name]["coins"] < math.ceil((6 + ((save[ctx.message.author.name]["coins"] / 100) * 10))):
            await ctx.message.reply("You do not have sufficient lunar coins. Use `$bazaar` to see prices.")
            return

        save[ctx.message.author.name]["coins"] -= math.ceil((6 + ((save[ctx.message.author.name]["coins"] / 100) * 10)))

        if random.randint(1, 20) <= 30:
            eulogies_dropped += 1
    elif type == "4":
        if save[ctx.message.author.name]["coins"] < math.ceil((9 + ((save[ctx.message.author.name]["coins"] / 100) * 16))):
            await ctx.message.reply("You do not have sufficient lunar coins. Use `$bazaar` to see prices.")
            return

        save[ctx.message.author.name]["coins"] -= math.ceil((9 + ((save[ctx.message.author.name]["coins"] / 100) * 16)))

        if random.randint(1, 20) <= 60:
            eulogies_dropped += 1
    elif type == "5":
        if save[ctx.message.author.name]["coins"] < math.ceil((12 + ((save[ctx.message.author.name]["coins"] / 100) * 25))):
            await ctx.message.reply("You do not have sufficient lunar coins. Use `$bazaar` to see prices.")
            return

        save[ctx.message.author.name]["coins"] -= math.ceil((12 + ((save[ctx.message.author.name]["coins"] / 100) * 25)))

        eulogies_dropped += 1 + random.randint(0, 5)
    elif type == "6":
        if save[ctx.message.author.name]["coins"] < math.ceil((15 + ((save[ctx.message.author.name]["coins"] / 100) * 40))):
            await ctx.message.reply("You do not have sufficient lunar coins. Use `$bazaar` to see prices.")
            return

        save[ctx.message.author.name]["coins"] -= math.ceil((15 + ((save[ctx.message.author.name]["coins"] / 100) * 40)))

        eulogies_dropped += 1 + random.randint(0, 10)

    reply = "Drops from Lunar Pod ("

    for i in range(0, int(type)): reply += u"\u2605"
    for i in range(0, (6 - int(type))): reply += u"\u2606"

    reply += "):\n" + eulogy_emoji + " " + str(eulogies_dropped)

    save[ctx.message.author.name]["eulogies"] += eulogies_dropped

    await ctx.message.reply(reply)

@bot.command()
async def bazaar(ctx):
    embed = discord.Embed(
        title="The Bazaar Between Time",
        description="Types of lunar pods that you can buy and open. Prices are displayed based on " + ctx.message.author.mention + "'s lunar coins.",
        color=discord.Color.red()
    )

    embed.add_field(
        name=u"Lunar Pod (\u2605\u2606\u2606\u2606\u2606\u2606)",
        value="5% chance for one eulogy.\nPrice: " + str(math.ceil((1 + ((save[ctx.message.author.name]["coins"] / 100))))) + " lunar coins.\nUse `$lunarpod 1` to open."
    )

    embed.add_field(
        name=u"Lunar Pod (\u2605\u2605\u2606\u2606\u2606\u2606)",
        value="15% chance for one eulogy.\nPrice: " + str(math.ceil((3 + ((save[ctx.message.author.name]["coins"] / 100) * 5)))) + " lunar coins.\nUse `$lunarpod 2` to open."
    )

    embed.add_field(
        name=u"Lunar Pod (\u2605\u2605\u2605\u2606\u2606\u2606)",
        value="30% chance for one eulogy.\nPrice: " + str(math.ceil((6 + ((save[ctx.message.author.name]["coins"] / 100) * 10)))) + " lunar coins.\nUse `$lunarpod 3` to open."
    )

    embed.add_field(
        name=u"Lunar Pod (\u2605\u2605\u2605\u2605\u2606\u2606)",
        value="60% chance for one eulogy.\nPrice: " + str(math.ceil((9 + ((save[ctx.message.author.name]["coins"] / 100) * 16)))) + " lunar coins.\nUse `$lunarpod 4` to open."
    )

    embed.add_field(
        name=u"Lunar Pod (\u2605\u2605\u2605\u2605\u2605\u2606)",
        value="Contains a guaranteed eulogy and up to 5 bonus eulogies.\nPrice: " + str(math.ceil((12 + (save[ctx.message.author.name]["coins"] / 25)))) + " lunar coins.\nUse `$lunarpod 5` to open."
    )

    embed.add_field(
        name=u"Lunar Pod (\u2605\u2605\u2605\u2605\u2605\u2605)",
        value="Contains a guaranteed eulogy and up to 10 bonus eulogies.\nPrice: " + str(math.ceil((15 + ((save[ctx.message.author.name]["coins"] / 100) * 40)))) + " lunar coins.\nUse `$lunarpod 6` to open."
    )
    
    await ctx.send(embed=embed)

@bot.command()
async def leaderboard(ctx):
    embed = discord.Embed(
        title="Eulogy Zero Leaderboard",
        description="The leaderboard of who has the most eulogies.",
        color=0x5efcff
    )

    leaderboard = []

    ids = []
    eulogycounts = []

    for key in save:
        ids.append(save[key]["id"])
        eulogycounts.append(save[key]["eulogies"])

    for i in range(len(ids)):
        eulogy_count = max(eulogycounts)
        user_id = ids[eulogycounts.index(eulogy_count)]

        leaderboard.append([user_id, eulogy_count])

        ids.remove(user_id)
        eulogycounts.remove(eulogy_count)
    
    for i in range(len(leaderboard)):
        user = await ctx.message.guild.fetch_member(leaderboard[i][0])
        
        embed.add_field(
            name=str(i + 1) + ". " + user.name,
            value=eulogy_emoji + str(leaderboard[i][1]),
            inline=False
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
    if message.author.bot == False:
        if "meow" in message.content.lower():
            await message.reply("Wowwwww, you meow like a cat! That means you are one, right? Shut the fuck up. If you want to be put on a leash and treated like a domestic animal, that's called a fetish, not “quirky” or “cute.” What part of you seriously thinks that any portion of acting like a feline establishes a reputation of appreciation? Is it your lack of any defining aspect of personality that urges you to resort to shitty representations of cats to create an illusion of meaning in your worthless life? Wearing “cat ears” in the shape of headbands further notes the complete absence of human attribution to your false sense of personality, such as intelligence or charisma in any form or shape. Where do you think this mindset's going to lead you? Do you think you're funny, random, quirky even? What makes you think that acting like a fucking cat will make a goddamn hyena laugh? I, personally, feel highly sympathetic towards you as your only escape from the worthless thing you call your existence is to pretend to be an animal. But it's not a worthy choice to assert this horrifying fact as a dominant trait, mainly because personality traits require an initial personality to lay their foundation on. You're not worthy of anybody's time, so go fuck off, \"cat-girl.\"")    

    # handle lunar coins dropping
    if random.randint(1, 100) <= 3 and message.author.bot == False:
        await message.reply("A lunar coin dropped!")
        
        try:
            save[message.author.name]["coins"] += 1
        except:
            save[message.author.name] = {
                "id": message.author.id,
                "coins": 1,
                "eulogies": 0
            }
   
    await bot.process_commands(message) # fix commands not working

# autosave every 60 secs
def autosave():
    while True:
        time.sleep(60)
        
        print("Saving to disk...", end=' ')

        with io.open("save.json", mode="w", encoding="utf-8") as savefile:
            savefile.write(json.dumps(save, sort_keys=True, indent=4))
            savefile.flush()
        
        print("Done!")
        
autosave_thread = threading.Thread(target=autosave, daemon=True)
autosave_thread.start()

print("Notice! Closing this window will turn off the bot.")
bot.run('token')
