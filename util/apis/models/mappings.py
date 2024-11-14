class Songs:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    @classmethod
    def create_table(cls, conn):
        """
            Used to make the table
        """
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS server_playlist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                artist_name TEXT,
                song_name TEXT NOT NULL,
                url TEXT NOT NULL
            )
        ''')
        
        conn.commit()