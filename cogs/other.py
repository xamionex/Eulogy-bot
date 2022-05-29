import discord
from discord.ext import commands
from cogs import utils


def setup(bot):
    bot.add_cog(OtherCommands(bot))


class OtherCommands(commands.Cog, name="Other commands"):
    """Uncategorized commands with general use."""
    COG_EMOJI = "❔"

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, name="echo")
    @commands.has_any_role('Newt Engineer', 'Eulogologist')
    @commands.guild_only()
    async def say(self, bot, *, message=None):
        """Echoes the message you send."""
        await utils.delete_message(bot)
        await bot.send(message)

    @commands.command(hidden=True, name="echoembed")
    @commands.has_any_role('Newt Engineer', 'Eulogologist')
    @commands.guild_only()
    async def Say(self, bot, *, message=None):
        """Echos the message you put in, was used for testing."""
        await utils.delete_message(bot)
        embed = discord.Embed(color=bot.author.color,
                              timestamp=bot.message.created_at)
        embed.set_author(name="Announcement!", icon_url=bot.author.avatar.url)
        embed.add_field(
            name=f"Sent by {bot.message.author}", value=str(message))
        await bot.send(embed=embed)

    @commands.command(hidden=True, name="reply")
    @commands.has_any_role('Newt Engineer', 'Eulogologist')
    @commands.guild_only()
    async def reply(self, bot, *, message=None):
        """Reply to someone's message with this command, It'll reply with the bot"""
        reference = bot.message.reference
        if reference is None:
            return await bot.reply(f"{bot.author.mention} You didn't reply to any message.")
        await reference.resolved.reply(message)
        await utils.delete_message(bot)

    @commands.command(hidden=True, name="namedm")
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def namedm(self, bot, user: discord.User, *, message=None):
        """DM someone with the message saying your name"""
        message = f"From {bot.author.mention}: {message}" or f"{bot.author.mention} sent you a message but it was empty"
        await user.send(message)
        await utils.delete_message(bot)

    @commands.command(hidden=True, name="dm")
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def dm(self, bot, user: discord.User, *, message=None):
        """DM someone without the message saying your name"""
        message = message or "Someone sent you a message but it was empty"
        await user.send(message)
        await utils.delete_message(bot)

    @commands.command(hidden=True, name="nick")
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def nick(self, bot, member: discord.Member, *, nick=None):
        """Changes a users nickname, mostly for testing purposes :)"""
        nick = nick or ""
        await member.edit(nick=nick)
        await utils.delete_message(bot)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def poll(self, bot):
        _tmp1 = bot.message.content.split(" ")
        poll = ""

        _tmp1.remove("{self.context.clean_prefix}poll")

        for word in _tmp1:
            poll += word + " "

        del _tmp1

        poll = await bot.message.channel.send("@here " + poll)

        await bot.message.delete()

        await poll.add_reaction("<:eulogy_yes:967622153245700136>")
        await poll.add_reaction("<:eulogy_no:967622221537345616>")
