import discord
import random
from discord.ext import commands

from json_commands import *


class Admin(commands.Cog, name="Main Commands"):
    """You make me une pocoloco"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="addadmin")
    async def add_admin(self, ctx, user: discord.User):
        """Adda adadadmin"""
        if ctx.author.id == 737259502646198354:  # Make sure to change this to your id, this is just to make it so only I can add admins
            admins = open_json("Cog/admin/Cog/admin/admins.json")
            for admin in admins:
                if admin['user_id'] == user.id:
                    await ctx.send(f"{user.mention} is already admin poop")
                    return
                new_admin = {
                    "user_id": user.id
                }
                admins.append(new_admin)
                save_json(admins, "Cog/admin/Cog/admin/admins.json")
                await ctx.send(f"{user.mention} is now admim11! Congratulatsason")
                return
        else:
            await ctx.send("Wait, your not me!")

    @commands.command(name="add")
    async def add(self, ctx, *, angry_message):
        """Add an angry message - for the cool guys only"""
        admins = open_json("Cog/admin/Cog/admin/admins.json")
        for admin in admins:
            if admin['user_id'] == ctx.author.id:
                angry_responses = open_json("Cog/admin/angry_responses.json")
                for angry_resonse in angry_responses:
                    if angry_resonse['response'] == angry_message:
                        await ctx.send("*This is a strong message!* This is already a response m8")
                        return
                new_response = {
                    "response": angry_message
                }
                angry_responses.append(new_response)
                save_json(angry_responses, "Cog/admin/angry_responses.json")
                await ctx.send(f"**{angry_message}** has been added")
                return
        await ctx.send("You aren't an admin m8. Daft pisser")

    @commands.command(name="delete")
    async def delete(self, ctx, *, angry_message):
        """Donker an angry message - for the cool guys only"""
        admins = open_json("Cog/admin/admins.json")
        for admin in admins:
            if admin['user_id'] == ctx.author.id:
                angry_responses = open_json("Cog/admin/Cog/admin/angry_responses.json")
                for angry_response in angry_responses:
                    if angry_response["response"] == angry_message:
                        angry_responses.remove(angry_response)
                        save_json(angry_responses, "Cog/admin/angry_responses.json")
                        await ctx.send(f"**{angry_message}** has been deleted")
                        break
                await ctx.send("That response was not found sorry luv.")
                return
        await ctx.send("You aren't an admin m8. Daft pisser")

    @commands.command(name="list")
    async def list(self, ctx):
        """Get a list of all responses"""
        responses = open_json("Cog/admin/angry_responses.json")
        response_list = []
        for response in responses:
            response_list.append(f"- {response['response']}\n")
        await ctx.send(f"```md\n{''.join(response_list)}```")

    @commands.command(name="stats")
    async def stats(self, ctx):
        """Stunktunktists"""
        guilds = len(self.bot.guilds)
        embed = discord.Embed(color=discord.Color.green())
        embed.add_field(name="Guilds", value=f"{guilds}", inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="admins")
    async def admins(self, ctx):
        """Cuck mins"""
        admins = open_json("Cog/admin/admins.json")
        admin_array = []
        for admin in admins:
            user = self.bot.get_user(admin['user_id'])
            admin_array.append(f"- {user.name} \n")
        await ctx.send(f"```md\n{''.join(admin_array)}```")

    @commands.command(name='invite')
    async def invite(self, ctx):
        """Inviter bot or something idk. Basically what I'm trying to say in the pudding haha!"""
        await ctx.send("<https://julians.work/angry> <-- click to invite bot")


def setup(bot):
    bot.add_cog(Admin(bot))


