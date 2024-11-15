import discord
from discord.ui import View
from dotenv import load_dotenv
from discord.ext import commands
from components.music_modal import SongButton
from util.random_movie import get_random_movie
from util.env_tokens import MOM_JOKES, DISCORD_TOKEN
from message_events.events_factory import OnEvents, Event

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True


# Initialize the bot with a command prefix
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.event
async def on_member_join(member):
    await member.create_dm()

    await member.dm_channel.send(
        f'Hello {member.name}, welcome to my Discord server!'
    )


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    events = OnEvents(message)

    await events.trigger_event(Event.SLUR)
    await events.trigger_event(Event.MUSIC)

    # Process commands after checking for slurs
    await bot.process_commands(message)


# Command to get a random movie
@bot.command(name='gimmie-movie')
async def random_movie(ctx):
    await ctx.send("Fetching a random movie... 🎬")
    movie = await get_random_movie()
    await ctx.send(movie)


# Command to add a song
@bot.command(name='add-song')
async def add_songs(ctx: commands.Context):
    view = View()
    view.add_item(SongButton())
    await ctx.send("Click the button to add a song!:", view=view)


# Dumb/silly commands that dont do anything
@bot.command(name='b')
async def funny_joke(ctx):
    response = 'bazinga'
    await ctx.send(response)


# A help commands to list all of DaveBots commands
@bot.command(name='dave-help-me')
async def help_command(ctx):
    """a function to list all of the possable commands"""

    await ctx.send("Here are all of my commands")
    await ctx.send("!b- I will say a funny joke from a funny show")
    await ctx.send("!gimmie-movie - I will give you a random movie")
    await ctx.send("!add-song - I will give you a button to press to add a song to the servers playlist")


if __name__ == '__main__':
    bot.run(DISCORD_TOKEN)