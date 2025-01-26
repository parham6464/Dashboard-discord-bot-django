from __future__ import annotations

from core.bot import Bot
from typing import Any, Optional , Callable , Literal , Union
from datetime import timedelta , datetime
from cogs.cog_config import Plugin
from discord.ext import commands
from humanfriendly import parse_timespan , InvalidTimespan
from discord import app_commands , User , utils as Utils , CategoryChannel , ForumChannel , PartialMessageable , Object , TextChannel , Thread , Permissions , StageChannel , VoiceChannel , Role , Attachment , Forbidden , Color
from pytz import UTC
from aiohttp import ClientSession
import aiohttp
import discord
import config
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from easy_pil import Editor , Canvas, load_image_async , Font
from config import TOKEN
import requests
from typing import Union 
from datetime import timedelta , datetime
import random , string
import asyncio
from discord import ui

cluster = MongoClient("url")
# Send a ping to confirm a successful connection
db = cluster["add"]
collection = db["add"]
collection_total = db['servers']


class BotAdvertise(Plugin):
    def __init__(self , bot:Bot):
        self.bot = bot

    async def cog_load(self):
        await super().cog_load()



    @app_commands.command(  
        name='add_addvertise_channel',
        description='this is the first step to install the bot'
    )
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id , i.guild.id))
    async def addvertise_channel(self,interaction:discord.Interaction , channel:discord.TextChannel):
        if (find:=collection.find_one({'server_id':interaction.guild.id})):
            channel_current = find['channel']
            if channel_current == channel.id:
                await interaction.reponse.send_message('this channel is already added' ,  ephemeral=True)
            else:
                collection.update_one({"server_id":interaction.guild.id} , {"$set":{"channel":channel.id}})
                await interaction.reponse.send_message("channel added" , ephemeral=True)
                
        else:
            collection.insert_one({"server_id":interaction.guild.id , 'channel':channel.id ,'banner_body':None , 'banner_title':None , 'banner_link':None , 'genres':[] , "active":True , 'tabadol':"all" , "tabadol_channels":[] })
            if (find2:=collection_total.find_one({'totality':1})):
                total_sv = find2['all_guilds']
                if interaction.guild.id not in total_sv:
                    total_sv.append(interaction.guild.id)
                    collection_total.update_one({"totality":1} , {"$set":{"all_guilds":total_sv}})
            else:
                tmp_guild = []
                tmp_guild.append(interaction.guild.id)
                collection_total.insert_one({'totality':1,"all_guilds":tmp_guild,"anime_guilds":[],"public_guilds":[],"development_guilds":[],"movie_guilds":[] , "game_guilds":[],"platto_guilds":[],"music_guilds":[] , 'shop_guilds':[]})    

                
            await interaction.response.send_message("your channel added" , ephemeral=True)



    @app_commands.command(
        name='add_server_genre',
        description='this is the second part of installation'
    )
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id , i.guild.id))
    @app_commands.choices(genres=[
    app_commands.Choice(name='پابلیک' , value=1),
    app_commands.Choice(name='موزیک' , value=2),
    app_commands.Choice(name='بازی' , value=3),
    app_commands.Choice(name='پلاتو' , value=4),
    app_commands.Choice(name='انیمیشن' , value=5),
    app_commands.Choice(name='فیلم' , value=6),
    app_commands.Choice(name='برنامه نویسی ' , value=7),
    app_commands.Choice(name='فروشگاه' , value=8),
    ]) 

    async def set_banner(self,interaction:discord.Interaction , genres:app_commands.Choice[int]):
        if (find:=collection.find_one({'server_id':interaction.guild.id})):
            if (find2:=collection_total.find_one({'totality':1})):
                anime_guilds = find2['anime_guilds']
                public_guilds = find2['public_guilds']
                development_guilds = find2['development_guilds']
                movie_guilds = find2['movie_guilds']
                game_guilds = find2['game_guilds']
                platto_guilds = find2['platto_guilds']
                music_guilds = find2['music_guilds']
                shop_guilds = find2['shop_guilds']

                
                genres_sv = find['genres']
                if genres.value == 1:
                    if 1 not in genres_sv:
                        genres_sv.append(1)
                        if 2 in genres_sv :
                            genres_sv.remove(2)
                        elif 3 in genres_sv:
                            genres_sv.remove(3)
                        elif 4 in genres_sv:
                            genres_sv.remove(4)
                        elif 5 in genres_sv:
                            genres_sv.remove(5)
                        elif 6 in genres_sv:
                            genres_sv.remove(6)
                        elif 7 in genres_sv:
                            genres_sv.remove(7)
                        elif 8 in genres_sv:
                            genres_sv.remove(8)
                        collection.update_one({"server_id":interaction.guild.id} , {"$set":{"genres":genres_sv}})
                    

                    if interaction.guild.id not in public_guilds:
                        public_guilds.append(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"public_guilds":public_guilds}})

                    ##################### removing duplicates in all genres ###############################
                    if interaction.guild.id in anime_guilds:
                        anime_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"anime_guilds":anime_guilds}})

                    elif interaction.guild.id in development_guilds:
                        development_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"development_guilds":development_guilds}})

                    elif interaction.guild.id in movie_guilds:
                        movie_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"movie_guilds":movie_guilds}})

                    elif interaction.guild.id in game_guilds :
                        game_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"game_guilds":game_guilds}})

                    elif interaction.guild.id in platto_guilds:
                        platto_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"platto_guilds":platto_guilds}})

                    elif interaction.guild.id in music_guilds:
                        music_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"music_guilds":music_guilds}})

                    elif interaction.guild.id in shop_guilds:
                        shop_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"shop_guilds":shop_guilds}})

                    ##################### removing duplicates in all genres ###############################
                    
                elif genres.value == 2:
                    if 2 not in genres_sv:
                        genres_sv.append(2)
                        if 1 in genres_sv :
                            genres_sv.remove(1)
                        elif 3 in genres_sv:
                            genres_sv.remove(3)
                        elif 4 in genres_sv:
                            genres_sv.remove(4)
                        elif 5 in genres_sv:
                            genres_sv.remove(5)
                        elif 6 in genres_sv:
                            genres_sv.remove(6)
                        elif 7 in genres_sv:
                            genres_sv.remove(7)
                        elif 8 in genres_sv:
                            genres_sv.remove(8)

                        collection.update_one({"server_id":interaction.guild.id} , {"$set":{"genres":genres_sv}})


                    if interaction.guild.id not in music_guilds:
                        music_guilds.append(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"music_guilds":music_guilds}})


                    ##################### removing duplicates in all genres ###############################
                    if interaction.guild.id in anime_guilds:
                        anime_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"anime_guilds":anime_guilds}})

                    elif interaction.guild.id in development_guilds:
                        development_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"development_guilds":development_guilds}})

                    elif interaction.guild.id in movie_guilds:
                        movie_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"movie_guilds":movie_guilds}})

                    elif interaction.guild.id in game_guilds :
                        game_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"game_guilds":game_guilds}})

                    elif interaction.guild.id in platto_guilds:
                        platto_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"platto_guilds":platto_guilds}})

                    elif interaction.guild.id in public_guilds:
                        public_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"public_guilds":public_guilds}})

                    elif interaction.guild.id in shop_guilds:
                        shop_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"shop_guilds":shop_guilds}})

                    ##################### removing duplicates in all genres ###############################


                elif genres.value == 3:
                    if 3 not in genres_sv:
                        genres_sv.append(3)
                        if 2 in genres_sv :
                            genres_sv.remove(2)
                        elif 1 in genres_sv:
                            genres_sv.remove(1)
                        elif 4 in genres_sv:
                            genres_sv.remove(4)
                        elif 5 in genres_sv:
                            genres_sv.remove(5)
                        elif 6 in genres_sv:
                            genres_sv.remove(6)
                        elif 7 in genres_sv:
                            genres_sv.remove(7)
                        elif 8 in genres_sv:
                            genres_sv.remove(8)


                        collection.update_one({"server_id":interaction.guild.id} , {"$set":{"genres":genres_sv}})

                    if interaction.guild.id not in game_guilds:
                        game_guilds.append(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"game_guilds":game_guilds}})

                    ##################### removing duplicates in all genres ###############################
                    if interaction.guild.id in anime_guilds:
                        anime_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"anime_guilds":anime_guilds}})

                    elif interaction.guild.id in development_guilds:
                        development_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"development_guilds":development_guilds}})

                    elif interaction.guild.id in movie_guilds:
                        movie_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"movie_guilds":movie_guilds}})

                    elif interaction.guild.id in music_guilds :
                        music_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"music_guilds":music_guilds}})

                    elif interaction.guild.id in platto_guilds:
                        platto_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"platto_guilds":platto_guilds}})

                    elif interaction.guild.id in public_guilds:
                        public_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"public_guilds":public_guilds}})

                    elif interaction.guild.id in shop_guilds:
                        shop_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"shop_guilds":shop_guilds}})

                    ##################### removing duplicates in all genres ###############################


                elif genres.value == 4:
                    if 4 not in genres_sv:
                        genres_sv.append(4)

                        if 2 in genres_sv :
                            genres_sv.remove(2)
                        elif 3 in genres_sv:
                            genres_sv.remove(3)
                        elif 1 in genres_sv:
                            genres_sv.remove(1)
                        elif 5 in genres_sv:
                            genres_sv.remove(5)
                        elif 6 in genres_sv:
                            genres_sv.remove(6)
                        elif 7 in genres_sv:
                            genres_sv.remove(7)
                        elif 8 in genres_sv:
                            genres_sv.remove(8)


                        collection.update_one({"server_id":interaction.guild.id} , {"$set":{"genres":genres_sv}})

                    if interaction.guild.id not in platto_guilds:
                        platto_guilds.append(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"platto_guilds":platto_guilds}})


                    ##################### removing duplicates in all genres ###############################
                    if interaction.guild.id in anime_guilds:
                        anime_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"anime_guilds":anime_guilds}})

                    elif interaction.guild.id in development_guilds:
                        development_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"development_guilds":development_guilds}})

                    elif interaction.guild.id in movie_guilds:
                        movie_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"movie_guilds":movie_guilds}})

                    elif interaction.guild.id in music_guilds :
                        music_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"music_guilds":music_guilds}})

                    elif interaction.guild.id in game_guilds:
                        game_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"game_guilds":game_guilds}})

                    elif interaction.guild.id in public_guilds:
                        public_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"public_guilds":public_guilds}})

                    elif interaction.guild.id in shop_guilds:
                        shop_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"shop_guilds":shop_guilds}})

                    ##################### removing duplicates in all genres ###############################


                elif genres.value == 5:
                    if 5 not in genres_sv:
                        genres_sv.append(5)
                        if 2 in genres_sv :
                            genres_sv.remove(2)
                        elif 3 in genres_sv:
                            genres_sv.remove(3)
                        elif 4 in genres_sv:
                            genres_sv.remove(4)
                        elif 1 in genres_sv:
                            genres_sv.remove(1)
                        elif 6 in genres_sv:
                            genres_sv.remove(6)
                        elif 7 in genres_sv:
                            genres_sv.remove(7)
                        elif 8 in genres_sv:
                            genres_sv.remove(8)


                        collection.update_one({"server_id":interaction.guild.id} , {"$set":{"genres":genres_sv}})

                    if interaction.guild.id not in anime_guilds:
                        anime_guilds.append(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"anime_guilds":anime_guilds}})

                    ##################### removing duplicates in all genres ###############################
                    if interaction.guild.id in platto_guilds:
                        platto_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"platto_guilds":platto_guilds}})

                    elif interaction.guild.id in development_guilds:
                        development_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"development_guilds":development_guilds}})

                    elif interaction.guild.id in movie_guilds:
                        movie_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"movie_guilds":movie_guilds}})

                    elif interaction.guild.id in music_guilds :
                        music_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"music_guilds":music_guilds}})

                    elif interaction.guild.id in game_guilds:
                        game_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"game_guilds":game_guilds}})

                    elif interaction.guild.id in public_guilds:
                        public_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"public_guilds":public_guilds}})

                    elif interaction.guild.id in shop_guilds:
                        shop_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"shop_guilds":shop_guilds}})

                    ##################### removing duplicates in all genres ###############################


                elif genres.value == 6:
                    if 6 not in genres_sv:
                        genres_sv.append(6)
                        if 2 in genres_sv :
                            genres_sv.remove(2)
                        elif 3 in genres_sv:
                            genres_sv.remove(3)
                        elif 4 in genres_sv:
                            genres_sv.remove(4)
                        elif 5 in genres_sv:
                            genres_sv.remove(5)
                        elif 1 in genres_sv:
                            genres_sv.remove(1)
                        elif 7 in genres_sv:
                            genres_sv.remove(7)
                        elif 8 in genres_sv:
                            genres_sv.remove(8)

                        collection.update_one({"server_id":interaction.guild.id} , {"$set":{"genres":genres_sv}})

                    if interaction.guild.id not in movie_guilds:
                        movie_guilds.append(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"movie_guilds":movie_guilds}})

                    ##################### removing duplicates in all genres ###############################
                    if interaction.guild.id in platto_guilds:
                        platto_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"platto_guilds":platto_guilds}})

                    elif interaction.guild.id in development_guilds:
                        development_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"development_guilds":development_guilds}})

                    elif interaction.guild.id in anime_guilds:
                        anime_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"anime_guilds":anime_guilds}})

                    elif interaction.guild.id in music_guilds :
                        music_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"music_guilds":music_guilds}})

                    elif interaction.guild.id in game_guilds:
                        game_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"game_guilds":game_guilds}})

                    elif interaction.guild.id in public_guilds:
                        public_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"public_guilds":public_guilds}})

                    elif interaction.guild.id in shop_guilds:
                        shop_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"shop_guilds":shop_guilds}})

                    ##################### removing duplicates in all genres ###############################


                elif genres.value == 7:
                    if 7 not in genres_sv:
                        genres_sv.append(7)
                        if 2 in genres_sv :
                            genres_sv.remove(2)
                        elif 3 in genres_sv:
                            genres_sv.remove(3)
                        elif 4 in genres_sv:
                            genres_sv.remove(4)
                        elif 5 in genres_sv:
                            genres_sv.remove(5)
                        elif 6 in genres_sv:
                            genres_sv.remove(6)
                        elif 1 in genres_sv:
                            genres_sv.remove(1)
                        elif 8 in genres_sv:
                            genres_sv.remove(8)

                        collection.update_one({"server_id":interaction.guild.id} , {"$set":{"genres":genres_sv}})


                    if interaction.guild.id not in development_guilds:
                        development_guilds.append(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"development_guilds":development_guilds}})

                    ##################### removing duplicates in all genres ###############################
                    if interaction.guild.id in platto_guilds:
                        platto_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"platto_guilds":platto_guilds}})

                    elif interaction.guild.id in movie_guilds:
                        movie_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"movie_guilds":movie_guilds}})

                    elif interaction.guild.id in anime_guilds:
                        anime_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"anime_guilds":anime_guilds}})

                    elif interaction.guild.id in music_guilds :
                        music_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"music_guilds":music_guilds}})

                    elif interaction.guild.id in game_guilds:
                        game_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"game_guilds":game_guilds}})

                    elif interaction.guild.id in public_guilds:
                        public_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"public_guilds":public_guilds}})

                    elif interaction.guild.id in shop_guilds:
                        shop_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"shop_guilds":shop_guilds}})

                    ##################### removing duplicates in all genres ###############################


                elif genres.value == 8:
                    if 8 not in genres_sv:
                        genres_sv.append(8)
                        if 2 in genres_sv :
                            genres_sv.remove(2)
                        elif 3 in genres_sv:
                            genres_sv.remove(3)
                        elif 4 in genres_sv:
                            genres_sv.remove(4)
                        elif 5 in genres_sv:
                            genres_sv.remove(5)
                        elif 6 in genres_sv:
                            genres_sv.remove(6)
                        elif 7 in genres_sv:
                            genres_sv.remove(7)
                        elif 1 in genres_sv:
                            genres_sv.remove(1)

                        collection.update_one({"server_id":interaction.guild.id} , {"$set":{"genres":genres_sv}})

                
                    if interaction.guild.id not in shop_guilds:
                        shop_guilds.append(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"shop_guilds":shop_guilds}})

                    ##################### removing duplicates in all genres ###############################
                    if interaction.guild.id in platto_guilds:
                        platto_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"platto_guilds":platto_guilds}})

                    elif interaction.guild.id in movie_guilds:
                        movie_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"movie_guilds":movie_guilds}})

                    elif interaction.guild.id in anime_guilds:
                        anime_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"anime_guilds":anime_guilds}})

                    elif interaction.guild.id in music_guilds :
                        music_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"music_guilds":music_guilds}})

                    elif interaction.guild.id in game_guilds:
                        game_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"game_guilds":game_guilds}})

                    elif interaction.guild.id in public_guilds:
                        public_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"public_guilds":public_guilds}})

                    elif interaction.guild.id in development_guilds:
                        development_guilds.remove(interaction.guild.id)
                        collection_total.update_one({"totality":1} , {"$set":{"development_guilds":development_guilds}})

                        ##################### removing duplicates in all genres ###############################

                        

                    await interaction.response.send_message('ژانر شما تنظیم شد' ,  ephemeral=True)

            else:
                await interaction.response.send_message("لطفا لینک را به درستی وارد کنید" , ephemeral=True )
                
        else:
            await interaction.response.send_message("اول چنل تبلیغات را با دستور /add_advertise_channel \n ثبت کنید و بعد از این دستور استفاده کنید" , ephemeral=True)


    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def add_banner(self,ctx , title_banner , link_banner , * , body_banner): 
        if (find:=collection.find_one({'server_id':ctx.guild.id})):
            if (find2:=collection_total.find_one({'totality':1})):
                collection.update_one({"server_id":ctx.guild.id} , {"$set":{"banner_body":body_banner  , "banner_title":title_banner , "banner_link":link_banner}})
                await ctx.send("done")
                

    @app_commands.command(
        name='add_tabadol_tag',
        description='this is a command to choose which server you wants to have exchange with'
    )
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id , i.guild.id))
    @app_commands.choices(genres=[
    app_commands.Choice(name='همه دسته ها' , value=9),
    app_commands.Choice(name='پابلیک' , value=1),
    app_commands.Choice(name='موزیک' , value=2),
    app_commands.Choice(name='بازی' , value=3),
    app_commands.Choice(name='پلاتو' , value=4),
    app_commands.Choice(name='انیمیشن' , value=5),
    app_commands.Choice(name='فیلم' , value=6),
    app_commands.Choice(name='برنامه نویسی ' , value=7),
    app_commands.Choice(name='فروشگاه' , value=8),
    ]) 
    async def advertise_tabadol(self,interaction:discord.Interaction , genres:app_commands.Choice[int]):
        if (find:=collection.find_one({'server_id':interaction.guild.id})):
            if (find2:=collection_total.find_one({'totality':1})):
                if genres.value == 9:
                    collection.update_one({"server_id":interaction.guild.id} , {"$set":{"tabadol":'all'}})
                else:
                    collection.update_one({"server_id":interaction.guild.id} , {"$set":{"tabadol":genres.value}})
                await interaction.response.send_message('تنظیم شد' , ephemeral=True)
            else:
                await interaction.response.send_message('دیتابیس خراب شده است' , ephemeral=True)
        else:
            await interaction.response.send_message("اول چنل تبلیغات را با دستور /add_advertise_channel \n ثبت کنید و بعد از این دستور استفاده کنید" , ephemeral=True)



    @app_commands.command(
        name='disable_advertise',
        description='for disabling the bot'
    )
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id , i.guild.id))
    async def disable_bot(self,interaction:discord.Interaction):
        if (find:=collection.find_one({'server_id':interaction.guild.id})):
            if (find2:=collection_total.find_one({'totality':1})):
                collection.update_one({"server_id":interaction.guild.id} , {"$set":{"active":False}})
                await interaction.response.send_message('تنظیم شد' , ephemeral=True)
            else:
                await interaction.response.send_message('دیتابیس خراب شده است' , ephemeral=True)
        else:
            await interaction.response.send_message("اول چنل تبلیغات را با دستور /add_advertise_channel \n ثبت کنید و بعد از این دستور استفاده کنید" , ephemeral=True)


    @app_commands.command(
        name='activate_bot',
        description='for activating the bot'
    )
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.user.id , i.guild.id))
    async def activate_bot(self,interaction:discord.Interaction):
        if (find:=collection.find_one({'server_id':interaction.guild.id})):
            if (find2:=collection_total.find_one({'totality':1})):
                collection.update_one({"server_id":interaction.guild.id} , {"$set":{"active":True}})
                await interaction.response.send_message('تنظیم شد' , ephemeral=True)
            else:
                await interaction.response.send_message('دیتابیس خراب شده است' , ephemeral=True)
        else:
            await interaction.response.send_message("اول چنل تبلیغات را با دستور /add_advertise_channel \n ثبت کنید و بعد از این دستور استفاده کنید" , ephemeral=True)

##################################################

async def setup(bot : Bot):
    await bot.add_cog(BotAdvertise(bot))
