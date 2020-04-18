import discord
from discord.ext import commands


class Olivia(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, description="permet de me parler")
    async def talk(self, ctx):
        await ctx.send("désoler mon papou ma dis que vous étiez pas prêt a me parler, attend encore un peu :kiss: :heart:")


def setup(bot):
    bot.add_cog(Olivia(bot))
