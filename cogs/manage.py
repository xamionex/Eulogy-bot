import main
import discord
from discord.ext import commands
from cogs import utils
import datetime
import json
import os
import sys


def setup(bot):
    bot.add_cog(ManageCommands(bot))


class ManageCommands(commands.Cog, name="Management"):
    """Commands for managing the bot."""
    COG_EMOJI = "🛠️"

    def __init__(self, bot):
        self.bot = bot
        self.save = bot.save
        self.hugs = bot.hugs
        self.extensions = utils.extensions()

    @commands.command(hidden=True, name="load")
    @commands.is_owner()
    async def load(self, bot, *, module: str):
        """Loads a module"""
        e = discord.Embed(
            description=f"Trying to load modules \"{module}\"", color=0x69FF69)
        module = module.split(sep=" ")
        for cog in module:
            if cog in self.extensions[0]:
                self.bot.load_extension(f"cogs.{cog}")
                e.add_field(name=f"{cog}", value="`✅` Success")
            else:
                e.add_field(name=f"{cog}", value="`❌` Not found")
        await utils.sendembed(bot, e, show_all=False, delete=3, delete_speed=5)

    @commands.command(hidden=True, name="unload")
    @commands.is_owner()
    async def unload(self, bot, *, module: str):
        """Unloads a module"""
        e = discord.Embed(
            description=f"Trying to unload modules \"{module}\"", color=0x69FF69)
        module = module.split(sep=" ")
        for cog in module:
            if cog in self.extensions[0]:
                self.bot.unload_extension(f"cogs.{cog}")
                e.add_field(name=f"{cog}", value="`✅` Success")
            else:
                e.add_field(name=f"{cog}", value="`❌` Not found")
        await utils.sendembed(bot, e, show_all=False, delete=3, delete_speed=5)

    @commands.command(hidden=True, name="reload")
    @commands.is_owner()
    async def reload(self, bot, *, module: str):
        """Reloads a module"""
        e = discord.Embed(
            description=f"Trying to reload modules \"{module}\"", color=0x69FF69)
        module = module.split(sep=" ")
        for cog in module:
            if cog in self.extensions[0]:
                self.bot.reload_extension(f"cogs.{cog}")
                e.add_field(name=f"{cog}", value="`✅` Success")
            elif cog == "all":
                for cog in self.extensions[0]:
                    self.bot.reload_extension(f"cogs.{cog}")
                    e.add_field(name=f"{cog}", value="`✅` Success")
            else:
                e.add_field(name=f"{cog}", value="`❌` Not found")
        await utils.sendembed(bot, e, show_all=False, delete=3, delete_speed=5)

    @commands.command(hidden=True, name="restart")
    @commands.is_owner()
    async def restart(self, bot):
        """Restarts the bot"""
        await utils.delete_message(bot)
        os.execv(sys.executable, ['python'] + sys.argv)

    @commands.command(hidden=True, name="modules")
    @commands.is_owner()
    async def modules(self, bot):
        """Lists modules"""
        modules = ", ".join(self.extensions[0])
        e = discord.Embed(title=f'Modules found:',
                          description=modules, color=0x69FF69)
        await utils.sendembed(bot, e, show_all=False, delete=3, delete_speed=5)

    @commands.command(hidden=True, name="prefix")
    @commands.is_owner()
    async def prefix(self, bot, prefix=None):
        """Shows or changes prefix"""
        if prefix is not None:
            with open('./data/prefixes.json', 'r') as f:
                prefixes = json.load(f)
            prefixes[str(self, bot.guild.id)] = prefix
            with open('./data/prefixes.json', 'w') as f:
                json.dump(prefixes, f, indent=4)
            await utils.sendembed(bot, discord.Embed(description=f'Prefix changed to: {prefix}'), False, 3, 5)
        else:
            await utils.sendembed(bot, discord.Embed(description=f'My prefix is `{main.get_prefix(self, bot.message)}`, you can also use slash commands\nFor more info use the {main.get_prefix(self, bot.message)}help command!'), False, 3, 20)

    @commands.command(hidden=True, name="modifycurrency")
    # change currency values of a target
    async def modifycurrency(self, bot, type, amount, target: discord.User):
        role = discord.utils.find(
            lambda r: r.name == 'Newt Engineer', bot.message.guild.roles)

        if not role in bot.message.author.roles:
            await bot.message.reply("You do not have permission to use this command.")
            return

        if type.lower() == "coins":
            await bot.message.reply(target.mention + "'s lunar coins have been changed by " + amount + "!")
        elif type.lower() == "eulogies":
            await bot.message.reply(target.mention + "'s eulogies have been changed by " + amount + "!")
        else:
            await bot.message.reply("Please input a valid currency.")
            return

        self.save[target.id][type.lower()] += int(amount)

    @commands.command(name="nexteulogy")
    async def nexteulogy(self, bot):
        role = discord.utils.find(
            lambda r: r.name == 'Eulogy Enjoyer', bot.message.guild.roles)

        await bot.message.reply("Eulogy " + str(len(role.members) - 2))

    @commands.command(pass_context=True)
    @commands.has_role("Newt Engineer")
    async def addrole(self, bot, user: discord.Member, role: discord.Role):
        await user.add_roles(role)
        await bot.send(f"hey {bot.author.name}, {user.name} has been given a role called: {role.name}")

    @commands.command(pass_context=True)
    @commands.has_role("Newt Engineer")
    async def takerole(self, bot, user: discord.Member, role: discord.Role):
        await user.remove_roles(role)
        await bot.send(f"hey {bot.author.name}, {user.name} has lost a role called: {role.name}")

    @commands.command(hidden=True, name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, bot, member: discord.Member, *, reason=None):  # kick member
        await member.kick(reason=reason)

        embed = discord.Embed(
            title="User Kicked",
            description="Kicked user " + str(member),
            timestamp=datetime.datetime.utcnow(),
            color=discord.Color.red()
        )

        embed.add_field(name="Reason", value=str(reason))

        await bot.message.channel.send(embed=embed)
        await bot.message.delete()

    @commands.command(hidden=True, name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, bot, member: discord.Member, *, reason=None):  # ban member
        await member.ban(reason=reason)

        embed = discord.Embed(
            title="User Banned",
            description="Banned user " + str(member),
            timestamp=datetime.datetime.utcnow(),
            color=discord.Color.red()
        )

        embed.add_field(name="Reason", value=str(reason))

        await bot.message.channel.send(embed=embed)
        await bot.message.delete()

    @commands.command(hidden=True, name="save")
    @commands.is_owner()
    async def forcesave(self, bot):
        print("Saving to disk...", end=' ')

        with open("./data/save.json", mode="w", encoding="utf-8") as savefile:
            savefile.write(json.dumps(self.save, sort_keys=True, indent=4))
            savefile.flush()

        with open("./data/hugs.txt", mode="w", encoding="utf-8") as file:
            file.write(str(self.hugs))
            file.flush()

        print("Done!")
