import discord
import random
from discord.ext import commands

from json_commands import *


class Angry(commands.Cog, name="Response Commands"):
    """You make me une pocoloco"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.content.startswith(self.bot.command_prefix):
            return

        if "Pog" in message.content:
            await message.channel.send("https://cdn.discordapp.com/attachments/746452338948046866/767071527496843264/rsz_pog2.png")
            return

        if "cum cookie" in message.content.lower():
            file = discord.File("Cog/responses/cumcookie.mp4", filename="cum-cookie.mp4")
            await message.channel.send(file=file)
            return

        mentions = message.mentions
        for mention in mentions:
            if mention.id == self.bot.user.id:
                response = get_angry()
                await message.channel.send(response)
                return

        # Prepare for what you are about to read, I call it being hella sexy!!!

        triggers = {
            "gamers": ["gamer", "game", "play", "playing"],
            "pingers": ['ping', 'mention', 'pinged', 'mentioned', 'everyone'],
            "cursed": ['2020', 'twenty twenty', 'worst year ever', 'worst year'],
            "cringed": ['minions', 'facebook', 'LOL!'],
            "sexy": ['sex', 'penis', 'dick', 'cock', 'cbt', 'cum', 'femboy', 'pp', 'hentai', 'felix', 'gay', 'bussy'],
            "ews": ['boobs', 'tits', 'pussy', 'boob']
        }

        responses = {
            "gamers": ['gamer gunk', 'Download ram here <https://julians.work/angry>', 'Can I join?', 'Is the party full?', 'Whats the score?', 'Did you start without me? Guys not again...', 'I have no one to play with. Every time I try to play a game I get kicked. Why does this keep happening to me? Why...'],
            "pingers": ['Who did it? I\'ll ping them back', 'I don\'t like this', 'All I can see is pings', 'Pong!!111!11!', 'Guys you can turn of pings in the notification settings for this server!', 'Please no not another ping....'],
            "cursed": ['Please don\'t curse us anymore', 'No, not 2020. Please no', 'I heard the aliens are up next', 'Whats 2020?', 'Oh god, what have you done?'],
            "cringed": ['MY KIDS LOVE MINIONS AS WELL!!!!', 'Are you also anti-vax? I don\' want my son to get autism!', '#flatEarthSociety', 'Trump 2020'],
            "sexy": ['hot', 'mmmmmm', 'tasty', 'Yo, can I get sum?', 'Give me... now!', 'I do love some of that', 'I\'m gonna cum', 'Yes please!', 'I\'ll have what they\'re having', 'How much?', 'Is there any left?'],
            "ews": ['ewwww', 'ucky', 'me no likey', 'I\'m gonna be sick', 'Why would you say that?', 'cock is better btw']
        }

        for word in message.content.split(" "):
            for trigger in triggers:
                for trig in triggers[trigger]:
                    if trig == word.lower():
                        response = responses[trigger][random.randint(0, len(responses[trigger]) - 1)]
                        await message.channel.send(response)
                        return

        # Damn you're still alive after reading that? Streamline af!


def setup(bot):
    bot.add_cog(Angry(bot))


def get_angry():
    angry_responses = open_json("Cog/responses/angry_responses.json")
    angry_response = angry_responses[random.randint(0, len(angry_responses)-1)]['response']
    return angry_response


