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
    from event import Events
    from quest import Quests
    from badge import Badges
    from trophy import Trophies
    from item import Items
    from ambar import Ambar
    from poll import Polls



timers = {}
timers1 = {}

'''https://discord.com/oauth2/authorize?client_id=1194121846640103474&permissions=8&scope=bot'''
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
    event_cog: 'Events'
    poll_cog: 'Polls'
    def __init__(self) -> None:
        self.cog_names = ['tourney', 'badge', 'trophy', 'item', 'ambar', 'quest','event','poll' ]
        super().__init__(
            command_prefix=self.get_prefixes,
            activity=discord.Activity(type=discord.ActivityType.listening, name='you'),
            help_command=None,
            strip_after_prefix=True,
            intents=discord.Intents.all(),
            case_insensitive=True,
            owner_ids=set(owner_ids),
        )
        
        with open('event_db.json', encoding='utf8') as file:
            self.event_db = json.load(file)
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
        with open('activity_db.json','r',encoding='utf-8') as json_file:
            self.activity_db = json.load(json_file)
        self.embed_color = 0x9845A8


    def save_user_db(self) -> None:
        with open('user_db.json', 'w', encoding='utf8') as file:
            json.dump(self.user_db, file, indent=4)  

    def save_activity_db(self) -> None:
        with open('activity_db.json', 'w', encoding='utf8') as file:
            json.dump(self.activity_db, file, indent=4)  
    
    def save_event_db(self) -> None:
        with open('event_db.json', 'w', encoding='utf8') as file:
            json.dump(self.event_db, file, indent=4)  

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

@bot.command(aliases=[])
@commands.is_owner()
async def Get(ctx) -> None:
    for member in ctx.guild.members:
        if f'{member.id}' not in bot.user_db['users']:   
            bot.user_db['users'][f'{member.id}'] = {
            "messages": 0,
            "channel_messages": {},
            "time": 0,
            "channel_time": {},
            "reactions_given": 0,
            "clips_shared": 0,
            "reactionsRecieved": 0,
            "playing_time": {},
            "eventsCheckin": [],
            "eventsDuration": {}
            }

            bot.save_user_db()



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
        "channel_messages": {},
        "time": 0,
        "channel_time": {},
        "reactions_given": 0,
        "clips_shared": 0,
        "reactionsRecieved": 0,
        "playing_time": {},
        "surveys": 0,
        "eventsCheckin": [],
        "eventsDuration": {}
        }

        bot.save_user_db()


