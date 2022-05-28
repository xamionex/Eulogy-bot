import json
import discord
from discord.ext import commands, bridge
from cogs import utils, block, configs
# afk command data
import time


def setup(bot):
    bot.add_cog(UserCommands(bot))


class UserCommands(commands.Cog, name="User Commands"):
    """User commands, mostly information."""
    COG_EMOJI = "👤"

    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command(name="rep")
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def rep(self, bot, user: discord.Member = None, type=None):
        """Add reputation to a user."""
        if user is None:
            e = discord.Embed(title=f"{self.bot.guild_prefixes[str(bot.guild.id)]}rep <mention> <type>",
                              description="`❌` **You must mention someone and pick one of these for the type of rep:**", color=0xFF6969)
            e.add_field(
                name="Positive", value=f"`{'`, `'.join(self.bot.rep_type_positive)}`")
            e.add_field(
                name="Negative", value=f"`{'`, `'.join(self.bot.rep_type_negative)}`")
            e.set_footer(
                text=f"For stats type {self.bot.guild_prefixes[str(bot.guild.id)]}showrep @user or {self.bot.guild_prefixes[str(bot.guild.id)]}showreps")
            await utils.sendembed(bot, e, show_all=False, delete=3, delete_speed=20)
            bot.command.reset_cooldown(bot)
            return
        if type not in self.bot.rep_type_combined:
            e = discord.Embed(
                description="`❌` **You must pick one of these for the type of rep:**", color=0xFF6969)
            e.add_field(
                name="Positive", value=f"`{'`, `'.join(self.bot.rep_type_positive)}`")
            e.add_field(
                name="Negative", value=f"`{'`, `'.join(self.bot.rep_type_negative)}`")
            e.set_footer(
                text=f"For stats type {self.bot.guild_prefixes[str(bot.guild.id)]}showrep @user or {self.bot.guild_prefixes[str(bot.guild.id)]}showreps")
            await utils.sendembed(bot, e, show_all=False, delete=3, delete_speed=15)
            bot.command.reset_cooldown(bot)
            return
        elif type in self.bot.rep_type_positive:
            if user.id == bot.author.id:
                await utils.senderror(bot, "You can't give rep to yourself")
            else:
                await UserUtils.change_rep(self, bot, "positive", user)
                await utils.sendembed(bot, discord.Embed(description=f"`➕` Giving {user.mention} positive rep"), show_all=False)
        elif type in self.bot.rep_type_negative:
            if user.id == bot.author.id:
                await utils.senderror(bot, "You can't give rep to yourself")
            else:
                await UserUtils.change_rep(self, bot, "negative", user)
                await utils.sendembed(bot, discord.Embed(description=f"`➖` Giving {user.mention} negative rep"), show_all=False)

    @commands.command(hidden=True, name="setrep")
    @commands.is_owner()
    async def setrep(self, bot, user: discord.Member, type, amount: int):
        """Set a user's reputation to a given amount."""
        if type in self.bot.rep_type_positive:
            await UserUtils.manage_rep(self, bot, "positive", user, amount)
            await utils.sendembed(bot, discord.Embed(description=f"`🛠️` Setting {user.mention}'s positive rep to {amount}"), show_all=False)
        elif type in self.bot.rep_type_negative:
            await UserUtils.manage_rep(self, bot, "negative", user, amount)
            await utils.sendembed(bot, discord.Embed(description=f"`🛠️` Setting {user.mention}'s negative rep to {amount}"), show_all=False)

    @bridge.bridge_command(name="showrep")
    async def showrep(self, bot, user: discord.Member = None):
        """Show a user's reputation"""
        user = user or bot.author
        rep = await UserUtils.get_rep(self, bot, user)
        e = discord.Embed(description=f"{user.mention}'s reputation:")
        e.add_field(name="Final Reputation", value=rep[0], inline=False)
        e.add_field(name="Positive Reputation", value=rep[1], inline=False)
        e.add_field(name="Negative Reputation", value=rep[2], inline=False)
        await utils.sendembed(bot, e, show_all=False, delete=3, delete_speed=20)

    @bridge.bridge_command(name="showreps")
    async def showreps(self, bot):
        """Shows global reputation of users"""
        f = 0
        p = 0
        n = 0
        for user in self.bot.reputation.items():
            p += user[1]["positive"]
            n += user[1]["negative"]
            f += user[1]["positive"] - user[1]["negative"]
        e = discord.Embed(description=f"**Global reputation:**")
        e.add_field(name="Final Reputation", value=f, inline=False)
        e.add_field(name="Positive Reputation", value=p, inline=False)
        e.add_field(name="Negative Reputation", value=n, inline=False)
        await utils.sendembed(bot, e, show_all=False, delete=3, delete_speed=20)

    @commands.command(hidden=True, name="resetrep")
    @commands.is_owner()
    async def resetrep(self, bot, user: discord.Member = None):
        """Reset a user's reputation"""
        user = user or bot.author
        rep = await UserUtils.open_rep(self, bot, user)
        rep.pop(str(user.id))
        try:
            await UserUtils.set_rep(self, bot, rep, user)
            await utils.sendembed(bot, e=discord.Embed(description=f"Successfully reset {user.mention}", color=0x66FF99))
        except:
            await utils.senderror(bot, f"Couldn't reset {user.mention}")

    @bridge.bridge_command(name="afk")
    async def afk(self, bot, *, reason=None):
        """Alerts users that mention you that you're AFK."""
        if reason:
            reason = utils.remove_newlines(reason)
        e = await UserUtils.setafk(self, bot, reason)
        await UserUtils.sendafk(self, bot, ["afk_alert", "afk_alert_dm"], e)

    @bridge.bridge_command(name="gn")
    async def gn(self, bot):
        """Sets your AFK to `Sleeping 💤`"""
        await UserUtils.setafk(self, bot, "Sleeping 💤")
        e = discord.Embed(description=f"Goodnight {bot.author.mention}")
        e.set_image(url="https://c.tenor.com/nPYfVs6FsBQAAAAS/kitty-kitten.gif")
        await UserUtils.sendafk(self, bot, ["afk_alert", "afk_alert_dm"], e)


