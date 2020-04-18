import discord
from discord.ext import commands
from secret import *


class ErrorBot(commands.Cog):

    def __init__(self, bot):
        self.bots = bot

    @commands.Cog.listener()
    async def on_error(self, ctx, error):
        await ctx.send("une erreur interne vien de se produire")
        print(f"{ERROR_REQUEST}" % (" [BOT]", f" {ctx.message.content} {error}"))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.send("désoler mais cette commande et soit inexsistante/soit en cours de maintenance")
        print(f"{ERROR_REQUEST}" % (" [BOT]", f" {ctx.message.content} {error}"))


def setup(bot):
    bot.add_cog(ErrorBot(bot))
