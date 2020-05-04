import discord
from discord.ext import commands
import os
from secret import *
import json
import operator

bot = commands.Bot(command_prefix="$")


# bot.remove_command("help")


async def update_data(level, user, guild):
    if not str(user.name) in level[guild]:
        level[guild][str(user.name)] = {}
        level[guild][str(user.name)]["experience"] = 0
        level[guild][str(user.name)]["level"] = 1
        level[guild][str(user.name)]["name"] = user.name
        level[guild][str(user.name)]["game win"] = 0
        level[guild][str(user.name)]["game lose"] = 0


async def add_experience(level, user, exp, guild):
    level[guild][str(user.name)]["experience"] += exp


async def delete_experience(level, user, exp, guild):
    level[guild][str(user.name)]["experience"] += exp


async def level_up(level, user, message, guild):
    exp = level[guild][str(user.name)]["experience"]
    lvl_start = level[guild][str(user.name)]["level"]
    lvl_end = int(exp ** (1 / 4))

    if lvl_start < lvl_end:
        await message.channel.send(f"bravo à {user.mention} qui est monter au niveau {lvl_end}")
        level[guild][str(user.name)]["level"] = lvl_end
        print(f"{SUCCESSFUL_REQUEST}" % (" [LEVEL]", f"{user.name} à level up dans le serveur {guild}"))


async def check_level(message):
    with open("./data/level.json", "r") as ll:
        level = json.load(ll)

    await update_data(level, message.author, message.guild.name)
    await add_experience(level, message.author, 5, message.guild.name)
    await level_up(level, message.author, message, message.guild.name)

    with open("./data/level.json", "w") as ll:
        json.dump(level, ll, indent=5)
    bot.command(message.content)


class Bot:

    def __init__(self):
        bot.add_listener(check_level, 'on_message')
        bot.run(TOKEN)

    @staticmethod
    @bot.command()
    async def show(ctx):
        with open("./data/level.json", "r") as ll:
            level = json.load(ll)

        leaderbord = []

        for i in level[ctx.guild.name]:
            leaderbord.append(level[ctx.guild.name][i]["experience"])

        leaderbord.sort()
        leaderbord.reverse()

        for exp in leaderbord:
            for i in level[ctx.guild.name]:
                if level[ctx.guild.name][i]["experience"] == exp:
                    leaderbord.append(level[ctx.guild.name][i])
                    del level[ctx.guild.name][i]
                    break
        with open("./data/level.json", "r") as ll:
            level = json.load(ll)
        del leaderbord[:len(level[ctx.guild.name])]
        ember = discord.Embed(
            author="Olivia",
            color=discord.Color.dark_gold()
        )
        for i in range(0, len(leaderbord)):
            if i == 0:
                ember.add_field(
                    name=f":trophy::first_place: {leaderbord[i]['name']}",
                    value=f"level: {leaderbord[i]['level']} \n experience: {leaderbord[i]['experience']}",
                    inline=False
                )
            elif i == 1:
                ember.add_field(
                    name=f":second_place: {leaderbord[i]['name']}",
                    value=f"level: {leaderbord[i]['level']} \n experience: {leaderbord[i]['experience']}",
                    inline=False
                )
            elif i == 2:
                ember.add_field(
                    name=f":third_place: {leaderbord[i]['name']}",
                    value=f"level: {leaderbord[i]['level']} \n experience: {leaderbord[i]['experience']}",
                    inline=False
                )
            else:
                ember.add_field(
                    name=f"{leaderbord[i]['name']}",
                    value=f"level: {leaderbord[i]['level']} \n experience: {leaderbord[i]['experience']}",
                    inline=False
                )
                pass
        await ctx.send(embed=ember)

        #print(json.dumps(leaderbord, indent=5))

    @staticmethod
    @bot.command(description="permettra de load une extension du bot 'exp: load MUSicBot'")
    async def load(ctx, extension):
        try:
            bot.load_extension(f'cogs.{extension}')
        except Exception as e:
            await ctx.send("sorry this cogs not found")
            print(f'error on loaded {extension} [  {e}  ]')

    @staticmethod
    @bot.command()
    async def unload(ctx, extension):
        try:
            bot.unload_extension(f'cogs.{extension}')
            print(f"{SUCCESSFUL_REQUEST}" % (" [LOAD]", f"{extension}"))
            print("extension have been unloaded")
        except Exception as e:
            print(f"{ERROR_REQUEST}" % " [LOAD]", f"{extension}")
            print(f'error on loaded {extension} [  {e}  ]')

    @staticmethod
    @bot.command()
    async def quit(ctx):
        await bot.change_presence(status=discord.Status.offline)
        await bot.logout()

    @staticmethod
    @bot.command(pass_context=True)
    async def helps(ctx):
        author = ctx.message.author
        ember = discord.Embed(
            description="hello tous le monde moi je suis olivia, la 2ème 'I.A' de mon papou yann,"
                        "j'ai une grande soeur qui s'appelle marta mais bon papou m'a choisi pour vous servir de bot,"
                        "j'espère que je répondrais a vos attentes :heart:",
            colour=discord.Colour.purple(),
            title=f""
        )
        ember.add_field(name='$ping',
                        value="cette command renvoie pong, cela permet de savoir si le bot es en ligne ou pas",
                        inline=True)
        ember.add_field(name="$join",
                        value="pour faire join Olivia dans le vocal")
        ember.add_field(name="$leave",
                        value="pour faire quitter Olivia du vocal")
        await ctx.send(author, embed=ember)

    @staticmethod
    @bot.command()
    @commands.check(dev_or_not)
    async def ping(ctx):
        await ctx.send("pong")

    @staticmethod
    @bot.event
    async def on_member_join(member):
        role = discord.utils.get(member.server.roles, name="membre")

        with open("data/level.json", "r") as ll:
            level = json.load(ll)

        await update_data(level, member)

        with open("data/level.json", "w") as ll:
            json.dump(level, ll, indent=5)

        await bot.add_roles(member, role)
        pass

    @staticmethod
    @bot.event
    async def on_guild_jon(guild):
        channel = guild.text_channels[0]
        await channel.send()

    @staticmethod
    @bot.event
    async def on_message_delete(message):
        if message.author.id != 597838914086240304:
            with open("data/level.json", "r") as ll:
                level = json.load(ll)

            await update_data(level, message.author)
            await delete_experience(level, message.author, 5)
            await level_up(level, message.author, message.channel)

            with open("data/level.json", "w") as ll:
                json.dump(level, ll, indent=5)
        author = message.author
        content = message.content
        channel = message.channel
        try:
            await channel.send("{}: {}".format(author, content))
        except Exception as e:
            print(f"{e} \n{author}: {content}")

    @staticmethod
    @bot.event
    async def on_ready():
        print(f'{INIT_REQUEST} init Olivia assistante')
        for file_name in os.listdir("./cogs"):
            try:
                if file_name.endswith('.py'):
                    print(f'{INIT_REQUEST} init cogs {file_name[:-3]}')
                    bot.load_extension(f"cogs.{file_name[:-3]}")
            except Exception as e:
                print(f'{ERROR_INIT_REQUEST} error on loaded {file_name[:-3]} [  {e}  ]')
        await bot.change_presence(activity=discord.Game(name="je veux devenir humaine", status=discord.Status.online))
        print(f"{SUCCESSFUL_REQUEST}" % (" [INIT]", "Olivia is ready"))


Bot()
