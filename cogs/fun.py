import discord
from discord.ext import commands, bridge
from cogs import block, utils, events
from typing import Optional
import datetime
import random
# get image from url
import aiohttp
# image
from io import BytesIO
from petpetgif import petpet


def setup(bot):
    bot.add_cog(FunCommands(bot))


class FunCommands(commands.Cog, name="Fun"):
    """Commands you can use on other users for fun."""
    COG_EMOJI = "🚀"

    def __init__(self, bot):
        self.bot = bot
        self.hug_gifs = bot.hug_gifs
        self.hug_words = bot.hug_words
        self.hug_words_bot = bot.hug_words_bot
        self.kiss_gifs = bot.kiss_gifs
        self.kiss_words = bot.kiss_words
        self.kiss_words_bot = bot.kiss_words_bot
        self.jokes = bot.jokes
        self.eulogy_emoji = bot.eulogy_emoji

    async def checkperm(self, bot, perm):
        if await block.BlockUtils.get_perm(perm, bot.author) or bot.author.guild_permissions.administrator:
            return
        else:
            await utils.senderror(bot, f"{bot.author.mention}, You aren\'t allowed to use this")

    async def checkping(self, bot, member):
        if await block.BlockUtils.get_perm("ping", member):
            await utils.senderror(bot, f"This person has disallowed me from using them in commands.")

    @bridge.bridge_command(name="pet")
    @commands.guild_only()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def pet(self, bot, member: Optional[discord.member.Member], emoji: Optional[discord.PartialEmoji], url=None):
        """Pet someone :D"""
        await self.checkperm(bot, "pet")
        attachment = None
        try:
            attachment = bot.message.attachments[0]
        except:
            pass
        image = member or emoji or attachment or url
        if type(image) == discord.PartialEmoji:
            what = "an emoji"
            image = await image.read()
        elif type(image) == discord.Attachment:
            what = "an image"
            image = await image.read()
        elif url is not None:
            url = bot.message.content.split(" ")[1]
            disable = {'<', '>'}
            for key in disable.items():
                url = url.replace(key, '')
            what = "an image"
            async with aiohttp.ClientSession().get(url) as url:
                if url.status != 200:
                    await utils.senderror(bot, "Could not download file")
                image = await url.read()
        elif type(image) == discord.member.Member:
            await self.checkping(bot, image)
            what = image.mention
            image = await image.avatar.with_format('png').read()
        else:
            await utils.senderror(bot, "Please use a custom emoji or tag a member to petpet their avatar.")
        # retrieve the image bytes above
        # file-like container to hold the emoji in memory
        source = BytesIO(image)  # sets image as "source"
        dest = BytesIO()  # container to store the petpet gif in memory
        # takes source (image) and makes pet-pet and puts into memory
        petpet.make(source, dest)
        # set the file pointer back to the beginning so it doesn't upload a blank file.
        dest.seek(0)
        filename = f"{image[0]}-petpet.gif"
        file = discord.File(dest, filename=filename)
        e = discord.Embed(description=f"{bot.author.mention} has pet {what}")
        e.set_image(url=f"attachment://{filename}")
        if await utils.CheckInstance(bot):
            await bot.respond(embed=e, file=file, mention_author=False)
        else:
            await bot.respond(embed=e, file=file)

    @commands.command(hidden=True, name="hug")
    @commands.guild_only()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def hug(self, bot, *, member: Optional[discord.Member]):
        """Hug someone :O"""
        await self.checkperm(bot, "weird")
        if member == None:
            events.hugs += 1
            e = discord.Embed(
                description=f"{bot.author.mention} you didnt mention anyone but you can still {(random.choice(self.hug_words_bot))} me!", color=0x0690FF)
        else:
            await self.checkping(bot, member)
            e = discord.Embed(
                description=f"{bot.author.mention} {(random.choice(self.hug_words))} {member.mention}", color=0x0690FF)
        e.set_image(url=(random.choice(self.hug_gifs)))
        await utils.sendembed(bot, e)

    @commands.command()
    async def hugcount(self, bot):
        await bot.message.reply("I have been hugged " + str(events.hugs) + " times. :heart:")

    @commands.command(hidden=True, name="kiss")
    @commands.guild_only()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def kiss(self, bot, *, member: Optional[discord.Member]):
        """Kiss someone :O"""
        await self.checkperm(bot, "weird")
        if member == None:
            e = discord.Embed(
                description=f"{bot.author.mention} you didnt mention anyone but you can still {(random.choice(self.kiss_words_bot))} me!", color=0x0690FF)
        else:
            await self.checkping(bot, member)
            e = discord.Embed(
                description=f"{bot.author.mention} {(random.choice(self.kiss_words))} {member.mention}", color=0x0690FF)
        e.set_image(url=(random.choice(self.kiss_gifs)))
        await utils.sendembed(bot, e)

    @commands.command(hidden=True, name="fall")
    @commands.guild_only()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def fall(self, bot, *, member: Optional[discord.Member]):
        """Make someone fall >:)"""
        await self.checkperm(bot, "joke")
        if member == None:
            e = discord.Embed(
                description=f"{bot.author.mention} you fell", color=0xFF6969)
        else:
            e = discord.Embed(
                description=f"{bot.author.mention} made {member.mention} fall!", color=0xFF6969)
        e.set_thumbnail(url=(
            "https://media.discordapp.net/attachments/854984817862508565/883437876493307924/image0-2.gif"))
        await utils.sendembed(bot, e)

    @commands.command(hidden=True, name="promote")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def promote(self, bot, member: discord.Member, *, message=None):
        """Promote someone :D"""
        await self.checkperm(bot, "joke")
        if member == bot.author:
            e = discord.Embed(
                description=f"{bot.author.mention} promoted themselves to {message}", color=0xFF6969)
        else:
            e = discord.Embed(
                description=f"{bot.author.mention} promoted {member.mention} to {message}", color=0xFF6969)
        await utils.sendembed(bot, e)

    @commands.command(hidden=True, name="noclip")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def noclip(self, bot):
        """Go rogue.."""
        e = discord.Embed(
            description=f"{bot.author.mention} is going rogue..", color=0xff0000)
        e.set_image(
            url=("https://c.tenor.com/xnQ97QtwQGkAAAAC/mm2roblox-fly-and-use-noclip.gif"))
        await utils.sendembed(bot, e)

    @commands.command(hidden=True, name="abuse")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def abuse(self, bot, *, member: Optional[discord.Member]):
        """Adbmind abuse!!"""
        if member == None:
            e = discord.Embed(
                description=f"{bot.author.mention} is going to abuse 😈", color=0xff0000)
        else:
            e = discord.Embed(
                description=f"{bot.author.mention} is going to abuse {member.mention} 😈", color=0xff0000)
        e.set_image(
            url=("https://i.pinimg.com/originals/e3/15/55/e31555da640e9f8afe59239ee1c2fc37.gif"))
        await utils.sendembed(bot, e)

    @commands.command(name="joke")
    async def joke(self, bot):  # send a random joke out of the list
        await bot.message.reply(random.choice(self.jokes))

    @commands.command(name="jokerep")
    async def jokerep(self, bot, *, jrep):  # suggest a joke to add to the bot
        await bot.message.channel.send(
            "Your joke was recorded. It will be added if Wiki or Crow approves of it.")
        jokefile = open("./data/jokes.txt", "a")
        jokefile.write("\n" + jrep + "\n")
        jokefile.close
        del jokefile

    @commands.command(name="fban")
    async def fban(self, bot, member: discord.Member, *, reason=None):
        e = discord.Embed(
            title="User Banned",
            description="Banned user " + str(member),
            timestamp=datetime.datetime.utcnow(),
            color=discord.Color.red()
        )

        e.add_field(name="Reason", value=str(reason))

        await utils.sendembed(bot, e, delete=2, delete_speed=None)

    @commands.command()
    async def eulogy(self, bot):  # send eulogy
        await bot.message.reply(self.eulogy_emoji)
