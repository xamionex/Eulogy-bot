import discord
from discord.ext import commands, bridge
import re
import os


async def CheckInstance(bot):
    if isinstance(bot, bridge.BridgeExtContext):
        return True  # prefix returns true
    elif isinstance(bot, bridge.BridgeApplicationContext):
        return False  # slash returns false


async def sendembed(bot, e, show_all=True, delete=1, delete_speed=5):
    if await CheckInstance(bot):  # checks if command is slash or not
        if delete == 0:
            await bot.respond(embed=e, mention_author=False, delete_after=delete_speed)
        elif delete == 1:
            await bot.respond(embed=e, mention_author=False)
        elif delete == 2:
            await bot.respond(embed=e, mention_author=False)
            await delete_message(bot, delete_speed)
        else:
            await bot.respond(embed=e, delete_after=delete_speed, mention_author=False)
            await delete_message(bot, delete_speed)
            # 0 deletes bots reply, 1 doesnt delete, 2 deletes only cause, 3 deletes all
    else:
        if show_all:
            await bot.respond(embed=e)
        else:
            await bot.respond(embed=e, ephemeral=True)
        # true shows in chat, false shows to user only


async def senddmembed(bot, e, delete=False, delete_speed=5):
    if delete:
        await bot.author.send(embed=e, delete_after=delete_speed)
    else:
        await bot.author.send(embed=e)
        # False doesnt delete, True deletes bot's msg


async def delete_message(bot, delete_speed=None):
    try:
        if delete_speed is None:
            await bot.message.delete()
        else:
            await bot.message.delete(delay=delete_speed)
    except Exception:
        return


async def senderror(bot, cerror):
    #e = discord.Embed(description=cerror, color=0xFF6969)
    # await sendembed(bot, e, False)
    if await CheckInstance(bot):
        raise commands.CommandError(cerror)
    else:
        raise discord.ApplicationCommandError(cerror)


def extensions():
    extensions = []
    skip_list = ["utils"]
    for module in next(os.walk("cogs"), (None, None, []))[2]:  # [] if no file
        module = module.replace('.py', '')
        if module not in skip_list:
            extensions.append(module)
    return extensions, skip_list


async def can_dm_user(user: discord.User) -> bool:
    ch = user.dm_channel
    if ch is None:
        ch = await user.create_dm()

    try:
        await ch.send()
    except discord.Forbidden:
        return False
    except discord.HTTPException:
        return True


def escape_markdown(text):
    # escapes `` and \ (discord's escape character), for more chars just add them inside ([])
    parse = re.sub(r"([\\`])", r"\\\1", text)
    reparse = re.sub(r"\\\\([\\`])", r"\1", parse)
    return reparse


def remove_newlines(text):
    new_text = " ".join(text.split())
    return new_text
