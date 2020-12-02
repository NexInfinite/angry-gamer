import discord
import asyncio
import random
from tokens import *
from discord.ext import commands, tasks

from json_commands import *

intents = discord.Intents().all()
bot = commands.Bot(command_prefix="a!", intents=intents)

startup_extensions = ["Cog.admin.help_command", "Cog.admin.main", "Cog.responses.main", "Cog.admin.eval"]


@bot.event
async def on_ready():
    # On read, after startup
    print(f"Connecting...\nConnected {bot.user}\n")  # Send message on connected
    gamer_loop.start()


if __name__ == "__main__":  # When script is loaded, this will run
    bot.remove_command("help")
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)  # Loads cogs successfully
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))  # Failed to load cog, with error


@tasks.loop()
async def gamer_loop():
    games = ['League of Legends', 'Rainbow Six Siege', 'Flappy birds', 'Devil May Cry 3', 'Dota 2', 'Dark souls', 'Cup head', "Don't ping me", "Don't ping me", "Don't ping me", "Don't ping me", "Don't ping me", "download more ram @ julians.work/angry", "download more ram @ julians.work/angry", "download more ram @ julians.work/angry"]
    random_game = games[random.randint(0, len(games) - 1)]
    await bot.change_presence(activity=discord.Game(name=random_game))
    while True:
        rng = random.randint(0, 20)
        if rng == 0:
            random_game = games[random.randint(0, len(games)-1)]
            await bot.change_presence(activity=discord.Game(name=random_game))
        await asyncio.sleep(60)


bot.run(TOKEN)  # Run bot with token
