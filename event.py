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


User: TypeAlias = discord.User | discord.Member
with open('config.json', encoding='utf8') as file: config = json.load(file)
token = config.get('token')

# class Event:
#     saving_attributes: tuple[str, ...] = ('id', 'name',  'event_start_time' , 'event_end_time',)
#     def __init__(self, cog: 'Events', id: Optional[str], name: str, event_start_time:str , event_end_time:str,  ) -> None:
#         self.cog = cog
#         self.id = id or os.urandom(16).hex()
#         self.name = name
#         self.event_start_time = event_start_time
#         self.event_end_time = event_end_time


#     def save(self) -> None:
#         self.cog.bot.event_db['events'].append(
#             {attr: getattr(self, attr) for attr in self.saving_attributes}
#         )
#         self.cog.bot.save_event_db()

#     def __str__(self) -> str:
#         # if self.prefix:
#         #     return f'{self.prefix} {self.name}'
#         return self.name


# class CreationModal(discord.ui.Modal):
    # def __init__(self, cog: 'Events', user:User, des:Optional[str], badge:str , badge1:Optional[str] , name:str, activity_name:str ) -> None:
    #     super().__init__(timeout=300.0, title='Create Quest')
    #     self.cog = cog
    #     self.user = user
    #     self.name = name
    #     self.badge = badge
    #     self.badge1 = badge1
    #     self.des = des
    #     self.activity_name = activity_name
    
    #     self.messages = discord.ui.TextInput(
    #         label='Messages Sent',
    #         placeholder='0',
    #         required=False,
    #     )


    #     for text_input in [self.messages,self.reactions_given ,self.clips_shared,self.playing_time,self.time]:
    #         # self.reactionsRecieved,self.surveys,self.eventsDuration,self.eventsCheckin]:
    #         self.add_item(text_input)

    # async def on_submit(self, interaction: discord.Interaction) -> None:
       
    #     messages, reactions_given, clips_shared, playing_time, time = self.messages.value ,self.reactions_given.value , self.clips_shared.value , self.playing_time.value ,self.time.value
    #     if self.cog.find(name=self.name):
    #         await interaction.response.send_message(
    #             embed=self.cog.bot.embed('A quest with that name already exists.'),
    #             ephemeral=True,
    #         )
    #         return
        
    #     event = Event(cog=self.cog, id=None, name=self.name, des=self.des , badge=self.badge, badge1=self.badge1, activity_name=self.activity_name , messages=messages , reactions_given=reactions_given , clips_shared = clips_shared, playing_time = playing_time, time=time )

    #     event.save()

    #     self.cog.bot.activity_db['tracked'].append(f'{self.activity_name}')
    #     self.cog.bot.save_activity_db()
    #     await interaction.response.send_message(
    #         embed=self.cog.bot.embed(
    #             title='Quest Created',
    #             description=f'Quest `{event}` has been created.',
    #         ),
    #     )


