from __future__ import annotations
import discord
import time
from datetime import datetime
from discord.ext import commands



import json
from typing import (
    TYPE_CHECKING,
    Awaitable,
    Optional,
    Callable,
    Any,
)
if TYPE_CHECKING:
    from quest import Quests
    from badge import Badges
    from trophy import Trophies
    from item import Items
    from ambar import Ambar



timers = {}
timers1 = {}

'''https://discord.com/api/oauth2/authorize?client_id=1194121846640103474&permissions=8&scope=bot%20applications.command'''
with open('config.json', encoding='utf8') as file: config = json.load(file)
token = config.get('token')
owner_ids = config.get('owner_ids').copy()


class Bot(commands.Bot):
    user: discord.User
    quest_cog: 'Quests'
    badge_cog: 'Badges'
    trophy_cog: 'Trophies'
    item_cog: 'Items'
    ambar_cog: 'Ambar'
    def __init__(self) -> None:
        self.cog_names = ['tourney', 'badge', 'trophy', 'item', 'ambar', 'quest', ]
        super().__init__(
            command_prefix=self.get_prefixes,
            activity=discord.Activity(type=discord.ActivityType.listening, name='you'),
            help_command=None,
            strip_after_prefix=True,
            intents=discord.Intents.all(),
            case_insensitive=True,
            owner_ids=set(owner_ids),
        )
        

        with open('user_db.json', encoding='utf8') as file:
            self.user_db = json.load(file)
        with open('tourney_db.json', encoding='utf8') as file:
            self.tourney_db = json.load(file)
        with open('badge_db.json', encoding='utf8') as file:
            self.badge_db = json.load(file)
        with open('trophy_db.json', encoding='utf8') as file:
            self.trophy_db = json.load(file)
        with open('item_db.json', encoding='utf8') as file:
            self.item_db = json.load(file)
        with open('ambar_db.json', encoding='utf8') as file:
            self.ambar_db = json.load(file)
        with open('quest_db.json', encoding='utf8') as file:
            self.quest_db = json.load(file)
        with open('game_db.json','r',encoding='utf-8') as json_file:
            self.game_db = json.load(json_file)
        self.embed_color = 0x9845A8


    def save_user_db(self) -> None:
        with open('user_db.json', 'w', encoding='utf8') as file:
            json.dump(self.user_db, file, indent=4)  

    def save_game_db(self) -> None:
        with open('game_db.json', 'w', encoding='utf8') as file:
            json.dump(self.game_db, file, indent=4)  
    
    def save_quest_db(self) -> None:
        with open('quest_db.json', 'w', encoding='utf8') as file:
            json.dump(self.quest_db, file, indent=4)  

    def save_tourney_db(self) -> None:
        with open('tourney_db.json', 'w', encoding='utf8') as file:
            json.dump(self.tourney_db, file, indent=4)

    def save_badge_db(self) -> None:
        with open('badge_db.json', 'w', encoding='utf8') as file:
            json.dump(self.badge_db, file, indent=4)

    def save_trophy_db(self) -> None:
        with open('trophy_db.json', 'w', encoding='utf8') as file:
            json.dump(self.trophy_db, file, indent=4)

    def save_item_db(self) -> None:
        with open('item_db.json', 'w', encoding='utf8') as file:
            json.dump(self.item_db, file, indent=4)

    def save_ambar_db(self) -> None:
        with open('ambar_db.json', 'w', encoding='utf8') as file:
            json.dump(self.ambar_db, file, indent=4)

    def get_prefixes(self, bot: commands.Bot, message: discord.Message) -> list[str]:
        return [
            '!',
        ]

    async def load(self, re: bool = False) -> None:
        func = self.reload_extension if re else self.load_extension
        for cog_name in self.cog_names: await func(cog_name)
        print('Cogs (re)loaded')

    async def setup_hook(self) -> None:
        await self.load()
        self.owner = self.application.owner # type: ignore
        print(f'\t\t\t\033[31m\033[1m >>> Logged in as {self.user.name}#{self.user.discriminator} <<< \033[0m')

    def embed(self, description: str, title: Optional[str] = None, color: Optional[int] = None) -> discord.Embed:
        return discord.Embed(
            title=title,
            description=description,
            color=color or self.embed_color,
        )

    async def is_admin(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id in owner_ids:
            return True
        await interaction.response.send_message(embed=self.embed('You are not an admin!'), ephemeral=True)
        return False


bot = Bot()
# intents = discord.Intents.default()
# intents.message_content = True
# client = discord.Client(intents=intents)

   



@bot.command(aliases=[])
@commands.is_owner()
async def Sync(ctx) -> None:
    await bot.tree.sync()
    await ctx.send('Successfully synced!')


@bot.command(aliases=[])
@commands.is_owner()
async def Reload(ctx) -> None:
    await bot.load(re=True)
    await ctx.send('Successfully reloaded!')


@bot.event
async def on_command_error(ctx, error) -> None:
    if isinstance(error, commands.NotOwner):
        print(f'{ctx.author} tried to run a command, but their id is not in the owners list.')
        return
    raise error

@bot.event
async def on_member_join(member):

    if f'{member.id}' in bot.user_db['users']:  
        print("welcome back")
    else:
        bot.user_db['users'][f'{member.id}'] = {
        "messages": 0,
        "time": 0,
        "reactionsGiven": 0,
        "clipsShared": 0,
        "reactionsRecieved": 0,
        "playingTime": {
            "Counter-Strike 12": 0,
            "Counter-Strike 2": 0
        },
        "surveys": 0,
        "eventsCheckin": [
            "None"
        ],
        "eventsDuration": 0
        }

        bot.save_user_db()


@bot.event
async def on_message(message):
  
  bot.user_db['users'][f'{message.author.id}']['messages'] += 1
  bot.save_user_db()

  for attch in message.attachments:
    attch_type, attch_format = attch.content_type.split('/') # Attachment.content_type returns a {type}/{file_format} string
    if attch_type == 'video':
       bot.user_db['users'][f'{message.author.id}']['clipsShared'] += 1
       bot.save_user_db()


@bot.event
async def on_voice_state_update(member ,oldState, newState):
  newUserChannel = newState.channel
  oldUserChannel = oldState.channel

  if oldUserChannel is None and newUserChannel != None:
    timers1[member.id] = time.time()
    print(f"{member.id} joined {newUserChannel}")

  if oldUserChannel != None and newUserChannel is None:
    start_time = timers1.pop(member.id, None)
    if start_time:
        audiotime = time.time() - start_time
        bot.user_db['users'][f'{member.id}']['time'] += audiotime
        bot.save_user_db()
        print(f"{member.id} listened  for {audiotime}") 

  if  oldUserChannel != None and newUserChannel != None and oldUserChannel.id != newUserChannel.id:
    print("Will use later for events tracking")


@bot.event
async def on_reaction_add(reaction, user):

    bot.user_db['users'][f'{user.id}']['reactionsGiven'] += 1
    bot.save_user_db()

    for attch in reaction.message.attachments:
       attch_type, attch_format = attch.content_type.split('/') # Attachment.content_type returns a {type}/{file_format} string
       if attch_type == 'video' and reaction.message.author.id != user.id:
        bot.user_db['users'][f'{reaction.message.author.id}']['reactionsRecieved'] += 1
        bot.save_user_db()


@bot.event
async def on_reaction_remove(reaction, user):

    bot.user_db['users'][f'{user.id}']['reactionsGiven'] -= 1
    bot.save_user_db()

    for attch in reaction.message.attachments:
       attch_type, attch_format = attch.content_type.split('/') # Attachment.content_type returns a {type}/{file_format} string
       if attch_type == 'video' and reaction.message.author.id != user.id:
         bot.user_db['users'][f'{reaction.message.author.id}']['reactionsRecieved'] -= 1
         bot.save_user_db() 


@bot.event
async def on_presence_update(before, after, ):
 

    # Check if the member started playing a game
    if (not before.activity or before.activity.name not in bot.game_db['tracked'] ) and (after.activity and after.activity.name in bot.game_db['tracked'] ):
        timers[after.id] = time.time()
        print(f"{after.id} started playing {after.activity.name}")
    # Check if the member stopped playing a game
    elif before.activity  and before.activity.name in bot.game_db['tracked'] and (not after.activity or after.activity.name not in bot.game_db['tracked'] ):
        start_time = timers.pop(after.id, None)
        if start_time:
            playtime = time.time() - start_time
            if before.activity.name in bot.user_db['users'][f'{after.id}']['playingTime']:
                bot.user_db['users'][f'{after.id}']['playingTime'][f'{before.activity.name}'] += playtime
                bot.save_user_db()
            else:
                bot.user_db['users'][f'{after.id}']['playingTime'][f'{before.activity.name}'] = playtime
                bot.save_user_db()

            print(f"{after.id} played {before.activity.name} for {playtime}") 

def main() -> None:
    bot.run(token)


if __name__ == '__main__':
    main()