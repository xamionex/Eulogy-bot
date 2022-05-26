from discord.ext import commands
import math
import random
import discord


def setup(bot):
    bot.add_cog(CurrencyCommands(bot))


class CurrencyCommands(commands.Cog, name="Currency Commands"):
    """Commands for currency."""
    COG_EMOJI = "❔"

    def __init__(self, bot):
        self.bot = bot
        self.save = bot.save
        self.eulogy_emoji = bot.eulogy_emoji
        self.lunar_symbol = bot.lunar_symbol

    @commands.command()
    async def currencyinfo(self, bot):
        info = """Everytime you send a message, there's a 15% chance for a lunar coin to drop.
        If a lunar coin drops, the bot will react with the lunar coin emote to your message.
        You can see how many lunar coins you have by using $lunarcoins. You can buy lunar pods with your coins using $lunarpod [tier].
        Every lunar pod scales differently in price with how many coins you have and has different amounts of eulogy it can drop.
        You can check in-depth stats for lunar pods with $bazaar. After acquiring some eulogies,
        you can use $eulogies to check how many eulogies you have and $leaderboard to see the five people with the most eulogies."""

        await bot.message.reply(info)

    @commands.command()
    async def lunarcoins(self, bot):
        try:
            await bot.message.reply("You have " + str(self.save[bot.message.author.id]["coins"]) + " " + self.lunar_symbol + "!")
        except:
            self.save[bot.message.author.id] = {
                "coins": 0,
                "eulogies": 0
            }

            await bot.message.reply("You have " + str(self.save[bot.message.author.id]["coins"]) + " " + self.lunar_symbol + "!")

    @commands.command()
    async def eulogies(self, bot):
        try:
            await bot.message.reply("You have " + str(self.save[bot.message.author.id]["eulogies"]) + " " + self.eulogy_emoji + "!")
        except:
            self.save[bot.message.author.id] = {
                "coins": 0,
                "eulogies": 0
            }

            await bot.message.reply("You have " + str(self.save[bot.message.author.id]["eulogies"]) + " " + self.eulogy_emoji + "!")

    @commands.command()
    async def lunarpod(self, bot, type=None):
        if not type in ["1", "2", "3", "4", "5", "6"] or type == None:
            await bot.message.reply("Use `$lunarpod [type]` to open a lunar pod. Use `$bazaar` to see types of lunar pods.")
            return

        if self.save[bot.message.author.id]["coins"] <= 0:
            await bot.message.reply("You do not have sufficient lunar coins. Use `$bazaar` to see prices.")
            return

        eulogies_dropped = 0

        if type == "1":
            if self.save[bot.message.author.id]["coins"] < 3:
                await bot.message.reply("You do not have sufficient lunar coins. Use `$bazaar` to see prices.")
                return

            self.save[bot.message.author.id]["coins"] -= 3

            if random.randint(1, 20) == 20:
                eulogies_dropped += 1
        elif type == "2":
            if self.save[bot.message.author.id]["coins"] < math.ceil((6 + ((self.save[bot.message.author.id]["coins"] / 100) * 8))):
                await bot.message.reply("You do not have sufficient lunar coins. Use `$bazaar` to see prices.")
                return

            self.save[bot.message.author.id]["coins"] -= math.ceil(
                (6 + ((self.save[bot.message.author.id]["coins"] / 100) * 8)))

            if random.randint(1, 100) <= 15:
                eulogies_dropped += 1
        elif type == "3":
            if self.save[bot.message.author.id]["coins"] < math.ceil((9 + ((self.save[bot.message.author.id]["coins"] / 100) * 16))):
                await bot.message.reply("You do not have sufficient lunar coins. Use `$bazaar` to see prices.")
                return

            self.save[bot.message.author.id]["coins"] -= math.ceil(
                (9 + ((self.save[bot.message.author.id]["coins"] / 100) * 16)))

            if random.randint(1, 20) <= 30:
                eulogies_dropped += 1
        elif type == "4":
            if self.save[bot.message.author.id]["coins"] < math.ceil((12 + ((self.save[bot.message.author.id]["coins"] / 100) * 24))):
                await bot.message.reply("You do not have sufficient lunar coins. Use `$bazaar` to see prices.")
                return

            self.save[bot.message.author.id]["coins"] -= math.ceil(
                (12 + ((self.save[bot.message.author.id]["coins"] / 100) * 24)))

            if random.randint(1, 20) <= 60:
                eulogies_dropped += 1
        elif type == "5":
            if self.save[bot.message.author.id]["coins"] < math.ceil((15 + ((self.save[bot.message.author.id]["coins"] / 100) * 32))):
                await bot.message.reply("You do not have sufficient lunar coins. Use `$bazaar` to see prices.")
                return

            self.save[bot.message.author.id]["coins"] -= math.ceil(
                (15 + ((self.save[bot.message.author.id]["coins"] / 100) * 32)))

            eulogies_dropped += 1 + random.randint(0, 5)
        elif type == "6":
            if self.save[bot.message.author.id]["coins"] < math.ceil((18 + ((self.save[bot.message.author.id]["coins"] / 100) * 40))):
                await bot.message.reply("You do not have sufficient lunar coins. Use `$bazaar` to see prices.")
                return

            self.save[bot.message.author.id]["coins"] -= math.ceil(
                (18 + ((self.save[bot.message.author.id]["coins"] / 100) * 40)))

            eulogies_dropped += 1 + random.randint(0, 10)

        reply = "Drops from Lunar Pod ("

        for i in range(0, int(type)):
            reply += u"\u2605"
        for i in range(0, (6 - int(type))):
            reply += u"\u2606"

        reply += "):\n" + self.eulogy_emoji + " " + str(eulogies_dropped)

        self.save[bot.message.author.id]["eulogies"] += eulogies_dropped

        await bot.message.reply(reply)

    @commands.command()
    async def bazaar(self, bot):
        embed = discord.Embed(
            title="The Bazaar Between Time",
            description="Types of lunar pods that you can buy and open. Prices are displayed based on " +
            bot.message.author.mention + "'s lunar coins.",
            color=discord.Color.red()
        )

        embed.add_field(
            name=u"Lunar Pod (\u2605\u2606\u2606\u2606\u2606\u2606)",
            value="5% chance for one eulogy.\nPrice: 3 " +
            self.lunar_symbol + ".\nUse `$lunarpod 1` to open."
        )

        embed.add_field(
            name=u"Lunar Pod (\u2605\u2605\u2606\u2606\u2606\u2606)",
            value="15% chance for one eulogy.\nPrice: " +
            str(math.ceil((6 + ((self.save[bot.message.author.id]["coins"] / 100) * 8)))
                ) + " " + self.lunar_symbol + ".\nUse `$lunarpod 2` to open."
        )

        embed.add_field(
            name=u"Lunar Pod (\u2605\u2605\u2605\u2606\u2606\u2606)",
            value="30% chance for one eulogy.\nPrice: " +
            str(math.ceil((9 + ((self.save[bot.message.author.id]["coins"] / 100) * 16)))
                ) + " " + self.lunar_symbol + ".\nUse `$lunarpod 3` to open."
        )

        embed.add_field(
            name=u"Lunar Pod (\u2605\u2605\u2605\u2605\u2606\u2606)",
            value="60% chance for one eulogy.\nPrice: " +
            str(math.ceil((12 + ((self.save[bot.message.author.id]["coins"] / 100) * 24)))
                ) + " " + self.lunar_symbol + ".\nUse `$lunarpod 4` to open."
        )

        embed.add_field(
            name=u"Lunar Pod (\u2605\u2605\u2605\u2605\u2605\u2606)",
            value="Contains a guaranteed eulogy and up to 5 bonus eulogies.\nPrice: " +
            str(math.ceil((15 + ((self.save[bot.message.author.id]["coins"] / 100) * 32)))
                ) + " " + self.lunar_symbol + ".\nUse `$lunarpod 5` to open."
        )

        embed.add_field(
            name=u"Lunar Pod (\u2605\u2605\u2605\u2605\u2605\u2605)",
            value="Contains a guaranteed eulogy and up to 10 bonus eulogies.\nPrice: " +
            str(math.ceil((18 + ((self.save[bot.message.author.id]["coins"] / 100) * 40)))
                ) + " " + self.lunar_symbol + ".\nUse `$lunarpod 6` to open."
        )

        await bot.send(embed=embed)

    @commands.command()
    async def leaderboard(self, bot):
        embed = discord.Embed(
            title="Eulogy Zero Leaderboard",
            description="The leaderboard of who has the most eulogies.",
            color=0x5efcff
        )

        leaderboard = []
        ids = []
        eulogycounts = []

        for key in self.save:
            ids.append(self.save[key]["id"])
            eulogycounts.append(self.save[key]["eulogies"])

        for i in range(5):
            eulogy_count = max(eulogycounts)
            user_id = ids[eulogycounts.index(eulogy_count)]

            leaderboard.append([user_id, eulogy_count])

            ids.remove(user_id)
            eulogycounts.remove(eulogy_count)

        for i in range(5):
            user = await bot.message.guild.fetch_member(leaderboard[i][0])

            embed.add_field(
                name=str(i + 1) + ". " + user.name,
                value=self.eulogy_emoji + str(leaderboard[i][1]),
                inline=False
            )

        await bot.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def diceroll(self, bot):  # roll a dice
        if random.randint(1, 6) == 6:
            await bot.message.reply("You rolled a 6, so here's a lunar coin!")

            try:
                self.save[bot.message.author.id]["coins"] += 1
            except:
                self.save[bot.message.author.id] = {
                    "coins": 1,
                    "eulogies": 0,
                    "id": bot.message.author.id
                }
        else:
            await bot.message.reply("You sadly didn't get a 6.")
