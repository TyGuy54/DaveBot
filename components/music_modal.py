import discord
from util.apis.database.db_ops import DB_Ops
from pathlib import Path
from discord.ui import Button

# Define the Feedback Modal class
class SongModal(discord.ui.Modal, title="Send us your Feedback"):
    artist_name = discord.ui.TextInput(
        label="Artists Name",
        style=discord.TextStyle.short,
        placeholder="Type your song name here...",
        required=False
    )

    song_name = discord.ui.TextInput(
        label="Song Name",
        style=discord.TextStyle.short,
        placeholder="Type your song name here...",
        required=True
    )
   
    song_url= discord.ui.TextInput(
        label="Song URL",
        style=discord.TextStyle.short,
        placeholder="Type your song url here...",
        required=True
    )
    
    async def insert_into_data_base(self, art_name, sng_name, url):
        try:
            # Initialize the database connection
            db = DB_Ops(Path('util/song_db/server_songs.db'))
            
            # Validate URL format (optional)
            if not url.startswith('https://'):
                print("Invalid URL provided")
                return
            
            # Insert the data into the database
            db.instert_data('server_playlist', {
                'artist_name': art_name,
                'song_name': sng_name,
                'url': url
            })
            print(f"Song added: {art_name} - {sng_name} - {url}")
        except Exception as e:
            print(f"Error inserting song into database: {e}")


    async def on_submit(self, interaction: discord.Interaction):
        # Insert the song into the database
        await self.insert_into_data_base(self.artist_name.value, self.song_name.value, self.song_url.value)
        
        # Confirm the addition to the user
        await interaction.response.send_message(
            f"Your song '{self.song_name.value}' was added to the database.", ephemeral=True
        )

# Define a button that will trigger the modal
class SongButton(Button):
    def __init__(self):
        super().__init__(label="Add a Song", style=discord.ButtonStyle.primary)

    async def callback(self, interaction: discord.Interaction):
        modal = SongModal()
        await interaction.response.send_modal(modal)