class Events(commands.GroupCog, name='event'):
    time =time.time()
    GUILD_ONLY = 2
    STAGE_INSTANCE = 1
    VOICE = 2
    EXTERNAL = 3

    # '''Class to create and list Discord events utilizing their API'''
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.base_api_url = 'https://discord.com/api/v10'
        self.auth_headers = {
            'Authorization':f'Bot {token}',
            'User-Agent':'DiscordBot (https://discord.com/oauth2/authorize?client_id=1194121846640103474) Python/3.9 aiohttp/3.8.1',
            'Content-Type':'application/json'
        }

    # @app_commands.command(name='list', description='List event')
    # @app_commands.default_permissions(administrator=True)
    # @commands.has_guild_permissions(administrator=True)
    # async def list_guild_events(self, interaction: discord.Interaction,guild_id: str) -> list:
    #     # '''Returns a list of upcoming events for the supplied guild ID
    #     # Format of return is a list of one dictionary per event containing information.'''
    #     event_retrieve_url = f'{self.base_api_url}/guilds/{guild_id}/scheduled-events'
    #     async with aiohttp.ClientSession(headers=self.auth_headers) as session:
    #         try:
    #             async with session.get(event_retrieve_url) as response:
    #                 response.raise_for_status()
    #                 assert response.status == 200
    #                 response_list = json.loads(await response.read())
    #         except Exception as e:
    #             print(f'EXCEPTION: {e}')
    #         finally:
    #             await session.close()
    #     await interaction.response.send_message(response_list)

    @app_commands.command(name='create', description='Create an event')
    @app_commands.default_permissions(administrator=True)
    @commands.has_guild_permissions(administrator=True)
    async def create_guild_event(
        self, interaction: discord.Interaction,
        guild_id: str, event_name: str, 
        event_description: str,  event_start_time: str, event_end_time: str,
        channel_id:str
    ) -> None:
        
          
        event_create_url = f'{self.base_api_url}/guilds/{guild_id}/scheduled-events'
        entity_type = Events.VOICE

        event_data = json.dumps({
            "name": event_name,
            "privacy_level": Events.GUILD_ONLY,
            "scheduled_start_time": event_start_time,
            "scheduled_end_time": event_end_time,
            "description": event_description,
            "channel_id": int(channel_id),
            "entity_metadata": None,
            "entity_type": entity_type
        })
        id = os.urandom(16).hex()

        async with aiohttp.ClientSession(headers=self.auth_headers) as session:
            try:
                async with session.post(event_create_url, data=event_data) as response:
                    response.raise_for_status()
                    assert response.status == 200
                    print(f"Post success: to {event_create_url}")
            except Exception as e:
                print(f'EXCEPTION: {e}')
                await session.close()
                return
            finally:
                self.bot.event_db['events'].append({
                    "id": id,
                    "name":event_name,
                    "channel_id": channel_id,
                    "start_time": (datetime.datetime.fromisoformat(event_start_time)).timestamp(),
                    "end_time":  (datetime.datetime.fromisoformat(event_end_time)).timestamp(),
                    "checkedin": [
                        "None"
                    ],
                    "registered": [
                        "None"
                    ],
                })
                
                self.bot.save_event_db()                
                await session.close()  

        await interaction.response.send_message(response)           

    @app_commands.command(name='register', description='Register for an event')
    @app_commands.default_permissions(administrator=True)
    @commands.has_guild_permissions(administrator=True)
    async def register(self, interaction: discord.Interaction,name: str) -> None:
        user = interaction.user
        li = [item.get('name') for item in self.bot.event_db['events']]
        if name not in li:
            await interaction.response.send_message(
             embed=self.bot.embed(
                title='Invalid Event',
                description=f'There is no such event.',
             ),
            ) 
            return

        for obj in self.bot.event_db['events']:
            if obj["name"] == name:
                obj["registered"].append(user.id)
                self.bot.save_event_db()

        await interaction.response.send_message("Registered")

    @app_commands.command(name='checkin', description='Checkin for an event')
    @app_commands.default_permissions(administrator=True)
    @commands.has_guild_permissions(administrator=True)
    async def checkin(self, interaction: discord.Interaction,name: str) -> None:
        user = interaction.user
        li = [item.get('name') for item in self.bot.event_db['events']]
        if name not in li:
            await interaction.response.send_message(
             embed=self.bot.embed(
                title='Invalid Event',
                description=f'There is no such event.',
             ),
            ) 
            return
        
        time = Events.time

        for obj in self.bot.event_db['events']:
            if obj["name"] == name:
                id = obj["id"]
                if obj["start_time"]<= time and obj["end_time"]>= time:
                    obj["checkedin"].append(user.id)
                    self.bot.save_event_db()
                    self.bot.user_db['users'][f'{user.id}']["eventsCheckin"].append(id)
                    self.bot.save_user_db()
                    await interaction.response.send_message("Checked In")    

        await interaction.response.send_message("You can Checkin only when the Event is live")    


    @checkin.autocomplete('name')
    @register.autocomplete('name')
    async def view_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        current = current.lower()
        try:
            found: list[app_commands.Choice[str]] = [
                app_commands.Choice(name=b['name'], value=b['name'])
                for b in self.bot.event_db['events']
                if current in b['name'].lower()
            ]
            if not found:
                raise IndexError
        except IndexError:
            return [app_commands.Choice(name='No quests found', value='')]
        return found


async def setup(bot: Bot) -> None:
    cog = Events(bot)
    bot.event_cog = cog
    await bot.add_cog(cog)

# author: j_sse#1732 https://github.com/69Jesse