import sqlite3
from pathlib import Path
from util.apis.database.db_ops import DB_Ops

async def get_a_song(search_term):
    db = DB_Ops(Path('util/song_db/server_songs.db'))
    
    # Fetch songs that match the search term
    conn = db.connection
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM server_playlist WHERE song_name LIKE ?", (f"%{search_term}%",))
        song = cursor.fetchone()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        conn.close()

    # If a matching song is found, return its details
    if song:
        return song['artist_name'], song['song_name'], song['url']
    else:
        return None

