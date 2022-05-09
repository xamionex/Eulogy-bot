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

# set up emojis
eulogy_emoji = "<:eulogy_zero:967096744800296970>"
lunar_coin_emoji = "<:lunar_coin:967122007089119242>"
lunar_symbol = "<:lunar_symbol:972089212264407070>"

# set up lists

jokes = [
    "Alien Head.",
    "Ion Surge.",
    "Suppressive Fire."
]

convo_replies = [
    "Yes.",
    "No.",
    "Definitely not.",
    "I guess?",
    "I'm not answering that.",
    "That doesn't matter.",
    "I don't think so.",
    "What exactly do you mean by that?",
    "I think so.",
    "I don't know, I just got here.",
    "I don't know.",
    "For sure.",
    "I agree.",
    "Most definitely yes."
]

# set up other things
last_dice_usage = 0
counter = 0
first_eulogycount = True

# load in save
with io.open('saves/save.json', mode='r', encoding='utf-8') as file:
    data = file.read()
    data.replace('\n', '')
    data.replace('\t', '')

save = json.loads(data)

# load in hugs
with io.open("saves/hugs.txt", mode='r', encoding='utf-8') as file:
    hugs = int(file.read())

# commands

@bot.command()
async def eulogy(ctx): # send eulogy
    await ctx.message.reply(eulogy_emoji)

@bot.command()
async def eulogycount(ctx): # count the total amount of times eulogy has been said
    global counter, first_eulogycount

    if first_eulogycount:
        first_eulogycount = False

        for channel in ctx.guild.text_channels: # go through every channel
            async for msg in channel.history(limit=None): # go through every message
                if "eulog" in msg.content.lower():
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
async def diceroll(ctx): # roll a dice
    global last_dice_usage

    if (last_dice_usage - time.time()) < -10:
        if random.randint(1,6) == 6:
            await ctx.message.reply("You rolled a 6, so here's a lunar coin!")

            try:
                save[ctx.message.author.name]["coins"] += 1
            except:
                save[ctx.message.author.name] = {
                    "coins": 0,
                    "eulogies": 0,
                    "id": ctx.message.author.id
                }
        else:
            await ctx.message.reply("You sadly didn't get a 6.")
        
        last_dice_usage = time.time()
    else:
        await ctx.message.reply("The dice is still on cooldown for another " + str(int(10 + (last_dice_usage - time.time()))) + " seconds.")

@bot.command()
async def echo(ctx, *, message):
    await ctx.send(message)
    await ctx.message.delete()

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
    embed = discord.Embed(
        title="User Banned",
        description="Banned user " + str(member),
        timestamp=datetime.datetime.utcnow(),
        color=discord.Color.red()
    )

    embed.add_field(name="Reason", value=str(reason))

    await ctx.message.channel.send(embed=embed)
    await ctx.message.delete()

@bot.command()
async def changelog(ctx):
    with io.open("changelog.txt", mode="r") as file:
        changelog = "```\n" + file.read() + "\n```"
    
    await ctx.message.reply(changelog)

@bot.command()
async def nexteulogy(ctx):
    role = discord.utils.find(lambda r: r.name == 'Eulogy Enjoyer', ctx.message.guild.roles)

    await ctx.message.reply("Eulogy " + str(len(role.members) - 2))

@bot.command()
async def hug(ctx, target: discord.User):
    global hugs

    if target == bot.user:
        hugs += 1
        await ctx.message.reply(":people_hugging: :heart:")
    else:
        await ctx.message.reply(ctx.message.author.mention + " is hugging " + target.mention + "! :heart:")

@bot.command()
async def hugcount(ctx):
    global hugs

    await ctx.message.reply("I have been hugged " + str(hugs) + " times. :people_hugging: :heart:")

