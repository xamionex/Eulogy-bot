import main
import discord
from discord.ext import commands, tasks
from cogs import utils as utilz, other
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
        self.save = bot.save
        self.hugs = bot.hugs
        self.convo_replies = bot.convo_replies
        self.eulogy_emoji = bot.eulogy_emoji
        self.lunar_coin_emoji = bot.lunar_coin_emoji
        self.lunar_symbol = bot.lunar_symbol
        self.autosave.start()

    def cog_unload(self):
        self.autosave.cancel()

    @commands.Cog.listener("on_ready")
    async def logged_in(self):
        print(f"Logged in as {self.bot.user} (ID: {self.bot.user.id})")
        print("------")

    @commands.Cog.listener("on_application_command_error")
    async def slash_command_error(self, bot: discord.ApplicationContext, error):
        if isinstance(error, commands.BotMissingPermissions):
            raise error
        elif isinstance(error, commands.CommandOnCooldown):
            e = discord.Embed(description=error, color=0xFF6969)
            await utilz.sendembed(bot, e, show_all=False)
        elif isinstance(error, discord.ApplicationCommandError):
            e = discord.Embed(description=error, color=0xFF6969)
            await utilz.sendembed(bot, e, show_all=False)
        raise error

    @commands.Cog.listener("on_command_error")
    async def command_error(self, bot, error):
        if isinstance(error, commands.CommandNotFound):
            raise error
        elif isinstance(error, commands.BotMissingPermissions):
            raise error
        elif isinstance(error, commands.CommandError):
            e = discord.Embed(description=f"`❌` {error}", color=0xFF6969)
            await utilz.sendembed(bot, e, delete=3)
        raise error

    @commands.Cog.listener("on_member_join")
    async def member_data(self, member):
        with open('./data/afk.json', 'r') as f:
            afk = json.load(f)
        await other.OtherUtils.update_data(afk, member)
        with open('./data/afk.json', 'w') as f:
            json.dump(afk, f, indent=4, sort_keys=True)

    @commands.Cog.listener("on_guild_join")
    async def guild_add_data(self, guild):
        with open('./data/prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefixes[str(guild.id)] = '$'
        with open('./data/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

    @commands.Cog.listener("on_guild_remove")
    async def guild_remove_data(self, guild):
        with open('./data/prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefixes.pop(str(guild.id))
        with open('./data/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

    @commands.Cog.listener("on_message")
    async def afk_check(self, message):
        # check if user is afk or members in message
        prefix = main.get_prefix(self, message)
        send = False
        afk_alert = discord.Embed(
            title=f"Members in your message are afk:")
        afk_alert.set_footer(
            text=f"Toggle: {prefix}alerts\nDMs Toggle: {prefix}dmalerts")
        if message.author.bot:
            return
        with open('./data/afk.json', 'r') as f:
            afk = json.load(f)
        for member in message.mentions:
            if member.bot or member.id == message.author.id:
                return
            if afk[f'{member.id}']['AFK']:
                send = True

                # gets afk message
                reason = afk[f'{member.id}']['reason']

                # gets unix time
                unix_time = int(time.time()) - int(afk[f'{member.id}']['time'])

                # user was afk for time.now() - time
                afktime = humanize.naturaltime(
                    datetime.datetime.now() - datetime.timedelta(seconds=unix_time))

                # add embed
                afk_alert.add_field(
                    name=f"{member.display_name.replace('[AFK]', '')} - {afktime}", value=f"\"{reason}\"", inline=True)

                # plus 1 time mentioned in afk.json
                afk[f'{member.id}']['mentions'] = int(
                    afk[f'{member.id}']['mentions']) + 1

                # save json
                with open('./data/afk.json', 'w') as f:
                    json.dump(afk, f, indent=4, sort_keys=True)

        if send:
            await other.OtherUtils.sendafk(self, message, ["afk_alert", "afk_alert_dm"], afk_alert)
        await other.OtherUtils.update_data(afk, message.author)
        # if message's author is afk continue
        if list(message.content.split())[0] != f'{prefix}afk' and afk[f'{message.author.id}']['AFK']:
            # unix now - unix since afk
            timeafk = int(time.time()) - \
                int(afk[f'{message.author.id}']['time'])

            # make time readable for user
            afktime = other.OtherUtils.period(datetime.timedelta(
                seconds=round(timeafk)), "{d}d {h}h {m}m {s}s")

            # get mentions
            mentionz = afk[f'{message.author.id}']['mentions']

            # make embed
            welcome_back = discord.Embed(
                description=f"**Welcome back {message.author.mention}!**")
            welcome_back.add_field(name="Afk for", value=afktime, inline=True)
            welcome_back.add_field(
                name="Mentioned", value=f"{mentionz} time(s)", inline=True)
            welcome_back.set_footer(
                text=f"Toggle: {prefix}wbalerts\nDMs Toggle: {prefix}wbdmalerts")

            # reset afk for user
            afk[f'{message.author.id}']['AFK'] = False
            afk[f'{message.author.id}']['reason'] = 'None'
            afk[f'{message.author.id}']['time'] = '0'
            afk[f'{message.author.id}']['mentions'] = 0
            with open('./data/afk.json', 'w') as f:
                json.dump(afk, f, indent=4, sort_keys=True)

            # try to reset nickname
            try:
                nick = message.author.display_name.replace('[AFK]', '')
                await message.author.edit(nick=nick)
            except:
                print(
                    f'I wasnt able to edit [{message.author} / {message.author.id}].')

            await other.OtherUtils.sendafk(self, message, ["wb_alert", "wb_alert_dm"], welcome_back)
        with open('./data/afk.json', 'w') as f:
            json.dump(afk, f, indent=4, sort_keys=True)

    @commands.Cog.listener("on_message")
    async def help_check(self, message):
        # check if user's message is only bot ping and reply with help, if not process commands
        if message.author.bot == False and self.bot.user.mentioned_in(message) and len(message.content) == len(self.bot.user.mention):
            await message.reply(embed=discord.Embed(description=f'My prefix is `{main.get_prefix(self, message)}`, you can also use slash commands\nFor more info use the {main.get_prefix(self, message)}help command!'), delete_after=20, mention_author=False)
        else:
            await self.bot.process_commands(message)

    @commands.Cog.listener("on_message")
    async def replies(self, message):
        global counter
        # automatic responses
        if "eulog" in message.content.lower():
            await message.add_reaction(self.eulogy_emoji)
            counter += 1
        if "cleansing pool" in message.content.lower():
            await message.reply("Watch your language.")

        if not message.author.bot:
            # "ask newt" functionality
            if self.bot.user.mentioned_in(message) and len(message.content) >= len(self.bot.user.mention):
                await message.reply(random.choice(self.convo_replies))
            # survivor responses
            annoying = {"mando": "Ew.",
                        "huntress": "Her burden :flushed:",
                        "bandit": "Bandit makes some mighty fine beans.",
                        "engi": "<:BUNGUS:977317901277212722> :heart: ***B U N G U S*** :heart: <:BUNGUS:977317901277212722>",
                        "arti": "Ion surge OP, pls nerf",
                        "merc": "I simply never get hit as i utilise my I-frames perfectly leaving no opening to be hit by enemy attacks, and if you dislike merc you simply have a massive skill issue and wasted your time trying to get bitches instead of studying the blade",
                        "rex": "Knock knock \n who's there? \n A concussion from a high amplitude sonic boom ⨉ What's pink and green and is about to show you the definition of pain?",
                        "loader": "Beat mitrhix into a bloody pulp any% speedrun",
                        "acrid": ":heart Acid doggy :heart:",
                        "cap": "Thermonuclear warfare :thumbsup:",
                        "gunner": "Epic railer MLG quickscope compilation #69",
                        "fiend viend": "I LOVE LEAN",
                        "goat ⨉ hoof ⨉ drink": """Go, go, go, go, go, go, go\n\nGotta go fast, gotta go fast\nGotta go faster, faster, faster, faster, faster!\n\nMovin' at speed of sound (make tracks!)\nQuickest hedgehog around\nGot ourselves a situation\nStuck in a new location\nWithout any explanation\nNo time for relaxation!\n\nDon't, don't, don't, don't, don't blink, don't think\nJust go, go, go, go, g-g-g-g-go, go!\n\nN-n-n-n-n-n-na\nN-n-n-n-n-n-na\n\nSonic, he's on the run!\nSonic, he's number one!\nSonic, he's comin' next!\nSo watch out... For Sonic X!\n\nGotta go fast (Sonic!)\nGotta go fast (Sonic!)\nGotta go faster, faster, faster, faster, faster!\nGo, go, go, go, go, go, go\nSonic X!\n\nGotta go fast, gotta go fast\nGotta go faster, faster, faster, faster, faster!\nSonic X!""",
                        "mul-t ⨉ mult ⨉ multi": "Haha MUL-T double nail go ***brrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr***",
                        "nya ⨉ meow": "Wowwwww, you meow like a cat! That means you are one, right? Shut the fuck up. If you want to be put on a leash and treated like a domestic animal, that's called a fetish, not “quirky” or “cute.” What part of you seriously thinks that any portion of acting like a feline establishes a reputation of appreciation? Is it your lack of any defining aspect of personality that urges you to resort to shitty representations of cats to create an illusion of meaning in your worthless life? Wearing “cat ears” in the shape of headbands further notes the complete absence of human attribution to your false sense of personality, such as intelligence or charisma in any form or shape. Where do you think this mindset's going to lead you? Do you think you're funny, random, quirky even? What makes you think that acting like a fucking cat will make a goddamn hyena laugh? I, personally, feel highly sympathetic towards you as your only escape from the worthless thing you call your existence is to pretend to be an animal. But it's not a worthy choice to assert this horrifying fact as a dominant trait, mainly because personality traits require an initial personality to lay their foundation on. You're not worthy of anybody's time, so go fuck off, \"cat-girl.\""
                        }

            for trigger, reply in annoying.items():
                multi_trigger = list(trigger.split(' ⨉ '))
                for triggers in multi_trigger:
                    if triggers in message.content.lower():
                        reply = random.choice(list(reply.split(' ⨉ ')))
                        await message.reply(reply)

        # handle lunar coins dropping
        if random.randint(1, 20) <= 3 and message.author.bot == False:
            await message.add_reaction(self.lunar_coin_emoji)

            try:

                self.save[message.author.id]["coins"] += 1
            except:
                self.save[message.author.id] = {
                    "coins": 1,
                    "eulogies": 0
                }

    @tasks.loop(minutes=1)
    async def autosave(self):
        print("Saving to disk...", end=' ')

        with open("./data/save.json", mode="w", encoding="utf-8") as savefile:
            savefile.write(json.dumps(self.save, sort_keys=True, indent=4))
            savefile.flush()

        with open("./data/hugs.txt", mode="w", encoding="utf-8") as file:
            file.write(str(self.hugs))
            file.flush()

        print("Done!")
