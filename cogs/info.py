import discord
from discord.ext import commands, bridge
from cogs import utils
from typing import Optional


def setup(bot):
    bot.add_cog(InfoCommands(bot))


class InfoCommands(commands.Cog, name="Informational"):
    """Commands that show you general information about multiple things."""
    COG_EMOJI = "ℹ️"

    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command(name="userinfo")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.guild_only()
    async def userinfo(self, bot, user: Optional[discord.Member]):
        """Shows you information about users"""
        user = user or bot.author
        date_format = "%a, %d %b %Y %I:%M %p"
        e = discord.Embed(color=0xdfa3ff, description=user.mention)
        e.set_author(name=str(user), icon_url=user.avatar.url)
        e.set_thumbnail(url=user.avatar.url)
        e.add_field(
            name="Joined",
            value=user.joined_at.strftime(date_format))
        members = sorted(bot.guild.members, key=lambda m: m.joined_at)
        e.add_field(
            name="Join position",
            value=str(members.index(user)+1))
        e.add_field(
            name="Registered",
            value=user.created_at.strftime(date_format))
        if len(user.roles) > 1:
            role_string = ' '.join([r.mention for r in user.roles][1:])
            e.add_field(
                name="Roles [{}]".format(
                    len(user.roles)-1),
                value=role_string,
                inline=False)
        # perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
        # e.add_field(
        # name="Guild permissions",
        # value=perm_string,
        # inline=False) # way too big for my liking tbh
        e.set_footer(text='ID: ' + str(user.id))
        await utils.sendembed(bot, e, show_all=False, delete=3, delete_speed=20)

    @bridge.bridge_command(name="ping")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def ping(self, bot):
        """Tells you the bot's ping."""
        e = discord.Embed(title=f"Pong! `{round(bot.latency * 1000)}ms`")
        e.set_image(url="https://c.tenor.com/LqNPvLVdzHoAAAAC/cat-ping.gif")
        await utils.sendembed(bot, e, show_all=False, delete=3)

    @commands.command()
    # count the total amount of times eulogy has been said
    async def eulogycount(self, bot):
        first_eulogycount = self.bot.first_eulogycount

        if first_eulogycount:
            first_eulogycount = False

            for channel in bot.guild.text_channels:  # go through every channel
                # go through every message
                async for msg in channel.history(limit=None):
                    if "eulog" in msg.content.lower():
                        counter += 1

        await bot.message.reply(str(counter) + " times.")
