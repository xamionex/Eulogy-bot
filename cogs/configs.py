from discord.ext import commands
import json


def setup(bot):
    bot.add_cog(Configs(bot))


class Configs(commands.Cog, name="Configs"):
    """Configuration objects (no commands)."""
    COG_EMOJI = "⚙️"

    def __init__(self, bot):
        bot.eulogy_emoji = "<:eulogy_zero:967096744800296970>"
        bot.lunar_coin_emoji = "<:lunar_coin:967122007089119242>"
        bot.lunar_symbol = "<:lunar_symbol:972089212264407070>"
        bot.last_dice_usage = 0
        bot.counter = 0
        bot.first_eulogycount = True
        with open('./data/save.json', mode='r', encoding='utf-8') as file:
            data = file.read()
            data.replace('\n', '')
            data.replace('\t', '')
        bot.save = json.loads(data)
        with open("./data/hugs.txt", mode='r', encoding='utf-8') as file:
            bot.hugs = int(file.read())
        bot.jokes = ["Alien Head.",
                     "Ion Surge.",
                     "Suppressive Fire."]
        bot.convo_replies = ["Yes.",
                             "No.",
                             "Definitely not.",
                             "I guess?",
                             "I'm not answering that.",
                             "That doesn't matter.",
                             "I don't think so.",
                             "What exactly do you mean by that?",
                             "I think so.",
                             "I don't know, I just got here.",
                             "I don't know.",
                             "For sure.",
                             "I agree.",
                             "Most definitely yes.",
                             "Fuck you."]
        bot.hug_gifs = ["https://media1.tenor.com/images/7e30687977c5db417e8424979c0dfa99/tenor.gif",
                        "https://media1.tenor.com/images/4d89d7f963b41a416ec8a55230dab31b/tenor.gif",
                        "https://media1.tenor.com/images/45b1dd9eaace572a65a305807cfaec9f/tenor.gif",
                        "https://media1.tenor.com/images/b4ba20e6cb49d8f8bae81d86e45e4dcc/tenor.gif",
                        "https://media1.tenor.com/images/949d3eb3f689fea42258a88fa171d4fc/tenor.gif",
                        "https://media1.tenor.com/images/72627a21fc298313f647306e6594553f/tenor.gif",
                        "https://media1.tenor.com/images/d3dca2dec335e5707e668b2f9813fde5/tenor.gif",
                        "https://media1.tenor.com/images/eee4e709aa896f71d36d24836038ed8a/tenor.gif",
                        "https://media1.tenor.com/images/b214bd5730fd2fdfaae989b0e2b5abb8/tenor.gif",
                        "https://media1.tenor.com/images/edea458dd2cbc76b17b7973a0c23685c/tenor.gif",
                        "https://media1.tenor.com/images/506aa95bbb0a71351bcaa753eaa2a45c/tenor.gif",
                        "https://media1.tenor.com/images/42922e87b3ec288b11f59ba7f3cc6393/tenor.gif",
                        "https://media1.tenor.com/images/bb841fad2c0e549c38d8ae15f4ef1209/tenor.gif",
                        "https://media1.tenor.com/images/234d471b1068bc25d435c607224454c9/tenor.gif",
                        "https://media1.tenor.com/images/de06f8f71eb9f7ac2aa363277bb15fee/tenor.gif"]
        bot.hug_words = ['hugged',
                         'cuddled',
                         'embraced',
                         'squeezed',
                         'is holding onto',
                         'is caressing']
        bot.hug_words_bot = ['hug',
                             'cuddle',
                             'embrace',
                             'squeeze',
                             'hold onto',
                             'caress']
        bot.kiss_gifs = ["https://c.tenor.com/YTsHLAJdOT4AAAAC/anime-kiss.gif",
                         "https://c.tenor.com/wDYWzpOTKgQAAAAC/anime-kiss.gif",
                         "https://c.tenor.com/F02Ep3b2jJgAAAAC/cute-kawai.gif",
                         "https://c.tenor.com/Xc6y_eh0IcYAAAAd/anime-kiss.gif",
                         "https://c.tenor.com/sDOs4aMXC6gAAAAd/anime-sexy-kiss-anime-girl.gif",
                         "https://c.tenor.com/dp6A2wF5EKYAAAAC/anime-love.gif",
                         "https://c.tenor.com/OOwVQiBrXiMAAAAC/good-morning.gif",
                         "https://c.tenor.com/I8kWjuAtX-QAAAAC/anime-ano.gif",
                         "https://c.tenor.com/TWbZjCy8iN4AAAAC/girl-anime.gif"]
        bot.kiss_words = ['kissed',
                          'smooched',
                          'embraced']
        bot.kiss_words_bot = ['kiss',
                              'smooch',
                              'embrace']
