from langchain.tools import tool

import requests
from dotenv import load_dotenv
import json
from os import getenv

load_dotenv()


@tool
def get_trending_movies(time_window: str = "week"):
    """
    Fetch movies that are currently trending

    Args:
        time_window (str, default='week', accepted_values="day", "week") Get trending movies for this specific time window

    Returns:
        str: A JSON string containing similar movies or an error message.
    """

    url = f"https://api.themoviedb.org/3/trending/movie/{time_window}"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {getenv('TMDB_ACCESS_TOKEN')}",
    }

    print(f"get_trending_movies called with params {time_window}")

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            json_response = response.json()
            results = json_response.get("results", [])

            if results:
                return json.dumps(
                    {
                        "results": [
                            {
                                "adult": member.get("adult"),
                                "genre_ids": member.get("genre_ids"),
                                "id": member.get("id"),
                                "title": member.get("title"),
                                "overview": member.get("overview"),
                                "release_date": member.get("release_date"),
                                "poster_path": member.get("poster_path"),
                            }
                            for member in results
                        ],
                        "page": json_response.get("page"),
                        "total_pages": json_response.get("total_pages"),
                    }
                )
            else:
                return "Could not find any trending movies"
        else:
            return f"Could not fetch results, TMDB API returned {response.status_code} code"
    except Exception as e:
        return f"Some error occurred: {str(e)}"


if __name__ == "__main__":
    print(get_trending_movies.invoke(({})))
