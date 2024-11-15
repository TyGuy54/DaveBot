import os
import aiohttp
import random
from util.env_tokens import MOVIE_ENDPOINT, MOVIE_KEY

# Function to fetch a random movie from OMDb API
async def get_random_movie():
    """Fetches a random movie using the TMDb API."""
    async with aiohttp.ClientSession() as session:
        # Set up the API endpoint with your API key
        url = MOVIE_ENDPOINT
        
        params = {
            "api_key": MOVIE_KEY,
            "sort_by": "popularity.desc",
            "vote_average.gte": 6,   # Get movies with decent ratings
            "vote_count.gte": 100,   # Ensure the movie is popular enough
            "page": random.randint(1, 500)  # Randomly pick a page for variety
        }

        async with session.get(url, params=params) as response:
            if response.status != 200:
                return "❌ Error fetching data from TMDb."

            data = await response.json()
            movies = data.get("results", [])
            
            # Check if we got any movies back
            if not movies:
                return "❌ No movies found."

            # Pick a random movie from the list
            random_movie = random.choice(movies)
            title = random_movie.get("title", "Unknown Title")
            year = random_movie.get("release_date", "Unknown Year")[:4]
            overview = random_movie.get("overview", "No plot available.")
            imdb_id = random_movie.get("imdb_id")
            movie_url = f"https://www.imdb.com/title/{imdb_id}" if imdb_id else "https://www.themoviedb.org/"

            # Return a formatted string with movie details
            return f"🎬 **{title}** ({year})\n🔗 [TMDb Link]({movie_url})\n📝 {overview}"