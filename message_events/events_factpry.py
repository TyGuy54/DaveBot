import aiohttp
from bot_commands.get_songs import get_a_song
from enum import Enum, auto
from util.env_tokens import MOM_JOKES

class Event(Enum):
    SLUR = auto()
    MUSIC = auto()


class OnEvents:
    def __init__(self, message):
        self.message = message
        self.current_event = None

    async def trigger_event(self, event: Event):
        match event:
            case Event.SLUR:
                await self.on_slur_event(self.message)
            case Event.MUSIC:
                await self.on_music_event(self.message)


    async def on_slur_event(self, message):
        # Read slurs into a list
        with open('util/slurs/en.txt', 'r') as slur_file:
            slurs = [line.strip().lower() for line in slur_file]

        # Check if the message contains a slur
        if any(slur in message.content.lower() for slur in slurs):
            async with aiohttp.ClientSession() as session:
                async with session.get(MOM_JOKES) as response:
                    if response.status == 200:
                        resp_json = await response.json()
                        joke = resp_json.get('joke', 'Yo mama so funny, she crashed the joke API!')
                        await message.channel.send(joke)
                    else:
                        await message.channel.send("❌ Couldn't fetch a joke right now, try again later.")


    async def on_music_event(self, message):
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