@bot.event
async def on_message(message):
  
  bot.user_db['users'][f'{message.author.id}']['messages'] += 1
  bot.save_user_db()
  channel_id=  str(message.channel.id)

  if channel_id in bot.user_db['users'][f'{message.author.id}']['channel_messages']:
        bot.user_db['users'][f'{message.author.id}']['channel_messages'][f'{channel_id}'] += 1
        bot.save_user_db()
  else:
        bot.user_db['users'][f'{message.author.id}']['channel_messages'][f'{channel_id}'] = 1
        bot.save_user_db()

  print(message)
  for attch in message.attachments:
    attch_type, attch_format = attch.content_type.split('/') # Attachment.content_type returns a {type}/{file_format} string
    if attch_type == 'video':
       bot.user_db['users'][f'{message.author.id}']['clips_shared'] += 1
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
    end_time =  time.time()
    channel_id = str(oldState.channel.id)
    audiotime =  end_time - start_time
    bot.user_db['users'][f'{member.id}']['time'] += audiotime
    bot.save_user_db()

    if channel_id in bot.user_db['users'][f'{member.id}']['channel_time']:
        bot.user_db['users'][f'{member.id}']['channel_time'][f'{channel_id}'] += audiotime
        bot.save_user_db()
    else:
        bot.user_db['users'][f'{member.id}']['channel_time'][f'{channel_id}'] = audiotime
        bot.save_user_db()
    
    for obj in bot.event_db['events']:
        if oldState.channel.id == int(obj['channel_id']):
            if  start_time <= obj["start_time"] and end_time >= obj["end_time"]:
                eventaudiotime =  obj["end_time"] - obj["start_time"]
                print("1")
                if obj['id'] in bot.user_db['users'][f'{member.id}']['eventsDuration']:
                    bot.user_db['users'][f'{member.id}']['eventsDuration'][f'{obj['id']}'] += eventaudiotime
                    bot.save_user_db()
                else:
                    bot.user_db['users'][f'{member.id}']['eventsDuration'][f'{obj['id']}'] = eventaudiotime
                    bot.save_user_db()

            elif  start_time <= obj["start_time"] and end_time <= obj["end_time"] and end_time > obj["start_time"]:
                eventaudiotime =  end_time - obj["start_time"]
                print("2")
                if obj['id'] in bot.user_db['users'][f'{member.id}']['eventsDuration']:
                    bot.user_db['users'][f'{member.id}']['eventsDuration'][f'{obj['id']}'] += eventaudiotime
                    bot.save_user_db()
                else:
                    bot.user_db['users'][f'{member.id}']['eventsDuration'][f'{obj['id']}'] = eventaudiotime
                    bot.save_user_db()

            elif  start_time >= obj["start_time"] and end_time <= obj["end_time"] :
                eventaudiotime =  end_time - start_time
                print("3")
                if obj['id'] in bot.user_db['users'][f'{member.id}']['eventsDuration']:
                    bot.user_db['users'][f'{member.id}']['eventsDuration'][f'{obj['id']}'] += eventaudiotime
                    bot.save_user_db()
                else:
                    bot.user_db['users'][f'{member.id}']['eventsDuration'][f'{obj['id']}'] = eventaudiotime
                    bot.save_user_db()


            elif  start_time >= obj["start_time"] and start_time < obj["end_time"] and end_time >= obj["end_time"]:
                eventaudiotime =  obj["end_time"] - start_time
                print("4")
                if obj['id'] in bot.user_db['users'][f'{member.id}']['eventsDuration']:
                    bot.user_db['users'][f'{member.id}']['eventsDuration'][f'{obj['id']}'] += eventaudiotime
                    bot.save_user_db()
                else:
                    bot.user_db['users'][f'{member.id}']['eventsDuration'][f'{obj['id']}'] = eventaudiotime
                    bot.save_user_db()

        
    print(f"{member.id} listened  for {audiotime}")


  if  oldUserChannel != None and newUserChannel != None and oldUserChannel.id != newUserChannel.id:
    start_time = timers1.pop(member.id, None)
    end_time =  time.time()
    channel_id =oldState.channel.id 
    audiotime =  end_time - start_time
    bot.user_db['users'][f'{member.id}']['time'] += audiotime
    bot.save_user_db()

    if channel_id in bot.user_db['users'][f'{member.id}']['channel_time']:
        bot.user_db['users'][f'{member.id}']['chennel_time'][f'{channel_id}'] += audiotime
        bot.save_user_db()
    else:
        bot.user_db['users'][f'{member.id}']['channel_time'][f'{channel_id}'] = audiotime
        bot.save_user_db()


    for obj in bot.event_db['events']:
        if oldState.channel.id == int(obj['channel_id']):
            if  start_time <= obj["start_time"] and end_time >= obj["end_time"]:
                eventaudiotime =  obj["end_time"] - obj["start_time"]
                print("1")
                if obj['id'] in bot.user_db['users'][f'{member.id}']['eventsDuration']:
                    bot.user_db['users'][f'{member.id}']['eventsDuration'][f'{obj['id']}'] += eventaudiotime
                    bot.save_user_db()
                else:
                    bot.user_db['users'][f'{member.id}']['eventsDuration'][f'{obj['id']}'] = eventaudiotime
                    bot.save_user_db()

            elif  start_time <= obj["start_time"] and end_time <= obj["end_time"] and end_time > obj["start_time"]:
                eventaudiotime =  end_time - obj["start_time"]
                print("2")
                if obj['id'] in bot.user_db['users'][f'{member.id}']['eventsDuration']:
                    bot.user_db['users'][f'{member.id}']['eventsDuration'][f'{obj['id']}'] += eventaudiotime
                    bot.save_user_db()
                else:
                    bot.user_db['users'][f'{member.id}']['eventsDuration'][f'{obj['id']}'] = eventaudiotime
                    bot.save_user_db()

            elif  start_time >= obj["start_time"] and end_time <= obj["end_time"] :
                eventaudiotime =  end_time - start_time
                print("3")
                if obj['id'] in bot.user_db['users'][f'{member.id}']['eventsDuration']:
                    bot.user_db['users'][f'{member.id}']['eventsDuration'][f'{obj['id']}'] += eventaudiotime
                    bot.save_user_db()
                else:
                    bot.user_db['users'][f'{member.id}']['eventsDuration'][f'{obj['id']}'] = eventaudiotime
                    bot.save_user_db()


            elif  start_time >= obj["start_time"] and start_time < obj["end_time"] and end_time >= obj["end_time"]:
                eventaudiotime =  obj["end_time"] - start_time
                print("4")
                if obj['id'] in bot.user_db['users'][f'{member.id}']['eventsDuration']:
                    bot.user_db['users'][f'{member.id}']['eventsDuration'][f'{obj['id']}'] += eventaudiotime
                    bot.save_user_db()
                else:
                    bot.user_db['users'][f'{member.id}']['eventsDuration'][f'{obj['id']}'] = eventaudiotime
                    bot.save_user_db()


        print(f"{member.id} listened  for {audiotime}")
        timers1[member.id] = time.time()
        print(f"{member.id} joined {newUserChannel}")  


