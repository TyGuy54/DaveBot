import os
import discord
import aiohttp
from bot_commands.get_songs import get_a_song
from componants.music_modal import SongButton
from discord.ui import View
from dotenv import load_dotenv
from discord.ext import commands
from bot_commands.random_movie import get_random_movie

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

TOKEN = os.getenv('DISCORD_TOKEN')

# Initialize the bot with a command prefix
bot = commands.Bot(command_prefix='!', intents=intents)

# Read slurs into a list
with open('util/slurs/en.txt', 'r') as slur_file:
    slurs = [line.strip().lower() for line in slur_file]

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

    # Check if the message contains a slur
    if any(slur in message.content.lower() for slur in slurs):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.yomama-jokes.com/api/v1/jokes/random/') as response:
                if response.status == 200:
                    resp_json = await response.json()
                    joke = resp_json.get('joke', 'Yo mama so funny, she crashed the joke API!')
                    await message.channel.send(joke)
                else:
                    await message.channel.send("❌ Couldn't fetch a joke right now, try again later.")

    # Check if the message starts with "Dave I want"
    if message.content.lower().startswith("dave i want"):
        # Extract the song name from the message
        # Get everything after "Dave I want"
        song_request = message.content[11:].strip() 
        
        if not song_request:
            await message.channel.send("Please specify the song you want!")
            return

        # Fetch the song based on the user's request
        songs = await get_a_song(song_request)

        # If a matching song is found, send its details
        if songs:
            artist, title, url = songs
            await message.channel.send(
                f"🎵 Here is your song:\n**Artist**: {artist}\n**Title**: {title}\n🔗 {url}"
            )
        else:
            await message.channel.send("Sorry, I couldn't find that song in the database.")

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


@bot.command(name='get-song-list')
async def get_song_list(ctx: commands.Context):
    pass


@bot.command(name='b')
async def funny_joke(ctx):
    response = 'bazinga'
    await ctx.send(response)


if __name__ == '__main__':
    bot.run(TOKEN)