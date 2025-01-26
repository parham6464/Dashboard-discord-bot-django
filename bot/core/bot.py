from __future__ import annotations

import os
import sys
from typing import Optional
from discord.ext import commands , tasks
from logging import getLogger; log  = getLogger("Bot")
import discord
from discord import app_commands 
from embed import Embed
from tortoise import Tortoise
import config
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
import requests
from discord import ui

cluster = MongoClient("url")
# Send a ping to confirm a successful connection
db = cluster["add"]
collection = db["add"]
collection_total = db['servers']


__all__ = (

    "Bot",
)
class buttons(ui.View):
    def __init__(self , bot:Bot , link):
        super().__init__(timeout=None)
        self.link = link
        self.bot = bot

        button = discord.ui.Button(label='عضو شدن', style=discord.ButtonStyle.url, url=self.link)
        self.add_item(button)
        
    async def on_timeout(self):
        # set the view to None so that the buttons are no longer available
        # or you could just disable the buttons if you want
        await self.message.edit(content="لینک منقضی شده است", view=None)


class Bot(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or('a!'),
            intents=discord.Intents.all(),
            chunk_guild_at_startup=False,
            help_command=None,
        )

    async def on_tree_error(self ,interaction:discord.Interaction , error:app_commands.AppCommandError):
        if isinstance(error , app_commands.CommandOnCooldown):
            return await interaction.response.send_message(f'command cooldown try after {round(error.retry_after)}Seconds' , ephemeral=True)
        if isinstance(error,app_commands.MissingPermissions):
            return await interaction.response.send_message(f'your permission is not enough',ephemeral=True)
        if isinstance(error , app_commands.BotMissingPermissions):
            return await interaction.response.send_message(f'bot permission is not enough' , ephemeral=True)
        if isinstance(error , app_commands.MissingRole):
            return await interaction.response.send_message(f'Bot Missing Role' , ephemeral=True)
        if isinstance(error , app_commands.CheckFailure):
            return await interaction.response.send_message(f'something went wrong try again' , ephemeral=True)


    async def setup_hook(self):

        for filename in os.listdir('cogs'):
            if not filename.startswith("_") and not filename.startswith("c"):
                await self.load_extension(f'cogs.{filename}.plugin')
                
    async def on_ready(self):
        log.info(f'logged in as {self.user} , ID: {self.user.id}')
        await self.change_presence(status=discord.Status.online , activity=discord.Activity(type=discord.ActivityType.watching, name="/help | a!help"))    

        self.advertise_core.start()

    @tasks.loop(minutes=12)
    async def advertise_core(self):
        if (find:=collection.find({"active":True} , { "server_id": 1, "genres": 1, "channel": 1 ,"banner_body":1 , 'banner_title':1 , 'banner_link':1 , "tabadol":1 , "tabadol_channels":1})):
            if (find2:=collection_total.find_one({'totality':1})):
                public_guilds = find2['public_guilds']
                music_guilds = find2['music_guilds']
                game_guilds = find2['game_guilds']
                platto_guilds = find2['platto_guilds']
                anime_guilds = find2['anime_guilds']
                movie_guilds = find2['movie_guilds']
                development_guilds =  find2['development_guilds']
                shop_guilds = find2['shop_guilds']
                turn = 0
                for sv in find:
                    tabadol = sv['tabadol']
                    if turn == 0:
                        all_guilds = find2['all_guilds']
                    else:
                        all_guilds = list(tmp_all_guilds)
                    turn +=1
                    tmp_all_guilds = list(all_guilds)
                    already_listed_sv = sv['tabadol_channels']
                    if tabadol == "all":
                        all_guilds.remove(str(sv['server_id']))
                        for i in already_listed_sv:
                            if i in all_guilds:
                                all_guilds.remove(i)
                        
                        if len(all_guilds) != 0 :
                            sv_tabadol = all_guilds[0]
                            already_listed_sv.append(all_guilds[0])
                            details_info = collection.find_one({"server_id":int(sv_tabadol)})
                            channel_adv = sv['channel']
                            guild = self.get_guild(int(sv['server_id']))

                            print(guild)
                            print(channel_adv)
                            
                            channel_adv_send = discord.utils.get(guild.text_channels , id=channel_adv)
                            print(channel_adv_send)
                            embed = discord.Embed(
                                title = details_info['banner_title'],
                                description=details_info['banner_body'] , 
                                color=0x0554FE , 
                                timestamp=datetime.now()
                            )
                            await channel_adv_send.send(embed=embed , view=buttons(bot= self,link=details_info['banner_link']))
                            collection.update_one({'server_id':int(sv['server_id'])} ,{"$set":{"tabadol_channels":already_listed_sv}})

                        else:
                            already_listed_sv = []
                            all_guilds = list(tmp_all_guilds)
                            if str(sv['server_id']) in all_guilds:
                                all_guilds.remove(str(sv['server_id']))
                            if len(all_guilds) != 0:
                                sv_tabadol = all_guilds[0]
                                already_listed_sv.append(sv_tabadol)
                                details_info = collection.find_one({"server_id":int(sv_tabadol)})
                                channel_adv = sv['channel']
                                guild = self.get_guild(int(sv['server_id']))

                                channel_adv_send = discord.utils.get(guild.text_channels , id=channel_adv)
                                embed = discord.Embed(
                                    title = details_info['banner_title'],
                                    description=details_info['banner_body'] , 
                                    color=0x0554FE , 
                                    timestamp=datetime.now()
                                )

                                await channel_adv_send.send(embed=embed , view=buttons(bot= self,link=details_info['banner_link']))
                                collection.update_one({'server_id':int(sv['server_id'])} ,{"$set":{"tabadol_channels":already_listed_sv}})

                    else:

                        if tabadol == '1':
                            all_guilds = list(public_guilds)
                        elif tabadol == '2':
                            all_guilds = list(music_guilds)
                        elif tabadol == '3':
                            all_guilds = list(game_guilds)
                        elif tabadol == '4':
                            all_guilds = list(platto_guilds)
                        elif tabadol == '5':
                            all_guilds = list(anime_guilds)
                        elif tabadol == '6':
                            all_guilds = list(movie_guilds)
                        elif tabadol == '7':
                            all_guilds = list(development_guilds)
                        elif tabadol == '8':
                            all_guilds = list(shop_guilds)

                        all_guilds.remove(str(sv['server_id']))
                        for i in already_listed_sv:
                            if i in all_guilds:
                                all_guilds.remove(i)
                        
                        if len(all_guilds) != 0 :
                            sv_tabadol = all_guilds[0]
                            already_listed_sv.append(all_guilds[0])
                            details_info = collection.find_one({"server_id":int(sv_tabadol)})
                            channel_adv = sv['channel']
                            guild = self.get_guild(int(sv['server_id']))

                            channel_adv_send = discord.utils.get(guild.text_channels , id=channel_adv)
                            
                            embed = discord.Embed(
                                title = details_info['banner_title'],
                                description=details_info['banner_body'] , 
                                color=0x0554FE , 
                                timestamp=datetime.now()
                            )

                            await channel_adv_send.send(embed=embed , view=buttons(bot= self,link=details_info['banner_link']))
                            collection.update_one({'server_id':int(sv['server_id'])} ,{"$set":{"tabadol_channels":already_listed_sv}})

                        else:
                            already_listed_sv = []
                            if tabadol == '1':
                                all_guilds = list(public_guilds)
                            elif tabadol == '2':
                                all_guilds = list(music_guilds)
                            elif tabadol == '3':
                                all_guilds = list(game_guilds)
                            elif tabadol == '4':
                                all_guilds = list(platto_guilds)
                            elif tabadol == '5':
                                all_guilds = list(anime_guilds)
                            elif tabadol == '6':
                                all_guilds = list(movie_guilds)
                            elif tabadol == '7':
                                all_guilds = list(development_guilds)
                            elif tabadol == '8':
                                all_guilds = list(shop_guilds)

                            if str(sv['server_id']) in all_guilds:
                                all_guilds.remove(str(sv['server_id']))
                            if len(all_guilds) != 0:
                                sv_tabadol = all_guilds[0]
                                already_listed_sv.append(all_guilds[0])
                                details_info = collection.find_one({"server_id":int(sv_tabadol)})
                                channel_adv = sv['channel']
                                guild = self.get_guild(int(sv['server_id']))

                                channel_adv_send = discord.utils.get(guild.text_channels , id=channel_adv)
                                
                                embed = discord.Embed(
                                    title = sv['banner_title'],
                                    description=sv['banner_body'] , 
                                    color=0x0554FE , 
                                    timestamp=datetime.now()
                                )

                                await channel_adv_send.send(embed=embed , view=buttons(bot= self,link=details_info['banner_link']))
                                collection.update_one({'server_id':int(sv['server_id'])} ,{"$set":{"tabadol_channels":already_listed_sv}})





    async def on_connect(self):
        log.info(f'succesfully connected')
        self.tree.on_error = self.on_tree_error
        # if '-sync' in sys.argv:
        synced_command = await self.tree.sync()
        log.info(f'synced {len(synced_command)} commands')

    async def success(self , message:str, interaction:discord.Interaction,*,ephemeral:bool=False , embed:Optional[bool] = True)->Optional[discord.WebhookMessage]:
        if embed:
            if interaction.response.is_done():
                return await interaction.followup.send(
                    embed = Embed(description=message , color =discord.Colour.green()),
                    ephemeral=ephemeral
                )
            return await interaction.response.send_message(
                embed = Embed(description=message , color=discord.Colour.green()),
                ephemeral=ephemeral
            )
        else:
            if interaction.response.is_done():
                return await interaction.followup.send(content=message , ephemeral=ephemeral)
            return await interaction.response.send_message(content=message , ephemeral=ephemeral)

    async def error(self , message:str, interaction:discord.Interaction,*,ephemeral:bool=True , embed:Optional[bool] = True)->Optional[discord.WebhookMessage]:
        if embed:
            if interaction.response.is_done():
                return await interaction.followup.send(
                    embed = Embed(description=message , color =discord.Colour.red()),
                    ephemeral=ephemeral
                )
            return await interaction.response.send_message(
                embed = Embed(description=message , color=discord.Colour.red()),
                ephemeral=ephemeral
            )
        else:
            if interaction.response.is_done():
                return await interaction.followup.send(content=message , ephemeral=ephemeral)
            return await interaction.response.send_message(content=message , ephemeral=ephemeral)
    


    async def get_or_fetch_guild(self,guild_id:int)-> discord.Guild | None:
        return self.get_guild(guild_id) or await self.fetch_guild(guild_id)

    
    def get_message(
        self,
        message_id:int,
        channel_id:int,
        guild_id:int,
    )->discord.PartialMessage:
        return self.get_partial_messageable(channel_id , guild_id=guild_id).get_partial_message(message_id)

