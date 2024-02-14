import discord
from discord.ext import commands
from discord import app_commands
from main import Bot
import math
import json

import os

from typing import (
    TypeAlias,
    Optional,
)


User: TypeAlias = discord.User | discord.Member


class Quest:
    saving_attributes: tuple[str, ...] = ('id', 'name', 'des', 'badge' , 'messages', 'reactions_given', 'clips_shared', 'playing_time', 'time' , 'game_name'  )
    def __init__(self, cog: 'Quests', id: Optional[str], name: str, des: Optional[str] , badge:str , messages:str, reactions_given:str , clips_shared:str ,  playing_time:str , time:str , game_name:str  ) -> None:
        self.cog = cog
        self.id = id or os.urandom(16).hex()
        self.name = name
        self.des = des
        self.badge = badge
        self.messages = messages
        self.clips_shared = clips_shared
        self.reactions_given = reactions_given
        self.playing_time = playing_time
        self.time = time
        self.game_name = game_name
        # self.reactionsRecieved = reactionsRecieved
        # self.surveys = surveys       
        # self.eventsDuration = eventsDuration
        # self.eventsCheckin = eventsCheckin


    def on_grant_message(self, user: User) -> str:
        message = self.on_grant
        for before, after in [
            ('{user_mention}', user.mention),
            ('{name}', self.name),
            # ('{prefix}', self.prefix),
            ('{user_badge_count}', sum(self.cog.data(id=user.id).values())),
            ('{full_name}', self),
        ]:
            message = message.replace(str(before), str(after))
        return message

    def save(self) -> None:
        assert self.cog.find(name=self.name) is None, 'Quest with this name already exists'
        self.cog.bot.quest_db['quests'].append(
            {attr: getattr(self, attr) for attr in self.saving_attributes}
        )
        self.cog.bot.save_quest_db()

    def __str__(self) -> str:
        # if self.prefix:
        #     return f'{self.prefix} {self.name}'
        return self.name


class CreationModal(discord.ui.Modal):
    def __init__(self, cog: 'Quests', user:User, des:Optional[str], badge:str , name:str, game_name:str ) -> None:
        super().__init__(timeout=300.0, title='Create Quest')
        self.cog = cog
        self.user = user
        self.name = name
        self.badge = badge
        self.des = des
        self.game_name = game_name
    
        self.messages = discord.ui.TextInput(
            label='Messages Sent',
            placeholder='0',
            required=False,
        )
        self.reactions_given = discord.ui.TextInput(
            label='Reactions Given',
            placeholder='0',
            required=False,
        )
        
        self.clips_shared = discord.ui.TextInput(
            label='Clips Shared',
            placeholder='0',
            required=False,
        )
        
        self.playing_time = discord.ui.TextInput(
            label='Time Spent playing Games',
            placeholder='0',
            required=False,
        )
        self.time = discord.ui.TextInput(
            label='Time Spent in Voice Channel',
            placeholder='0 Seconds',
            required=False,
        )
        # self.reactionsRecieved = discord.ui.TextInput(
        #     label='Reactions Recieved',
        #     placeholder='0',
        #     required=False,
        # )
        # self.surveys = discord.ui.TextInput(
        #     label='Surveys Completed',
        #     placeholder='0',
        #     required=False,
        # )
        # self.eventsDuration = discord.ui.TextInput(
        #     label='Time Spent in Events',
        #     placeholder='0 Seconds',
        #     required=False,
        # )
        # self.eventsCheckin = discord.ui.TextInput(
        #     label='Events Checked In',
        #     placeholder='0',
        #     required=False,
        # )

        # self.on_grant = discord.ui.TextInput(
        #     label='On Grant',
        #     default=(
        #         'Hey, {user_mention}! You have obtained the **{name}** badge!\n'
        #         'You now have {user_badge_count} badges in total.\n\n'
        #         'I hope you enjoy your **{full_name}** badge!'
        #     ),
        #     style=discord.TextStyle.long,
        #)
        for text_input in [self.messages,self.reactions_given ,self.clips_shared,self.playing_time,self.time]:
            # self.reactionsRecieved,self.surveys,self.eventsDuration,self.eventsCheckin]:
            self.add_item(text_input)

    async def on_submit(self, interaction: discord.Interaction) -> None:
       
        messages, reactions_given, clips_shared, playing_time, time = self.messages.value ,self.reactions_given.value , self.clips_shared.value , self.playing_time.value ,self.time.value
        if self.cog.find(name=self.name):
            await interaction.response.send_message(
                embed=self.cog.bot.embed('A quest with that name already exists.'),
                ephemeral=True,
            )
            return
        
        quest = Quest(cog=self.cog, id=None, name=self.name, des=self.des , badge=self.badge, game_name=self.game_name , messages=messages , reactions_given=reactions_given , clips_shared = clips_shared, playing_time = playing_time, time=time )
        # reactionsRecieved =reactionsRecieved ,
        # surveys = surveys,
        # eventsDuration = eventsDuration,
        # eventsCheckin = eventsCheckin
        quest.save()
        # with open('games_db.json','r',encoding='utf-8') as json_file:
        #     games_converted = json.load(json_file)

        self.cog.bot.game_db['tracked'].append(f'{self.game_name}')
        self.cog.bot.save_game_db()
        await interaction.response.send_message(
            embed=self.cog.bot.embed(
                title='Quest Created',
                description=f'Quest `{quest}` has been created.',
            ),
        )


