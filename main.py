import discord
from discord.ext import bridge
import json
from cogs import utils

# set prefix commands


def get_prefix(bot, msg):
    with open("./data/prefixes.json", "r") as f:
        prefixes = json.load(f)
        try:
            prefix = prefixes.get(str(msg.guild.id))
        except AttributeError:
            prefix = "$"
    return prefix


def when_mentioned_or_function(func):
    def inner(bot, msg):
        r = list(func(bot, msg))
        # uncomment below to enable mention for prefix
        #r = commands.when_mentioned(bot, msg) + r
        return r
    return inner


# set up intents
intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True

# set up discord related stuff
#statusinput = input("status:")
#activity = discord.Game(name=statusinput)
bot = bridge.Bot(
    command_prefix=when_mentioned_or_function(get_prefix),
    description="This is a Bot made by Wiki and Crow.",
    # activity=activity,
    status=discord.Status.online,
    intents=intents
)


@bot.event
async def on_message(message):
    # remove markdown
    message.content = utils.escape_markdown(message.content)
    # stop if user is bot or is mentioning @everyone
    if message.mention_everyone or message.author.bot:
        return

extensions = utils.extensions()
for module in extensions[0]:
    bot.load_extension(f"cogs.{module}")
print("Found", end=" ")
print(*extensions[0], sep=', ')
print("Ignored", end=" ")
print(*extensions[1], sep=', ')
bot.run("NzU2MDg4MDk1NDc2MTU0NDAw.X2Mv6Q.q_UWcwrUhUejpp-k7M6T2yGQ1DM")