@bot.event
async def on_reaction_add(reaction, user):

    bot.user_db['users'][f'{user.id}']['reactions_given'] += 1
    bot.save_user_db()

    for attch in reaction.message.attachments:
       attch_type, attch_format = attch.content_type.split('/') # Attachment.content_type returns a {type}/{file_format} string
       if attch_type == 'video' and reaction.message.author.id != user.id:
        bot.user_db['users'][f'{reaction.message.author.id}']['reactionsRecieved'] += 1
        bot.save_user_db()


@bot.event
async def on_reaction_remove(reaction, user):

    bot.user_db['users'][f'{user.id}']['reactions_given'] -= 1
    bot.save_user_db()

    for attch in reaction.message.attachments:
       attch_type, attch_format = attch.content_type.split('/') # Attachment.content_type returns a {type}/{file_format} string
       if attch_type == 'video' and reaction.message.author.id != user.id:
         bot.user_db['users'][f'{reaction.message.author.id}']['reactionsRecieved'] -= 1
         bot.save_user_db() 


@bot.event
async def on_presence_update(before, after, ):
 

    # Check if the member started playing a activity
    if (not before.activity or before.activity.name not in bot.activity_db['tracked'] ) and (after.activity and after.activity.name in bot.activity_db['tracked'] ):
        timers[after.id] = time.time()
        print(f"{after.id} started playing {after.activity.name}")
    # Check if the member stopped playing a activity
    elif before.activity  and before.activity.name in bot.activity_db['tracked'] and (not after.activity or after.activity.name not in bot.activity_db['tracked'] ):
        start_time = timers.pop(after.id, None)
        if start_time:
            playtime = time.time() - start_time
            if before.activity.name in bot.user_db['users'][f'{after.id}']['playing_time']:
                bot.user_db['users'][f'{after.id}']['playing_time'][f'{before.activity.name}'] += playtime
                bot.save_user_db()
            else:
                bot.user_db['users'][f'{after.id}']['playing_time'][f'{before.activity.name}'] = playtime
                bot.save_user_db()

            print(f"{after.id} played {before.activity.name} for {playtime}") 

def main() -> None:
    bot.run(token)


if __name__ == '__main__':
    main()