class UserUtils():
    def __init__(self, bot):
        self.bot = bot

    async def open_member_rep(self, bot, user):
        rep = self.bot.reputation
        if str(user.id) in rep:
            return False
        else:
            await UserUtils.set_rep(self, bot, rep, user)

    async def set_rep(self, bot, rep, user):
        rep[str(user.id)] = {}
        for value in self.bot.rep_type_list:
            rep[str(user.id)][value] = 0
        configs.save(self.bot.reputation_path, "w", rep)
        return True

    async def get_rep(self, bot, user):
        rep = await UserUtils.open_rep(self, bot, user)
        current_rep = rep[str(user.id)]["positive"] - \
            rep[str(user.id)]["negative"]
        reps = [current_rep,
                rep[str(user.id)]["positive"],
                rep[str(user.id)]["negative"]]
        return reps

    async def change_rep(self, bot, change, user):
        rep = await UserUtils.open_rep(self, bot, user)
        rep[str(user.id)][change] += 1
        configs.save(self.bot.reputation_path, "w", rep)

    async def manage_rep(self, bot, change, user, amount):
        rep = await UserUtils.open_rep(self, bot, user)
        rep[str(user.id)][change] = amount
        configs.save(self.bot.reputation_path, "w", rep)

    async def open_rep(self, bot, user):
        await UserUtils.open_member_rep(self, bot, user)
        return self.bot.reputation

    async def setafk(self, bot, reason):
        afk = self.bot.afk
        if not reason:
            reason = 'AFK'
        elif reason and len(reason) > 100:
            await utils.senderror(bot, "You went over the 100 character limit")
        await UserUtils.update_data(afk, bot.author)
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
        if await block.GlobalBlockUtils.get_global_perm(self, bot, perm[0], bot.author):
            if await block.GlobalBlockUtils.get_global_perm(self, bot, perm[1], bot.author):
                await utils.senddmembed(bot, e)
            else:
                if isinstance(bot, bridge.BridgeApplicationContext):
                    await bot.reply(embed=e, ephemeral=True)
                else:
                    await bot.reply(embed=e, delete_after=10, mention_author=False)
