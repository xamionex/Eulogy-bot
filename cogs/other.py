import discord
from discord.ext import commands, bridge
from cogs import utils, block
# afk command data
import json
import time


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

    @bridge.bridge_command(name="afk")
    async def afk(self, bot, *, reason=None):
        """Alerts users that mention you that you're AFK."""
        if reason:
            reason = utils.remove_newlines(reason)
        e = await OtherUtils.setafk(self, bot, reason)
        await OtherUtils.sendafk(self, bot, ["afk_alert", "afk_alert_dm"], e)

    @bridge.bridge_command(name="gn")
    async def gn(self, bot):
        """Sets your AFK to `Sleeping 💤`"""
        await OtherUtils.setafk(self, bot, "Sleeping 💤")
        e = discord.Embed(description=f"Goodnight {bot.author.mention}")
        e.set_image(url="https://c.tenor.com/nPYfVs6FsBQAAAAS/kitty-kitten.gif")
        await OtherUtils.sendafk(self, bot, ["afk_alert", "afk_alert_dm"], e)

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


class OtherUtils():
    def __init__(self, bot):
        self.bot = bot

    async def setafk(self, bot, reason):
        with open('./data/afk.json', 'r') as f:
            afk = json.load(f)
        if not reason:
            reason = 'AFK'
        elif reason and len(reason) > 100:
            await utils.senderror(
                "You went over the 100 character limit")
        await OtherUtils.update_data(afk, bot.author)
        afk[f'{bot.author.id}']['reason'] = f'{reason}'
        if afk[f'{bot.author.id}']['AFK']:
            rply = discord.Embed(
                description=f"Goodbye {bot.author.mention}, Updated alert to \"{reason}\"")
        else:
            afk[f'{bot.author.id}']['AFK'] = True
            afk[f'{bot.author.id}']['time'] = int(time.time())
            afk[f'{bot.author.id}']['mentions'] = 0
            rply = discord.Embed(
                description=f"Goodbye {bot.author.mention}, Set alert to \"{reason}\"")
            try:
                await bot.author.edit(nick=f'[AFK] {bot.author.display_name}')
            except:
                pass
        with open('./data/afk.json', 'w') as f:
            json.dump(afk, f, indent=4, sort_keys=True)
        return rply

    async def update_data(afk, user):
        if not f'{user.id}' in afk:
            afk[f'{user.id}'] = {}
            afk[f'{user.id}']['AFK'] = False

    def period(delta, pattern):
        d = {'d': delta.days}
        d['h'], rem = divmod(delta.seconds, 3600)
        d['m'], d['s'] = divmod(rem, 60)
        return pattern.format(**d)

    async def sendafk(self, bot, perm, e):
        if await block.GlobalBlockUtils.get_global_perm(perm[0], bot.author):
            if await block.GlobalBlockUtils.get_global_perm(perm[1], bot.author):
                await utils.senddmembed(bot, e)
            else:
                if isinstance(bot, bridge.BridgeApplicationContext):
                    await bot.reply(embed=e, ephemeral=True)
                else:
                    await bot.reply(embed=e, delete_after=10, mention_author=False)
