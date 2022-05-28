import json
import discord
from discord.ext import commands, bridge
# cogs
import secrets
from cogs import block, utils

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds = True


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
        r = commands.when_mentioned(bot, msg) + r
        return r
    return inner


bot = bridge.Bot(
    command_prefix=when_mentioned_or_function(get_prefix),
    description="This is a Bot made by Wiki and Crow.",
    intents=intents,
    allowed_mentions=discord.AllowedMentions(
        everyone=False,      # Whether to ping @everyone or @here mentions
        roles=False,         # Whether to ping role @mentions
        # activity=discord.Game(name=input("Playing Status:")),
    ),
)


@bot.before_invoke
async def on_command(ctx):
    try:
        if ctx.author.guild_permissions.administrator:
            ctx.command.reset_cooldown(ctx)
    except:
        pass
    try:
        if await block.BlockUtils.get_perm(ctx, ctx, "blacklist", ctx.author) and ctx.author.guild_permissions.administrator == False:
            raise commands.CommandError(
                f"{ctx.author.mention}, You were **blocked** from using this bot, direct message <@139095725110722560> if you feel this is unfair")
    except AttributeError:
        pass


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
bot.run(secrets.secret)
