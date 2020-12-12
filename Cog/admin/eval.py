import ast
import discord
import asyncio
from tokens import *
import json_commands as jc

from discord.ext import commands
from functools import wraps, partial


def async_wrap(func):
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)
    return run 

def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the or else
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)


class Eval(commands.Cog, name="Eval Commands"):
    """You make me une pocoloco"""

    def __init__(self, bot):
        self.bot = bot
        self.ctx = None
        self.values = []

    @commands.command()
    async def eval(self, ctx, *, cmd):
        """Evaluates input. Lolw someone easelse code!"""
        admins = jc.open_json("Cog/admin/admins.json")
        for admin in admins:
            if admin['user_id'] == ctx.author.id:
                fn_name = "_eval_expr"

                cmds = cmd.strip("` ")

                # add a layer of indentation
                full = []
                for line in cmds.splitlines():
                    if line.startswith("print"):
                        full.append(f"await {line}")
                    full.append(line)
                cmd = "\n".join(f"    {i}" for i in full)

                # wrap in async def body
                body = f"async def {fn_name}():\n{cmd}"

                parsed = ast.parse(body)
                body = parsed.body[0].body

                insert_returns(body)

                self.ctx = ctx

                async def custom_print(value):
                    await ctx.send(value)

                env = {
                    'bot': ctx.bot,
                    'discord': discord,
                    'commands': commands,
                    'ctx': ctx,
                    '__import__': __import__,
                    'print': custom_print,
                    'reload': lambda: self.reload_bot(ctx),
                    'change_status': self.change_status
                }
                exec(compile(parsed, filename="<ast>", mode="exec"), env)

                try:
                    result = (await eval(f"{fn_name}()", env))
                except Exception as e:
                    result = e
                    await ctx.send(e)
                    return
                for value in self.values:
                    try:
                        if TOKEN in value:
                            await ctx.send("This output contains sensitive information, therefore it has been ctrl alt deleted")
                            return
                    except:
                        pass
                return
        await ctx.send("YOu're bnot an admins!!!!11!!?!?!?....,,.,.,.,.,.,.,. a a a a a a a a a a a")

    async def change_status(self, status):
        await self.bot.change_presence(activity=discord.Game(name=status))
        await self.ctx.send(f"Change status to `playing {status}`")
    

    async def reload_bot(self, ctx):
        await ctx.send("reloading...")
        await self.bot.logout()
        await self.bot.login()


def setup(bot):
    bot.add_cog(Eval(bot))