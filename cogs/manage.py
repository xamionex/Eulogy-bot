import datetime
import json
import discord
import os
import sys
from discord.ext import commands
from cogs import utils, configs

extensions = utils.extensions()


def setup(bot):
    bot.add_cog(ManageCommands(bot))


class ManageCommands(commands.Cog, name="Management"):
    """Commands for managing the bot."""
    COG_EMOJI = "🛠️"

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, name="log")
    @commands.is_owner()
    async def log(self, ctx):
        args = ctx.message.content.split(" ")
        if args[1] == "ctx":
            find = getattr(ctx, args[2])
        elif args[1] == "self.ctx":
            find = getattr(self.ctx, args[2])
        else:
            find = getattr(getattr(self, args[1]), args[2])
        print(find)
        await utils.sendembed(ctx, discord.Embed(description=find), show_all=False, delete=3, delete_speed=5)

    @commands.command(hidden=True, name="load")
    @commands.is_owner()
    async def load(self, ctx, *, module: str):
        """Loads a module"""
        e = discord.Embed(
            description=f"Trying to load modules \"{module}\"", color=0x69FF69)
        module = module.split(sep=" ")
        for cog in module:
            if cog in extensions[0]:
                self.ctx.load_extension(f"cogs.{cog}")
                e.add_field(name=f"{cog}", value="`✅` Success")
            else:
                e.add_field(name=f"{cog}", value="`❌` Not found")
        await utils.sendembed(ctx, e, show_all=False, delete=3, delete_speed=5)

    @commands.command(hidden=True, name="unload")
    @commands.is_owner()
    async def unload(self, ctx, *, module: str):
        """Unloads a module"""
        e = discord.Embed(
            description=f"Trying to unload modules \"{module}\"", color=0x69FF69)
        module = module.split(sep=" ")
        for cog in module:
            if cog in extensions[0]:
                self.ctx.unload_extension(f"cogs.{cog}")
                e.add_field(name=f"{cog}", value="`✅` Success")
            else:
                e.add_field(name=f"{cog}", value="`❌` Not found")
        await utils.sendembed(ctx, e, show_all=False, delete=3, delete_speed=5)

    @commands.command(hidden=True, name="reload")
    @commands.is_owner()
    async def reload(self, ctx, *, module: str):
        """Reloads a module"""
        e = discord.Embed(
            description=f"Trying to reload modules \"{module}\"", color=0x69FF69)
        module = module.split(sep=" ")
        for cog in module:
            if cog in extensions[0]:
                self.ctx.reload_extension(f"cogs.{cog}")
                e.add_field(name=f"{cog}", value="`✅` Success")
            elif cog == "all":
                for cog in extensions[0]:
                    self.ctx.reload_extension(f"cogs.{cog}")
                    e.add_field(name=f"{cog}", value="`✅` Success")
            else:
                e.add_field(name=f"{cog}", value="`❌` Not found")
        await utils.sendembed(ctx, e, show_all=False, delete=3, delete_speed=5)

    @commands.command(hidden=True, name="restart")
    @commands.is_owner()
    async def restart(self, ctx):
        """Restarts the bot"""
        await utils.delete_message(ctx)
        os.execv(sys.executable, ['python'] + sys.argv)

    @commands.command(hidden=True, name="modules")
    @commands.is_owner()
    async def modules(self, ctx):
        """Lists modules"""
        modules = ", ".join(extensions[0])
        e = discord.Embed(title=f'Modules found:',
                          description=modules, color=0x69FF69)
        await utils.sendembed(ctx, e, show_all=False, delete=3, delete_speed=5)

    @commands.command(hidden=True, name="prefix")
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, prefix=None):
        """Shows or changes prefix"""
        if prefix is not None:
            with open('./data/prefixes.json', 'r') as f:
                prefixes = json.load(f)
            prefixes[str(ctx.guild.id)] = prefix
            with open('./data/prefixes.json', 'w') as f:
                json.dump(prefixes, f, indent=4)
            await utils.sendembed(ctx, discord.Embed(description=f'Prefix changed to: {prefix}'), False, 3, 5)
        else:
            await utils.sendembed(ctx, discord.Embed(description=f'My prefix is `{self.ctx.guild_prefixes[str(ctx.guild.id)]}` or {self.ctx.user.mention}, you can also use slash commands\nFor more info use the /help command!'), False, 3, 20)

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

    @commands.group(hidden=True, name="triggers", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def triggers(self, bot):
        """Triggers that reply whenever someone mentions a trigger"""
        await utils.senderror(bot, f"No command specified, do {self.bot.guild_prefixes[str(bot.guild.id)]}help triggers for more info")

    @triggers.group(hidden=True, name="match", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def match(self, bot):
        """Text triggers that have a match in one of the user's words"""
        await utils.senderror(bot, f"No command specified, do {self.bot.guild_prefixes[str(bot.guild.id)]}help triggers match for more info")

    @match.command(hidden=True, name="toggle")
    @commands.has_permissions(administrator=True)
    async def matchtoggletriggers(self, bot):
        """Toggles match message triggers"""
        await ManageUtils.toggletriggers(self, bot, "match")

    @match.command(hidden=True, name="list")
    @commands.has_permissions(administrator=True)
    async def matchlisttriggers(self, bot):
        """Lists match message triggers"""
        await ManageUtils.listtriggers(self, bot, "match")

    @match.command(hidden=True, name="add")
    @commands.has_permissions(administrator=True)
    async def matchaddtrigger(self, bot, trigger: str, *, reply: str):
        f"""Adds a match message trigger (ex. {self.bot.guild_prefixes[str(bot.guild.id)]}triggers match add trigger|anothertrigger this is the reply)"""
        await ManageUtils.addtrigger(self, bot, trigger, reply, "match")

    @match.command(hidden=True, name="rem")
    @commands.has_permissions(administrator=True)
    async def matchremovetrigger(self, bot, *, trigger: str):
        f"""Removes a match message trigger (ex. {self.bot.guild_prefixes[str(bot.guild.id)]}triggers match del this|trigger other|trigger)"""
        await ManageUtils.removetrigger(self, bot, trigger, "match")

    @triggers.group(hidden=True, name="regex", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def regex(self, bot):
        """Text triggers that have a regex match in one of the user's words"""
        await utils.senderror(bot, f"No command specified, do {self.bot.guild_prefixes[str(bot.guild.id)]}help triggers regex for more info")

    @regex.command(hidden=True, name="toggle")
    @commands.has_permissions(administrator=True)
    async def regextoggletriggers(self, bot):
        """Toggles regex message triggers"""
        await ManageUtils.toggletriggers(self, bot, "regex")

    @regex.command(hidden=True, name="list")
    @commands.has_permissions(administrator=True)
    async def regexlisttriggers(self, bot):
        """Lists regex message triggers"""
        await ManageUtils.listtriggers(self, bot, "regex")

    @regex.command(hidden=True, name="add")
    @commands.has_permissions(administrator=True)
    async def regexaddtrigger(self, bot, trigger: str, *, reply: str):
        f"""Adds a regex message trigger, underscores are replaced with a space (ex. {self.bot.guild_prefixes[str(bot.guild.id)]}triggers regex add this_trigger|another_trigger this is the reply)"""
        await ManageUtils.addtrigger(self, bot, trigger, reply, "regex")

    @regex.command(hidden=True, name="rem")
    @commands.has_permissions(administrator=True)
    async def regexremovetrigger(self, bot, *, trigger: str):
        f"""Removes a regex message trigger, underscores are replaced with a space (ex. {self.bot.guild_prefixes[str(bot.guild.id)]}triggers regex del this|trigger another_trigger)"""
        await ManageUtils.removetrigger(self, bot, trigger, "regex")


class ManageUtils():
    def __init__(self, bot):
        self.bot = bot

    async def define_triggers(self, bot):
        triggers = self.bot.triggers
        if str(bot.guild.id) not in triggers:
            triggers[str(bot.guild.id)] = {}
            triggers[str(bot.guild.id)]["regex"] = {}
            triggers[str(bot.guild.id)]["regex"]["toggle"] = False
            triggers[str(bot.guild.id)]["regex"]["triggers"] = {}
            triggers[str(bot.guild.id)]["match"] = {}
            triggers[str(bot.guild.id)]["match"]["toggle"] = False
            triggers[str(bot.guild.id)]["match"]["triggers"] = {}
        return triggers

    async def toggletriggers(self, bot, type: str):
        triggers = await ManageUtils.define_triggers(self, bot)
        if triggers[str(bot.guild.id)][type]["toggle"]:
            triggers[str(bot.guild.id)][type]["toggle"] = False
            await utils.sendembed(bot, discord.Embed(description=f"❌ Disabled {type} triggers", color=0xFF6969), False)
        else:
            triggers[str(bot.guild.id)][type]["toggle"] = True
            await utils.sendembed(bot, discord.Embed(description=f"✅ Enabled {type} triggers", color=0x66FF99), False)
        configs.save(self.bot.triggers_path, "w", triggers)

    async def listtriggers(self, bot, type: str):
        triggers = await ManageUtils.define_triggers(self, bot)
        if triggers[str(bot.guild.id)][type]["triggers"]:
            e = discord.Embed(description=f"Triggers found:")
            for trigger, reply in triggers[str(bot.guild.id)][type]["triggers"].items():
                if type == "regex":
                    trigger = trigger.replace(" ", "_")
                e.add_field(name=trigger, value=reply)
            await utils.sendembed(bot, e, show_all=False, delete=3, delete_speed=20)
        else:
            await utils.senderror(bot, "No triggers found")

    async def addtrigger(self, bot, trigger: str, reply: str, type: str):
        triggers = await ManageUtils.define_triggers(self, bot)
        triggers_list = triggers[str(bot.guild.id)][type]["triggers"]
        if type == "regex":
            trigger = trigger.replace("_", " ")
        e = discord.Embed(title=f"🛠️ Trying to add trigger:", color=0x66FF99)
        old_reply = None
        try:
            old_reply = triggers_list[trigger]
        except:
            pass
        triggers_list[trigger] = reply
        if old_reply is not None:
            e.add_field(
                name=f"Overwrote: {', '.join(trigger.split('|'))}", value=f"**Old reply:** `{old_reply}`\n**New reply:** `{triggers_list[trigger]}`")
        else:
            e.add_field(
                name=f"Trigger: {', '.join(trigger.split('|'))}", value=f"**Reply:** `{reply}`")
        await utils.sendembed(bot, e, False)
        configs.save(self.bot.triggers_path, "w", triggers)

    async def removetrigger(self, bot, trigger: str, type: str):
        triggers = await ManageUtils.define_triggers(self, bot)
        triggers_list = triggers[str(bot.guild.id)][type]["triggers"]
        trigger = trigger.split(" ")
        e = discord.Embed(
            title=f"🛠️ Trying to remove triggers:", color=0x66FF99)
        for item in trigger:
            try:
                if type == "regex":
                    item = item.replace("_", " ")
                reply = triggers_list[str(item)]
                triggers_list.pop(str(item))
                e.add_field(
                    name=f"✅ Removed {item.replace(' ', '_')}", value=f"`{reply}`")
            except:
                e.add_field(name="❌ Couldn't find", value=f"`{item}`")
        await utils.sendembed(bot, e, False)
        configs.save(self.bot.triggers_path, "w", triggers)
