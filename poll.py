import discord
from discord.ext import commands
from discord import app_commands
from main import Bot
import math
import json
import time

import os
import aiohttp
from typing import (
    TypeAlias,
    Optional,
)
import datetime



class Polls(commands.GroupCog, name='poll'):

    def __init__(self, bot: Bot) -> None:
        self.bot = bot


    @app_commands.command(name='create', description='Create a poll')
    @app_commands.default_permissions(administrator=True)
    @commands.has_guild_permissions(administrator=True)
    async def poll(self, interaction: discord.Interaction,question: str, option1: Optional[str] = None , option2: Optional[str] = None, 
                   option3: Optional[str] = None, option4: Optional[str] = None,option5: Optional[str] = None, role:discord.Role=None):
        
        await interaction.response.send_message("Creating poll...", ephemeral=True)           
        try:
            listen = [option1, option2, option3, option4, option5]
            yonice = []
            for i in listen:
                if i != None:
                    yonice.append(i)
            if role == None:
                if len(yonice) == 2:
                    emb = discord.Embed(color=discord.Color.blurple(), title=f"{question}",description=f"1️⃣ : {yonice[0]}\n2️⃣: {yonice[1]}")
                    msg = await interaction.channel.send(embed=emb)
                    await msg.add_reaction("1️⃣")
                    await msg.add_reaction("2️⃣")
                elif len(yonice) == 3:
                    emb = discord.Embed(color=discord.Color.blurple(), title=f"{question}",description=f"1️⃣ : {yonice[0]}\n2️⃣: {yonice[1]}\n3️⃣: {yonice[2]}")
                    msg = await interaction.channel.send(embed=emb)
                    await msg.add_reaction("1️⃣")
                    await msg.add_reaction("2️⃣")               
                    await msg.add_reaction("3️⃣")
                elif len(yonice) == 4:
                    emb = discord.Embed(color=discord.Color.blurple(), title=f"{question}",description=f"1️⃣ : {yonice[0]}\n2️⃣: {yonice[1]}\n3️⃣: {yonice[2]}\n4️⃣: {yonice[3]}")
                    msg = await interaction.channel.send(embed=emb)
                    await msg.add_reaction("1️⃣")
                    await msg.add_reaction("2️⃣")   
                    await msg.add_reaction("3️⃣")
                    await msg.add_reaction("4️⃣")
                elif len(yonice) == 5:
                    emb = discord.Embed(color=discord.Color.blurple(), title=f"{question}",description=f"1️⃣ : {yonice[0]}\n2️⃣: {yonice[1]}\n3️⃣: {yonice[2]}\n4️⃣: {yonice[3]}\n5️⃣: {yonice[4]}")
                    msg = await interaction.channel.send(embed=emb)
                    await msg.add_reaction("1️⃣")
                    await msg.add_reaction("2️⃣")   
                    await msg.add_reaction("3️⃣")
                    await msg.add_reaction("4️⃣")
                    await msg.add_reaction("5️⃣")
            else:
                if len(yonice) == 2:
                    emb = discord.Embed(color=discord.Color.blurple(), title=f"{question}",description=f"1️⃣: {yonice[0]}\n2️⃣: {yonice[1]}")
                    msg = await interaction.channel.send(f"{role.mention}",embed=emb)
                    await msg.add_reaction("1️⃣")
                    await msg.add_reaction("2️⃣")
                elif len(yonice) == 3:
                    emb = discord.Embed(color=discord.Color.blurple(), title=f"{question}",description=f"1️⃣: {yonice[0]}\n2️⃣: {yonice[1]}\n3️⃣: {yonice[2]}")
                    msg = await interaction.channel.send(f"{role.mention}",embed=emb)
                    await msg.add_reaction("1️⃣")
                    await msg.add_reaction("2️⃣")               
                    await msg.add_reaction("3️⃣")
                elif len(yonice) == 4:
                    emb = discord.Embed(color=discord.Color.blurple(), title=f"{question}",description=f"1️⃣: {yonice[0]}\n2️⃣: {yonice[1]}\n3️⃣: {yonice[2]}\n4️⃣: {yonice[3]}")
                    msg = await interaction.channel.send(f"{role.mention}",embed=emb)
                    await msg.add_reaction("1️⃣")
                    await msg.add_reaction("2️⃣")   
                    await msg.add_reaction("3️⃣")
                    await msg.add_reaction("4️⃣")
                elif len(yonice) == 5:
                    emb = discord.Embed(color=discord.Color.blurple(), title=f"{question}",description=f"1️⃣: {yonice[0]}\n2️⃣: {yonice[1]}\n3️⃣: {yonice[2]}\n4️⃣: {yonice[3]}\n5️⃣: {yonice[4]}")
                    msg = await interaction.channel.send(f"{role.mention}",embed=emb)
                    await msg.add_reaction("1️⃣")
                    await msg.add_reaction("2️⃣")   
                    await msg.add_reaction("3️⃣")
                    await msg.add_reaction("4️⃣")
                    await msg.add_reaction("5️⃣")
            listen=[]
            yonice=[]
            await interaction.delete_original_response()
        except Exception as e:
            print(e)
            await interaction.delete_original_response()
            await interaction.followup.send("Ann error occured, try again later.", ephemeral=True)



async def setup(bot: Bot) -> None:
    cog = Polls(bot)
    bot.poll_cog = cog
    await bot.add_cog(cog)