@bot.command()
async def poll(ctx):
    _tmp1 = ctx.message.content.split(" ")
    poll = ""

    _tmp1.remove("$poll")

    for word in _tmp1:
        poll += word + " "

    del _tmp1

    poll = await ctx.message.channel.send("@here " + poll)

    await ctx.message.delete()

    await poll.add_reaction("<:eulogy_yes:967622153245700136>")
    await poll.add_reaction("<:eulogy_no:967622221537345616>")

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
        name=f"{prefixvar}diceroll",
        value="Randomly picks a number between 1 and 6 and gives a lunar coin if it lands on 6. 30 seconds cooldown.",
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

    embed.add_field(
        name=f"{prefixvar}changelog",
        value="Show the changelog for the latest update.",
        inline=False
    )

    embed.add_field(
        name=f"{prefixvar}nexteulogy",
        value="Shows the next eulogy nickname to be used.",
        inline=False
    )

    embed.add_field(
        name=f"{prefixvar}hug [target]",
        value="Hugs the target. Newt would also love to be hugged.",
        inline=False
    )

    embed.add_field(
        name=f"{prefixvar}hugcount",
        value="Shows how many times newt has been hugged.",
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
        await ctx.message.reply("You have " + str(save[ctx.message.author.name]["coins"]) + " " + lunar_symbol + "!")
    except:
        save[ctx.message.author.name] = {
            "coins": 0,
            "eulogies": 0,
            "id": ctx.message.author.id
        }

        await ctx.message.reply("You have " + str(save[ctx.message.author.name]["coins"]) + " " + lunar_symbol + "!")

@bot.command()
async def eulogies(ctx):
    try:
        await ctx.message.reply("You have " + str(save[ctx.message.author.name]["eulogies"]) + " " + eulogy_emoji + "!")
    except:
        save[ctx.message.author.name] = {
            "coins": 0,
            "eulogies": 0,
            "id": ctx.message.author.id
        }

        await ctx.message.reply("You have " + str(save[ctx.message.author.name]["eulogies"]) + " " + eulogy_emoji + "!")

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
        if save[ctx.message.author.name]["coins"] < 3:
            await ctx.message.reply("You do not have sufficient lunar coins. Use `$bazaar` to see prices.")
            return

        save[ctx.message.author.name]["coins"] -= 3

        if random.randint(1, 20) == 20:
            eulogies_dropped += 1
    elif type == "2":
        if save[ctx.message.author.name]["coins"] < math.ceil((6 + ((save[ctx.message.author.name]["coins"] / 100) * 8))):
            await ctx.message.reply("You do not have sufficient lunar coins. Use `$bazaar` to see prices.")
            return

        save[ctx.message.author.name]["coins"] -= math.ceil((6 + ((save[ctx.message.author.name]["coins"] / 100) * 8)))

        if random.randint(1, 100) <= 15:
            eulogies_dropped += 1
    elif type == "3":
        if save[ctx.message.author.name]["coins"] < math.ceil((9 + ((save[ctx.message.author.name]["coins"] / 100) * 16))):
            await ctx.message.reply("You do not have sufficient lunar coins. Use `$bazaar` to see prices.")
            return

        save[ctx.message.author.name]["coins"] -= math.ceil((9 + ((save[ctx.message.author.name]["coins"] / 100) * 16)))

        if random.randint(1, 20) <= 30:
            eulogies_dropped += 1
    elif type == "4":
        if save[ctx.message.author.name]["coins"] < math.ceil((12 + ((save[ctx.message.author.name]["coins"] / 100) * 24))):
            await ctx.message.reply("You do not have sufficient lunar coins. Use `$bazaar` to see prices.")
            return

        save[ctx.message.author.name]["coins"] -= math.ceil((12 + ((save[ctx.message.author.name]["coins"] / 100) * 24)))

        if random.randint(1, 20) <= 60:
            eulogies_dropped += 1
    elif type == "5":
        if save[ctx.message.author.name]["coins"] < math.ceil((15 + ((save[ctx.message.author.name]["coins"] / 100) * 32))):
            await ctx.message.reply("You do not have sufficient lunar coins. Use `$bazaar` to see prices.")
            return

        save[ctx.message.author.name]["coins"] -= math.ceil((15 + ((save[ctx.message.author.name]["coins"] / 100) * 32)))

        eulogies_dropped += 1 + random.randint(0, 5)
    elif type == "6":
        if save[ctx.message.author.name]["coins"] < math.ceil((18 + ((save[ctx.message.author.name]["coins"] / 100) * 40))):
            await ctx.message.reply("You do not have sufficient lunar coins. Use `$bazaar` to see prices.")
            return

        save[ctx.message.author.name]["coins"] -= math.ceil((18 + ((save[ctx.message.author.name]["coins"] / 100) * 40)))

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
        value="5% chance for one eulogy.\nPrice: 3 " + lunar_symbol + ".\nUse `$lunarpod 1` to open."
    )

    embed.add_field(
        name=u"Lunar Pod (\u2605\u2605\u2606\u2606\u2606\u2606)",
        value="15% chance for one eulogy.\nPrice: " + str(math.ceil((6 + ((save[ctx.message.author.name]["coins"] / 100) * 8)))) + " " + lunar_symbol + ".\nUse `$lunarpod 2` to open."
    )

    embed.add_field(
        name=u"Lunar Pod (\u2605\u2605\u2605\u2606\u2606\u2606)",
        value="30% chance for one eulogy.\nPrice: " + str(math.ceil((9 + ((save[ctx.message.author.name]["coins"] / 100) * 16)))) + " " + lunar_symbol + ".\nUse `$lunarpod 3` to open."
    )

    embed.add_field(
        name=u"Lunar Pod (\u2605\u2605\u2605\u2605\u2606\u2606)",
        value="60% chance for one eulogy.\nPrice: " + str(math.ceil((12 + ((save[ctx.message.author.name]["coins"] / 100) * 24)))) + " " + lunar_symbol + ".\nUse `$lunarpod 4` to open."
    )

    embed.add_field(
        name=u"Lunar Pod (\u2605\u2605\u2605\u2605\u2605\u2606)",
        value="Contains a guaranteed eulogy and up to 5 bonus eulogies.\nPrice: " + str(math.ceil((15 + ((save[ctx.message.author.name]["coins"] / 100) * 32)))) + " " + lunar_symbol + ".\nUse `$lunarpod 5` to open."
    )

    embed.add_field(
        name=u"Lunar Pod (\u2605\u2605\u2605\u2605\u2605\u2605)",
        value="Contains a guaranteed eulogy and up to 10 bonus eulogies.\nPrice: " + str(math.ceil((18 + ((save[ctx.message.author.name]["coins"] / 100) * 40)))) + " " + lunar_symbol + ".\nUse `$lunarpod 6` to open."
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

    for i in range(5):
        eulogy_count = max(eulogycounts)
        user_id = ids[eulogycounts.index(eulogy_count)]

        leaderboard.append([user_id, eulogy_count])

        ids.remove(user_id)
        eulogycounts.remove(eulogy_count)
    
    for i in range(5):
        user = await ctx.message.guild.fetch_member(leaderboard[i][0])
        
        embed.add_field(
            name=str(i + 1) + ". " + user.name,
            value=eulogy_emoji + str(leaderboard[i][1]),
            inline=False
        )

    await ctx.send(embed=embed)

@bot.command()
async def modifycurrency(ctx, type, amount, target: discord.User): # change currency values of a target
    role = discord.utils.find(lambda r: r.name == 'Newt Engineer', ctx.message.guild.roles)

    if not role in  ctx.message.author.roles:
        await ctx.message.reply("You do not have permission to use this command.")
        return

    if type.lower() == "coins":
        await ctx.message.reply(target.mention + "'s lunar coins have been changed by " + amount + "!")
    elif type.lower() == "eulogies":
        await ctx.message.reply(target.mention + "'s eulogies have been changed by " + amount + "!")
    else:
        await ctx.message.reply("Please input a valid currency.")
        return
    
    save[target.name][type.lower()] += int(amount)

# events
@bot.event
async def on_ready():
    print("Connected.")
    print("Awaiting commands.")

@bot.event
async def on_message(message):
    global counter

    # automatic responses
    if "eulog" in message.content.lower():
        await message.add_reaction(eulogy_emoji)
        counter += 1
    if "cleansing pool" in message.content.lower():
        await message.reply("Watch your language.")
    if message.author.bot == False and not "$hug" in message.content.lower():
        if "meow" in message.content.lower():
            await message.reply("Wowwwww, you meow like a cat! That means you are one, right? Shut the fuck up. If you want to be put on a leash and treated like a domestic animal, that's called a fetish, not “quirky” or “cute.” What part of you seriously thinks that any portion of acting like a feline establishes a reputation of appreciation? Is it your lack of any defining aspect of personality that urges you to resort to shitty representations of cats to create an illusion of meaning in your worthless life? Wearing “cat ears” in the shape of headbands further notes the complete absence of human attribution to your false sense of personality, such as intelligence or charisma in any form or shape. Where do you think this mindset's going to lead you? Do you think you're funny, random, quirky even? What makes you think that acting like a fucking cat will make a goddamn hyena laugh? I, personally, feel highly sympathetic towards you as your only escape from the worthless thing you call your existence is to pretend to be an animal. But it's not a worthy choice to assert this horrifying fact as a dominant trait, mainly because personality traits require an initial personality to lay their foundation on. You're not worthy of anybody's time, so go fuck off, \"cat-girl.\"")    
        if bot.user.mentioned_in(message): # "ask newt" functionality
            await message.reply(random.choice(convo_replies))

    # handle lunar coins dropping
    if random.randint(1, 20) <= 3 and message.author.bot == False:
        await message.add_reaction(lunar_coin_emoji)
        
        try:
            save[message.author.name]["coins"] += 1
        except:
            save[message.author.name] = {
                "id": message.author.id,
                "coins": 1,
                "eulogies": 0
            }        
    
    await bot.process_commands(message) # fix commands not working

# save thread functions
def autosave():
    while True:
        time.sleep(60)
        
        print("Saving to disk...", end=' ')

        with io.open("saves/save.json", mode="w", encoding="utf-8") as savefile:
            savefile.write(json.dumps(save, sort_keys=True, indent=4))
            savefile.flush()

        with io.open("saves/hugs.txt", mode="w", encoding="utf-8") as file:
            file.write(str(hugs))
            file.flush()
        
        print("Done!")

def force_save():
    while True:
        input()
        
        print("Saving to disk...", end=' ')

        with io.open("saves/save.json", mode="w", encoding="utf-8") as savefile:
            savefile.write(json.dumps(save, sort_keys=True, indent=4))
            savefile.flush()
        
        with io.open("saves/hugs.txt", mode="w", encoding="utf-8") as file:
            file.write(str(hugs))
            file.flush()
        
        print("Done!")
        
autosave_thread = threading.Thread(target=autosave, daemon=True)
forcesave_thread = threading.Thread(target=force_save, daemon=True)

autosave_thread.start()
forcesave_thread.start()

print("Notice! Closing this window will turn off the bot.")

with io.open("newt token.txt") as file:
    token = file.read()

bot.run(token)