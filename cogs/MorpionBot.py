import discord
from discord.ext import commands
from secret import *


class MorpionBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, description="permet de me parler")
    @commands.check(dev_or_not)
    async def talk(self, ctx):
        await ctx.send("désoler mon papou ma dis que vous étiez pas prêt a me parler, attend encore un peu :kiss: :heart:")


def setup(bot):
    bot.add_cog(MorpionBot(bot))