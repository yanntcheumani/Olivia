from builtins import type
import os
import discord
from discord.ext import commands
from secret import *
import youtube_dl
import shutil
import json


class MusicBot(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.players_music = {}
        self.queues_music = {}

    @commands.command(description="permet de faire rejoindre Olivia dans le vocal")
    async def join(self, ctx):
        print(f"{SUCCESSFUL_REQUEST}" % (" [ACTION]", "[JOIN] Olivia join vocal"))
        channel = ctx.message.author.voice.channel
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

    @commands.command(pass_context=True, description="fait sortir le bot du vocal")
    async def leave(self, ctx):
        print(f"{SUCCESSFUL_REQUEST}" % (" [ACTION]", "[LEAVE] Olivia leave vocal"))
        channel = ctx.message.author.voice.channel
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()

    @commands.command(description="permet de mettre une musique en pause")
    async def pause(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            voice.pause()
            print(f"{SUCCESSFUL_REQUEST}" % (' [ACTION]', f'[MUSIC] paused!'))
            await ctx.send("music paused")
        else:
            await ctx.send("aucune musique n'est en train d'être écoutée")

    @commands.command(description="permet de reprendre la music la ou elle sait arreter")
    async def resume(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_paused():
            voice.resume()
            print(f"{SUCCESSFUL_REQUEST}" % (' [ACTION]', f'[MUSIC] resume!'))
            await ctx.send("music resume")
        else:
            await ctx.send("aucune musique n'est entrain d'être écouter")

    @commands.command(description="permet de stopper la musique qui est en cours")
    async def stop(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        self.queues_music.clear()
        if voice and voice.is_playing():
            voice.stop()
            print(f"{SUCCESSFUL_REQUEST}" % (' [ACTION]', f'[MUSIC] stopped!'))
            await ctx.send("music stopped")
        else:
            await ctx.send("aucune musique n'est entrain d'être écouter")

    @commands.command(pass_context=True, description="permet de lancer une musique il faut que le bot soit dans le vocal")
    async def play(self, ctx, url: str):
        """        def check_queue():
            global name

            Queue_infile = os.path.isdir("./data/Queue")
            if Queue_infile is True:
                Dir = os.path.abspath(os.path.relpath("./data/Queue"))
                length = len(os.listdir(Dir))
                still_q = length - 1
                try:
                    first_file = os.listdir(Dir)[0]
                except:
                    print(f"{WAITING_REQUEST}" % (" [INFOS]", "no more queues"))
                    self.queues_music.clear()
                    return
                main_location = os.path.dirname(os.path.realpath(__file__))
                song_path = os.path.abspath(os.path.realpath("./data/Queue") + "/" + first_file)

                if length != 0:
                    print(f"{SUCCESSFUL_REQUEST}" % ("[MUSIC]", "playing a next queue"))
                    song_there = os.path.isfile("song1.mp3")

                    if song_there:
                        os.remove("song.mp3")
                    shutil.move(song_path, main_location)

                    for file in os.listdir("./"):
                        if file.endswith('.mp3'):
                            name = file
                            print(f"{WAITING_REQUEST}" % (' [ACTION]', f'[RENAME] rename file {file}'))
                            os.rename(name, "song.mp3")
                            os.system("mv song.mp3 ./data/")
                    print(f"{WAITING_REQUEST}" % (' [ACTION]', f'[PLAY] music'))
                    voice.play(discord.FFmpegPCMAudio("./data/song.mp3"), after=lambda e: self.play())
                    voice.source = discord.PCMVolumeTransformer(voice.source)
                    voice.source.volume = 0.07
                    ctx.send(f"playing {name}")
                else:
                    self.queues_music.clear()
                    print(f"{SUCCESSFUL_REQUEST}" % (' [ACTION]', f'[PLAY] music finish'))
                    return
            else:
                self.queues_music.clear()
                print(f"{WAITING_REQUEST}" % (" [INFOS]", "no song were queues"))
                return"""
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
                self.queues_music.clear()

        except PermissionError:
            await ctx.send("y a eu une erreur da mon côter j'ai prévenir mon papou")
            return

        Queue_infile = os.path.isdir("./data/Queue")
        try:
            queue_folder = "./data/Queue"
            if Queue_infile is True:
                print(f"{WAITING_REQUEST}" % (" [REMOVE]", "Dir Queue"))
                shutil.rmtree(queue_folder)
                print(f"{SUCCESSFUL_REQUEST}" % (" [REMOVE]", "queue folder is delete"))
        except:
            print(f"{ERROR_REQUEST}" % (" [REMOVE]", "no old queue folder"))
            pass

        print(f"{SUCCESSFUL_REQUEST}" % (" [ACTION]", "[PLAY] Olivia play music"))

        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        ydl_opt = {
            'format': "bestaudio/best",
            'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
            }],
        }
        try:
            with youtube_dl.YoutubeDL(ydl_opt) as ydl:
                print(f"{WAITING_REQUEST}" % (' [ACTION]', f'[LOADING] {ydl}'))
                ydl.download([url])
            for file in os.listdir("./"):
                if file.endswith('.mp3'):
                    name = file
                    print(f"{WAITING_REQUEST}" % (' [ACTION]', f'[RENAME] rename file {file}'))
                    os.rename(name, "song.mp3")
                    os.system("mv song.mp3 ./data/")
        except Exception as e:
            await ctx.send("désoler ils c'est passer quelque chose lors du lancement de la music veuillez réessayer")
            print(f"{SUCCESSFUL_REQUEST}" % (' [ACTION]', f'[LOADING] lol error! {e}'))

        print(f"{SUCCESSFUL_REQUEST}" % (' [ACTION]', f'[LOADING] Done!'))
        print(f"{WAITING_REQUEST}" % (' [ACTION]', f'[PLAY] music'))
        voice.play(discord.FFmpegPCMAudio("./data/song.mp3"), after=lambda e: print(f"{SUCCESSFUL_REQUEST}" % (" [MUSIC]", "music finis")))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.07
        nname = name.split("-", 2)
        await ctx.send(f"playing {name}")

    @commands.command(pass_context=True, description="permet de rajouter une musique en attente")
    @commands.check(dev_or_not)
    async def queue(self, ctx, url: str):
        Queue_infile = os.path.isdir("./data/Queue")

        if Queue_infile is False:
            os.mkdir("./data/Queue")
        Dir = os.path.abspath("./data/Queue")
        q_num = len(os.listdir(Dir))
        q_num += 1
        add_queue = 1
        while add_queue:
            if q_num in self.queues_music:
                q_num += 1
            else:
                add_queue = False
            self.queues_music[q_num] = q_num
        queue_path = os.path.abspath(os.path.relpath("./data/Queue") + f"/song{q_num}.%(ext)s")
        ydl_opt = {
            'format': "bestaudio/best",
            'outtmpl': queue_path,
            'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
            }],
        }

        try:
            with youtube_dl.YoutubeDL(ydl_opt) as ydl:
                print(f"{WAITING_REQUEST}" % (' [ACTION]', f'[LOADING] {ydl}'))
                ydl.download([url])
        except Exception as e:
            await ctx.send("désoler ils c'est passer quelque chose lors du lancement de la music veuillez réessayer")
            print(f"{SUCCESSFUL_REQUEST}" % (' [ACTION]', f'[LOADING] lol error! {e}'))
        print(f"{SUCCESSFUL_REQUEST}" % (' [ACTION]', f'[LOADING] Done!'))
        await ctx.send("ajouts du song " + str(url) + " dans la liste d'attente")

def setup(bot):
    bot.add_cog(MusicBot(bot))
