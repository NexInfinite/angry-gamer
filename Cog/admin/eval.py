import ast
import discord
import json_commands as jc

from discord.ext import commands


def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
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

    @commands.command()
    async def eval(self, ctx, *, cmd):
        """Evaluates input. Lolw someone easelse code!"""
        admins = jc.open_json("Cog/admin/admins.json")
        for admin in admins:
            if admin['user_id'] == ctx.author.id:
                fn_name = "_eval_expr"

                cmd = cmd.strip("` ")

                # add a layer of indentation
                cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

                # wrap in async def body
                body = f"async def {fn_name}():\n{cmd}"

                parsed = ast.parse(body)
                body = parsed.body[0].body

                insert_returns(body)

                env = {
                    'bot': ctx.bot,
                    'discord': discord,
                    'commands': commands,
                    'ctx': ctx,
                    '__import__': __import__
                }
                exec(compile(parsed, filename="<ast>", mode="exec"), env)

                result = (await eval(f"{fn_name}()", env))
                await ctx.send(result)
                return
        await ctx.send("YOu're bnot an admins!!!!11!!?!?!?....,,.,.,.,.,.,.,.")


def setup(bot):
    bot.add_cog(Eval(bot))