class Quests(commands.GroupCog, name='quest'):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @app_commands.command(name='create', description='Create a quest')
    @app_commands.default_permissions(administrator=True)
    @commands.has_guild_permissions(administrator=True)
    async def create(self, interaction: discord.Interaction, name:str, badge_name:str, game_name:str, description: Optional[str] = None) -> None:
        if not await self.bot.is_admin(interaction=interaction): return
        #image_url = image.url if image is not None else None
        # quest = await self.find_with_send(interaction=interaction, name=name)
        # if quest is None:
        #     return
        # with open('badge_db.json','r',encoding='utf-8') as json_file:
        #     badges_converted = json.load(json_file)

        li = [item.get('name') for item in self.bot.badge_db['badges']]
        if badge_name not in li:
            await interaction.response.send_message(
             embed=self.bot.embed(
                title='Invalid Badge',
                description=f'There is no such badge.',
             ),
            ) 
            return  
        await interaction.response.send_modal(CreationModal(cog=self, user=interaction.user, des=description , name=name, badge=badge_name , game_name=game_name))

    @app_commands.command(name='delete', description='Delete a quest')
    @app_commands.default_permissions(administrator=True)
    @commands.has_guild_permissions(administrator=True)
    async def delete(self, interaction: discord.Interaction, name: str) -> None:
        if not await self.bot.is_admin(interaction=interaction): return
        quest = await self.find_with_send(interaction=interaction, name=name)
        if quest is None:
            return
        for i, data in enumerate(self.bot.quest_db['quests']):
            if data['id'] == quest.id:
                self.bot.quest_db['quests'].pop(i)
                break
        for id, data in list(self.bot.quest_db['users'].items()):
            data.pop(quest.id, None)
            self.set_data(id=int(id), data=data, save=False)
        self.bot.save_quests_db()
        await interaction.response.send_message(
            embed=self.bot.embed(
                title='Quest Deleted',
                description=f'Quest `{quest}` has been deleted.',
            ),
        )


    @app_commands.command(name='view', description='View a certain quest')
    async def view(self, interaction: discord.Interaction, name: str) -> None:
        quest = await self.find_with_send(interaction=interaction, name=name)
        if quest is None:
            return
        embed = self.bot.embed(
            title=f'Quest Information: **{quest}**',
            description=(
                f'Name : `{quest.name}`\n'
                f'Description : `{quest.des}`\n'
                f'Activities :\n'
                f'  -Messages Sent : `{quest.messages}` messages\n'
                f'  -Time in Voice Channels : `{math.trunc(int(quest.time)/360)}` hours\n'
                f'  -Reactions Given : `{quest.reactions_given}` reactions\n'
                f'  -Clips Shared : `{quest.clips_shared}` clips\n'
                f'  -Playing Time : `{math.trunc(int(quest.playing_time)/360)}` hours on `{quest.game_name}`\n'
                f'Badge(s) : `{quest.badge}`\n'
            ),
        )
        await interaction.response.send_message(embed=embed)
        

    def find(self, name: Optional[str] = None, id: Optional[str] = None) -> Optional[Quest]:
        if name is None and id is None:
            raise ValueError('Either name or id must be provided.')
        key, value = ('name', name.lower()) if name is not None else ('id', id)
        for b in self.bot.quest_db['quests']:
            item = b[key]
            if key == 'name':
                item = item.lower()
            if item == value:
                return Quest(cog=self, **b)
        return None

    async def find_with_send(self, interaction: discord.Interaction, name: str) -> Optional[Quest]:
        quest = self.find(name=name)
        if quest is None:
            await interaction.response.send_message(
                embed=self.bot.embed('No quest with that name exists.'),
                ephemeral=True,
            )
        return quest

    def data(self, id: int) -> dict[str, int]:
        return self.bot.quest_db['users'].get(str(id), {})

    def set_data(self, id: int, data: dict[str, int], save: bool = True) -> None:
        if data:
            self.bot.quest_db['users'][str(id)] = data
        else:
            self.bot.quest_db['users'].pop(str(id), None)
        if save:
            self.bot.save_quest_db()

    @create.autocomplete('badge_name')
    async def create_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        current = current.lower()
        try:
            found: list[app_commands.Choice[str]] = [
                app_commands.Choice(name=b['name'], value=b['name'])
                for b in self.bot.badge_db['badges']
                if current in b['name'].lower()
            ]
            if not found:
                raise IndexError
        except IndexError:
            return [app_commands.Choice(name='No badges found', value='')]
        return found
    

    @delete.autocomplete('name')
    @view.autocomplete('name')
    async def view_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        current = current.lower()
        try:
            found: list[app_commands.Choice[str]] = [
                app_commands.Choice(name=b['name'], value=b['name'])
                for b in self.bot.quest_db['quests']
                if current in b['name'].lower()
            ]
            if not found:
                raise IndexError
        except IndexError:
            return [app_commands.Choice(name='No quests found', value='')]
        return found


async def setup(bot: Bot) -> None:
    cog = Quests(bot)
    bot.quest_cog = cog
    await bot.add_cog(cog)

# author: j_sse#1732 https://github.com/69Jesse