import main
import discord
from discord.ext import commands, tasks
from cogs import utils, users, configs
import json
import random
import time
# afk command data
import datetime
import humanize


def setup(bot):
    bot.add_cog(Events(bot))


class Events(commands.Cog, name="Events"):
    """Event listeners (no commands)."""
    COG_EMOJI = "🛠️"

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_ready")
    async def logged_in(self):
        print(f"Logged in as {self.bot.user} (ID: {self.bot.user.id})")
        print("------")

    @commands.Cog.listener("on_application_command_error")
    async def slash_command_error(self, bot: discord.ApplicationContext, error):
        if isinstance(error, commands.BotMissingPermissions):
            raise error
        elif isinstance(error, commands.CommandOnCooldown):
            e = discord.Embed(description=f"`❌` {error}", color=0xFF6969)
            await utils.sendembed(bot, e, show_all=False)
        elif isinstance(error, discord.ApplicationCommandError):
            e = discord.Embed(description=f"`❌` {error}", color=0xFF6969)
            await utils.sendembed(bot, e, show_all=False)
        raise error

    @commands.Cog.listener("on_command_error")
    async def command_error(self, bot, error):
        if isinstance(error, commands.CommandNotFound):
            raise error
        elif isinstance(error, commands.BotMissingPermissions):
            raise error
        elif isinstance(error, commands.CommandError):
            e = discord.Embed(description=f"`❌` {error}", color=0xFF6969)
            await utils.sendembed(bot, e, delete=3)
        raise error

    @commands.Cog.listener("on_member_join")
    async def member_data(self, member):
        afk = self.bot.afk
        await users.UserUtils.update_data(afk, member)
        configs.save(self.bot.afk_path, "w", afk)

    @commands.Cog.listener("on_guild_join")
    async def guild_add_data(self, guild):
        prefixes = self.bot.guild_prefixes
        prefixes[str(guild.id)] = '-'
        configs.save(self.bot.guild_prefixes_path, "w", prefixes)

        perms = self.bot.perms
        perms[str(guild.id)] = {}
        configs.save(self.bot.perms_path, "w", perms)

        triggers = self.bot.triggers
        triggers[str(guild.id)] = {}
        triggers[str(guild.id)]["regex"] = {}
        triggers[str(guild.id)]["regex"]["toggle"] = False
        triggers[str(guild.id)]["regex"]["triggers"] = {}
        triggers[str(guild.id)]["match"] = {}
        triggers[str(guild.id)]["match"]["toggle"] = False
        triggers[str(guild.id)]["match"]["triggers"] = {}
        configs.save(self.bot.triggers_path, "w", triggers)

    @commands.Cog.listener("on_guild_remove")
    async def guild_remove_data(self, guild):
        prefixes = self.bot.guild_prefixes
        prefixes.pop(str(guild.id))
        configs.save(self.bot.guild_prefixes_path, "w", prefixes)

        perms = self.bot.perms
        perms.pop(str(guild.id))
        configs.save(self.bot.perms_path, "w", perms)

        triggers = self.bot.triggers
        triggers.pop(str(guild.id))
        configs.save(self.bot.triggers_path, "w", triggers)

    @commands.Cog.listener("on_message")
    async def memes_channel(self, message):
        # delete messages in Northstar memes :dread:
        if message.channel.id == 973438217196040242:
            await message.delete(delay=random.randrange(100, 3600, 100))

    @commands.Cog.listener("on_message")
    async def afk_check(self, message):
        # check if user is afk or members in message
        prefix = main.get_prefix(self.bot, message)
        send = False
        afk_alert = discord.Embed(
            title=f"Members in your message are afk:")
        afk_alert.set_footer(
            text=f"Toggle: {prefix}alerts\nDMs Toggle: {prefix}dmalerts")
        if message.author.bot:
            return

        for member in message.mentions:
            if member.bot or member.id == message.author.id:
                return
            if self.bot.afk[f'{member.id}']['AFK']:
                send = True

                # gets afk message
                reason = self.bot.afk[f'{member.id}']['reason']

                # gets unix time
                unix_time = int(time.time()) - \
                    int(self.bot.afk[f'{member.id}']['time'])

                # user was afk for time.now() - time
                afktime = humanize.naturaltime(
                    datetime.datetime.now() - datetime.timedelta(seconds=unix_time))

                # add embed
                afk_alert.add_field(
                    name=f"{member.display_name.replace('[AFK]', '')} - {afktime}", value=f"\"{reason}\"", inline=True)

                # plus 1 time mentioned in afk.json
                self.bot.afk[f'{member.id}']['mentions'] = int(
                    self.bot.afk[f'{member.id}']['mentions']) + 1

                # save json
                configs.save(self.bot.afk_path, 'w', self.bot.afk)

        if send:
            await users.UserUtils.sendafk(self, message, ["afk_alert", "afk_alert_dm"], afk_alert)
        await users.UserUtils.update_data(self.bot.afk, message.author)
        # if message's author is afk continue
        if list(message.content.split(" "))[0] != f'{prefix}afk' and self.bot.afk[f'{message.author.id}']['AFK']:
            # unix now - unix since afk
            timeafk = int(time.time()) - \
                int(self.bot.afk[f'{message.author.id}']['time'])

            # make time readable for user
            afktime = users.UserUtils.period(datetime.timedelta(
                seconds=round(timeafk)), "{d}d {h}h {m}m {s}s")

            # get mentions
            mentionz = self.bot.afk[f'{message.author.id}']['mentions']

            # make embed
            welcome_back = discord.Embed(
                description=f"**Welcome back {message.author.mention}!**")
            welcome_back.add_field(name="Afk for", value=afktime, inline=True)
            welcome_back.add_field(
                name="Mentioned", value=f"{mentionz} time(s)", inline=True)
            welcome_back.set_footer(
                text=f"Toggle: {prefix}wbalerts\nDMs Toggle: {prefix}wbdmalerts")

            # reset afk for user
            self.bot.afk[f'{message.author.id}']['AFK'] = False
            self.bot.afk[f'{message.author.id}']['reason'] = 'None'
            self.bot.afk[f'{message.author.id}']['time'] = '0'
            self.bot.afk[f'{message.author.id}']['mentions'] = 0
            configs.save(self.bot.afk_path, 'w', self.bot.afk)

            # try to reset nickname
            try:
                nick = message.author.display_name.replace('[AFK]', '')
                await message.author.edit(nick=nick)
            except:
                print(
                    f'I wasnt able to edit [{message.author} / {message.author.id}].')

            await users.UserUtils.sendafk(self, message, ["wb_alert", "wb_alert_dm"], welcome_back)
        configs.save(self.bot.afk_path, 'w', self.bot.afk)

    @commands.Cog.listener("on_message")
    async def help_check(self, message):
        # check if user's message is only bot ping and reply with help, if not process commands
        if message.author.bot == False and self.bot.user.mentioned_in(message) and len(message.content) == len(self.bot.user.mention):
            await message.reply(embed=discord.Embed(description=f'My prefix is `{self.bot.guild_prefixes[str(message.guild.id)]}` or {self.bot.user.mention}, you can also use slash commands\nFor more info use the /help command!'), delete_after=20, mention_author=False)
        else:
            await self.bot.process_commands(message)

    @commands.Cog.listener("on_message")
    async def word_triggers(self, message):
        if message.author.bot or isinstance(message.channel, discord.DMChannel):
            return
        await self.trigger(message, "match")
        await self.trigger(message, "regex")
        await self.replies(message)

    async def replies(self, message):
        global counter
        # automatic responses
        if "eulog" in message.content.lower():
            await message.add_reaction(self.bot.eulogy_emoji)
            counter += 1
        if "cleansing pool" in message.content.lower():
            await message.reply("Watch your language.")

        if not message.author.bot:
            # "ask newt" functionality
            if self.bot.user.mentioned_in(message) and len(message.content) >= len(self.bot.user.mention):
                await message.reply(random.choice(self.bot.convo_replies))

        # handle lunar coins dropping
        if random.randint(1, 20) <= 3 and message.author.bot == False:
            await message.add_reaction(self.bot.lunar_coin_emoji)

            try:
                self.bot.save[message.author.id]["coins"] += 1
            except:
                self.bot.save[message.author.id] = {
                    "coins": 1,
                    "eulogies": 0
                }

    async def trigger(self, message, type: str):
        if type == "regex":
            msg = message.content.lower()
        else:
            msg = message.content.split(" ")
        if self.bot.triggers[str(message.guild.id)][type]["toggle"]:
            for trigger, reply in self.bot.triggers[str(message.guild.id)][type]["triggers"].items():
                multi_trigger = list(trigger.split('|'))
                for triggers in multi_trigger:
                    if triggers in msg:
                        reply = random.choice(list(reply.split('|')))
                        await message.reply(reply)
                        break
